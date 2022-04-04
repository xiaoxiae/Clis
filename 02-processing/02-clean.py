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

bpy.ops.mesh.primitive_plane_add()
plane_obj = None
for obj in bpy.data.objects:
    if obj.name.lower() == "plane":
        plane_obj = obj

model.location = (0, CUTOFF_OFFSET / 1000, 0)
plane_obj.rotation_euler[0] = math.pi / 2

operation = model.modifiers.new(type="BOOLEAN", name="bool 1")
operation.object = plane_obj
operation.operation = "DIFFERENCE"

# apply the modifier and remove the plane
bpy.context.view_layer.objects.active = model
bpy.ops.object.modifier_apply(modifier="bool 1")

bpy.data.objects.remove(plane_obj, do_unlink=True)

# preserve the object with the most polygons
model.select_set(True)
bpy.ops.mesh.separate(type="LOOSE")

obj_most_vertices = None
obj_most_vertices_count = 0

for obj in bpy.data.objects:
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    if obj_most_vertices_count < len(bm.verts):
        obj_most_vertices_count = len(bm.verts)
        obj_most_vertices = obj

for obj in bpy.data.objects:
    if obj is not obj_most_vertices:
        bpy.data.objects.remove(obj, do_unlink=True)

# decimate it
# this code could probably be more elegant but it sorks
modifier = obj_most_vertices.modifiers.new("DecimateMod", "DECIMATE")
modifier.ratio = 0.03
modifier.use_collapse_triangulate = True

bpy.ops.export_scene.obj(filepath=arguments.output)
