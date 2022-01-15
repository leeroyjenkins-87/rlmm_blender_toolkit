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
from mathutils import Matrix, Vector
from math import degrees, radians, pi

class setPosX(bpy.types.Operator):
    bl_idname = "custom.set_pos_x"
    bl_label = "Set Positive X Rotation"
    bl_description = "Change Local Rotation"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
    
        bpy.context.scene.value = 90
        bpy.context.scene.axis = 'X'
        bpy.context.scene.xBool = True
        bpy.context.scene.yBool = False
        bpy.context.scene.zBool = False

        bpy.ops.custom.error_check_rotation()
        
        return {'FINISHED'}


class setNegX(bpy.types.Operator):
    bl_idname = "custom.set_neg_x"
    bl_label = "Set Negative X Rotation"
    bl_description = "Change Local Rotation"

    # @classmethod
    # def poll(cls, context):
        # return context.selected_objects is not None

    def execute(self, context):

        bpy.context.scene.value = -90
        bpy.context.scene.axis = 'X'
        bpy.context.scene.xBool = True
        bpy.context.scene.yBool = False
        bpy.context.scene.zBool = False
        
        bpy.ops.custom.error_check_rotation()
         
        return {'FINISHED'}


class setPosY(bpy.types.Operator):
    bl_idname = "custom.set_pos_y"
    bl_label = "Set Positive Y Rotation"
    bl_description = "Change Local Rotation"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):

        bpy.context.scene.value = 90
        bpy.context.scene.axis = 'Y'
        bpy.context.scene.xBool = False
        bpy.context.scene.yBool = True
        bpy.context.scene.zBool = False
        
        bpy.ops.custom.error_check_rotation()
         
        return {'FINISHED'}


class setNegY(bpy.types.Operator):
    bl_idname = "custom.set_neg_y"
    bl_label = "Set Negative Y Rotation"
    bl_description = "Change Local Rotation"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):

        bpy.context.scene.value = -90
        bpy.context.scene.axis = 'Y'
        bpy.context.scene.xBool = False
        bpy.context.scene.yBool = True
        bpy.context.scene.zBool = False
        
        bpy.ops.custom.error_check_rotation()
        
        return {'FINISHED'}

class setPosZ(bpy.types.Operator):
    bl_idname = "custom.set_pos_z"
    bl_label = "Set Positive Z Rotation"
    bl_description = "Change Local Rotation"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):

        bpy.context.scene.value = 90
        bpy.context.scene.axis = 'Z'
        bpy.context.scene.xBool = False
        bpy.context.scene.yBool = False
        bpy.context.scene.zBool = True
        
        bpy.ops.custom.error_check_rotation()
    
        return {'FINISHED'}

class setNegZ(bpy.types.Operator):
    bl_idname = "custom.set_neg_z"
    bl_label = "Set Negative Z Rotation"
    bl_description = "Change Local Rotation"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):

        bpy.context.scene.value = -90
        bpy.context.scene.axis = 'Z'
        bpy.context.scene.xBool = False
        bpy.context.scene.yBool = False
        bpy.context.scene.zBool = True
        
        bpy.ops.custom.error_check_rotation()
        
        return {'FINISHED'}
        
class errorCheckRotation(bpy.types.Operator):
    bl_idname = "custom.error_check_rotation"
    bl_label = "Set Object Rotation"
    bl_description = "Change Local Rotation"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):

        objHolder = ''
        
        if bpy.context.scene.collectRotations == True:
            if bpy.context.scene.collectionHolder != '':
                objCount = len(bpy.data.collections[bpy.context.scene.collectionHolder].objects[:])
                self.setRotation(objCount, objHolder)
            else:
                bpy.context.scene.errorCode = 0
                bpy.ops.custom.error_message('INVOKE_DEFAULT')                
        else:
            if len(bpy.context.selected_objects) < 1:
                bpy.context.scene.errorCode = 1
                bpy.ops.custom.error_message('INVOKE_DEFAULT')
            else:
                objHolder = bpy.context.selected_objects
                objCount = len(bpy.context.selected_objects[:])
                self.setRotation(objCount, objHolder)
        
        return {'FINISHED'}
        
    def setRotation(self, inVar1, inVar2):
           
        objCount = inVar1
        objHolder = inVar2

        for selectedObj in bpy.context.selected_objects:
            selectedObj.select_set(False)

        loopCount = 0
        
        while loopCount < objCount:

            if bpy.context.scene.collectRotations == True:
                obj = bpy.data.collections[bpy.context.scene.collectionHolder].objects[loopCount]
            else:
                obj = objHolder[loopCount]

            obj.select_set(True)

            bpy.context.view_layer.objects.active = obj
          
           
            bpy.ops.transform.rotate(value=radians(bpy.context.scene.value),
                                     orient_axis=bpy.context.scene.axis,
                                     orient_type='LOCAL',
                                     orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                     orient_matrix_type='LOCAL',
                                     constraint_axis=(bpy.context.scene.xBool, bpy.context.scene.yBool, bpy.context.scene.zBool),
                                     mirror=True,
                                     use_proportional_edit=False,
                                     proportional_edit_falloff='SMOOTH',
                                     proportional_size=1,
                                     use_proportional_connected=False,
                                     use_proportional_projected=False,
                                     release_confirm=True)
            
            # round to 0 decimal places.
            for idx, rot in enumerate(obj.rotation_euler):
                obj.rotation_euler[idx] = radians(round(degrees(rot)%360, 0))

            obj.select_set(False)

            loopCount += 1

        if bpy.context.scene.collectRotations == False:
            loopCount = 0
            while loopCount < objCount:
                objHolder[loopCount].select_set(state=True)
                loopCount += 1

        return {'FINISHED'}