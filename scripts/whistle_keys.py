from build123d import *
from bd_warehouse.fastener import HexNut
import math
# Parametric compression-spring key concept, revision 0.1.
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
pad_thickness = 3.8
pad_compression = 1.2
lever_thickness = 3.0
lever_width = 6.0
pad_diameter = 11.0
pivot_offset = 4.15
pivot_diameter = 2.0
pivot_clearance = 0.25
hub_radius = 2.0
hub_length = 6.0
pad_centre_lift = 4.0
liner_thickness = 0.5
clamp_width = 6.0
clamp_wall = 3.0
clamp_split_gap = 0.8
clamp_offset = 13.0
rail_width = 7.0
rail_top = 5.0
ear_thickness = 2.0
axial_clearance = 0.3
spring_od = 2.4
spring_fit = 0.4
spring_free_length = 6.4
spring_solid_height = 2.9
spring_rate_n_per_mm = 1.71
spring_solid_margin = 0.6
spring_pocket_depth = 0.5
spring_seat_width = 5.0
spring_seat_floor = 1.0
spring_tube_clearance = 0.3
spring_lateral_offset = 0.65
nut_af = 4.0
nut_height = 1.6
nut_fit = 0.25
screw_clearance_d = 2.4
lug_width = 5.0
lug_height = 3.5
# Derived geometry; all lengths mm, angles degrees.
r = tube_od/2
tube_id = tube_od-2*tube_wall
assert 0 < tube_wall < r
pivot_x = -(r+pivot_offset)
lever_bottom = r+pad_thickness-pad_compression
pivot_z = lever_bottom+lever_thickness/2
open_angle = math.degrees(math.asin(pad_centre_lift/-pivot_x))
rail_x_min = pivot_x-rail_width/2
rail_x_max = pivot_x+rail_width/2
holes = [(4,hole4_y,hole4_d),(5,hole5_y,hole5_d),(6,hole6_y,hole6_d)]
clamp_ys = [hole6_y-clamp_offset,hole4_y+clamp_offset]
rail_y_min = clamp_ys[0]-clamp_width/2
rail_y_max = clamp_ys[1]+clamp_width/2
clamp_inner_r = r+liner_thickness
clamp_outer_r = clamp_inner_r+clamp_wall
lug_x = clamp_outer_r+lug_width/2-0.5

spring_x = -(r + spring_lateral_offset)
seat_right = spring_x + spring_seat_width/2
seat_bottom = math.sqrt(max(0, r*r-seat_right*seat_right)) + spring_tube_clearance
seat_floor_z = seat_bottom + spring_seat_floor
spring_top_closed = lever_bottom + spring_pocket_depth
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

def nut_tool(x,y,z0,height):
    return Pos(x,y,z0)*extrude(RegularPolygon((nut_af+nut_fit)/math.sqrt(3),6),amount=height)

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
        frame=checked(frame-cyl_y(pivot_diameter/2,ear_thickness+0.2,pivot_x,y+dy,pivot_z))
    stop_x0=rail_x_min
    stop_x1=rail_x_min+1.0
    stop_top=pivot_z+math.tan(math.radians(open_angle))*(stop_x0-pivot_x)-(lever_thickness/2)/math.cos(math.radians(open_angle))
    frame=checked(frame.fuse(box_at(stop_x0,stop_x1,y-2,y+2,rail_top-0.5,stop_top)))
    frame=checked(frame.fuse(box_at(rail_x_max-0.3,rail_x_max+2,y+2.5,y+3,rail_top-0.5,lever_bottom)))
    seat=box_at(spring_x-spring_seat_width/2,spring_x+spring_seat_width/2,y-spring_seat_width/2,y+spring_seat_width/2,seat_bottom,seat_floor_z+spring_pocket_depth)
    frame=checked(frame.fuse(seat))
    frame=checked(frame-hole_z(spring_x,y,seat_floor_z,seat_floor_z+spring_pocket_depth+0.1,spring_od+spring_fit))
show(frame,'frame')

# Finger contact is circular; the narrower arm leaves room for bearing ears.
lever=box_at(pivot_x-4.5,1,-lever_width/2,lever_width/2,lever_bottom,lever_bottom+lever_thickness)
lever=checked(lever.fuse(hole_z(0,0,lever_bottom,lever_bottom+lever_thickness,pad_diameter)))
lever=checked(lever.fuse(cyl_y(hub_radius,hub_length,pivot_x,0,pivot_z)))
lever=checked(lever-cyl_y((pivot_diameter+pivot_clearance)/2,hub_length+2,pivot_x,0,pivot_z))
lever=checked(lever-hole_z(spring_x,0,lever_bottom-0.1,spring_top_closed,spring_od+spring_fit))
show(lever,'lever_blank')

# Reference lower tube segment, not an acoustically designed whistle.
tube=checked(cyl_y(r,120,0,60,0)-cyl_y(tube_id/2,122,0,60,0))
for number,y,d in holes:
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
    pad=hole_z(0,y,lever_bottom-pad_thickness,lever_bottom,pad_diameter-0.5)
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
    pin=cyl_y(pivot_diameter/2,bearing_offsets[1]-bearing_offsets[0]+ear_thickness+1,pivot_x,y,pivot_z)
    pins[number]=pin
    show(pin,'pin'+str(number))

# Assembly is a named compound; individual print parts are checked separately.
assembly=Compound(children=[p.moved(Location()) for p in [frame,*caps,tube,*keys.values(),*pads.values(),*spring_envelopes.values(),*pins.values()]])
assembly.label='Burke_whistle_key_concept'
show(assembly,'assembly_open')
result=frame
print('Spring lengths, closed/open/free:',spring_length_closed,spring_length_open,spring_free_length)
print('Pad centre travel and key angle:',pad_centre_lift,open_angle)

def export_parts(directory):
    """Optional regeneration export after MCP validation. Directory must exist."""
    for name,part in [('frame',frame),('lever_blank',lever),('clamp_cap_0',caps[0])]:
        export_step(part, str(directory)+'/'+name+'.step')
        export_stl(part, str(directory)+'/'+name+'.stl')
