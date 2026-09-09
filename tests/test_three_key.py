"""Engineering checks for the measured three-key extension."""
import math
from pathlib import Path

import pytest
import trimesh
from build123d import Axis, Compound, Location, Pos, RegularPolygon, ShapeList, Vector, Plane, section, extrude, import_step
from scripts.build_ci import load_model


@pytest.fixture(scope='module')
def model():
    m=load_model('three_key')
    m['local_frames']={}
    for n in [4,5,6]:
        y=m['hole_centres'][n]
        half=max(m['levers'][n].bounding_box().size.Y,m['pad_blanks'][n].bounding_box().size.Y)/2+0.1
        region=m['box_at'](-50,50,y-half,y+half,-50,50)
        clipped=m['frame'].intersect(region)
        m['local_frames'][n]=Compound(children=list(clipped)) if isinstance(clipped,ShapeList) else clipped
    return m


def volume(a,b):
    result=a.intersect(b)
    if result is None:
        return 0
    return sum(p.volume for p in result) if isinstance(result,ShapeList) else result.volume


def pose(m,n,angle):
    y=m['hole_centres'][n]
    axis=Axis((m['pivot_x'],y,m['pivot_z']),(0,1,0))
    return [part.moved(Location((0,y,0))).rotate(axis,-angle)
            for part in [m['levers'][n],m['pad_blanks'][n]]]


def test_measured_holes_and_independent_spacing(model):
    m=model
    assert m['hole_bottoms']=={3:100,4:79.15,5:62.05,6:35.3}
    assert m['hole_axial_diameters']=={3:5.8,4:5.09,5:7.8,6:7.6}
    assert [m['hole_centres'][n] for n in [4,5,6]]==pytest.approx([81.695,65.95,39.1])
    assert set(m['keys'])==set(m['pads'])==set(m['pins'])=={4,5,6}
    assert len(m['caps'])==3
    assert m['middle_clamp_y']==pytest.approx(52.475)


@pytest.mark.parametrize('n',[4,5,6])
def test_travel_stop_and_open_airway(model,n):
    m=model
    for step in range(21):
        key,pad=pose(m,n,m['open_angle']*step/20)
        for obstacle in [m['local_frames'][n],m['tube'],*m['caps']]:
            assert volume(key,obstacle)<1e-5,(n,step,'key collision')
        for obstacle in [m['local_frames'][n],*m['caps']]:
            assert volume(pad,obstacle)<1e-5,(n,step,'pad collision')
        assert volume(key,pad)<1e-5
        for cap in m['caps']:
            assert key.distance_to(cap)>=1.0
            assert pad.distance_to(cap)>=1.0
    key,pad=pose(m,n,m['open_angle'])
    assert volume(pad,m['tube'])<1e-5
    airway=m['hole_z'](0,m['hole_centres'][n],0,m['r']+1,m['hole_axial_diameters'][n])
    for obstacle in [key,pad,m['frame'],*m['caps']]:
        assert volume(airway,obstacle)<1e-5,(n,'open airway')
    stop=m['opening_stops'][n]
    assert key.distance_to(stop)<1e-5
    assert volume(pose(m,n,m['open_angle']+1)[0],stop)>0.1
    assert pose(m,n,0)[0].distance_to(stop)>0.2


def test_keys_cannot_collide_in_any_combination(model):
    m=model
    # Rotation is about Y: axial extents do not change at any key angle.
    for n,next_n in [(6,5),(5,4)]:
        for a in [m['keys'][n],m['pads'][n]]:
            for b in [m['keys'][next_n],m['pads'][next_n]]:
                assert b.bounding_box().min.Y-a.bounding_box().max.Y>=1.0


@pytest.mark.parametrize('n',[4,5,6])
def test_pad_sealing_band_and_backing(model,n):
    m=model
    pad=m['pad_blanks'][n]
    for offset in [1.5,1.75,2]:
        radius=m['hole_axial_diameters'][n]/2+offset
        for degree in range(0,360,10):
            angle=math.radians(degree)
            x,y=radius*math.cos(angle),radius*math.sin(angle)
            z=math.sqrt((m['r']-0.1)**2-x*x)
            assert pad.is_inside(Vector(x,y,z)),(n,offset,degree)
    assert pad.is_inside(Vector(0,0,m['lever_bottom']-1))
    assert m['pad_sizes'][n]>=m['hole_axial_diameters'][n]+4


def test_mounting_grip_and_upper_finger_margin(model):
    m=model
    for part in [m['frame'],*m['caps']]:
        assert volume(part,m['tube'])<1e-5
    # At least 5 mm from raised upper band to hole 3 footward edge.
    assert m['hole_bottoms'][3]-(max(m['clamp_ys'])+m['clamp_band_width']/2)>=5
    travel=m['clamp_radial_clearance']+0.01
    frame=m['frame'].moved(Location((0,0,travel)))
    assert volume(frame,m['tube'])>1e-4
    assert m['clamp_split_gap']-2*travel>=0.8
    for cap in m['caps']:
        assert volume(cap,m['frame'])<1e-5
        tight=cap.moved(Location((0,0,-travel)))
        assert volume(tight,m['tube'])>1e-4
        assert volume(tight,frame)<1e-5
        bb=cap.bounding_box()
        throat=m['box_at'](-m['r'],m['r'],bb.min.Y-1,bb.max.Y+1,-20,0)
        assert volume(cap,throat)<1e-5


def test_pins_can_be_inserted_in_order_4_5_6(model):
    m=model
    start=m['rail_y_min']-m['pivot_length']-2
    installed=[]
    for n in [4,5,6]:
        end=m['hole_centres'][n]+m['pivot_length']/2
        sweep=m['cyl_y'](m['pivot_diameter']/2,end-start,m['pivot_x'],(start+end)/2,m['pivot_z'])
        # Feed through empty lower bearings; fit the uppermost pin first.
        for part in [m['frame'],m['tube'],*m['caps'],*m['keys'].values(),*installed]:
            assert volume(sweep,part)<1e-5,(n,'insertion')
        for y in m['clamp_ys']:
            for x in [-m['lug_x'],m['lug_x']]:
                z=m['clamp_split_z']+m['clamp_split_gap']/2+m['lug_height']
                head=m['hole_z'](x,y,z,z+m['bolt_head_height'],4)
                assert volume(sweep,head)<1e-5
        installed.append(m['pins'][n])
    span=max(m['bearing_offsets'])-min(m['bearing_offsets'])+m['ear_thickness']
    assert (m['pivot_length']-span)/2>=0.5
    assert m['pivot_diameter']+m['pivot_support_clearance']==pytest.approx(1.1)


def test_spring_preload_and_solid_margin(model):
    m=model
    assert m['spring_solid_height']+0.5<m['spring_length_closed']<m['spring_length_open']<m['spring_free_length']
    assert m['spring_length_closed']-m['spring_peg_length']>=0.5


def test_print_parts_and_round_trips(model):
    m=model
    output=Path(__file__).resolve().parents[1]/'build/three-key'
    assert len(m['print_parts'])==9 # One cap mesh printed three times.
    for name,part in m['print_parts'].items():
        assert part.is_valid and len(part.solids())==1
        assert abs(part.bounding_box().min.Z)<1e-5
        assert sum(f.area for f in part.faces() if f.bounding_box().max.Z<1e-5)>10
        restored=import_step(str(output/f'{name}.step'))
        assert restored.is_valid and len(restored.solids())==1
        assert restored.volume==pytest.approx(part.volume,rel=1e-6)
        mesh=trimesh.load_mesh(output/f'{name}.stl')
        assert mesh.is_watertight and mesh.is_winding_consistent
        assert mesh.volume==pytest.approx(part.volume,rel=0.01)


def test_all_six_clamp_bolts_have_clear_passages(model):
    m=model
    for y in m['clamp_ys']:
        for x in [-m['lug_x'],m['lug_x']]:
            bolt=m['hole_z'](x,y,-15,15,2.0)
            for part in [m['frame'],*m['caps']]:
                assert volume(bolt,part)<1e-5,(x,y,'M2 bolt passage')


def test_nuts_insert_from_below_seat_and_cannot_spin(model):
    m=model
    assert m['nut_boss_diameter']/2-(m['nut_across_flats']+m['nut_pocket_clearance'])/math.sqrt(3)>=1.0
    assert m['lug_height']-m['nut_pocket_depth']>=1.5
    for y in m['clamp_ys']:
        for x in [-m['lug_x'],m['lug_x']]:
            ceiling=m['rail_bottom']+m['nut_pocket_depth']
            profile=RegularPolygon(m['nut_across_flats']/math.sqrt(3),6,rotation=30)
            nut=Pos(x,y,ceiling-m['nut_thickness'])*extrude(profile,amount=m['nut_thickness'])
            assert volume(nut,m['frame'])<1e-5
            sweep=Pos(x,y,m['rail_bottom']-3)*extrude(profile,amount=m['nut_pocket_depth']+3)
            assert volume(sweep,m['frame'])<1e-5
            assert volume(nut.moved(Location((0,0,0.05))),m['frame'])>0.01 # Bearing roof.
            assert volume(nut.rotate(Axis((x,y,0),(0,0,1)),30),m['frame'])>0.1 # Anti-rotation.
            # Solid material surrounds every pocket corner, including external bosses.
            probe_radius=(m['nut_across_flats']+m['nut_pocket_clearance'])/math.sqrt(3)+0.5
            for angle in range(0,360,30):
                a=math.radians(angle)
                assert m['frame'].is_inside(Vector(x+probe_radius*math.cos(a),y+probe_radius*math.sin(a),m['rail_bottom']+0.8))


def test_all_three_keys_and_pads_are_interchangeable(model):
    # Compare occupied solids, not just nominal diameters or equal volumes.
    for collection in ('levers', 'pad_blanks'):
        reference = model[collection][4]
        for n in (5, 6):
            candidate = model[collection][n]
            common_volume = volume(reference, candidate)
            assert reference.volume + candidate.volume - 2*common_volume < 1e-5
    assert list(model['pad_sizes'].values()) == pytest.approx([12.3]*3)


def test_pad_tabs_guide_insertion_and_prevent_crosswise_seating(model):
    m=model
    pad,key=m['pad_blanks'][4],m['levers'][4]
    # Both equivalent axial orientations seat and insert without bending the tabs.
    for angle in (0,180):
        oriented=pad.rotate(Axis.Z,angle)
        for drop in (0,0.2,0.6,1.2,2.0):
            assert volume(oriented.moved(Location((0,0,-drop))),key)<1e-5
    assert volume(pad.rotate(Axis.Z,90),key)>0.1
    assert volume(pad.moved(Location((0,0,0.05))),key)>0.1 # Cup roof limits insertion.
    assert m['lever_bottom']-m['pad_tab_height']>m['r']+1
    assert pad.bounding_box().size.Y<key.bounding_box().size.Y
    # Continuous seal-band assertions above still apply to each larger, tabbed pad.


def test_clamp_cap_band_starts_on_bed_without_a_floating_arch(model):
    m=model
    cap=m['print_parts']['clamp_cap_print']
    first=section(cap,section_by=Plane.XY.offset(0.08))
    # Previously only two disconnected tab islands existed in the first 1 mm.
    assert len(first.faces())==1
    assert first.bounding_box().size.X==pytest.approx(cap.bounding_box().size.X)
    assert first.bounding_box().size.Y==pytest.approx(cap.bounding_box().size.Y)
    assert cap.bounding_box().size.Z==pytest.approx(5.0)
    for original,y in zip(m['caps'],m['clamp_ys']):
        assert original.bounding_box().min.Y==pytest.approx(y-m['clamp_band_width']/2)
        assert original.bounding_box().max.Y==pytest.approx(y+m['clamp_width']/2)
        # Preserve >=0.8 mm axial wall from the clearance bore to the trimmed edge.
        assert m['clamp_band_width']/2-m['screw_clearance_d']/2>=0.8-1e-6
