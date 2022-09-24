import bpy
import bmesh

import os

from math import *

from .mdl import *
from .Utilities import *
from .Blender import*

def build_mdl(mdl, filename):

    bpy.ops.object.add(type="ARMATURE")
    ob = bpy.context.object
    ob.rotation_euler = ( radians(-90), 0, 0 )
    ob.name = str(filename)

    amt = ob.data
    amt.name = str(filename)

    index = 0

    for mdl_mesh in mdl.meshes:

        empty = add_empty(str(index), ob)

        mesh = bpy.data.meshes.new(str(index))
        obj = bpy.data.objects.new(str(index), mesh)

        empty.users_collection[0].objects.link(obj)

        obj.parent = empty

        vertexList = {}
        facesList = []
        normals = []

        last_vertex_count = 0

        bm = bmesh.new()
        bm.from_mesh(mesh)

        # Set vertices
        for j in range(len(mdl_mesh.positions)):
            vertex = bm.verts.new(mdl_mesh.positions[j])

            if mdl_mesh.normals[j] != []:
                vertex.normal = mdl_mesh.normals[j]
                normals.append(mdl_mesh.normals[j])

            vertex.index = last_vertex_count + j

            vertexList[last_vertex_count + j] = vertex

        faces = StripToTriangle(mdl_mesh.faces)
  
        # Set faces
        for j in range(0, len(mdl_mesh.faces)):
            try:
                face = bm.faces.new([vertexList[faces[j][0] + last_vertex_count], vertexList[faces[j][1] + last_vertex_count], vertexList[faces[j][2] + last_vertex_count]])
                face.smooth = True
                facesList.append([face, [vertexList[faces[j][0] + last_vertex_count], vertexList[faces[j][1] + last_vertex_count], vertexList[faces[j][2]] + last_vertex_count]])
            except:
                pass


        bm.to_mesh(mesh)
        bm.free()



        # Set normals
        mesh.use_auto_smooth = True

        if normals != []:
            try:
                mesh.normals_split_custom_set_from_vertices(normals)
            except:
                pass

        last_vertex_count += len(mdl_mesh.positions)

        index += 1        

def main(filepath, files, clear_scene):
    if clear_scene:
        clearScene()

    folder = (os.path.dirname(filepath))

    for i, j in enumerate(files):

        path_to_file = (os.path.join(folder, j.name))

        file = open(path_to_file, 'rb')
        filename =  path_to_file.split("\\")[-1]
        file_extension =  os.path.splitext(path_to_file)[1]
        file_size = os.path.getsize(path_to_file)

        br = BinaryReader(file)

        mdl = MDL()
        mdl.read(br)
        build_mdl(mdl, filename)
