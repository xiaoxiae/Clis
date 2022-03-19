"""A standalone script that is called to convert a hold OBJ file to a simplified OBJ
file with removed floor. It's standalone because it throws SEGFAULT when terminating."""

# links that I used:
# - https://blenderartists.org/t/remove-a-vertex-from-a-bmesh/539966/3
# - https://gist.github.com/neon-ninja/9e535ec20e08979c5f8860d5804bdfae
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("input", help="The input OBJ file path.")
parser.add_argument("output", help="The output OBJ file path.")

arguments = parser.parse_args()

import math
import bpy
import bmesh

import os
import sys

sys.path.append("..")
from config import *
from utilities import *

# remove everything from the scene
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)

bpy.ops.import_scene.obj(filepath=arguments.input)

model = bpy.data.objects[-1]

# modify the mesh using bmesh
bm = bmesh.new()
bm.from_mesh(model.data)


def dist(p1, p2):
    """Return the Euclidean distance of two points in R^d space."""
    return math.sqrt(sum([(x1 - x2) ** 2 for x1, x2 in zip(p1, p2)]))


coordinate_index = 2

cutoff = sum([MARKERS[m][coordinate_index] for m in MARKERS]) / len(MARKERS)

for vertex in list(bm.verts):
    # remove by the average of the marker coordinates
    if vertex.co[coordinate_index] < cutoff:
        bm.verts.remove(vertex)

# convert it back from bmesh
bm.to_mesh(model.data)

# separate by loose parts (there will be some, since markers are likely slightly raised)
bpy.ops.mesh.separate(type="LOOSE")

obj_closest = None
obj_closest_distance = float("inf")

# only preserve the object closest to the origin (only in terms of x and y)
for obj in bpy.data.objects:
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    average_position = [0, 0]
    for vertex in list(bm.verts):
        for i in range(2):
            average_position[i] += vertex.co[i]

    for i in range(2):
        average_position[i] /= len(bm.verts)

    dist_to_origin = dist(average_position, [0, 0])

    if dist_to_origin < obj_closest_distance:
        obj_closest_distance = dist_to_origin
        obj_closest = obj

for obj in bpy.data.objects:
    if obj is not obj_closest:
        bpy.data.objects.remove(obj, do_unlink=True)

# decimate it
# this code could probably be more elegant but it sorks
modifier = model.modifiers.new("DecimateMod", "DECIMATE")
modifier.ratio = 0.03
modifier.use_collapse_triangulate = True

bpy.ops.export_scene.obj(filepath=arguments.output)
