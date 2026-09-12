from build123d import *
import math
# Three-key prototype derived from the working hole-4 mechanism.
# Hole-4 TPU seal worked in the player trial; new larger pads need trials.
# All lengths mm. See docs/measurements.md for measured versus assumed values.
# Edit this parameter block; regenerate through build123d MCP execute_file.
# Small springs and pad sealing must be physically tested before instrument use.
tube_od = 14.2
tube_wall = 0.396875
# Independent bottom-edge measurements, not chained centre estimates.
hole_bottoms = {3: 100.0, 4: 79.15, 5: 62.05, 6: 35.30}
hole_axial_diameters = {3: 5.8, 4: 5.09, 5: 7.8, 6: 7.6}
hole_centres = {n: bottom + hole_axial_diameters[n]/2 for n,bottom in hole_bottoms.items()}
hole4_y, hole5_y, hole6_y = [hole_centres[n] for n in [4,5,6]]
hole4_d, hole5_d, hole6_d = [hole_axial_diameters[n] for n in [4,5,6]]
hole45_spacing = hole4_y-hole5_y
# Circular hole envelopes conservatively use axial diameters. Transverse sizes
# of holes 5/6 are unconfirmed; these are clearance references, not acoustic bores.
pad_back_height = 2.6 # Rigid key underside above tube crown
lever_thickness = 3.0
lever_width = 4.0
lever_tail_extension = 3.5
back_web_overlap = 0.1
upper_arm_width = 6.0 # Broader load path into the pad cup; hinge remains 4 mm
upper_arm_radial_extra = 1.0 # Added on the outside, clear of the whistle
arm_reinforcement_start_z = 3.4 # Above fixed bearing heads
arm_reinforcement_full_z = 6.0
arm_width_blend_start_z = 5.5 # Preserve the spring shoulder and hinge interfaces
arm_width_blend_end_z = 7.5
arm_transition_radius = 0.8 # Filled inside corner above spring housing
pad_diameter = 14.2 # Integral pad face; keeps the previous key envelope
pivot_offset = 4.15
pivot_diameter = 1.0
pivot_length = 12.0
pivot_clearance = 0.25
pivot_support_clearance = 0.1 # Trial 1.1 mm fixed bores for the 1.0 mm steel pin
hub_radius = 2.0
hub_length = 4.0
hinge_bore_min_wall = 0.9 # Continuous collar survives the spring-clearance cut
hinge_collar_frame_clearance = 0.2
liner_thickness = 0.0 # Player uses direct contact with brass
clamp_radial_clearance = 0.05 # 14.3 mm nominal seat for measured 14.2 mm tube
clamp_band_width = 4.0 # Raised band; bolt supports retain full clamp_width
clamp_width = 6.0
clamp_wall = 3.0
clamp_split_gap = 1.2
clamp_split_z = -7.0 # Lower joint and M2 heads below the pivot insertion line
pin_access_clearance = 0.1
bolt_head_height = 2.0 # M2 socket-head envelope; verify purchased hardware
clamp_offset = 11.0 # Bring mouthpiece-side clamp 2 mm towards test hole
adjacent_hole_margin = 1.0
rail_width = 7.0
return_rail_width = 5.0 # Opposite-side connection between the two clamp bases
rail_top = clamp_split_z-clamp_split_gap/2
ear_thickness = 3.2 # Retains 0.5 mm pin protrusion at each end of a 12 mm pin
support_head_radius = 3.0 # Independent of the rotating hub: thicker fixed bearing crown
pin_lead_in = 0.25 # Shallow conical entry on both faces; bore stays 1.1 mm
support_root_width = 6.0
support_bridge_drop = 2.3 # 0.3 mm below the rotating 2 mm radius hub
support_tail_bridge_drop = 3.6 # Clears the tail at the 35-degree opening stop
support_tail_relief_inset = 0.35 # Keep at least 0.2 mm below the tilted tail at 35 degrees
support_shoulder_drop = 1.2 # Broad pillar starts below pin approach clearance
axial_clearance = 0.3
# Spring variants. Only the coil size and the parts that touch it change; the
# seat spacing, opening and hinge are shared, so both builds keep the same
# 0.376 mm nominal preload. scripts/build_ci.py selects a variant by pre-setting
# spring_variant; run on its own this file builds the 2 mm spring.
spring_variant = globals().get('spring_variant', '2mm')
# The coil axis passes close to the reinforced hinge collar at full opening,
# so a wider coil needs a higher seat and a smaller opening angle. At 35 degrees
# a 3 mm coil fouls the collar; 26 degrees is the largest opening that keeps
# 0.2 mm clearance and useful preload on a 5 mm free length.
spring_options = {
    '2mm': dict(od=2.0, wire=0.3, free=5.0, solid=2.0, seat_width=3.2,
                peg=1.2, peg_tip=1.0, seat_height=3.1, open_degrees=35.0),
    # 6 mm free length buys the preload the higher seat costs, so the 35 degree
    # opening and full pad lift are kept.
    '3mm': dict(od=3.0, wire=0.4, free=6.0, solid=2.2, seat_width=4.2,
                peg=1.8, peg_tip=1.5, seat_height=3.70, open_degrees=35.0),
    # Same coil on a 5 mm free length. 30 degrees is the most opening that
    # holds 0.2 mm collar clearance at the 0.35 mm preload standard; 31 needs
    # a seat so high that preload falls to 0.33.
    '3mm-short': dict(od=3.0, wire=0.4, free=5.0, solid=2.2, seat_width=4.2,
                      peg=1.8, peg_tip=1.5, seat_height=3.52, open_degrees=30.0),
}
assert spring_variant in spring_options, spring_variant
_spring = spring_options[spring_variant]
spring_od = _spring['od']
spring_wire_diameter = _spring['wire']
spring_solid_height = _spring['solid']
spring_seat_width = _spring['seat_width']
spring_peg_diameter = _spring['peg']
spring_peg_tip_diameter = _spring['peg_tip']
spring_seat_height = _spring['seat_height']
spring_free_length = _spring['free']
# EVA-lined prototype: more clearance above the holes, limited by collar fouling.
opening_angle_degrees = _spring['open_degrees']
# Solid heights are user assumptions, not measured. Measure the actual coils:
# the retained 2.8 mm closed spacing leaves room for 2.3 mm solid at the 0.5 mm
# margin below, and the assert fires if the real spring stacks taller.
spring_fit = 0.4
spring_rate_n_per_mm = None # Unknown; do not infer force
spring_solid_margin = 0.5
spring_socket_depth = 1.5
spring_floor_extra_depth = 0.0 # Increase to reduce preload; keep return at full opening
spring_peg_length = 1.5
spring_holder_top_bevel = 0.8 # Clearance for the wider EVA carrier during opening
# Over-travel at closure: the foam must be the only stop, not the spring holder.
# At 0.3 the key landed on the holder 1.2 degrees past nominal closure, capping
# foam compression at 0.44 mm (22%) however hard the key was pressed.
spring_housing_relief = 0.8
spring_web_overlap = 0.8 # Extend each side web into its fixed hinge pillar
spring_web_hub_clearance = 0.3
spring_socket_brace_angle = 50.0 # Rising underside replaces the socket-mouth shelf
spring_closed_length = 2.8 # Fixed CAD seat spacing, not an adjustment screw
spring_tube_clearance = 0.3
spring_lateral_offset = 1.25
screw_clearance_d = 2.4
nut_across_flats = 4.0 # Standard M2 DIN 934 default; confirm actual nuts
nut_thickness = 1.6
nut_pocket_clearance = 0.3 # Total across-flats allowance for PETG fit
nut_pocket_depth = 1.9
nut_boss_diameter = 7.0 # >= 1 mm wall at hex corners
lug_width = 5.0
lug_height = 3.5
rail_bottom = clamp_split_z-clamp_split_gap/2-lug_height # Flush base for flat printing
# The EVA is glued straight onto the key, so there is no separate TPU carrier
# and no retaining ring: the whole pad face is one uninterrupted glue surface.
eva_liner_thickness = 2.0 # User's sheet; liner is cut, not printed
eva_compression_allowance = 0.2 # Trial compression at closure, not measured hardness
# Finger face. The pad boss used to run out to the arm's own 12.7 mm crown,
# leaving a flat-topped drum standing proud of the arm: 725 mm3 of PETG above
# the recess, 77% of the key. A flat face at 11.0 meets the arm's curve
# tangentially at x = +-6.35, so the crown is trimmed without leaving a step.
key_top_height = 11.0
key_top_chamfer = 1.2 # Relieved rim; the flat centre still prints face down
eva_template_thickness = 2.0
eva_template_samples = 128
# Derived geometry; all lengths mm, angles degrees.
r = tube_od/2
tube_id = tube_od-2*tube_wall
assert 0 < tube_wall < r
lever_bottom = r+pad_back_height
arm_radius = lever_bottom+lever_thickness/2
pivot_x = -arm_radius
pivot_z = 0.0
open_angle = opening_angle_degrees
eva_inner_radius = r-eva_compression_allowance # Uncompressed sealing surface
eva_outer_radius = eva_inner_radius+eva_liner_thickness # Recess floor in the carrier
pad_backing_thickness = key_top_height-eva_outer_radius # PETG above the recess
pad_centre_lift = arm_radius*math.sin(math.radians(open_angle))+lever_bottom*(math.cos(math.radians(open_angle))-1)
rail_x_min = pivot_x-rail_width/2
rail_x_max = pivot_x+rail_width/2
holes = [(n,hole_centres[n],hole_axial_diameters[n]) for n in [4,5,6]]
lower_clamp_offset = 11.0
middle_clamp_y = (hole_bottoms[5]+hole_bottoms[6]+hole_axial_diameters[6])/2
clamp_ys = [hole6_y-lower_clamp_offset,middle_clamp_y,hole4_y+clamp_offset]
rail_y_min = min(clamp_ys)-clamp_width/2
rail_y_max = max(clamp_ys)+clamp_width/2
clamp_inner_r = r+liner_thickness+clamp_radial_clearance
clamp_outer_r = clamp_inner_r+clamp_wall
lug_x = clamp_outer_r+lug_width/2-0.5
lug_inner_x = min(lug_x-lug_width/2, math.sqrt(clamp_outer_r**2-(clamp_split_z-clamp_split_gap/2)**2)-0.8)

# Sideways compression spring keeps the key's top clear for the finger.
# The coil axis passes over the pivot at this height, so clearance to the hinge
# collar is spring_z - collar radius - coil radius. The 3 mm coil needs 0.25 mm
# more height than the 2 mm one, which costs preload at full opening.
spring_z = spring_seat_height
# The arm's width blend must start above the spring-clearance shoulder, so the
# transition fillet lands on a constant-width edge. Unchanged for the 2 mm coil.
arm_width_blend_start_z = max(arm_width_blend_start_z,
                             spring_z+spring_seat_width/2+spring_housing_relief+0.1)
assert arm_width_blend_start_z < arm_width_blend_end_z
hinge_collar_radius = (pivot_diameter+pivot_clearance)/2+hinge_bore_min_wall
spring_floor_x = -(r+1.2) + spring_floor_extra_depth
spring_moving_x = -(r+1.2) - spring_closed_length
spring_socket_rim_x = -(r+1.2) - spring_socket_depth
spring_length_closed = spring_floor_x-spring_moving_x
spring_x = spring_moving_x
spring_holder_back_x = rail_x_max # Flush back; no ledge beyond the frame rail
rail_x_min = min(rail_x_min, -lug_x-lug_width/2)
assert spring_length_closed > spring_solid_height+spring_solid_margin
assert pad_diameter > max(hole4_d,hole5_d,hole6_d)+2
assert min(hole4_y-hole5_y,hole5_y-hole6_y)>pad_diameter+1
# The recess must not eat through the key plate above it.
assert pad_backing_thickness >= 2.0
assert key_top_chamfer < pad_diameter/2 - max(hole4_d,hole5_d,hole6_d)/2

def checked(shape):
    info=measure(shape)
    assert info['volume']>0 and len(shape.solids())==1 and shape.is_valid
    return shape

def box_at(x0,x1,y0,y1,z0,z1):
    return Pos((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)*Box(x1-x0,y1-y0,z1-z0)

def cyl_y(radius,length,x,y,z):
    return Pos(x,y,z)*Rot(90,0,0)*Cylinder(radius,length)

def hole_z(x,y,z0,z1,diameter):
    return Pos(x,y,(z0+z1)/2)*Cylinder(diameter/2,z1-z0)

frame=box_at(rail_x_min,rail_x_max,rail_y_min,rail_y_max,rail_bottom,rail_top)
show(frame,'frame')


# Three split clamps: two ends and one between holes 5 and 6.
caps=[]
for y in clamp_ys:
    ring=checked(cyl_y(clamp_outer_r,clamp_width,0,y,0)-cyl_y(clamp_inner_r,clamp_width+2,0,y,0))
    upper=checked(ring & box_at(-20,20,y-clamp_width,y+clamp_width,-20,clamp_split_z-clamp_split_gap/2))
    # Fill the notches beneath the arc-to-tab junctions with one continuous base.
    base=box_at(-lug_x-lug_width/2,lug_x+lug_width/2,
                y-clamp_width/2,y+clamp_width/2,
                clamp_split_z-clamp_split_gap/2-lug_height,
                clamp_split_z-clamp_split_gap/2)
    # Raise the central cradle so the lowered bolt joint still seats on the tube.
    cradle=box_at(-clamp_inner_r,clamp_inner_r,y-clamp_width/2,y+clamp_width/2,
                  clamp_split_z-clamp_split_gap/2-lug_height,-r+1.0)
    base=checked(base.fuse(cradle))
    base=checked(base-cyl_y(clamp_inner_r,clamp_width+2,0,y,0))
    upper=checked(upper.fuse(base))
    cap=checked(ring & box_at(-20,20,y-clamp_band_width/2,y+clamp_band_width/2,clamp_split_z+clamp_split_gap/2,20))
    for x in [-lug_x,lug_x]:
        upper=checked(upper.fuse(box_at((-lug_x-lug_width/2 if x<0 else lug_inner_x),(-lug_inner_x if x<0 else lug_x+lug_width/2),y-clamp_width/2,y+clamp_width/2,clamp_split_z-clamp_split_gap/2-lug_height,clamp_split_z-clamp_split_gap/2)))
        cap=checked(cap.fuse(box_at((-lug_x-lug_width/2 if x<0 else lug_inner_x),(-lug_inner_x if x<0 else lug_x+lug_width/2),y-clamp_width/2,y+clamp_width/2,clamp_split_z+clamp_split_gap/2,clamp_split_z+clamp_split_gap/2+lug_height)))
        cap=checked(cap-hole_z(x,y,-15,15,screw_clearance_d))
    # Trim only the bed-facing tab overhang so the entire curved band starts
    # on the bed after +90-degree X rotation. Keep band and bolt positions.
    cap=checked(cap & box_at(-30,30,y-clamp_band_width/2,y+clamp_width/2,-20,20))
    # Open throat lets the deeper cap lift off the tube without sliding from its end.
    cap=checked(cap-box_at(-clamp_inner_r,clamp_inner_r,y-clamp_width,y+clamp_width,-20,0))
    frame=checked(frame.fuse(upper))
    caps.append(cap)
# Close the frame on the opposite side, below the tube and moving keys.
return_rail=box_at(lug_x+lug_width/2-return_rail_width,lug_x+lug_width/2,
                   rail_y_min,rail_y_max,rail_bottom,rail_top)
frame=checked(frame.fuse(return_rail))
for y in clamp_ys:
    for x in [-lug_x,lug_x]:
        frame=checked(frame-hole_z(x,y,-15,15,screw_clearance_d))
        # Use loose external M2 nuts; tiny captive pockets leave weak tab walls.
show(frame,'frame')
for i,cap in enumerate(caps): show(cap,'clamp_cap_'+str(i))



# Bearings, opening stop and spring seats; the TPU pad stops closure.
opening_stops={}
bearing_offsets = [-hub_length/2-axial_clearance-ear_thickness/2,hub_length/2+axial_clearance+ear_thickness/2]
for number,y,d in holes:
    for dy in bearing_offsets:
        ear=box_at(pivot_x-support_head_radius,pivot_x+support_head_radius,y+dy-ear_thickness/2,y+dy+ear_thickness/2,rail_top-0.5,pivot_z)
        ear=checked(ear.fuse(cyl_y(support_head_radius,ear_thickness,pivot_x,y+dy,pivot_z)))
        # Full rail-width buttress below the pin; no slender tapered lower stem.
        root=box_at(rail_x_min,rail_x_max,y+dy-ear_thickness/2,y+dy+ear_thickness/2,
                    rail_top-0.5,pivot_z-support_shoulder_drop)
        ear=checked(ear.fuse(root))
        frame=checked(frame.fuse(ear))
        frame=checked(frame-cyl_y((pivot_diameter+pivot_support_clearance)/2,ear_thickness+0.2,pivot_x,y+dy,pivot_z))
        # Guide the pin into each bore rather than loading a sharp printed lip.
        bore_r=(pivot_diameter+pivot_support_clearance)/2
        for side in (-1,1):
            mouth=Plane(origin=(pivot_x,y+dy+side*ear_thickness/2,pivot_z),
                        z_dir=(0,-side,0))*Cone(bore_r+pin_lead_in,bore_r,pin_lead_in,
                                              align=(Align.CENTER,Align.CENTER,Align.MIN))
            frame=checked(frame-mouth)
    # Broad positive opening stop matches the underside of the rear key tail.
    stop_x0=pivot_x-2.5
    stop_x1=pivot_x-1.0
    def tail_plane_z(x):
        return pivot_z+math.tan(math.radians(open_angle))*(x-pivot_x)-(lever_thickness/2)/math.cos(math.radians(open_angle))
    opening_stop=Pos(0,y+1.8,0)*extrude(Plane.XZ*Polygon((stop_x0,rail_top-0.5),(stop_x1,rail_top-0.5),(stop_x1,tail_plane_z(stop_x1)),(stop_x0,tail_plane_z(stop_x0)),align=None),amount=3.6)
    opening_stops[number]=opening_stop
    show(opening_stop,"opening_stop"+str(number))
    frame=checked(frame.fuse(opening_stop))
    seat=box_at(spring_socket_rim_x,spring_holder_back_x,y-spring_seat_width/2,y+spring_seat_width/2,rail_top-0.2,spring_z+spring_seat_width/2)
    # A sloping underside braces the socket mouth without a flat support shelf.
    # The full key sweep checks this added stock against the rotating hub.
    recess_back_x=pivot_x+hub_radius+spring_web_hub_clearance
    # Tangent underside leaves a known radial clearance around the new collar.
    brace_angle=math.radians(spring_socket_brace_angle)
    recess_top_z=(hinge_collar_radius+hinge_collar_frame_clearance)/math.cos(brace_angle)-(spring_socket_rim_x-pivot_x)*math.tan(brace_angle)
    recess_low_z=recess_top_z-(recess_back_x-spring_socket_rim_x)*math.tan(math.radians(spring_socket_brace_angle))
    recess=Pos(0,y+spring_seat_width,0)*extrude(Plane.XZ*Polygon(
        (spring_socket_rim_x-0.1,rail_top-1),(recess_back_x,rail_top-1),
        (recess_back_x,recess_low_z),(spring_socket_rim_x,recess_top_z),
        (spring_socket_rim_x-0.1,recess_top_z),align=None),amount=2*spring_seat_width)
    seat=checked(seat-recess)
    frame=checked(frame.fuse(seat))
    # Tie the upright to both bearings on the tube-facing side of the hub.
    # Keep the spring-facing mouth accessible and the pin approach unobstructed.
    web_half_width=hub_length/2+axial_clearance+spring_web_overlap
    web=box_at(pivot_x+hub_radius+spring_web_hub_clearance,spring_holder_back_x,
               y-web_half_width,y+web_half_width,
               rail_top-0.2,spring_z+spring_seat_width/2)
    frame=checked(frame.fuse(web))
    socket=Pos((spring_socket_rim_x+spring_floor_x)/2-0.05,y,spring_z)*Rot(0,90,0)*Cylinder((spring_od+spring_fit)/2,spring_floor_x-spring_socket_rim_x+0.1)
    frame=checked(frame-socket)
    top_z=spring_z+spring_seat_width/2
    bevel=Pos(0,y+web_half_width+0.1,0)*extrude(Plane.XZ*Polygon(
        (spring_holder_back_x-spring_holder_top_bevel,top_z),
        (spring_holder_back_x+0.1,top_z-spring_holder_top_bevel-0.1),
        (spring_holder_back_x+0.1,top_z+0.1),
        (spring_holder_back_x-spring_holder_top_bevel,top_z+0.1),align=None),
        amount=2*web_half_width+0.2)
    frame=checked(frame-bevel)
# A continuous low spine joins all three pedestals without tall free-standing stems.
spine=box_at(rail_x_min,rail_x_max,
             min(y for _,y,_ in holes)+min(bearing_offsets)-ear_thickness/2,
             max(y for _,y,_ in holes)+max(bearing_offsets)+ear_thickness/2,
             rail_top-0.5,pivot_z-support_tail_bridge_drop)
frame=checked(frame.fuse(spine))
# Join the lower bearing pillars and spring-seat base into one solid pedestal.
for number,y,d in holes:
    bridge=box_at(rail_x_min,rail_x_max,
                  y+min(bearing_offsets)-ear_thickness/2,
                  y+max(bearing_offsets)+ear_thickness/2,
                  rail_top-0.5,pivot_z-support_bridge_drop)
    tail_clearance=box_at(rail_x_min-1,pivot_x-support_tail_relief_inset,
                         y-hub_length,y+hub_length,
                         pivot_z-support_tail_bridge_drop,pivot_z+1)
    bridge=checked(bridge-tail_clearance)
    frame=checked(frame.fuse(bridge))
# Let each cap seat and tighten: the raised spine must step down at clamps.
for y in clamp_ys:
    cap_clearance=box_at(rail_x_min-0.1,rail_x_max+0.1,
                         y-clamp_width/2-0.2,y+clamp_width/2+0.2,
                         rail_top,pivot_z+5)
    frame=checked(frame-cap_clearance)
# Drill through the completed spine as well as the clamp bases.
for y in clamp_ys:
    for x in [-lug_x,lug_x]:
        frame=checked(frame-hole_z(x,y,-15,15,screw_clearance_d))
# Open-bottom hex pockets prevent the six M2 nuts turning once engaged.
# Local bosses preserve wall thickness without moving existing bolt centres.
for y in clamp_ys:
    for x in [-lug_x,lug_x]:
        boss=hole_z(x,y,rail_bottom,rail_top,nut_boss_diameter)
        frame=checked(frame.fuse(boss))
        pocket=Pos(x,y,rail_bottom-0.01)*extrude(
            RegularPolygon((nut_across_flats+nut_pocket_clearance)/math.sqrt(3),6,rotation=30),
            amount=nut_pocket_depth+0.01)
        frame=checked(frame-pocket)
        frame=checked(frame-hole_z(x,y,-15,15,screw_clearance_d))
show(frame,'frame')
show(opening_stop,'opening_stop')

levers={}
foam_blanks={}
pad_sizes={}
for number,y,d in holes:
    # One interchangeable key, sized to cover the largest measured hole.
    pad_sizes[number]=pad_diameter
    # Curved arm follows the tube from a low side pivot up to the pad cup.
    arm_outer=cyl_y(arm_radius+lever_thickness/2,lever_width,0,0,0)
    arm_inner=cyl_y(arm_radius-lever_thickness/2,lever_width+2,0,0,0)
    lever=checked(arm_outer-arm_inner)
    lever=checked(lever & box_at(-arm_radius-5,-0.2,-lever_width,lever_width,0,arm_radius+5))
    # Reinforce the curved arm outward and fan it into the existing pad cup.
    # Both ramps start on the old arm; avoid an abrupt added shoulder.
    outer_r=arm_radius+lever_thickness/2
    reinforced_r=outer_r+upper_arm_radial_extra
    root_x=-math.sqrt(outer_r**2-arm_reinforcement_start_z**2)
    reinforcement=cyl_y(reinforced_r,upper_arm_width,0,0,0)-cyl_y(
        arm_radius-lever_thickness/2,upper_arm_width+2,0,0,0)
    radial_ramp=Pos(0,upper_arm_width/2,0)*extrude(Plane.XZ*Polygon(
        (root_x,arm_reinforcement_start_z),(-reinforced_r,arm_reinforcement_full_z),
        (-reinforced_r,lever_bottom+lever_thickness),
        (-0.2,lever_bottom+lever_thickness),(-0.2,arm_reinforcement_start_z),
        align=None),amount=upper_arm_width,dir=(0,-1,0))
    width_ramp=Pos(-reinforced_r-1,0,0)*extrude(Plane.YZ*Polygon(
        (-lever_width/2,arm_reinforcement_start_z),(lever_width/2,arm_reinforcement_start_z),
        (lever_width/2,arm_width_blend_start_z),(upper_arm_width/2,arm_width_blend_end_z),
        (upper_arm_width/2,lever_bottom+lever_thickness),
        (-upper_arm_width/2,lever_bottom+lever_thickness),
        (-upper_arm_width/2,arm_width_blend_end_z),(-lever_width/2,arm_width_blend_start_z),
        align=None),amount=reinforced_r+2,dir=(1,0,0))
    reinforcement=checked(reinforcement & radial_ramp & width_ramp)
    lever=checked(lever.fuse(reinforcement))
    lever=checked(lever.fuse(hole_z(0,0,lever_bottom,lever_bottom+lever_thickness,pad_diameter)))
    lever=checked(lever.fuse(cyl_y(hub_radius,hub_length,pivot_x,0,pivot_z)))
    lever=checked(lever.fuse(box_at(pivot_x-lever_tail_extension,pivot_x+0.5,-lever_width/2,lever_width/2,-lever_thickness/2,lever_thickness/2)))
    # Fill the unused rear notch. A tangent joins the tail's upper rear corner
    # to the reinforced outer arc, avoiding another narrow neck or inside corner.
    back_x=pivot_x-lever_tail_extension
    back_z=lever_thickness/2
    distance_squared=back_x**2+back_z**2
    assert distance_squared>reinforced_r**2
    tangent_scale=reinforced_r**2/distance_squared
    tangent_offset=reinforced_r*math.sqrt(distance_squared-reinforced_r**2)/distance_squared
    tangent_x=tangent_scale*back_x+tangent_offset*back_z
    tangent_z=tangent_scale*back_z-tangent_offset*back_x
    back_web=Pos(0,lever_width/2,0)*extrude(Plane.XZ*Polygon(
        (back_x,back_z-back_web_overlap),(back_x,back_z),(tangent_x,tangent_z),
        (pivot_x+0.5,tangent_z),(pivot_x+0.5,back_z-back_web_overlap),align=None),
        amount=lever_width,dir=(0,-1,0))
    lever=checked(lever.fuse(back_web))
    lever=checked(lever-cyl_y((pivot_diameter+pivot_clearance)/2,hub_length+2,pivot_x,0,pivot_z))
    # Clearance around the fixed spring housing throughout the opening sweep.
    lever=checked(lever-box_at(spring_socket_rim_x-spring_housing_relief,0,-lever_width,lever_width,-2,spring_z+spring_seat_width/2+spring_housing_relief))
    # A concave fillet fills the stress-concentrating inside shoulder with material.
    transition_edges=[e for e in lever.edges()
                      if abs(e.center().X-(spring_socket_rim_x-spring_housing_relief))<1e-6
                      and abs(e.center().Z-(spring_z+spring_seat_width/2+spring_housing_relief))<1e-6
                      and abs(e.length-lever_width)<1e-6]
    assert len(transition_edges)==1
    lever=checked(fillet(transition_edges,arm_transition_radius))
    # A sideways peg faces into the fixed spring socket.
    seat_tool=Pos(spring_moving_x+5,0,spring_z)*Rot(0,90,0)*Cylinder((spring_od+spring_fit)/2,10)
    lever=checked(lever-seat_tool)
    spring_peg=Pos(spring_moving_x,0,spring_z)*Rot(0,90,0)*Cone(spring_peg_diameter/2,spring_peg_tip_diameter/2,spring_peg_length,align=(Align.CENTER,Align.CENTER,Align.MIN))
    lever=checked(lever.fuse(spring_peg))
    # Restore a full annular collar after the clearance and spring-seat cuts.
    # Its concentric shape has the same envelope at every key angle.
    collar=checked(cyl_y(hinge_collar_radius,hub_length,pivot_x,0,pivot_z)-
                   cyl_y((pivot_diameter+pivot_clearance)/2,hub_length+2,pivot_x,0,pivot_z))
    lever=checked(lever.fuse(collar))
    # Integral dished pad boss: the key plate carries the foam directly, so the
    # glue face is a single cylindrical surface with no ring, notch or step.
    pad_boss=hole_z(0,0,0,lever_bottom+lever_thickness,pad_diameter)
    pad_boss=checked(pad_boss-cyl_y(eva_outer_radius,pad_diameter+2,0,0,0))
    contact_faces=[f for f in pad_boss.faces()
                   if f.geom_type==GeomType.CYLINDER and f.normal_at().Z < -0.5]
    assert len(contact_faces)==1
    foam_blank=checked(thicken(contact_faces,amount=eva_liner_thickness))
    foam_blanks[number]=foam_blank
    show(foam_blank,'eva_liner'+str(number))
    lever=checked(lever.fuse(pad_boss))
    # Trim the crown down to the finger face. The reinforced arm reaches radius
    # 13.7, so the cut runs across the whole key and the arm's curve rises into
    # the flat face instead of standing proud of it. The bend probed by the
    # strength tests sits at z 7.5-8.5 and is untouched.
    lever=checked(lever-box_at(-30,30,-30,30,key_top_height,40))
    # Relieve the finger face's own boundary, not the pad circle. The arm
    # reaches the face at full height, so chamfering the circle cut a 1.4 mm
    # trench between arm and pad; chamfering the face edges leaves that
    # junction continuous and only softens the free rim.
    top_face=[f for f in lever.faces()
              if f.geom_type==GeomType.PLANE and abs(f.center().Z-key_top_height)<1e-6]
    assert len(top_face)==1
    lever=checked(chamfer(top_face[0].edges(),key_top_chamfer))
    show(lever,'lever_blank'+str(number))

    levers[number]=lever

# Reference lower tube segment, not an acoustically designed whistle.
tube=checked(cyl_y(r,120,0,60,0)-cyl_y(tube_id/2,122,0,60,0))
for number,y,d in [(n,hole_centres[n],hole_axial_diameters[n]) for n in [3,4,5,6]]:
    tube=checked(tube-hole_z(0,y,0,r+1,d))
show(tube,'reference_tube')

keys={}
foam_liners={}
spring_envelopes={}
pins={}
for number,y,d in holes:
    label='key'+str(number)
    RevoluteJoint(label,to_part=frame,axis=Axis((pivot_x,y,pivot_z),(0,1,0)),angular_range=(-open_angle,0))
    key=levers[number].moved(Location((0,y,0)))
    RigidJoint('pivot',to_part=key,joint_location=frame.joints[label].location)
    frame.joints[label].connect_to(key.joints['pivot'],angle=-open_angle)
    keys[number]=key
    show(key,label)
    foam_liner=foam_blanks[number].moved(Location((0,y,0))).rotate(
        Axis((pivot_x,y,pivot_z),(0,1,0)),-open_angle)
    foam_liners[number]=foam_liner
    show(foam_liner,'foam_liner'+str(number))
    # Straight cylindrical spring envelope follows both pocket centres.
    # Real compression spring flexes/tilts as the lever moves.
    spring_start=Vector(spring_floor_x,y,spring_z)
    theta=math.radians(open_angle)
    dx=spring_moving_x-pivot_x
    dz=spring_z-pivot_z
    spring_end=Vector(pivot_x+dx*math.cos(theta)-dz*math.sin(theta),y,pivot_z+dx*math.sin(theta)+dz*math.cos(theta))
    axis_vector=spring_end-spring_start
    spring_length_open=axis_vector.length
    assert spring_length_open < spring_free_length
    env=Plane(origin=spring_start,z_dir=axis_vector)*Cylinder(spring_od/2,spring_length_open,align=(Align.CENTER,Align.CENTER,Align.MIN))
    spring_envelopes[number]=env
    show(env,'spring_envelope'+str(number))
    pin=cyl_y(pivot_diameter/2,pivot_length,pivot_x,y,pivot_z)
    pins[number]=pin
    show(pin,'pin'+str(number))

# Assembly is a named compound; individual print parts are checked separately.
assembly=Compound(children=[p.moved(Location()) for p in [frame,*caps,tube,*keys.values(),*foam_liners.values(),*spring_envelopes.values(),*pins.values()]])
assembly.label='Burke_three_key_prototype'
show(assembly,'assembly_open')
# Closed pose for inspecting the pad stack against the whistle. The blanks are
# authored in contact with the tube, so closure needs no rotation.
assembly_closed=Compound(children=[p.moved(Location()) for p in
    [frame,*caps,tube,
     *[levers[n].moved(Location((0,hole_centres[n],0))) for n in [4,5,6]],
     *[foam_blanks[n].moved(Location((0,hole_centres[n],0))) for n in [4,5,6]],
     *pins.values()]])
assembly_closed.label='Burke_three_key_prototype_closed'
show(assembly_closed,'assembly_closed')
print('Spring lengths, closed/open/free:',spring_length_closed,spring_length_open,spring_free_length)
print('Pad centre travel and key angle:',pad_centre_lift,open_angle)

# Separate print-oriented copies; assembly remains in instrument coordinates.
def on_bed(part):
    bb=part.bounding_box()
    return part.moved(Location((-(bb.min.X+bb.max.X)/2,-(bb.min.Y+bb.max.Y)/2,-bb.min.Z)))
print_parts={
    'frame_print': on_bed(frame),
    'clamp_cap_print': on_bed(caps[0].rotate(Axis.X,90)),
}
# Unroll the cylindrical liner at its mid-thickness radius. The shape on flat
# sheet is wider than its projected circular sealing footprint on the whistle.
eva_neutral_radius=eva_inner_radius+eva_liner_thickness/2
eva_outline_points=[]
for index in range(eva_template_samples):
    a=2*math.pi*index/eva_template_samples
    x=(pad_diameter/2)*math.cos(a)
    y=(pad_diameter/2)*math.sin(a)
    eva_outline_points.append((eva_neutral_radius*math.asin(x/eva_outer_radius),y))
eva_cut_outline=Polygon(*eva_outline_points,align=None)
template=extrude(eva_cut_outline,amount=eva_template_thickness)
# Raised grip follows the long (across-whistle) direction. Trace the base edge.
template=checked(template.fuse(box_at(-4,4,-1.5,1.5,eva_template_thickness-0.1,7)))
print_parts['eva_cutting_template']=on_bed(template)
show(eva_cut_outline,'eva_cut_outline')
# The three keys are one geometry, so export one file and print it three times,
# as the clamp cap already is.
print_parts['lever_print']=on_bed(levers[holes[0][0]].rotate(Axis.X,180))
for name,part in print_parts.items(): show(part,name)

# Horizontal test bores match the printing direction of the actual hinges.
# With the clipped base corner at lower left: left to right 0.9, 1.0, 1.1, 1.25 mm.
coupon=box_at(0,24,0,8,0,1)
coupon=checked(coupon-box_at(-0.1,1.5,-0.1,1.5,-0.1,1.1))
for index,diameter in enumerate([0.9,1.0,1.1,1.25]):
    cx=3+index*6
    coupon=checked(coupon.fuse(box_at(cx-2,cx+2,3,5,0.9,6)))
    coupon=checked(coupon-cyl_y(diameter/2,2.2,cx,4,4))
print_parts['pin_fit_coupon']=coupon
show(coupon,'pin_fit_coupon')
result=frame

def export_parts(directory):
    for name,part in print_parts.items():
        export_step(part,str(directory)+'/'+name+'.step')
        export_stl(part,str(directory)+'/'+name+'.stl')
