# SolidPython at https://github.com/SolidCode/SolidPython
from solid import *

# Simple hook to be used as hand tool to grab bags or other stuff without touching it

def rounder(height, radius, tolerance=0.5):
    # Adding 1 mm extra padding to ensure proper sustraction
    res = cube([radius+1, radius+1, height+tolerance*4])-\
          translate([0, 0, -0.5])(cylinder(r=radius, h=height+3))
    res = translate([0, 0, -tolerance])(res)
    return res

def round_cube(width, length, height, radius):
    res = cube([width, length, height])-rotate([0, 0, 90])(rounder(height, radius))
    corner1 = translate([radius, radius, 0])(rotate([0, 0, 180])(rounder(height, radius)))
    corner2 = translate([radius, length-radius, 0])(rotate([0, 0, 90])(rounder(height, radius)))
    corner3 = translate([width-radius, radius, 0])(rotate([0, 0, 270])(rounder(height, radius)))
    corner4 = translate([width-radius, length-radius, 0])(rounder(height, radius))
    return res-corner1-corner2-corner3-corner4

def hollow_round_cube(width, length, height, radius, girth):
    res = round_cube(width + girth * 2, length + girth * 2, height, radius)
    hole = translate([girth, girth, -1])(round_cube(width, length, height + 2, radius))
    return res - hole

def double_hollow_round_cube(width, length, height, radius, girth):
    first = hollow_round_cube(width, length, height, radius, girth)
    second = translate([-width - girth, 0, 0])\
            (hollow_round_cube(width, length, height, radius, girth))
    return first + second

def hook(width, length, height, radius, girth, finger_length):
    res = translate([0, -girth, 0])(hollow_round_cube(width, length, height, radius, girth))
    inn = translate([girth, length-girth-2, -1])(cube([width, length + 4, height + 2]))
    tip = translate([width+girth, length+girth/2, 0])(cylinder(r=girth/2, h=height))
    joint = rounder(height, radius*2, 0)
    join1 = translate([radius*2+girth, length-radius*2+girth+finger_length, 0])\
            (rotate([0, 0, 90])(joint))
    join2 = translate([- width + girth+2+radius/2 -1, length-radius * 2+girth+finger_length, 0])\
            (joint)
    finger = translate([0, -girth*2.5, 0])\
            (cube([girth, finger_length + girth * 2.5 + length, girth]))
    fingertip = translate([girth/2, -girth*2.5, 0])(cylinder(r=girth / 2, h=height))
    return translate([0, -length-girth-finger_length, 0])\
            (res-inn+tip+finger+fingertip+join1+join2)


def tool(width, length, height, radius, girth, finger_length, hook_length):
    handler = double_hollow_round_cube(width, length, height, radius, girth)
    h = hook(width, hook_length, height, radius, girth, finger_length)
    joint = translate([0, -girth, 0])(cube([girth, girth*2, height]))
    return h+handler+joint

# Units are mm
hole_width = 25
hole_length = hole_width
hook_length = hole_width/1.5
finger_length = hole_width*1.5
girth = 8
height = girth
radius = hole_width/4

res = tool(hole_width, hole_length, height, radius, girth, finger_length, hook_length)

scad_render_to_file(res, "grab_hook.scad")
