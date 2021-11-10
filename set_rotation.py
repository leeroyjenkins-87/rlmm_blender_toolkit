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

class set_rotation(bpy.types.Operator):
    def __init__(self, idname: str, label: str, description: str,
                 value: int, axis: str):

        bl_idname = idname
        bl_label = label
        bl_description = description

        self.value = value
        self.axis = axis

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        if bpy.context.scene.collectRotations == True:
            objCount = len(bpy.data.collections[bpy.context.scene.collectionHolder].objects[:])
        else:
            objHolder = bpy.context.selected_objects
            objCount = len(bpy.context.selected_objects[:])

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

            bpy.ops.transform.rotate(value=radians(self.value), orient_axis=self.axis, orient_type='LOCAL',
                                     orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='LOCAL',
                                     constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False,
                                     proportional_edit_falloff='SMOOTH', proportional_size=1,
                                     use_proportional_connected=False, use_proportional_projected=False,
                                     release_confirm=True)

            for idx, rot in enumerate(obj.rotation_euler):
                obj.rotation_euler[idx] = degrees(rot) % 360

            obj.select_set(False)

            loopCount += 1

        if bpy.context.scene.collectRotations == False:
            loopCount = 0
            while loopCount < objCount:
                objHolder[loopCount].select_set(state=True)
                loopCount += 1

        return {'FINISHED'}


class setPosX(set_rotation):
    def __init__(self):
        super().__init__(idname="custom.set_pos_x",
                         label="Set Positive X Rotation",
                         description="Change Local Rotation",
                         value=90, axis='X')


class setNegX(set_rotation):
    def __init__(self):
        super().__init__(idname="custom.set_neg_x",
                         label="Set Negative X Rotation",
                         description="Change Local Rotation",
                         value=-90, axis='X')


class setPosY(set_rotation):
    def __init__(self):
        super().__init__(idname="custom.set_pos_y",
                         label="Set Positive Y Rotation",
                         description="Change Local Rotation",
                         value=90, axis='Y')


class setNegY(set_rotation):
    def __init__(self):
        super().__init__(idname="custom.set_neg_y",
                         label="Set Negative Y Rotation",
                         description="Change Local Rotation",
                         value=-90, axis='Y')

class setPosZ(set_rotation):
    def __init__(self):
        super().__init__(idname="custom.set_pos_z",
                         label="Set Positive Z Rotation",
                         description="Change Local Rotation",
                         value=90, axis='Z')


class setNegZ(set_rotation):
    def __init__(self):
        super().__init__(idname="custom.set_neg_z",
                         label="Set Negative Z Rotation",
                         description="Change Local Rotation",
                         value=-90, axis='Z')