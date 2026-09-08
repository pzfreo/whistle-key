"""Package existing oriented STL meshes as a three-plate Bambu Studio project.

Geometry comes from build123d exports. This does not slice or emit printer G-code.
Bambu metadata follows its bbs_3mf.cpp importer and PartPlate grid conventions.
"""
import argparse
import json
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

import lib3mf
import numpy as np
import trimesh

CORE = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('', CORE)
ROOT = Path(__file__).resolve().parents[1]
# Locations are minimum XY corners in local plate coordinates, millimetres.
PLATES = [
    ('1 PETG - pin fit first', (0, 0), [
        ('pin_fit_coupon', 'Pin fit coupon', (116, 124), 1),
    ]),
    ('2 PETG - frame key and two caps', (307.2, 0), [
        ('frame_print', 'Frame - outer rail side down', (93, 100), 1),
        ('lever_print', 'Key - finger face down', (139, 106), 1),
        ('clamp_cap_print', 'Clamp cap 1 - end face down', (93, 145), 1),
        ('clamp_cap_print', 'Clamp cap 2 - end face down', (139, 145), 1),
    ]),
    ('3 TPU 95A - pad external spool', (0, -307.2), [
        ('tpu_pad_print', 'TPU pad - flat back down', (123, 123), 2),
    ]),
]


def meta(parent, key, value):
    ET.SubElement(parent, 'metadata', key=key, value=str(value))


def package(source, output, dry_run=False):
    plates = PLATES
    if dry_run:
        entries = list(PLATES[1][2]) + [
            ("tpu_pad_print", "Rigid pad - PETG dry fit", (139, 125), 1),
            ("pin_fit_coupon", "Pin fit coupon", (93, 170), 1),
        ]
        plates = [("PETG dry fit - all six parts", (0, 0), entries)]
    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    config = ET.Element('config')
    plate_records = []
    report = []
    for plate_id, (name, origin, entries) in enumerate(plates, 1):
        ids = []
        occupied = []
        for stem, label, xy, filament in entries:
            path = source / (stem + '.stl')
            original = trimesh.load_mesh(path)
            if not original.is_watertight or not original.is_winding_consistent:
                raise ValueError(f'Invalid source mesh: {path}')
            low, high = original.bounds
            if abs(low[2]) > 1e-4:
                raise ValueError(f'Source is not on bed: {stem}')
            local_low = np.array([*xy, 0.0])
            local_high = local_low + high - low
            if np.any(local_low < 0) or np.any(local_high > [256, 256, 256]):
                raise ValueError(f'Part outside P1S bed: {label}')
            for a, b in occupied:
                # Require 6 mm between bounding rectangles, including brim room.
                if np.all(local_low[:2] < b[:2]+6) and np.all(local_high[:2]+6 > a[:2]):
                    raise ValueError(f'Overlapping print footprints: {label}')
            occupied.append((local_low, local_high))
            # Preserve the validated STL connectivity instead of re-welding
            # tiny pin features through lib3mf's STL import tolerance.
            resource = model.AddMeshObject()
            vertices = []
            for point in original.vertices:
                vertex = lib3mf.Position()
                for axis in range(3):
                    vertex.Coordinates[axis] = float(point[axis])
                vertices.append(vertex)
            triangles = []
            for face in original.faces:
                triangle = lib3mf.Triangle()
                for axis in range(3):
                    triangle.Indices[axis] = int(face[axis])
                triangles.append(triangle)
            resource.SetGeometry(vertices, triangles)
            resource.SetName(label)
            identity = lib3mf.Transform()
            for axis in range(3):
                identity.Fields[axis][axis] = 1
            item = model.AddBuildItem(resource, identity)
            obj_id = resource.GetResourceID()
            transform = lib3mf.Transform()
            for axis in range(3):
                transform.Fields[axis][axis] = 1
            offset = local_low-low+np.array([*origin, 0])
            for axis in range(3):
                transform.Fields[3][axis] = float(offset[axis])
            item.SetObjectTransform(transform)
            obj = ET.SubElement(config, 'object', id=str(obj_id))
            settings = {
                'name': label, 'extruder': filament,
                'layer_height': '0.12' if filament == 2 else '0.16',
                'wall_loops': '4', 'sparse_infill_density': '100%' if stem == 'tpu_pad_print' else '25%',
                'enable_support': '1' if stem in ['frame_print', 'lever_print'] else '0',
                'support_type': 'normal(auto)',
                'brim_type': 'outer_only' if stem in ['frame_print', 'clamp_cap_print'] else 'no_brim',
                'brim_width': '3',
            }
            for key, value in settings.items():
                meta(obj, key, value)
            ids.append(obj_id)
            report.append({'id': obj_id, 'name': label, 'source': path.name,
                           'plate': plate_id, 'filament': filament,
                           'local_min': local_low.tolist(), 'local_max': local_high.tolist(),
                           'volume_mm3': float(original.volume)})
        plate_records.append((plate_id, name, ids))
    for plate_id, name, ids in plate_records:
        plate = ET.SubElement(config, 'plate')
        meta(plate, 'plater_id', plate_id)
        meta(plate, 'plater_name', name)
        for obj_id in ids:
            inst = ET.SubElement(plate, 'model_instance')
            meta(inst, 'object_id', obj_id)
            meta(inst, 'instance_id', 0)
            meta(inst, 'identify_id', obj_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    model.QueryWriter('3mf').WriteToFile(str(output))
    with zipfile.ZipFile(output) as archive:
        files = {n: archive.read(n) for n in archive.namelist()}
    xml = ET.fromstring(files['3D/3dmodel.model'])
    xml.set('xmlns:BambuStudio', 'http://schemas.bambulab.com/package/2021')
    for name, text in [('Application', 'BambuStudio-02.05.00.66'),
                       ('BambuStudio:3mfVersion', '1'),
                       ('Description', ('All-PETG dry-fit prototype including rigid pad. ' if dry_run else 'Burke single-key prototype. PETG and TPU on separate plates. ') +
                        'P1S 0.4 mm nozzle. Unsliced: select actual filament and bed profiles before slicing.')]:
        element = ET.Element(f'{{{CORE}}}metadata', name=name)
        element.text = text
        xml.insert(0, element)
    for item in xml.findall(f'{{{CORE}}}build/{{{CORE}}}item'):
        item.set('printable', '1')
    files['3D/3dmodel.model'] = ET.tostring(xml, encoding='utf-8', xml_declaration=True)
    files['Metadata/model_settings.config'] = ET.tostring(config, encoding='utf-8', xml_declaration=True)
    settings = {
        'name': 'project_settings', 'from': 'project',
        'printer_settings_id': 'Bambu Lab P1S 0.4 nozzle',
        'printer_model': 'Bambu Lab P1S', 'printer_variant': '0.4',
        'nozzle_diameter': ['0.4'], 'printable_height': '256',
        'printable_area': ['0x0', '256x0', '256x256', '0x256'],
        'bed_exclude_area': ['0x0', '18x0', '18x28', '0x28'],
        'print_settings_id': '0.16mm Optimal @BBL X1C',
        'layer_height': '0.16', 'initial_layer_print_height': '0.2',
        'wall_loops': '4', 'top_shell_layers': '5', 'bottom_shell_layers': '5',
        'enable_prime_tower': '0', 'print_sequence': 'by layer',
        'filament_settings_id': ['Generic PETG'] if dry_run else ['Generic PETG', 'Generic TPU'],
        'filament_type': ['PETG'] if dry_run else ['PETG', 'TPU'], 'filament_diameter': ['1.75'] if dry_run else ['1.75', '1.75'],
        'filament_colour': ['#5B91B0'] if dry_run else ['#5B91B0', '#E7A24B'],
    }
    files['Metadata/project_settings.config'] = json.dumps(settings, indent=2).encode()
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            archive.writestr(name, data)
    # Independent format reader verifies the resulting ZIP/model still parses.
    check = wrapper.CreateModel()
    check.QueryReader('3mf').ReadFromFile(str(output))
    count = 0
    it = check.GetBuildItems()
    while it.MoveNext():
        count += 1
    assert count == len(report) == 6
    output.with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')
    print(f'Created {output}: {len(plates)} plate(s), {count} correctly oriented parts')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT/'exports/single-key/print-oriented')
    parser.add_argument('--output', type=Path, default=ROOT/'exports/single-key/whistle-key-P1S.3mf')
    parser.add_argument("--dry-run", action="store_true", help="All-PETG single plate, including rigid pad")
    args = parser.parse_args()
    package(args.source, args.output, args.dry_run)
