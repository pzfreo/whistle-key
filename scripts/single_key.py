from build123d import *
import math
# Single-key prototype for hole 4; all dimensions provisional.
# TPU sealing lip is experimental; no physical seal has been verified.
# All lengths mm. Defaults are NOT measured Burke dimensions.
# Edit this parameter block; regenerate through build123d MCP execute_file.
# Small springs and pad sealing must be physically tested before instrument use.
tube_od = 12.7
tube_wall = 0.396875
hole4_y = 85.0
hole5_y = 68.0
hole6_y = 43.0
hole4_d = 6.0
hole5_d = 6.0
hole6_d = 5.0
pad_back_height = 2.6 # Rigid key underside above tube crown
lever_thickness = 3.0
lever_width = 6.0
pad_diameter = 11.0
pivot_offset = 4.15
pivot_diameter = 1.0
pivot_length = 12.0
pivot_clearance = 0.25
pivot_support_clearance = 0.0 # Tune using the PETG fit coupon
hub_radius = 2.0
hub_length = 6.0
pad_centre_lift = 6.0 # Clears the curved lip above the open hole
liner_thickness = 0.5
clamp_width = 6.0
clamp_wall = 3.0
clamp_split_gap = 0.8
clamp_offset = 13.0
rail_width = 7.0
rail_top = 5.0
ear_thickness = 2.0
axial_clearance = 0.3
spring_od = 2.0
spring_fit = 0.4
spring_free_length = 5.0
spring_solid_height = 2.0 # User assumption, not measured
spring_rate_n_per_mm = None # Unknown; do not infer force
spring_solid_margin = 0.5
spring_pocket_depth = 0.5
spring_seat_width = 3.2
spring_closed_length = 2.8 # Fixed CAD seat spacing, not an adjustment screw
spring_tube_clearance = 0.3
spring_lateral_offset = 1.25
screw_clearance_d = 2.4
lug_width = 5.0
lug_height = 3.5
tpu_outer_diameter = 10.5
tpu_recess_diameter = 8.5
tpu_lip_height = 0.8
tpu_interference = 0.2
pad_locator_width = 3.0
pad_locator_length = 2.0
pad_locator_height = 0.8
pad_locator_clearance = 0.2
# Derived geometry; all lengths mm, angles degrees.
r = tube_od/2
tube_id = tube_od-2*tube_wall
assert 0 < tube_wall < r
pivot_x = -(r+pivot_offset)
lever_bottom = r+pad_back_height
pivot_z = lever_bottom+lever_thickness/2
open_angle = math.degrees(math.asin(pad_centre_lift/-pivot_x))
rail_x_min = pivot_x-rail_width/2
rail_x_max = pivot_x+rail_width/2
holes = [(4,hole4_y,hole4_d)]
clamp_ys = [hole4_y-clamp_offset,hole4_y+clamp_offset]
rail_y_min = clamp_ys[0]-clamp_width/2
rail_y_max = clamp_ys[1]+clamp_width/2
clamp_inner_r = r+liner_thickness
clamp_outer_r = clamp_inner_r+clamp_wall
lug_x = clamp_outer_r+lug_width/2-0.5

spring_x = -(r + spring_lateral_offset)
seat_right = spring_x + spring_seat_width/2
seat_bottom = math.sqrt(max(0, r*r-seat_right*seat_right)) + spring_tube_clearance
spring_top_closed = lever_bottom + spring_pocket_depth
seat_floor_z = spring_top_closed - spring_closed_length
assert seat_floor_z - seat_bottom >= 1.0
spring_length_closed = spring_top_closed-seat_floor_z
spring_x_arm = spring_x-pivot_x
assert spring_length_closed > spring_solid_height + spring_solid_margin
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

frame=box_at(rail_x_min,rail_x_max,rail_y_min,rail_y_max,clamp_split_gap/2,rail_top)
show(frame,'frame')


# Split clamp rings, joined to spine only at the two ends.
caps=[]
for y in clamp_ys:
    ring=checked(cyl_y(clamp_outer_r,clamp_width,0,y,0)-cyl_y(clamp_inner_r,clamp_width+2,0,y,0))
    upper=checked(ring & box_at(-20,20,y-clamp_width,y+clamp_width,clamp_split_gap/2,20))
    cap=checked(ring & box_at(-20,20,y-clamp_width,y+clamp_width,-20,-clamp_split_gap/2))
    for x in [-lug_x,lug_x]:
        upper=checked(upper.fuse(box_at(x-lug_width/2,x+lug_width/2,y-clamp_width/2,y+clamp_width/2,clamp_split_gap/2,clamp_split_gap/2+lug_height)))
        cap=checked(cap.fuse(box_at(x-lug_width/2,x+lug_width/2,y-clamp_width/2,y+clamp_width/2,-clamp_split_gap/2-lug_height,-clamp_split_gap/2)))
        cap=checked(cap-hole_z(x,y,-15,15,screw_clearance_d))
    frame=checked(frame.fuse(upper))
    caps.append(cap)
for y in clamp_ys:
    for x in [-lug_x,lug_x]:
        frame=checked(frame-hole_z(x,y,-15,15,screw_clearance_d))
        # Use loose external M2 nuts; tiny captive pockets leave weak tab walls.
show(frame,'frame')
for i,cap in enumerate(caps): show(cap,'clamp_cap_'+str(i))



# Bearings, fixed stops and spring seats; no spring adjustment hardware.
bearing_offsets = [-hub_length/2-axial_clearance-ear_thickness/2,hub_length/2+axial_clearance+ear_thickness/2]
for number,y,d in holes:
    for dy in bearing_offsets:
        ear=box_at(pivot_x-hub_radius,pivot_x+hub_radius,y+dy-ear_thickness/2,y+dy+ear_thickness/2,rail_top-0.5,pivot_z)
        ear=checked(ear.fuse(cyl_y(hub_radius,ear_thickness,pivot_x,y+dy,pivot_z)))
        frame=checked(frame.fuse(ear))
        frame=checked(frame-cyl_y((pivot_diameter+pivot_support_clearance)/2,ear_thickness+0.2,pivot_x,y+dy,pivot_z))
    stop_x0=rail_x_min
    stop_x1=rail_x_min+1.0
    stop_top=pivot_z+math.tan(math.radians(open_angle))*(stop_x0-pivot_x)-(lever_thickness/2)/math.cos(math.radians(open_angle))
    frame=checked(frame.fuse(box_at(stop_x0,stop_x1,y-2,y+2,rail_top-0.5,stop_top)))
    frame=checked(frame.fuse(box_at(rail_x_max-0.3,rail_x_max+2,y+2,y+3,rail_top-0.5,lever_bottom)))
    seat=box_at(spring_x-spring_seat_width/2,spring_x+spring_seat_width/2,y-spring_seat_width/2,y+spring_seat_width/2,seat_bottom,seat_floor_z+spring_pocket_depth)
    frame=checked(frame.fuse(seat))
    frame=checked(frame-hole_z(spring_x,y,seat_floor_z,seat_floor_z+spring_pocket_depth+0.1,spring_od+spring_fit))
    # Sloping gussets eliminate the flat cantilever underside, clear of brass.
    seat_gusset=Pos(0,y+spring_seat_width/2,0)*extrude(Plane.XZ*Polygon((rail_x_max-0.1,seat_bottom-(seat_right-rail_x_max)-0.3),(seat_right,seat_bottom),(rail_x_max-0.1,seat_bottom),align=None),amount=spring_seat_width)
    frame=checked(frame.fuse(seat_gusset))
    stop_gusset=Pos(0,y+3,0)*extrude(Plane.XZ*Polygon((rail_x_max-0.1,rail_top-2.8),(rail_x_max+2,rail_top-0.5),(rail_x_max-0.1,rail_top-0.5),align=None),amount=1.0)
    frame=checked(frame.fuse(stop_gusset))
show(frame,'frame')

# Finger contact is circular; the narrower arm leaves room for bearing ears.
lever=box_at(pivot_x-4.5,1,-lever_width/2,lever_width/2,lever_bottom,lever_bottom+lever_thickness)
lever=checked(lever.fuse(hole_z(0,0,lever_bottom,lever_bottom+lever_thickness,pad_diameter)))
lever=checked(lever.fuse(cyl_y(hub_radius,hub_length,pivot_x,0,pivot_z)))
lever=checked(lever-cyl_y((pivot_diameter+pivot_clearance)/2,hub_length+2,pivot_x,0,pivot_z))
lever=checked(lever-hole_z(spring_x,0,lever_bottom-0.1,spring_top_closed,spring_od+spring_fit))
# Flat finger face is the print-bed face, including the hinge barrel.
lever=checked(lever & box_at(pivot_x-10,pad_diameter,-pad_diameter,pad_diameter,lever_bottom-3,lever_bottom+lever_thickness))
# Rectangular boss keeps the cylindrical TPU pad aligned with the tube.
lever=checked(lever.fuse(box_at(-pad_locator_width/2,pad_locator_width/2,-pad_locator_length/2,pad_locator_length/2,lever_bottom-pad_locator_height,lever_bottom+0.1)))
show(lever,'lever_blank')

# Continuous TPU roof and cylindrical sealing lip; flat back locates in key.
pad_blank=hole_z(0,0,0,lever_bottom,tpu_outer_diameter)
pad_blank=checked(pad_blank-cyl_y(r-tpu_interference,tpu_outer_diameter+2,0,0,0))
recess=checked(cyl_y(r-tpu_interference+tpu_lip_height,tpu_outer_diameter+2,0,0,0) & hole_z(0,0,0,lever_bottom,tpu_recess_diameter))
pad_blank=checked(pad_blank-recess)
locator_w=pad_locator_width+pad_locator_clearance
locator_l=pad_locator_length+pad_locator_clearance
pad_blank=checked(pad_blank-box_at(-locator_w/2,locator_w/2,-locator_l/2,locator_l/2,lever_bottom-pad_locator_height-0.1,lever_bottom+0.1))
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
    spring_start=Vector(spring_x,y,seat_floor_z)
    theta=math.radians(open_angle)
    dx=spring_x-pivot_x
    dz=spring_top_closed-pivot_z
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
    'frame_print': on_bed(frame),
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
