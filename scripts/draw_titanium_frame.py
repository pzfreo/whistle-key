#!/usr/bin/env python3
"""Draftwright machining-review sheets from the verified, datum-aligned STEP.

Use a separate environment: see drawings/titanium/README.md. The source model
is a PETG prototype; these sheets intentionally do not release it for titanium.
"""
from pathlib import Path
import ast
import hashlib
import zipfile
import pypdfium2 as pdfium
import json
import argparse
from contextlib import contextmanager
from unittest.mock import patch
from importlib.metadata import version

from build123d import import_step, GeomType, CenterOf, Plane, section
from OCP.BRepAdaptor import BRepAdaptor_Surface
from draftwright import Sheet
from draftwright.annotations import sections as section_engine

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'drawings/titanium'
STEP = OUT / 'frame-reference.step'


def parameters():
    """Read the model's parameter block without rebuilding any CAD geometry."""
    tree = ast.parse((ROOT / 'scripts/three_key.py').read_text())
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'frame' for t in node.targets):
            break
        nodes.append(node)
    values = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), 'three_key_parameters', 'exec'), values)
    return values


def verify_reference(part, m):
    """Check schedule against actual STEP surfaces, not just parameter arithmetic."""
    origin_y = m['clamp_ys'][0]
    clamps = [y-origin_y for y in m['clamp_ys']]
    key_y = [y-origin_y for _,y,_ in m['holes']]
    cylinders = []
    for face in part.faces():
        if face.geom_type == GeomType.CYLINDER:
            cyl = BRepAdaptor_Surface(face.wrapped).Cylinder()
            direction = cyl.Axis().Direction()
            axis = max(range(3), key=lambda i: abs((direction.X(),direction.Y(),direction.Z())[i]))
            cylinders.append((cyl.Radius(),axis,face))
    def check(radius, axis, expected, depth):
        found = [f for r,a,f in cylinders if abs(r-radius)<1e-6 and a==axis]
        assert len(found)==len(expected), ('cylinder count',radius,axis,len(found))
        points = sorted(tuple(round(v,6) for v in f.center(CenterOf.MASS)) for f in found)
        assert points == sorted(tuple(round(v,6) for v in p) for p in expected), ('surface locations',points,expected)
        assert all(abs(tuple(f.bounding_box().size)[axis]-depth)<1e-6 for f in found)
    bolt_z = (m['nut_pocket_depth']+m['lug_height'])/2
    check(m['screw_clearance_d']/2,2,[(x,y,bolt_z) for y in clamps for x in (-m['lug_x'],m['lug_x'])],m['lug_height']-m['nut_pocket_depth'])
    offset = m['hub_length']/2+m['axial_clearance']+m['ear_thickness']/2
    check((m['pivot_diameter']+m['pivot_support_clearance'])/2,1,
          [(m['pivot_x'],y+dy,-m['rail_bottom']) for y in key_y for dy in (-offset,offset)],m['ear_thickness'])
    check((m['spring_od']+m['spring_fit'])/2,0,
          [((m['spring_floor_x']+m['spring_socket_rim_x'])/2,y,m['spring_z']-m['rail_bottom']) for y in key_y],m['spring_socket_depth'])
    walls = [f for f in part.faces() if f.geom_type==GeomType.PLANE and
             abs(f.bounding_box().min.Z)<1e-6 and abs(f.bounding_box().max.Z-m['nut_pocket_depth'])<1e-6]
    assert len(walls)==36, ('nut pocket walls',len(walls))
    af=m['nut_across_flats']+m['nut_pocket_clearance']
    for x in (-m['lug_x'],m['lug_x']):
        for y in clamps:
            matches=[f for f in walls if abs(((f.center().X-x)**2+(f.center().Y-y)**2)**0.5-af/2)<1e-6]
            assert len(matches)==6
            assert all(abs(f.area-af/(3**0.5)*m['nut_pocket_depth'])<1e-6 for f in matches)
    original=import_step(str(ROOT/'exports/three-key/print-oriented/frame_print.step'))
    shift_y=(m['rail_y_min']+m['rail_y_max'])/2-origin_y
    def vertices(shape,dy=0):
        return sorted((round(v.X,6),round(v.Y+dy,6),round(v.Z,6)) for v in shape.vertices())
    assert vertices(original,shift_y)==vertices(part), 'STEP differs from current print-frame vertices'
    assert abs(original.volume-part.volume)<1e-5
    return dict(bolt_holes=6,hinge_bores=6,spring_sockets=3,nut_pockets=6,
                surface_positions_and_depths='PASS',reference_translation='PASS',
                clamp_section_area_mm2=section(part,section_by=Plane.XZ).area)


@contextmanager
def corrected_section(cut_y):
    """Bounded workaround for the pinned Draftwright section renderer.

    Upstream hatches every rear-facing face, including uncut faces behind the
    plane, and points arrows opposite its +Y viewing direction. Restrict hatch
    to the actual cut plane and point the indicators into the retained half.
    No view positions or dimensions are manually laid out.
    """
    hatch = section_engine._section_hatch_edges
    evidence = {'hatched_face_areas_mm2': [], 'excluded_uncut_faces': 0}
    def on_cut(face, sx, sz, spacing):
        bb = face.bounding_box()
        if abs(bb.min.Y-cut_y)>1e-5 or abs(bb.max.Y-cut_y)>1e-5:
            evidence['excluded_uncut_faces'] += 1
            return []
        evidence['hatched_face_areas_mm2'].append(face.area)
        return hatch(face,sx,sz,spacing)
    def arrows(dwg,y_page,x0,x1,*,section,ctx):
        e=section_engine
        size=dwg.draft.arrow_length
        prefix=e._section_identity(section)[2]
        for x,side in ((x0,'left'),(x1,'right')):
            tip=y_page+2.5*size
            arrow=e.Pos(x,tip)*e.ArrowHead(size,head_type=e.HeadType.STRAIGHT,rotation=90)
            arrow.fixed_ink_polygons=e._leader_ink_polygons((x,tip),(x,y_page),arrow_length=size,line_width=0.0)[-1:]
            ctx.place(arrow,f'{prefix}_arrow_{side}')
            end=tip-size
            wing=e.Compound(children=[e.Edge.make_line(e.Vector(x,y_page,0),e.Vector(x,end,0))])
            wing.fixed_ink_polygons=(e._stroke_polygon((x,y_page),(x,end),dwg.draft.line_width),)
            ctx.place(wing,f'{prefix}_wing_{side}')
    with patch.object(section_engine,'_section_hatch_edges',on_cut), patch.object(section_engine,'_add_cutting_plane_arrows',arrows):
        yield evidence


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    m = parameters()
    part = import_step(str(STEP))
    bb = part.bounding_box()
    assert part.is_valid and len(part.solids()) == 1
    origin_y = m['clamp_ys'][0]
    clamp_y = [y-origin_y for y in m['clamp_ys']]
    keys = [(n,y-origin_y) for n,y,_ in m['holes']]
    assert abs(bb.min.Y + m['nut_boss_diameter']/2) < 1e-6
    assert abs(bb.max.Y - (clamp_y[-1]+m['nut_boss_diameter']/2)) < 1e-6
    assert abs(bb.min.Z) < 1e-6
    common = dict(material='Ti / TBD', tolerance='DRAFT / SEE NOTES',
                  drawn_by='PZFREO', date='2026-09-08', revision='P1', projection='third',
                  page='A2', scale=2, detail_view=False)
    parser = argparse.ArgumentParser()
    parser.add_argument('--package-only', action='store_true')
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--sheet', choices=('general','features'))
    args = parser.parse_args()
    physical_checks = verify_reference(part,m)
    if args.verify_only:
        print(json.dumps(physical_checks,indent=2))
        return
    previous = OUT/'drawing-checks.json'
    reports = json.loads(previous.read_text()).get('sheets', {}) if previous.exists() else {}
    for name, title in [('general','FRAME / MACHINING REVIEW'), ('features','FRAME / FEATURE SCHEDULE')]:
        if args.package_only or (args.sheet and name != args.sheet):
            continue
        s = Sheet(part, title=title, number='WK-TI-001-'+('1' if name=='general' else '2'), **common)
        env = s.envelope(part)
        for dim in env.dimension_ids():
            s.dimension(env, dim)
        if name == 'general':
            s.auto_views()
            s.add_section_view('A', at=clamp_y[0])
            s.notes([
                'QUOTATION / DFM REVIEW ONLY - NOT RELEASED FOR MACHINING.',
                'Units mm. Do not scale. Read with sheet 2 and frame-reference.step.',
                'One-piece lower frame; caps, keys, pads and hardware excluded.',
                'CNC mill/drill from solid. Sheet profile cutting alone is insufficient.',
                'Material: titanium; grade and stock condition to be agreed.',
                'Nominal geometry retained from PETG prototype d24a674.',
                'Proposed general linear tolerance +/-0.10; angles +/-0.5 deg.',
                'Functional fits on sheet 2 override general proposal; confirm before release.',
                'Deburr all edges. Proposed edge break 0.10-0.20 except fits/stops.',
                'Whistle seats: proposed Ra 1.6 um; no burrs or tool ridges.',
                'Protect spring seats, stop faces and bearing lands from edge breaks.',
                'CAD defines unlisted contours; all sharp internal corners need DFM review.',
                'Section A-A: foot-end clamp at Y=0. Pocket floor Z=1.90.',
                'Base top Z=3.50; nominal nut-pocket roof thickness 1.60.',
            ], title='SCOPE AND PROPOSED FINISH', prefer='tr')
            s.notes([
                'HOLD 1: confirm hole 5/6 measurements and resulting key positions.',
                'HOLD 2: 1.10 CAD pin bores are a PRINT allowance, not a metal friction fit.',
                'Agree pin retention and bore limits using actual 1 x 12 steel pins.',
                'HOLD 3: six sharp hex pockets need EDM/broaching or approved relief.',
                'No unapproved cutter radii in key sweeps, seats or nut corners.',
                'HOLD 4: confirm titanium grade, clamp fit and all proposed tolerances.',
                'A geometry drawing does not establish titanium clamp compliance.',
            ], title='RELEASE HOLDS', prefer='br')
        else:
            # Only selected manufacturing dimensions: tables locate repeated features
            # without an unreadable forest of automatically repeated dimensions.
            bolts = [(x,y,3.5) for y in clamp_y for x in [-m['lug_x'],m['lug_x']]]
            bolt = s.hole(diameter=m['screw_clearance_d'], at=bolts[0],axis='z',
                          count=6,members=bolts)
            s.dimension(bolt, 'bore.diameter')
            springs = [(m['spring_socket_rim_x'], y, m['spring_z']-m['rail_bottom']) for _,y in keys]
            spring = s.hole(diameter=m['spring_od']+m['spring_fit'],at=springs[0],
                            axis='x',through=False,depth=m['spring_socket_depth'],count=3,members=springs)
            s.dimension(spring, 'bore.diameter')
            ears = [(m['pivot_x'], y+dy, -m['rail_bottom']) for _,y in keys for dy in m['bearing_offsets']] if 'bearing_offsets' in m else [(m['pivot_x'], y+dy, -m['rail_bottom']) for _,y in keys for dy in (-3.8,3.8)]
            hinge = s.hole(diameter=m['pivot_diameter']+m['pivot_support_clearance'],
                           at=ears[0],axis='y',count=6,members=ears)
            s.dimension(hinge, 'bore.diameter')
            s.table([('FEATURE', 'X', 'Y', 'Z / DIRECTION')]+[
                (f'Clamp {i+1}: 2 bolts / nut pockets',f'+/-{m["lug_x"]:.3f}',f'{y:.3f}','Z axis')
                for i,y in enumerate(clamp_y)]+[
                (f'Key {n}: spring socket',f'{m["spring_socket_rim_x"]:.3f}',f'{y:.3f}',f'{m["spring_z"]-m["rail_bottom"]:.3f} / +X')
                for n,y in keys]+[
                (f'Key {n}: paired hinge bores',f'{m["pivot_x"]:.3f}',f'{y:.3f} +/- 3.800',f'{-m["rail_bottom"]:.3f} / Y')
                for n,y in keys],name='coordinate_schedule',prefer='tr')
            s.notes([
                'Coordinate origin: X=whistle axis; Y=foot-end clamp centre; Z=base.',
                '+Y points toward mouthpiece. All coordinates match supplied STEP.',
                '6 bolt holes: diameter 2.40 THRU; proposed +0.05 / -0.00.',
                '6 nut pockets from underside: 4.30 AF x 1.90 deep; proposal +/-0.05.',
                'Nut pocket flat normals parallel X. Nominal nut 4.00 AF x 1.60.',
                'Pocket roof Z=1.90; lug top Z=3.50; roof thickness 1.60.',
                '3 spring sockets: diameter 2.40 x 1.50 full-diameter depth.',
                'Socket floor X=-8.300; flat floor required, drill tip not included.',
                '6 hinge bores: CAD diameter 1.10 through 3.00-thick ears; FIT ON HOLD.',
                'Each hinge pair: 4.60 clear axial gap; 10.60 outer span.',
                'Common hinge axis X=-11.200, Z=11.100. Verify all six coaxial.',
                '3 whistle seats: R7.150, axis X=0 / Z=11.100, axial width 6.00.',
                'Seat radius proposed +/-0.02; all seats share one axis.',
                'Key spacing 4-5=15.745 / 5-6=26.850 nominal; MEASUREMENT HOLD.',
            ],title='FEATURE DEFINITIONS / PROPOSED FITS',prefer='br')
        with corrected_section(clamp_y[0]) as section_checks:
            d = s.build()
        if name == 'general':
            assert section_checks['hatched_face_areas_mm2'], 'Missing cut-plane hatch'
            assert section_checks['excluded_uncut_faces'] > 0
            assert abs(sum(section_checks['hatched_face_areas_mm2'])-physical_checks['clamp_section_area_mm2']) < 1e-5
        before = d.lint_summary()
        d.repair()
        after = d.lint_summary()
        reports[name] = dict(before_repair=before, after_repair=after,
                             section_checks=section_checks, scale=d.scale, page=[d.page_w,d.page_h])
        (OUT/f'{name}-checks.json').write_text(json.dumps(reports[name],indent=2,default=str)+'\n')
        paths=d.export(str(OUT/f'frame-{name}'), formats=('svg','pdf','dxf'))
        print(name, paths, after['by_code'], flush=True)
    reports = {p.stem.removesuffix('-checks'): json.loads(p.read_text()) for p in OUT.glob('*-checks.json') if p.name != 'drawing-checks.json'}
    report = dict(source_sha256=hashlib.sha256(STEP.read_bytes()).hexdigest(),
                  model_sha256=hashlib.sha256((ROOT/'scripts/three_key.py').read_bytes()).hexdigest(),
                  generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  draftwright=version('draftwright'), build123d=version('build123d'),
                  bbox_mm=[bb.size.X,bb.size.Y,bb.size.Z],volume_mm3=part.volume,
                  physical_checks=physical_checks,
                  status='QUOTATION / DFM REVIEW - NOT RELEASED',sheets=reports)
    if 'general' in reports:
        assert abs(sum(reports['general']['section_checks']['hatched_face_areas_mm2'])-physical_checks['clamp_section_area_mm2']) < 1e-5
    (OUT/'drawing-checks.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
    if all((OUT/f'frame-{name}.pdf').exists() for name in ('general','features')):
        combined=pdfium.PdfDocument.new()
        for name in ('general','features'):
            with pdfium.PdfDocument(OUT/f'frame-{name}.pdf') as source:
                assert len(source)==1
                combined.import_pages(source)
        assert len(combined)==2
        combined.save(OUT/'frame-machining-review.pdf')
        combined.close()
        with zipfile.ZipFile(OUT/'frame-titanium-review.zip','w',zipfile.ZIP_DEFLATED) as package:
            for path in sorted(OUT.iterdir()):
                if path.suffix in ('.pdf','.svg','.dxf','.step','.json','.md','.txt'):
                    package.write(path, 'drawings/titanium/'+path.name)
            package.write(Path(__file__), 'scripts/draw_titanium_frame.py')
            package.write(ROOT/'scripts/three_key.py', 'scripts/three_key.py')
        print('Packaged frame-machining-review.pdf and frame-titanium-review.zip',flush=True)


if __name__ == '__main__':
    main()
