"""A standalone script that is called to convert a hold OBJ file to a simplified OBJ
file with removed floor. It's standalone because it throws SEGFAULT when terminating."""

# links that I used:
# - https://blenderartists.org/t/remove-a-vertex-from-a-bmesh/539966/3
# - https://gist.github.com/neon-ninja/9e535ec20e08979c5f8860d5804bdfae
import bpy
import bmesh
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("input", help="The input OBJ file path.")
parser.add_argument("output", help="The output OBJ file path.")

arguments = parser.parse_args()

# remove everything from the scene
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)

bpy.ops.import_scene.obj(filepath=arguments.input)

model = bpy.data.objects[-1]

# modify the mesh using bmesh
bm = bmesh.new()
bm.from_mesh(model.data)

for vertex in list(bm.verts):
    # TODO: do something with vertices here
    # if random.random() < 0.2:
    #    bm.verts.remove(vertex)
    pass

# convert it back from bmesh
bm.to_mesh(model.data)

# decimate it
# this code could probably be more elegant but it sorks
modifier = model.modifiers.new('DecimateMod', 'DECIMATE')
modifier.ratio = 0.03
modifier.use_collapse_triangulate = True

bpy.ops.export_scene.obj(filepath=arguments.output)
