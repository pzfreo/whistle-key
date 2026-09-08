from build123d import *
import math
# Single-key prototype for hole 4; measured OD and hole 4, trial mechanism.
# Continuous TPU sealing face is experimental; no physical seal verified.
# All lengths mm. See docs/measurements.md for measured versus assumed values.
# Edit this parameter block; regenerate through build123d MCP execute_file.
# Small springs and pad sealing must be physically tested before instrument use.
tube_od = 14.2
tube_wall = 0.396875
hole4_y = 81.68
hole45_spacing = 16.0
hole5_y = hole4_y - hole45_spacing
hole6_y = 43.0
hole4_d = 5.09
hole5_d = 6.0
hole6_d = 5.0
pad_back_height = 2.6 # Rigid key underside above tube crown
lever_thickness = 3.0
lever_width = 4.0
arm_transition_radius = 0.8 # Filled inside corner above spring housing
pad_diameter = 11.0
pivot_offset = 4.15
pivot_diameter = 1.0
pivot_length = 12.0
pivot_clearance = 0.25
pivot_support_clearance = 0.1 # Trial 1.1 mm fixed bores for the 1.0 mm steel pin
hub_radius = 2.0
hub_length = 4.0
opening_angle_degrees = 20.0 # Trial low-hinge opening; verify airway and comfort
liner_thickness = 0.5
clamp_width = 6.0
clamp_wall = 3.0
clamp_split_gap = 0.8
clamp_split_z = -7.0 # Lower joint and M2 heads below the pivot insertion line
pin_access_clearance = 0.1
bolt_head_height = 2.0 # M2 socket-head envelope; verify purchased hardware
clamp_offset = 13.0
adjacent_hole_margin = 1.0
rail_width = 7.0
rail_top = clamp_split_z-clamp_split_gap/2
rail_bottom = rail_top-3.0
ear_thickness = 3.0
support_root_width = 6.0
support_shoulder_drop = 1.2 # Broad pillar starts below pin approach clearance
axial_clearance = 0.3
spring_od = 2.0
spring_fit = 0.4
spring_free_length = 5.0
spring_solid_height = 2.0 # User assumption, not measured
spring_rate_n_per_mm = None # Unknown; do not infer force
spring_solid_margin = 0.5
spring_socket_depth = 1.5
spring_floor_extra_depth = 0.0 # Increase to reduce preload; keep return at full opening
spring_wire_diameter = 0.3
spring_peg_diameter = 1.2
spring_peg_tip_diameter = 1.0
spring_peg_length = 1.5
spring_seat_width = 3.2
spring_closed_length = 2.8 # Fixed CAD seat spacing, not an adjustment screw
spring_tube_clearance = 0.3
spring_lateral_offset = 1.25
screw_clearance_d = 2.4
lug_width = 5.0
lug_height = 3.5
tpu_outer_diameter = hole4_d + 4.5
tpu_interference = 0.2
pad_ring_height = 1.2
pad_ring_wall = 0.8
pad_ring_clearance = 0.3 # Total diametral clearance for glue and printed fit
pad_ring_inner_diameter = tpu_outer_diameter + pad_ring_clearance
pad_ring_outer_diameter = pad_ring_inner_diameter + 2*pad_ring_wall
pad_diameter = max(pad_diameter, pad_ring_outer_diameter)
# Derived geometry; all lengths mm, angles degrees.
r = tube_od/2
tube_id = tube_od-2*tube_wall
assert 0 < tube_wall < r
lever_bottom = r+pad_back_height
arm_radius = lever_bottom+lever_thickness/2
pivot_x = -arm_radius
pivot_z = 0.0
open_angle = opening_angle_degrees
pad_centre_lift = arm_radius*math.sin(math.radians(open_angle))+lever_bottom*(math.cos(math.radians(open_angle))-1)
rail_x_min = pivot_x-rail_width/2
rail_x_max = pivot_x+rail_width/2
holes = [(4,hole4_y,hole4_d)]
lower_clamp_offset = min(clamp_offset, hole45_spacing-hole5_d/2-clamp_width/2-adjacent_hole_margin)
assert lower_clamp_offset-clamp_width/2 > hub_length/2+axial_clearance+ear_thickness
clamp_ys = [hole4_y-lower_clamp_offset,hole4_y+clamp_offset]
rail_y_min = clamp_ys[0]-clamp_width/2
rail_y_max = clamp_ys[1]+clamp_width/2
clamp_inner_r = r+liner_thickness
clamp_outer_r = clamp_inner_r+clamp_wall
lug_x = clamp_outer_r+lug_width/2-0.5
lug_inner_x = min(lug_x-lug_width/2, math.sqrt(clamp_outer_r**2-(clamp_split_z-clamp_split_gap/2)**2)-0.8)

# Sideways compression spring keeps the key's top clear for the finger.
spring_z = 2.6
spring_floor_x = -(r+1.2) + spring_floor_extra_depth
spring_moving_x = -(r+1.2) - spring_closed_length
spring_socket_rim_x = -(r+1.2) - spring_socket_depth
spring_length_closed = spring_floor_x-spring_moving_x
spring_x = spring_moving_x
rail_x_min = min(rail_x_min, -lug_x-lug_width/2)
assert spring_length_closed > spring_solid_height+spring_solid_margin
assert pad_diameter > max(hole4_d,hole5_d,hole6_d)+2
assert min(hole4_y-hole5_y,hole5_y-hole6_y)>pad_diameter+1

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


# Split clamp rings, joined to spine only at the two ends.
caps=[]
for y in clamp_ys:
    ring=checked(cyl_y(clamp_outer_r,clamp_width,0,y,0)-cyl_y(clamp_inner_r,clamp_width+2,0,y,0))
    upper=checked(ring & box_at(-20,20,y-clamp_width,y+clamp_width,-20,clamp_split_z-clamp_split_gap/2))
    # Fill the notches beneath the arc-to-tab junctions with one continuous base.
    base=box_at(-lug_x-lug_width/2,lug_x+lug_width/2,
                y-clamp_width/2,y+clamp_width/2,
                clamp_split_z-clamp_split_gap/2-lug_height,
                clamp_split_z-clamp_split_gap/2)
    base=checked(base-cyl_y(clamp_inner_r,clamp_width+2,0,y,0))
    upper=checked(upper.fuse(base))
    cap=checked(ring & box_at(-20,20,y-clamp_width,y+clamp_width,clamp_split_z+clamp_split_gap/2,20))
    for x in [-lug_x,lug_x]:
        upper=checked(upper.fuse(box_at((-lug_x-lug_width/2 if x<0 else lug_inner_x),(-lug_inner_x if x<0 else lug_x+lug_width/2),y-clamp_width/2,y+clamp_width/2,clamp_split_z-clamp_split_gap/2-lug_height,clamp_split_z-clamp_split_gap/2)))
        cap=checked(cap.fuse(box_at((-lug_x-lug_width/2 if x<0 else lug_inner_x),(-lug_inner_x if x<0 else lug_x+lug_width/2),y-clamp_width/2,y+clamp_width/2,clamp_split_z+clamp_split_gap/2,clamp_split_z+clamp_split_gap/2+lug_height)))
        cap=checked(cap-hole_z(x,y,-15,15,screw_clearance_d))
    # Open throat lets the deeper cap lift off the tube without sliding from its end.
    cap=checked(cap-box_at(-clamp_inner_r,clamp_inner_r,y-clamp_width,y+clamp_width,-20,0))
    frame=checked(frame.fuse(upper))
    caps.append(cap)
for y in clamp_ys:
    for x in [-lug_x,lug_x]:
        frame=checked(frame-hole_z(x,y,-15,15,screw_clearance_d))
        # Use loose external M2 nuts; tiny captive pockets leave weak tab walls.
show(frame,'frame')
for i,cap in enumerate(caps): show(cap,'clamp_cap_'+str(i))



# Bearings, opening stop and spring seats; the TPU pad stops closure.
bearing_offsets = [-hub_length/2-axial_clearance-ear_thickness/2,hub_length/2+axial_clearance+ear_thickness/2]
for number,y,d in holes:
    for dy in bearing_offsets:
        ear=box_at(pivot_x-hub_radius,pivot_x+hub_radius,y+dy-ear_thickness/2,y+dy+ear_thickness/2,rail_top-0.5,pivot_z)
        ear=checked(ear.fuse(cyl_y(hub_radius,ear_thickness,pivot_x,y+dy,pivot_z)))
        # Full rail-width buttress below the pin; no slender tapered lower stem.
        root=box_at(rail_x_min,rail_x_max,y+dy-ear_thickness/2,y+dy+ear_thickness/2,
                    rail_top-0.5,pivot_z-support_shoulder_drop)
        ear=checked(ear.fuse(root))
        frame=checked(frame.fuse(ear))
        frame=checked(frame-cyl_y((pivot_diameter+pivot_support_clearance)/2,ear_thickness+0.2,pivot_x,y+dy,pivot_z))
    # Broad positive opening stop matches the underside of the rear key tail.
    stop_x0=pivot_x-2.5
    stop_x1=pivot_x-1.0
    def tail_plane_z(x):
        return pivot_z+math.tan(math.radians(open_angle))*(x-pivot_x)-(lever_thickness/2)/math.cos(math.radians(open_angle))
    opening_stop=Pos(0,y+1.8,0)*extrude(Plane.XZ*Polygon((stop_x0,rail_top-0.5),(stop_x1,rail_top-0.5),(stop_x1,tail_plane_z(stop_x1)),(stop_x0,tail_plane_z(stop_x0)),align=None),amount=3.6)
    frame=checked(frame.fuse(opening_stop))
    seat=box_at(spring_socket_rim_x,spring_floor_x+0.9,y-spring_seat_width/2,y+spring_seat_width/2,rail_top-0.2,spring_z+spring_seat_width/2)
    # Recess the housing foot clear of the rotating hub.
    seat=checked(seat-box_at(spring_socket_rim_x-0.1,pivot_x+hub_radius+0.3,y-spring_seat_width,y+spring_seat_width,rail_top-1,0.5))
    frame=checked(frame.fuse(seat))
    socket=Pos((spring_socket_rim_x+spring_floor_x)/2-0.05,y,spring_z)*Rot(0,90,0)*Cylinder((spring_od+spring_fit)/2,spring_floor_x-spring_socket_rim_x+0.1)
    frame=checked(frame-socket)
show(frame,'frame')
show(opening_stop,'opening_stop')

# Curved arm follows the tube from a low side pivot up to the pad cup.
arm_outer=cyl_y(arm_radius+lever_thickness/2,lever_width,0,0,0)
arm_inner=cyl_y(arm_radius-lever_thickness/2,lever_width+2,0,0,0)
lever=checked(arm_outer-arm_inner)
lever=checked(lever & box_at(-arm_radius-5,-0.2,-lever_width,lever_width,0,arm_radius+5))
lever=checked(lever.fuse(hole_z(0,0,lever_bottom,lever_bottom+lever_thickness,pad_diameter)))
lever=checked(lever.fuse(cyl_y(hub_radius,hub_length,pivot_x,0,pivot_z)))
lever=checked(lever.fuse(box_at(pivot_x-3.5,pivot_x+0.5,-lever_width/2,lever_width/2,-lever_thickness/2,lever_thickness/2)))
lever=checked(lever-cyl_y((pivot_diameter+pivot_clearance)/2,hub_length+2,pivot_x,0,pivot_z))
# Clearance around the fixed spring housing throughout the opening sweep.
lever=checked(lever-box_at(spring_socket_rim_x-0.3,0,-lever_width,lever_width,-2,spring_z+spring_seat_width/2+0.3))
# A concave fillet fills the stress-concentrating inside shoulder with material.
transition_edges=[e for e in lever.edges()
                  if abs(e.center().X-(spring_socket_rim_x-0.3))<1e-6
                  and abs(e.center().Z-(spring_z+spring_seat_width/2+0.3))<1e-6
                  and abs(e.length-lever_width)<1e-6]
assert len(transition_edges)==1
lever=checked(fillet(transition_edges,arm_transition_radius))
# A sideways peg faces into the fixed spring socket.
seat_tool=Pos(spring_moving_x+5,0,spring_z)*Rot(0,90,0)*Cylinder((spring_od+spring_fit)/2,10)
lever=checked(lever-seat_tool)
spring_peg=Pos(spring_moving_x,0,spring_z)*Rot(0,90,0)*Cone(spring_peg_diameter/2,spring_peg_tip_diameter/2,spring_peg_length,align=(Align.CENTER,Align.CENTER,Align.MIN))
lever=checked(lever.fuse(spring_peg))
lever=checked(lever-hole_z(0,0,0,lever_bottom,pad_ring_inner_diameter))
# Shallow retaining cup: glue the flat-backed TPU pad inside this ring.
pad_ring=checked(hole_z(0,0,lever_bottom-pad_ring_height,lever_bottom+0.1,pad_ring_outer_diameter)-hole_z(0,0,lever_bottom-pad_ring_height-0.1,lever_bottom+0.2,pad_ring_inner_diameter))
lever=checked(lever.fuse(pad_ring))
show(lever,'lever_blank')

# Continuous concave TPU contact face and plain flat glue backing.
pad_blank=hole_z(0,0,0,lever_bottom,tpu_outer_diameter)
pad_blank=checked(pad_blank-cyl_y(r-tpu_interference,tpu_outer_diameter+2,0,0,0))
show(pad_blank,'tpu_pad')

# Reference lower tube segment, not an acoustically designed whistle.
tube=checked(cyl_y(r,120,0,60,0)-cyl_y(tube_id/2,122,0,60,0))
for number,y,d in [(4,hole4_y,hole4_d),(5,hole5_y,hole5_d),(6,hole6_y,hole6_d)]:
    tube=checked(tube-hole_z(0,y,0,r+1,d))
show(tube,'reference_tube')

keys={}
pads={}
spring_envelopes={}
pins={}
for number,y,d in holes:
    label='key'+str(number)
    RevoluteJoint(label,to_part=frame,axis=Axis((pivot_x,y,pivot_z),(0,1,0)),angular_range=(-open_angle,0))
    key=lever.moved(Location((0,y,0)))
    RigidJoint('pivot',to_part=key,joint_location=frame.joints[label].location)
    frame.joints[label].connect_to(key.joints['pivot'],angle=-open_angle)
    keys[number]=key
    show(key,label)
    pad=pad_blank.moved(Location((0,y,0)))
    pad=pad.rotate(Axis((pivot_x,y,pivot_z),(0,1,0)),-open_angle)
    pads[number]=pad
    show(pad,'pad'+str(number))
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
assembly=Compound(children=[p.moved(Location()) for p in [frame,*caps,tube,*keys.values(),*pads.values(),*spring_envelopes.values(),*pins.values()]])
assembly.label='Burke_single_key_prototype'
show(assembly,'assembly_open')
print('Spring lengths, closed/open/free:',spring_length_closed,spring_length_open,spring_free_length)
print('Pad centre travel and key angle:',pad_centre_lift,open_angle)

# Separate print-oriented copies; assembly remains in instrument coordinates.
def on_bed(part):
    bb=part.bounding_box()
    return part.moved(Location((-(bb.min.X+bb.max.X)/2,-(bb.min.Y+bb.max.Y)/2,-bb.min.Z)))
print_parts={
    'frame_print': on_bed(frame.rotate(Axis.Y,-90)),
    'lever_print': on_bed(lever.rotate(Axis.X,180)),
    'clamp_cap_print': on_bed(caps[0].rotate(Axis.X,90)),
    'tpu_pad_print': on_bed(pad_blank.rotate(Axis.X,180)),
}
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
