"""Checks specific to the 3 mm spring variant of the three-key mechanism.

The variant shares scripts/three_key.py with the 2 mm build, so the full
geometry suite in test_three_key.py already covers everything the spring does
not touch. This module pins the parts that do change, confirms the shared
kinematics are genuinely unchanged, and re-runs the collision checks that the
larger socket and taller seat could break.
"""
import math

import pytest
from build123d import Align, Axis, Compound, Cylinder, Location, Plane, ShapeList, Vector

from scripts.build_ci import load_model


VARIANTS = {
    'three_key_3mm_spring': dict(free=6.0, seat_z=3.70, angle=27.0,
                                 lift=4.027, preload=1.495, open_gap=3.090),
    'three_key_3mm_short_spring': dict(free=5.0, seat_z=3.52, angle=27.0,
                                       lift=4.027, preload=0.578, open_gap=3.090),
}


@pytest.fixture(scope='module', params=sorted(VARIANTS))
def m(request):
    model = load_model(request.param)
    model['expected'] = VARIANTS[request.param]
    model['local_frames'] = {}
    for n in [4, 5, 6]:
        y = model['hole_centres'][n]
        half = model['levers'][n].bounding_box().size.Y/2+0.1
        region = model['box_at'](-50, 50, y-half, y+half, -50, 50)
        clipped = model['frame'].intersect(region)
        model['local_frames'][n] = (Compound(children=list(clipped))
                                    if isinstance(clipped, ShapeList) else clipped)
    return model


@pytest.fixture(scope='module')
def baseline():
    return load_model('three_key')


def volume(a, b):
    total = 0.0
    for left in a.solids():
        for right in b.solids():
            hit = left.intersect(right)
            if hit is not None:
                total += (sum(p.volume for p in hit) if isinstance(hit, ShapeList)
                          else hit.volume)
    return total


def pose(m, n, angle):
    y = m['hole_centres'][n]
    axis = Axis((m['pivot_x'], y, m['pivot_z']), (0, 1, 0))
    return [part.moved(Location((0, y, 0))).rotate(axis, -angle)
            for part in [m['levers'][n], m['foam_blanks'][n]]]


def test_coil_size_and_the_parts_that_touch_it(m):
    assert m['spring_variant'].startswith('3mm')
    assert m['spring_od'] == pytest.approx(3.0)
    assert m['spring_free_length'] == pytest.approx(m['expected']['free'])
    assert m['spring_wire_diameter'] == pytest.approx(0.4)
    # Socket bore, seat width and peg all follow the coil.
    assert m['spring_od']+m['spring_fit'] == pytest.approx(3.4)
    assert m['spring_seat_width'] == pytest.approx(4.2)
    # At least 0.4 mm of seat wall beside the bore on each side.
    assert (m['spring_seat_width']-(m['spring_od']+m['spring_fit']))/2 >= 0.4
    # The peg must enter the coil bore, not foul the wire.
    coil_bore = m['spring_od']-2*m['spring_wire_diameter']
    assert m['spring_peg_diameter'] == pytest.approx(1.8)
    assert m['spring_peg_tip_diameter'] == pytest.approx(1.5)
    assert coil_bore-m['spring_peg_diameter'] >= 0.3


def test_preload_and_solid_margin_survive_the_bigger_coil(m):
    assert (m['spring_solid_height']+0.5 < m['spring_length_closed']
            < m['spring_length_open'] < m['spring_free_length'])
    assert m['spring_length_closed']-m['spring_peg_length'] >= 0.5
    # Assumed solid height, not measured; this is the check that catches a
    # taller real spring at the retained 2.8 mm closed spacing.
    assert m['spring_solid_height'] == pytest.approx(2.2)


def test_kinematics_match_the_2mm_build(m, baseline):
    # Pad, hinge, frame envelope and closed seat spacing are untouched.
    for key in ('spring_length_closed', 'pivot_x', 'lever_bottom', 'pad_diameter',
                'eva_liner_thickness', 'pad_backing_thickness'):
        assert m[key] == pytest.approx(baseline[key]), key
    for n in (4, 5, 6):
        assert m['foam_blanks'][n].volume == pytest.approx(
            baseline['foam_blanks'][n].volume)
    # All three variants share the 27 degree opening, so lift is identical; the
    # wider coil differs only in seat height and the parts that touch it.
    assert m['spring_z'] == pytest.approx(m['expected']['seat_z'])
    assert m['open_angle'] == pytest.approx(baseline['open_angle'])
    assert m['pad_centre_lift'] == pytest.approx(baseline['pad_centre_lift'])
    preload = m['spring_free_length']-m['spring_length_open']
    assert preload == pytest.approx(m['expected']['preload'], abs=0.001)
    # Judge travel against the preload standard, not against the 2 mm build: a
    # 3 mm coil of 0.4 mm wire is several times stiffer, and the short-spring
    # variant sits on a higher seat so it carries less travel at 27 degrees.
    assert preload > 0.35
    assert m['levers'][4].volume != pytest.approx(baseline['levers'][4].volume)
    assert m['frame'].volume != pytest.approx(baseline['frame'].volume)


@pytest.mark.parametrize('n', [4, 5, 6])
def test_travel_is_still_clear_with_the_larger_socket(m, n):
    # The seat top rises with the wider socket, so recheck the whole sweep.
    for step in range(21):
        key, liner = pose(m, n, m['open_angle']*step/20)
        for obstacle in [m['local_frames'][n], m['tube'], *m['caps']]:
            assert volume(key, obstacle) < 1e-5, (n, step, 'key collision')
        for obstacle in [m['local_frames'][n], *m['caps']]:
            assert volume(liner, obstacle) < 1e-5, (n, step, 'liner collision')
    stop = m['opening_stops'][n]
    assert pose(m, n, m['open_angle'])[0].distance_to(stop) < 1e-5
    assert volume(pose(m, n, m['open_angle']+1)[0], stop) > 0.1


def test_bigger_coil_still_clears_the_hinge_collar_through_travel(m):
    # The 3 mm coil is a wider swept cylinder past the same collar, so repeat
    # the travel sweep from the 2 mm build with the variant's own dimensions.
    ring = m['cyl_y'](1.525, 4.0, m['pivot_x'], 0, 0)-m['cyl_y'](0.625, 6, m['pivot_x'], 0, 0)
    for n, y, d in m['holes']:
        installed = ring.moved(Location((0, y, 0)))
        assert installed.distance_to(m['frame']) >= 0.2-1e-5
        for step in range(21):
            theta = math.radians(m['open_angle']*step/20)
            start = Vector(m['spring_floor_x'], y, m['spring_z'])
            dx = m['spring_moving_x']-m['pivot_x']
            end = Vector(m['pivot_x']+dx*math.cos(theta)-m['spring_z']*math.sin(theta),
                         y, dx*math.sin(theta)+m['spring_z']*math.cos(theta))
            delta = end-start
            # The 2 mm build holds 0.35 mm here. A 3 mm coil of 0.4 mm wire
            # is several times stiffer, so less travel still means more force;
            # the binding limit is collar clearance, not this margin.
            assert delta.length <= m['spring_free_length']-0.35
            assert delta.length >= m['spring_solid_height']+m['spring_solid_margin']
            coil = Plane(origin=start, z_dir=delta)*Cylinder(
                m['spring_od']/2, delta.length, align=(Align.CENTER, Align.CENTER, Align.MIN))
            assert installed.distance_to(coil) >= 0.2-1e-5, (n, step)
    # The open pad must still stay clear of the airway above the hole.
    for n in (4, 5, 6):
        assert m['foam_liners'][n].distance_to(m['tube']) > 3.0
    assert min(m['foam_liners'][n].distance_to(m['tube']) for n in (4, 5, 6)) == \
        pytest.approx(m['expected']['open_gap'], abs=0.002)
    # Clearance from the socket bore down to the braced recess roof.
    assert m['spring_z']-(m['spring_od']+m['spring_fit'])/2-m['recess_top_z'] >= 0.6


def test_variant_prints_the_same_five_parts(m):
    assert set(m['print_parts']) == {'frame_print', 'clamp_cap_print', 'lever_print',
                                     'eva_cutting_template', 'pin_fit_coupon'}
    for part in m['print_parts'].values():
        assert part.is_valid and len(part.solids()) == 1
        assert abs(part.bounding_box().min.Z) < 1e-5
