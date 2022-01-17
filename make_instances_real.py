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


class makeInstancesReal(bpy.types.Operator):
    bl_idname = "custom.make_instances_real"
    bl_label = "Seperate And Make Instances Real"
    bl_description = "Seperate And Make Instances Real"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
    
    # if parent does not have child
        if bpy.context.scene.prefabPLANE == None:
            bpy.context.scene.errorCode = 4
            bpy.ops.custom.error_message('INVOKE_DEFAULT') 
            
        elif len(bpy.context.scene.prefabPLANE.children) < 1:
            bpy.context.scene.errorCode = 4
            bpy.ops.custom.error_message('INVOKE_DEFAULT') 
            
        else:
        
            for selectedOBJ in bpy.data.objects:
                selectedOBJ.select_set(False)

            dupePLANE = bpy.context.scene.prefabPLANE

            prefabCollection = bpy.context.scene.prefabPLANE.users_collection[0]

            dupePLANE.select_set(True)

            bpy.context.view_layer.objects.active = dupePLANE

            bpy.ops.object.duplicates_make_real()

            udkCollection = bpy.data.collections.new('UDK Collection')

            bpy.context.scene.collection.children.link(udkCollection)

            objCollection = bpy.data.collections.new(str(bpy.context.scene.prefabOBJ.users_collection[0].name).rstrip('.123456789'))

            bpy.context.scene.collection.children['UDK Collection'].children.link(objCollection)

            bpy.context.scene.collectionHolder = "{}".format(str(objCollection.name))

            for obj in bpy.context.selected_objects:
                if obj.type != 'MESH':
                    continue

                prefabCollection.objects.unlink(obj)

                objCollection.objects.link(obj)

                obj.name = bpy.context.scene['prefabOBJ'].name
                
            bpy.context.scene.collectRotations = True
            bpy.context.scene.collectData = True

        return {'FINISHED'}