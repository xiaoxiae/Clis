"""Calculate the volume of an obj file.
Note that it has to have correct normals!"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", help="The input OBJ file path.")

arguments = parser.parse_args()

import io
from contextlib import redirect_stdout

stdout = io.StringIO()
with redirect_stdout(stdout):
    import bpy
    import bmesh

    # remove everything from the scene
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.ops.import_scene.obj(filepath=arguments.input)

    model = bpy.data.objects[-1]

    # modify the mesh using bmesh
    bm = bmesh.new()
    bm.from_mesh(model.data)
    volume = float( bm.calc_volume() )

print(volume)
