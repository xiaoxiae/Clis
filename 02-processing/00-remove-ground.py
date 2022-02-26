# https://blenderartists.org/t/remove-a-vertex-from-a-bmesh/539966/3
import bpy, bmesh

bpy.ops.import_scene.obj(filepath="model.obj")

bm = bmesh.new()
bm.from_mesh(bpy.data.objects[-1].data)  # TODO: will this always work?

for vertex in list(bm.verts):
    # TODO: do something with vertices here
    #if random.random() < 0.2:
    #    bm.verts.remove(vertex)
    pass

bm.to_mesh(bpy.data.objects[-1].data)

bpy.ops.export_scene.obj(filepath="adjusted_model.obj")
