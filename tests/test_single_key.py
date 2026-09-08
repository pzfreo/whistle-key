"""Functional geometry checks; physical sealing and print quality remain trials."""
import math
from pathlib import Path
import sys

import pytest
from build123d import Axis, Location, ShapeList, Vector, import_step
import trimesh

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.build_ci import load_model


@pytest.fixture(scope="module")
def model():
    return load_model()


def overlap_volume(a, b):
    intersection = a.intersect(b)
    if intersection is None:
        return 0
    if isinstance(intersection, ShapeList):
        return sum(part.volume for part in intersection)
    return intersection.volume


def test_printable_solids_and_bed_placement(model):
    for name, part in model["print_parts"].items():
        assert part.is_valid, name
        assert len(part.solids()) == 1, name
        assert part.volume > 0, name
        assert abs(part.bounding_box().min.Z) < 1e-5, name
        bed_faces = [f for f in part.faces() if f.bounding_box().max.Z < 1e-5]
        assert sum(f.area for f in bed_faces) > 10, name


def test_frame_and_caps_clear_reference_tube(model):
    for part in [model["frame"], *model["caps"]]:
        assert overlap_volume(part, model["tube"]) < 1e-5
    for cap in model["caps"]:
        assert overlap_volume(cap, model["frame"]) < 1e-5


def test_rigid_key_movement_and_pad_locator_fit(model):
    m = model
    axis = Axis((m["pivot_x"], m["hole4_y"], m["pivot_z"]), (0, 1, 0))
    for step in range(21):
        angle = -m["open_angle"] * step / 20
        key = m["lever"].moved(Location((0, m["hole4_y"], 0))).rotate(axis, angle)
        pad = m["pad_blank"].moved(Location((0, m["hole4_y"], 0))).rotate(axis, angle)
        for obstacle in [m["frame"], m["tube"]]:
            assert overlap_volume(key, obstacle) < 1e-5, (step, "key interference")
        assert overlap_volume(key, pad) < 1e-5, (step, "locator interference")
        assert overlap_volume(pad, m["frame"]) < 1e-5, (step, "pad/frame")
    assert overlap_volume(m["pads"][4], m["tube"]) < 1e-5


def test_spring_has_open_preload_and_closed_travel(model):
    m = model
    assert 0 < m["spring_solid_height"] + m["spring_solid_margin"] < m["spring_length_closed"]
    assert m["spring_length_closed"] < m["spring_length_open"] < m["spring_free_length"]


def test_pin_spans_supports_without_blocking_key(model):
    m = model
    span = max(m["bearing_offsets"]) - min(m["bearing_offsets"]) + m["ear_thickness"]
    assert (m["pivot_length"] - span) / 2 >= 0.5
    assert m["pivot_clearance"] > 0
    assert overlap_volume(m["pins"][4], m["keys"][4]) < 1e-5


def test_export_round_trip(model):
    output = Path(__file__).resolve().parents[1] / "build"
    for name, original in model["print_parts"].items():
        step = import_step(str(output / f"{name}.step"))
        assert step.is_valid and len(step.solids()) == 1, name
        assert step.volume == pytest.approx(original.volume, rel=1e-6), name
        mesh = trimesh.load_mesh(output / f"{name}.stl")
        assert mesh.is_watertight, name
        assert mesh.is_winding_consistent, name
        assert mesh.volume == pytest.approx(original.volume, rel=0.01), name


def test_open_key_leaves_airway_above_hole_clear(model):
    """E06: at least 1 mm above the tube crown over the whole hole is clear.

    This is a geometric screening target, not an acoustic acceptance test.
    """
    m = model
    airway = m["hole_z"](0, m["hole4_y"], 0, m["r"] + 1.0, m["hole4_d"])
    for part in [m["frame"], *m["caps"], m["keys"][4], m["pads"][4]]:
        assert overlap_volume(airway, part) < 1e-5


def test_closed_pad_has_continuous_sealing_band(model):
    """E07: a sampled 0.5 mm wide band surrounds the hole on the curved tube.

    Probe within the intended compressed lip, 0.1 mm radially into brass.
    This checks nominal seal geometry, not TPU compliance or airtightness.
    """
    m = model
    for offset in [1.5, 1.75, 2.0]:
        radius = m["hole4_d"] / 2 + offset
        for degree in range(0, 360, 5):
            angle = math.radians(degree)
            x, y = radius * math.cos(angle), radius * math.sin(angle)
            z = math.sqrt((m["r"] - 0.1) ** 2 - x ** 2)
            assert m["pad_blank"].is_inside(Vector(x, y, z)), (offset, degree)


def test_pad_preserves_an_unbroken_backing(model):
    """E08: retain at least a 1 mm solid layer below the flat glue backing."""
    m = model
    backing_z = m["lever_bottom"]
    for x in [-1.5, 0, 1.5]:
        for y in [-1, 0, 1]:
            for depth in [0.01, 0.5, 1.0]:
                assert m["pad_blank"].is_inside(Vector(x, y, backing_z - depth))


def test_lower_clamp_leaves_space_around_hole5(model):
    """Keep a 1 mm axial margin around the neighbouring uncovered hole."""
    m = model
    lowest_clamp_edge = min(m["clamp_ys"]) - m["clamp_width"] / 2
    hole5_upper_edge = m["hole5_y"] + m["hole5_d"] / 2
    assert lowest_clamp_edge - hole5_upper_edge >= 1.0 - 1e-6


def test_pad_contact_face_has_no_central_relief(model):
    """The contact face is continuous across the centre, not an annular lip."""
    m = model
    for x in [-2, -1, 0, 1, 2]:
        for y in [-2, -1, 0, 1, 2]:
            z = math.sqrt((m["r"] - 0.1) ** 2 - x ** 2)
            assert m["pad_blank"].is_inside(Vector(x, y, z))


def test_pad_ring_leaves_tpu_exposed_and_glue_clearance(model):
    m = model
    assert m["pad_ring_inner_diameter"] - m["tpu_outer_diameter"] >= 0.2
    assert m["pad_ring_wall"] >= 0.8
    # The rigid rim must remain at least 1 mm above the tube crown at closure.
    assert m["lever_bottom"] - m["pad_ring_height"] - m["r"] >= 1.0


def test_spring_locators_have_clearance_and_do_not_bottom_out(model):
    m = model
    spring_id = m["spring_od"] - 2*m["spring_wire_diameter"]
    assert spring_id - m["spring_peg_diameter"] >= 0.3
    assert m["spring_length_closed"] - m["spring_peg_length"] >= 0.5
    assert m["spring_socket_rim_x"] - m["spring_moving_x"] >= 0.5
    assert m["spring_floor_x"] - m["spring_socket_rim_x"] >= 1.0


def test_opening_stop_contacts_and_blocks_overtravel(model):
    m = model
    axis = Axis((m["pivot_x"], m["hole4_y"], m["pivot_z"]), (0, 1, 0))
    closed = m["lever"].moved(Location((0, m["hole4_y"], 0)))
    assert closed.distance_to(m["opening_stop"]) > 0.2
    assert m["keys"][4].distance_to(m["opening_stop"]) < 1e-5
    beyond = closed.rotate(axis, -(m["open_angle"] + 1))
    assert overlap_volume(beyond, m["opening_stop"]) > 0.1


def test_hinge_stays_below_playing_surface(model):
    m = model
    # Hardware envelope at the pivot stays at least 2 mm below tube crown.
    assert m["pivot_z"] + m["hub_radius"] <= m["r"] - 2
    assert m["pivot_support_clearance"] == 0  # Player-confirmed 1.0 mm bore.
