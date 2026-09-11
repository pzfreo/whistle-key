"""Engineering checks for the measured three-key extension."""
import math
from pathlib import Path

import pytest
import trimesh
from build123d import Align, Cylinder, Axis, Compound, GeomType, Location, Pos, RegularPolygon, ShapeList, Vector, Plane, section, extrude, import_step
from scripts.build_ci import load_model


@pytest.fixture(scope='module')
def model():
    m=load_model('three_key')
    m['local_frames']={}
    for n in [4,5,6]:
        y=m['hole_centres'][n]
        half=m['levers'][n].bounding_box().size.Y/2+0.1
        region=m['box_at'](-50,50,y-half,y+half,-50,50)
        clipped=m['frame'].intersect(region)
        m['local_frames'][n]=Compound(children=list(clipped)) if isinstance(clipped,ShapeList) else clipped
    return m


def volume(a,b):
    # Intersect placed solids individually. OCCT's touching-compound boolean
    # can report a spurious overlap for the key + EVA assembly even when
    # each solid has positive separation from the obstacle.
    total=0.0
    for left in a.solids():
        for right in b.solids():
            result=left.intersect(right)
            if result is not None:
                total += sum(p.volume for p in result) if isinstance(result,ShapeList) else result.volume
    return total


def pose(m,n,angle):
    y=m['hole_centres'][n]
    axis=Axis((m['pivot_x'],y,m['pivot_z']),(0,1,0))
    return [part.moved(Location((0,y,0))).rotate(axis,-angle)
            for part in [m['levers'][n],m['foam_blanks'][n]]]


def test_measured_holes_and_independent_spacing(model):
    m=model
    assert m['hole_bottoms']=={3:100,4:79.15,5:62.05,6:35.3}
    assert m['hole_axial_diameters']=={3:5.8,4:5.09,5:7.8,6:7.6}
    assert [m['hole_centres'][n] for n in [4,5,6]]==pytest.approx([81.695,65.95,39.1])
    assert set(m['keys'])==set(m['foam_liners'])==set(m['pins'])=={4,5,6}
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


def test_foam_is_the_only_closure_stop(model):
    m=model
    # Finger force must compress the foam, not land the key on the spring
    # holder. With 0.3 mm relief the key bottomed 1.2 degrees past nominal
    # closure, capping compression at 0.44 mm (22%) and leaking in the player
    # trial. Foam needs roughly 25-40% compression to seal on a hole rim.
    y=m['hole_centres'][5]
    axis=Axis((m['pivot_x'],y,m['pivot_z']),(0,1,0))
    for over in (1.0,2.0,3.0):
        pressed=m['levers'][5].moved(Location((0,y,0))).rotate(axis,over)
        assert volume(pressed,m['frame'])<1e-5,(over,'key lands on the frame')
        assert volume(pressed,m['tube'])<1e-5,(over,'key reaches the tube')
    # 3 degrees of over-travel is 0.59 mm of pad movement, so 0.79 mm total
    # compression: about 39% of the 2 mm liner.
    assert m['arm_radius']*math.sin(math.radians(3.0))>0.55
    assert m['spring_housing_relief']>=0.8


def test_keys_cannot_collide_in_any_combination(model):
    m=model
    # Rotation is about Y: axial extents do not change at any key angle.
    for n,next_n in [(6,5),(5,4)]:
        for a in [m['keys'][n],m['foam_liners'][n]]:
            for b in [m['keys'][next_n],m['foam_liners'][next_n]]:
                assert b.bounding_box().min.Y-a.bounding_box().max.Y>=1.0


@pytest.mark.parametrize('n',[4,5,6])
def test_pad_sealing_band_and_backing(model,n):
    m=model
    pad=m['foam_blanks'][n]
    for offset in [0.5,1.0,1.5]:
        radius=m['hole_axial_diameters'][n]/2+offset
        for degree in range(0,360,10):
            angle=math.radians(degree)
            x,y=radius*math.cos(angle),radius*math.sin(angle)
            z=math.sqrt((m['r']-0.1)**2-x*x)
            assert pad.is_inside(Vector(x,y,z)),(n,offset,degree)
    # Solid PETG directly above the recess; the key is its own pad backing.
    assert m['levers'][n].is_inside(Vector(0,0,m['eva_outer_radius']+0.5))
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


def test_fixed_bearings_have_reinforced_crowns_and_continuous_stems(model):
    m=model
    # Geometric minimum stock, not a prediction of printed breaking strength.
    # A 2.2 mm ligament must remain above and beside the 1.1 mm working bore.
    for n,y,d in m['holes']:
        for dy in m['bearing_offsets']:
            for axial in (-1.3,0,1.3):
                for angle in range(0,181,15):
                    a=math.radians(angle)
                    assert m['frame'].is_inside(Vector(
                        m['pivot_x']+2.75*math.cos(a),y+dy+axial,
                        m['pivot_z']+2.75*math.sin(a)))
            # Wider material carries the bearing into the existing pedestal.
            for z in (-0.8,-1.5,-2.5,-3.5):
                for dx in (-2.7,2.7):
                    assert m['frame'].is_inside(Vector(m['pivot_x']+dx,y+dy,z))


def test_print_parts_and_round_trips(model):
    m=model
    output=Path(__file__).resolve().parents[1]/'build/three-key'
    # One file per distinct geometry: the key and the cap are each printed
    # three times. EVA sheet is cut, not printed.
    assert len(m['print_parts'])==5
    assert set(m['print_parts'])=={'frame_print','clamp_cap_print','lever_print',
                                   'eva_cutting_template','pin_fit_coupon'}
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
    for collection in ('levers', 'foam_blanks'):
        reference = model[collection][4]
        for n in (5, 6):
            candidate = model[collection][n]
            common_volume = volume(reference, candidate)
            assert reference.volume + candidate.volume - 2*common_volume < 1e-5
    assert list(model['pad_sizes'].values()) == pytest.approx([14.2]*3)


def test_pad_face_is_one_clean_glue_surface(model):
    m=model
    # The EVA is glued straight to the key, so the face it sticks to must be a
    # single uninterrupted cylinder: no retaining ring, tab notch or step.
    for n in (4,5,6):
        key=m['levers'][n]
        facing=[f for f in key.faces()
                if f.geom_type==GeomType.CYLINDER and f.normal_at().Z<-0.5
                and f.radius is not None
                and f.radius==pytest.approx(m['eva_outer_radius'])]
        assert len(facing)==1
        # The whole nominal pad footprint is available to glue against.
        assert facing[0].area>0.9*math.pi*(m['pad_diameter']/2)**2
        # Nothing of the key intrudes below the recess into the foam.
        assert volume(key,m['foam_blanks'][n])<1e-5
        assert key.distance_to(m['foam_blanks'][n])<1e-5


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


def test_spring_uprights_are_tied_to_both_bearings(model):
    m=model
    for n,y,d in m['holes']:
        # A solid 0.5 x 1 mm section crosses each former upright/pillar gap.
        for side in (-1,1):
            lo,hi=sorted((y+side*1.5,y+side*2.5))
            link=m['box_at'](-8.8,-8.3,lo,hi,0.2,1.2)
            assert volume(link,m['frame'])==pytest.approx(link.volume,abs=1e-6)
        # The original spring diameter has a clear approach into its socket.
        approach=Plane(origin=(m['spring_socket_rim_x']-1,y,m['spring_z']),
                       z_dir=(1,0,0))*Cylinder(
                           m['spring_od']/2,m['spring_floor_x']-m['spring_socket_rim_x']+1,
                           align=(Align.CENTER,
                                  Align.CENTER,
                                  Align.MIN))
        assert volume(approach,m['frame'])<1e-5


def test_spring_holder_backs_are_flush_and_socket_shelves_are_braced(model):
    m=model
    for n,y,d in m['holes']:
        # No lip outside the rail over the full height of the spring upright.
        outside=m['box_at'](m['rail_x_max']+0.001,m['rail_x_max']+1,
                            y-3.1,y+3.1,m['rail_top']-0.2,4.3)
        assert volume(outside,m['frame'])<1e-6
        # Retain material behind the blind socket after trimming its back.
        assert m['frame'].is_inside(Vector(m['spring_floor_x']+0.3,y,m['spring_z']))
        # Continuous material below the old shelf, sloping down towards its root.
        for x,z in [(-9.6,0.95),(-9.3,0.55),(-9.0,0.25)]:
            assert m['frame'].is_inside(Vector(x,y,z))


def test_upper_key_arm_has_stock_across_the_reinforced_bend(model):
    m=model
    # Physical stock checks at two sections of the bend, including near both
    # side faces: the former 4 mm wide / 3 mm radial arm fails these probes.
    for key in m['levers'].values():
        for x,z in [(-11.0,7.5),(-10.5,8.5)]:
            for y in (-2.8,0,2.8):
                assert key.is_inside(Vector(x,y,z))
        # The hinge still fits the existing bearing gap.
        hinge_region=m['box_at'](-20,0,-10,10,-2,3.0)
        lower=key.intersect(hinge_region)
        if isinstance(lower,ShapeList):
            lower=Compound(children=list(lower))
        assert lower.bounding_box().size.Y==pytest.approx(4.0)


def test_hinge_bore_has_continuous_stock_and_clears_frame(model):
    m=model
    # 0.9 mm radial material around the full 1.25 mm working bore, across
    # the complete bearing length. The old spring-side cut failed this check.
    ring=m['cyl_y'](1.525,4.0,m['pivot_x'],0,0)-m['cyl_y'](0.625,6,m['pivot_x'],0,0)
    for n,y,d in m['holes']:
        assert volume(ring,m['levers'][n])==pytest.approx(ring.volume,abs=1e-5)
        installed=ring.moved(Location((0,y,0)))
        # A concentric collar has the same clearance at every rotation angle.
        assert installed.distance_to(m['frame'])>=0.2-1e-5
        # Check the tilting spring throughout travel, not only when closed.
        for step in range(21):
            theta=math.radians(m['open_angle']*step/20)
            start=Vector(m['spring_floor_x'],y,m['spring_z'])
            dx=m['spring_moving_x']-m['pivot_x']
            end=Vector(m['pivot_x']+dx*math.cos(theta)-m['spring_z']*math.sin(theta),
                       y,dx*math.sin(theta)+m['spring_z']*math.cos(theta))
            delta=end-start
            # Retain at least 0.35 mm nominal preload, without approaching solid.
            assert delta.length <= m['spring_free_length']-0.35
            assert delta.length >= m['spring_solid_height']+m['spring_solid_margin']
            spring=Plane(origin=start,z_dir=delta)*Cylinder(m['spring_od']/2,delta.length,
                       align=(Align.CENTER,Align.CENTER,Align.MIN))
            assert installed.distance_to(spring)>=0.2-1e-5
    assert m['spring_z']-(m['spring_od']+m['spring_fit'])/2-m['recess_top_z']>=0.6


def test_key_back_has_continuous_stock_above_hinge_tail(model):
    m=model
    # Stock across the formerly empty rear notch, across most of the 4 mm width.
    required=m['box_at'](-13.4,-13.0,-1.8,1.8,2.0,3.4)
    for key in m['levers'].values():
        assert volume(required,key)==pytest.approx(required.volume,abs=1e-6)


def test_eva_facing_template_and_more_lift(model):
    m=model
    assert m['eva_liner_thickness']==pytest.approx(2.0)
    # Carrier floor left above the deeper recess, and tabs kept inside it.
    assert m['pad_backing_thickness']==pytest.approx(3.8)
    assert m['pad_backing_thickness']>=2.0
    assert m['spring_od']==pytest.approx(2.0)
    assert m['spring_free_length']==pytest.approx(5.0)
    assert m['spring_length_closed']==pytest.approx(2.8)
    assert m['open_angle']==pytest.approx(35.0)
    # At least 4.6 mm centre lift and 3 mm nearest-edge clearance at full opening.
    assert m['pad_centre_lift']>4.6
    for n in (4,5,6):
        assert m['foam_liners'][n].distance_to(m['tube'])>3.0
        # Integral pad face spans the full 14.2 mm key pad across the whistle.
        assert m['foam_blanks'][n].bounding_box().size.Y==pytest.approx(14.2)
        assert m['foam_blanks'][n].is_valid and len(m['foam_blanks'][n].solids())==1
    outline=m['eva_cut_outline']
    assert outline.bounding_box().size.X==pytest.approx(14.59224,abs=0.01)
    assert outline.bounding_box().size.Y==pytest.approx(14.2)
    # The nominal unrolled sheet agrees with the offset-surface volume within
    # 0.3%, allowing the sampled outline and CAD offset approximation.
    assert outline.area*m['eva_liner_thickness']==pytest.approx(m['foam_blanks'][4].volume,rel=0.003)
    # Closed pose is a published output; the liner must sit on the tube with
    # the nominal 0.2 mm interference rather than float above it.
    assert m['assembly_closed'].is_valid
    for n in (4,5,6):
        seated=m['foam_blanks'][n].moved(Location((0,m['hole_centres'][n],0)))
        assert volume(seated,m['tube'])>1.0
    guide=m['print_parts']['eva_cutting_template']
    base=section(guide,section_by=Plane.XY.offset(0.5))
    assert len(base.faces())==1
    assert base.area==pytest.approx(outline.area,rel=1e-5)
    assert guide.bounding_box().size.Z==pytest.approx(7)
