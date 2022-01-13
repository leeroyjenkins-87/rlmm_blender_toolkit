# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy


class setParent(bpy.types.Operator):
    bl_idname = "custom.set_parent"
    bl_label = "Set Parent"
    bl_description = "Parent Object to Plane"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):

        dupeOBJ = bpy.context.scene.prefabOBJ
        dupePLANE = bpy.context.scene.prefabPLANE
        
        if dupeOBJ is None or dupePLANE is None:
            bpy.context.scene.errorCode = 2
            bpy.ops.custom.error_message('INVOKE_DEFAULT')
        
        else:
            # PARENT OBJECT TO PLANE
            dupeOBJ.parent = dupePLANE

            #Does the User want the object to scale? If yes then.
            if bpy.context.scene.scaleFACES == True:
                dupePLANE.use_instance_faces_scale = True
            else:
                dupePLANE.use_instance_faces_scale = False

            # SET INSTANCING TO FACES ON PARENT
            dupePLANE.instance_type = 'FACES'

        return {'FINISHED'}