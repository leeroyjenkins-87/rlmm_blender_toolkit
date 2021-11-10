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

#import the bpy module to access blender API
import bpy

class RLMMPJ_PT_Panel(bpy.types.Panel):
    bl_idname = "RLMMPJ_PT_Panel"
    bl_label = "Project Name"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'

    #create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):

        layout = self.layout

        box_projectname = layout.box()
        box_projectname.label(text="Project Name", icon='DESKTOP')

        row_projectname = box_projectname.row()
        row_projectname.prop(context.scene, 'projectName')


class RLMM_PT_Panel(bpy.types.Panel):
    bl_idname = "RLMM_PT_Panel"
    bl_label = "Objects: Location/Rotation"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'

    #create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):

        layout = self.layout

        box_selectarrayobjects = layout.row().box()
        # ICON OBJECT_DATA IS THE SQUARE INSIDE THE SELECT BOX
        box_selectarrayobjects.label(text="Select Array Objects",icon='EYEDROPPER')
        box_selectarrayobjects.prop_search(context.scene, "prefabOBJ", context.scene, "objects")
        box_selectarrayobjects.prop_search(context.scene, "prefabPLANE", context.scene, "objects")

        box_objectinstances = layout.row().box()
        box_objectinstances.label(text="Object Instances", icon='LINKED')
        box_scalefaces = box_objectinstances.box()
        box_scalefaces.prop(context.scene, "scaleFACES")
        box_scalefaces.operator('custom.set_parent', text="Set Parent/Scale")
        box_scalefaces.operator('custom.make_instances_real', text="Make Instances Real")

        box_setrotations = layout.box()
        box_setrotations.label(text="Set Rotation",icon='ORIENTATION_LOCAL')
        box_collectrotations = box_setrotations.box()
        box_collectrotations.prop(context.scene, "collectRotations")

        row_setrotations = box_collectrotations.row(align=True)
        row_setrotations.operator('custom.set_neg_x', text="-X")
        row_setrotations.operator('custom.set_pos_x', text="+X")
        row_setrotations.operator('custom.set_neg_y', text="-Y")
        row_setrotations.operator('custom.set_pos_y', text="+Y")
        row_setrotations.operator('custom.set_neg_z', text="-Z")
        row_setrotations.operator('custom.set_pos_z', text="+Z")

        box_exportdata = layout.box()
        box_exportdata.label(text="Export Data", icon='EXPORT')
        box_collectdata = box_exportdata.box()
        box_collectdata.prop(context.scene, "collectData")
        box_collectdata.prop(context.scene, "collectMaterials")
        box_collectdata.prop(context.scene, "physMat")

        row_confpath = box_collectdata.row()
        row_confpath.prop(context.scene, 'conf_path')
        row_sendtoudk = box_collectdata.row()
        row_sendtoudk.operator('custom.send_to_udk', text="Send to UDK")

class RLMMBrushes_PT_Panel(bpy.types.Panel):
    bl_idname = "RLMMBrushes_PT_Panel"
    bl_label = "Brushes"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'

    #create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):
        layout = self.layout

        box_t3dfile = layout.box()
        box_t3dfile.label(text="T3D File", icon='CUBE')
        box_t3dfile.operator('custom.send_to_t3d', text="Create Custom Brush")
