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
    bl_label = "UDK: Set Directories"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'

#create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):
        
        layout = self.layout

        boxLayout1 = layout.row().box()
        
        boxLayout1.prop(context.scene, 'projectName')
        boxLayout1.prop(context.scene, 'conf_path')
        
class RLMM_Parent_PT_Panel(bpy.types.Panel):
    bl_idname = "RLMM_Parent_PT_Panel"
    bl_label = "Objects: Parent/Child"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'

#create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):
        
        layout = self.layout

        boxLayout1 = layout.row().box()
        # ICON OBJECT_DATA IS THE SQUARE INSIDE THE SELECT BOX
        boxLayout1.label(text="Select Array Objects",icon='EYEDROPPER')   
        boxLayout1.prop_search(context.scene, "prefabOBJ", context.scene, "objects")
        boxLayout1.prop_search(context.scene, "prefabPLANE", context.scene, "objects")
        
        boxLayout2 = layout.row().box()  
        boxLayout2.label(text="Object Instances",icon='LINKED')
        boxLayout4 = boxLayout2.box()
        boxLayout4.prop(context.scene, "scaleFACES")
        boxLayout4.operator('custom.set_parent', text="Set Parent/Scale")
        boxLayout4.operator('custom.make_instances_real', text="Make Instances Real")

class RLMM_Rotate_PT_Panel(bpy.types.Panel):
    bl_idname = "RLMM_Rotate_PT_Panel"
    bl_label = "Objects: Rotate"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'
    bl_options = {"DEFAULT_CLOSED"}

#create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):
        layout = self.layout
    
        boxLayout3 = layout.box()
        boxLayout3.label(text="Set Rotation",icon='ORIENTATION_LOCAL')
        boxlayout8 = boxLayout3.box()
        boxlayout8.prop(context.scene, "collectRotations")

        subrow = boxlayout8.row(align=True)
        subrow.operator('custom.set_neg_x', text="-X")
        subrow.operator('custom.set_pos_x', text="+X")
        subrow.operator('custom.set_neg_y', text="-Y")
        subrow.operator('custom.set_pos_y', text="+Y")
        subrow.operator('custom.set_neg_z', text="-Z")
        subrow.operator('custom.set_pos_z', text="+Z")
   

class RLMM_Attach_PT_Panel(bpy.types.Panel):
    bl_idname = "RLMM_Attach_PT_Panel"
    bl_label = "Objects: Hard Attach"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'
    bl_options = {"DEFAULT_CLOSED"}

#create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        
        boxLayout1 = layout.box()
        boxLayout1.label(text="Hard Attach to Child",icon='LINKED')
        boxLayout2 = boxLayout1.row().box() 

        rows = 3
        row = boxLayout2.row()
        row.template_list("Hard_Attach_UL_Items", "", scn, "hard_collection", scn, "hard_index", rows=rows)

        col = row.column(align=True)
        col.operator("custom.hard_attach_up_down", icon='ADD', text="").action = 'ADD'
        col.operator("custom.hard_attach_up_down", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("custom.hard_attach_up_down", icon='TRIA_UP', text="").action = 'UP'
        col.operator("custom.hard_attach_up_down", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = boxLayout1.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("custom.remove_duplicates", icon="GHOST_ENABLED")

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

        boxLayout9 = layout.box()
        boxLayout9.label(text="Boost",icon='AUTO')
        boxLayout10 = boxLayout9.box()
        boxLayout10.prop(context.scene, "customBoostMesh")
        boxLayout10.prop(context.scene, "customBoostParticles")

        boxLayout4 = layout.box()
        boxLayout4.label(text="Export Data",icon='EXPORT')
        boxlayout5 = boxLayout4.box()
        boxlayout5.prop(context.scene, "ishardAttach")
        boxlayout5.prop(context.scene, "isArchetype")
        boxlayout5.prop(context.scene, "collectData")
        boxlayout5.prop(context.scene, "collectMaterials")
        boxlayout5.prop(context.scene, "physMat")
        
        row2 = boxlayout5.row()
        row2.operator('custom.send_to_udk', text="Send to UDK")
        
class RLMMBRUSHES_PT_Panel(bpy.types.Panel):
    bl_idname = "RLMMBRUSHES_PT_Panel"
    bl_label = "Brushes"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'
    bl_options = {"DEFAULT_CLOSED"}

#create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):
        
        layout = self.layout

        boxLayout9 = layout.box()
        boxLayout9.label(text="T3D File",icon='CUBE')
        boxLayout9.operator('custom.send_to_t3d', text="Create Custom Brush")
        
class UDKDEFAULT_PT_Panel(bpy.types.Panel):
    bl_idname = "UDKDEFAULT_PT_Panel"
    bl_label = "UDK Default Objects"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'
    bl_options = {"DEFAULT_CLOSED"}

#create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):
        
        layout = self.layout

        boxLayout = layout.box()
        boxLayout.label(text="Objects To Create",icon='EXPORT')
        boxlayout2 = boxLayout.box()
        boxlayout2.prop(context.scene, "defPillar")
        boxlayout2.prop(context.scene, "defGoals")
        boxlayout2.prop(context.scene, "defSpawns")
        boxlayout2.prop(context.scene, "defBoost")
        row = boxlayout2.row()
        row.operator('custom.default_objects', text="Create Default Objects")

class errorMessage(bpy.types.Operator):
    bl_idname = "custom.error_message"
    bl_label = "MESSAGE BOX"                   
    
    def draw(self, context):
    
        errorCodeList = ['"UDK Collection" HAS NOT BEEN CREATED,REMOVE "Auto Collect" OR,RUN "Make Instances Real"',
                     'NO OBJECTS SELECTED',
                     'NO PARENT/CHILD SELECTED',
                     'UDK PROJECT NAME IS MISSING,GO TO "Set Directories",GO TO "UDK",CLICK THE FOLDER ICON,NAVIGATE TO YOUR UDK PROJECT AND SELECT IT',
                     '"Parent/Scale" HAS NOT BEEN SET',
                     'READY TO PASTE INTO UDK']
                     
        layout = self.layout
        
        text = errorCodeList[bpy.context.scene.errorCode].split(',')

        boxLayout = layout.box()
        
        for lines in text:
            boxLayout.label(text=lines)

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)