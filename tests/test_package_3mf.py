"""Check material assignments, quantities and preserved print orientation."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

import numpy as np
import pytest
import trimesh

from scripts.package_3mf import CORE, package

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('dry_run', [False, True])
@pytest.mark.parametrize('three_key', [False, True])
def test_project_preserves_meshes_and_material_plates(tmp_path, dry_run, three_key):
    output = tmp_path/'project.3mf'
    source = ROOT/('build/three-key' if three_key else 'build')
    package(source, output, dry_run, three_key)
    report = json.loads(output.with_suffix('.json').read_text())
    assert len(report) == (12 if three_key else 6)
    assert sum(r['source'] == 'clamp_cap_print.stl' for r in report) == (3 if three_key else 2)
    with zipfile.ZipFile(output) as archive:
        xml = ET.fromstring(archive.read('3D/3dmodel.model'))
        config = ET.fromstring(archive.read('Metadata/model_settings.config'))
        settings = json.loads(archive.read('Metadata/project_settings.config'))
        assert not any(n.endswith('.gcode') for n in archive.namelist())
    assert len(config.findall('plate')) == (1 if dry_run else 3)
    assert settings['filament_type'] == (['PETG'] if dry_run else ['PETG', 'TPU'])
    objects = {int(o.attrib['id']): o for o in xml.findall(f'{{{CORE}}}resources/{{{CORE}}}object')}
    items = {int(i.attrib['objectid']): i for i in xml.findall(f'{{{CORE}}}build/{{{CORE}}}item')}
    assert len(items) == (12 if three_key else 6)
    for record in report:
        obj = objects[record['id']]
        vertices = np.array([[float(v.attrib[a]) for a in ['x','y','z']]
                             for v in obj.findall(f'{{{CORE}}}mesh/{{{CORE}}}vertices/{{{CORE}}}vertex')])
        faces = np.array([[int(t.attrib[a]) for a in ['v1','v2','v3']]
                         for t in obj.findall(f'{{{CORE}}}mesh/{{{CORE}}}triangles/{{{CORE}}}triangle')])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
        original = trimesh.load_mesh(source/record['source'])
        assert mesh.is_watertight and mesh.is_winding_consistent
        assert mesh.volume == pytest.approx(original.volume, rel=1e-5)
        assert np.allclose(mesh.bounds, original.bounds, atol=1e-4)
        values = np.array([float(v) for v in items[record['id']].attrib['transform'].split()])
        assert np.allclose(values[:9].reshape(3,3), np.eye(3))  # no accidental rotation/scaling
        assert abs(mesh.bounds[0,2]+values[11]) < 1e-4
        if dry_run:
            assert record['filament'] == 1
            placed = mesh.bounds+values[9:]
            assert (placed[0] >= -1e-4).all() and (placed[1] <= 256).all()
