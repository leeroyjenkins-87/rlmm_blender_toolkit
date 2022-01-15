bl_info = {
    "name": "RLMM Toolkit",
    "author": "LeeroyJenkins0G",
    "version": (1, 0, 16),   # addon plugin version
    "blender": (2, 80, 0),  # minimum blender version
    "location": "View3D > Sidebar > Gen Tab",
    "description": "RLMM Toolkit: Blender to UDK",
    "warning": "",
    "wiki_url": "https://rocketleaguemapmaking.com",
    "category": "View 3D",
}

#import the bpy module to access blender API
import bpy
import bmesh
import pyperclip
from mathutils import Matrix, Vector
from math import degrees, radians, pi


#WARNING: this is written and tested for blender 2.79
#blender 2.8 and newer will likely have a different python API

class RLMMPJ_PT_Panel(bpy.types.Panel):
    bl_idname = "RLMMPJ_PT_Panel"
    bl_label = "Set Directories"
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

        boxLayout1 = layout.row().box()
        # ICON OBJECT_DATA IS THE SQUARE INSIDE THE SELECT BOX
        boxLayout1.label(text="Select Array Objects",icon='EYEDROPPER')   
        boxLayout1.prop_search(context.scene, "prefabOBJ", context.scene, "objects")
        boxLayout1.prop_search(context.scene, "prefabPLANE", context.scene, "objects")
        
        boxLayout2 = layout.row().box()  
        boxLayout2.label(text="Object Instances",icon='LINKED')
        boxlayout7 = boxLayout2.box()
        boxlayout7.prop(context.scene, "scaleFACES")
        boxlayout7.operator('custom.set_parent', text="Set Parent/Scale")
        boxlayout7.operator('custom.make_instances_real', text="Make Instances Real")
        
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
        
        boxLayout4 = layout.box()
        boxLayout4.label(text="Export Data",icon='EXPORT')
        boxlayout5 = boxLayout4.box()
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
    
class makeInstancesReal(bpy.types.Operator):
    bl_idname = "custom.make_instances_real"
    bl_label = "Seperate And Make Instances Real"
    bl_description = "Seperate And Make Instances Real"
    
    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
        
    def execute(self, context):
        
        for selectedOBJ in bpy.data.objects:
            selectedOBJ.select_set(False)
        
        dupePLANE = bpy.context.scene.prefabPLANE
        
        prefabCollection = bpy.context.scene.prefabPLANE.users_collection[0]
        
        dupePLANE.select_set(True)

        bpy.context.view_layer.objects.active = dupePLANE

        bpy.ops.object.duplicates_make_real()
        
        if ('UDK Collection' not in str(bpy.data.collections[:])):
            udkCollection = bpy.data.collections.new('UDK Collection')
            bpy.context.scene.collection.children.link(udkCollection)
        
        if (str(bpy.context.scene.prefabOBJ.users_collection[0].name).rstrip('.123456789') not in str(bpy.data.collections['UDK Collection'].children[:])):
            objCollection = bpy.data.collections.new(str(bpy.context.scene.prefabOBJ.users_collection[0].name).rstrip('.123456789'))
            bpy.context.scene.collection.children['UDK Collection'].children.link(objCollection)
        else:
            #DOES A COLLECTION WITH THIS NAME EXIST AND WHERE IS IT
            #collChild = #found collection index
            objCollection = bpy.context.scene.collection.children['UDK Collection'].children[collChild]
        
        bpy.context.scene.collectionHolder = "{}".format(str(objCollection.name))
        
        for obj in bpy.context.selected_objects:
            if obj.type != 'MESH':
                continue
            
            prefabCollection.objects.unlink(obj)
            
            objCollection.objects.link(obj)
            
            obj.name = bpy.context.scene['prefabOBJ'].name
        
        return {'FINISHED'}
    
    
class setNegX(bpy.types.Operator):
    bl_idname = "custom.set_neg_x"
    bl_label = "Set Negative X Rotation"
    bl_description = "Change Local Rotation"
    
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
            
            bpy.ops.transform.rotate(value=radians(-90), orient_axis='X', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

            objRotationX = obj.rotation_euler[0]
            objRotationY = obj.rotation_euler[1]
            objRotationZ = obj.rotation_euler[2]
            
            if objRotationZ >= radians(360):
                obj.rotation_euler[2] = objRotationZ + radians(360) * round(objRotationZ / radians(360), 0)
            elif objRotationZ <= radians(360):
                obj.rotation_euler[2] = objRotationZ - radians(360) * round(objRotationZ / radians(360), 0)
            if objRotationY >= radians(360):
                obj.rotation_euler[1] = objRotationY + radians(360) * round(objRotationY / radians(360), 0)
            elif objRotationY <= radians(360):
                obj.rotation_euler[1] = objRotationY - radians(360) * round(objRotationY / radians(360), 0)
            if objRotationX >= radians(360):
                obj.rotation_euler[0] = objRotationX + radians(360) * round(objRotationX / radians(360), 0)
            elif objRotationX <= radians(360):
                obj.rotation_euler[0] = objRotationX - radians(360) * round(objRotationX / radians(360), 0)
 
            obj.select_set(False)
            
            loopCount += 1
            
        if bpy.context.scene.collectRotations == False:
            loopCount = 0
            while loopCount < objCount:
                objHolder[loopCount].select_set(state=True)
                loopCount += 1
    
        return {'FINISHED'}
    
class setPosX(bpy.types.Operator):
    bl_idname = "custom.set_pos_x"
    bl_label = "Set Positive X Rotation"
    bl_description = "Change Local Rotation"
    
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
            
            bpy.ops.transform.rotate(value=radians(90), orient_axis='X', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

            
            objRotationX = obj.rotation_euler[0]
            objRotationY = obj.rotation_euler[1]
            objRotationZ = obj.rotation_euler[2]
            
            if objRotationZ >= radians(360):
                obj.rotation_euler[2] = objRotationZ + radians(360) * round(objRotationZ / radians(360), 0)
            elif objRotationZ <= radians(360):
                obj.rotation_euler[2] = objRotationZ - radians(360) * round(objRotationZ / radians(360), 0)
            if objRotationY >= radians(360):
                obj.rotation_euler[1] = objRotationY + radians(360) * round(objRotationY / radians(360), 0)
            elif objRotationY <= radians(360):
                obj.rotation_euler[1] = objRotationY - radians(360) * round(objRotationY / radians(360), 0)
            if objRotationX >= radians(360):
                obj.rotation_euler[0] = objRotationX + radians(360) * round(objRotationX / radians(360), 0)
            elif objRotationX <= radians(360):
                obj.rotation_euler[0] = objRotationX - radians(360) * round(objRotationX / radians(360), 0)
 
            obj.select_set(False)
            
            loopCount += 1
            
        if bpy.context.scene.collectRotations == False:
            loopCount = 0
            while loopCount < objCount:
                objHolder[loopCount].select_set(state=True)
                loopCount += 1
            
        return {'FINISHED'}
    
class setNegY(bpy.types.Operator):
    bl_idname = "custom.set_neg_y"
    bl_label = "Set Negative Y Rotation"
    bl_description = "Change Local Rotation"
    
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
            
            bpy.ops.transform.rotate(value=radians(-90), orient_axis='Y', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
            
            objRotationX = obj.rotation_euler[0]
            objRotationY = obj.rotation_euler[1]
            objRotationZ = obj.rotation_euler[2]
            
            if objRotationZ >= radians(360):
                obj.rotation_euler[2] = objRotationZ + radians(360) * round(objRotationZ / radians(360), 0)
            elif objRotationZ <= radians(360):
                obj.rotation_euler[2] = objRotationZ - radians(360) * round(objRotationZ / radians(360), 0)
            if objRotationY >= radians(360):
                obj.rotation_euler[1] = objRotationY + radians(360) * round(objRotationY / radians(360), 0)
            elif objRotationY <= radians(360):
                obj.rotation_euler[1] = objRotationY - radians(360) * round(objRotationY / radians(360), 0)
            if objRotationX >= radians(360):
                obj.rotation_euler[0] = objRotationX + radians(360) * round(objRotationX / radians(360), 0)
            elif objRotationX <= radians(360):
                obj.rotation_euler[0] = objRotationX - radians(360) * round(objRotationX / radians(360), 0)
          
            obj.select_set(False)
            
            loopCount += 1
            
        if bpy.context.scene.collectRotations == False:
            loopCount = 0
            while loopCount < objCount:
                objHolder[loopCount].select_set(state=True)
                loopCount += 1
    
        return {'FINISHED'}
    
class setPosY(bpy.types.Operator):
    bl_idname = "custom.set_pos_y"
    bl_label = "Set Positive Y Rotation"
    bl_description = "Change Local Rotation"
    
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
            
            bpy.ops.transform.rotate(value=radians(90), orient_axis='Y', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

            objRotationX = obj.rotation_euler[0]
            objRotationY = obj.rotation_euler[1]
            objRotationZ = obj.rotation_euler[2]
            
            if objRotationZ >= radians(360):
                obj.rotation_euler[2] = objRotationZ + radians(360) * round(objRotationZ / radians(360), 0)
            elif objRotationZ <= radians(360):
                obj.rotation_euler[2] = objRotationZ - radians(360) * round(objRotationZ / radians(360), 0)
            if objRotationY >= radians(360):
                obj.rotation_euler[1] = objRotationY + radians(360) * round(objRotationY / radians(360), 0)
            elif objRotationY <= radians(360):
                obj.rotation_euler[1] = objRotationY - radians(360) * round(objRotationY / radians(360), 0)
            if objRotationX >= radians(360):
                obj.rotation_euler[0] = objRotationX + radians(360) * round(objRotationX / radians(360), 0)
            elif objRotationX <= radians(360):
                obj.rotation_euler[0] = objRotationX - radians(360) * round(objRotationX / radians(360), 0)
        
            obj.select_set(False)
            
            loopCount += 1
            
        if bpy.context.scene.collectRotations == False:
            loopCount = 0
            while loopCount < objCount:
                objHolder[loopCount].select_set(state=True)
                loopCount += 1
    
        return {'FINISHED'}
    
class setNegZ(bpy.types.Operator):
    bl_idname = "custom.set_neg_z"
    bl_label = "Set Negative Y Rotation"
    bl_description = "Change Local Rotation"
    
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
            
            bpy.ops.transform.rotate(value=radians(-90), orient_axis='Z', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

            objRotationX = obj.rotation_euler[0]
            objRotationY = obj.rotation_euler[1]
            objRotationZ = obj.rotation_euler[2]
            
            if objRotationZ >= radians(360):
                obj.rotation_euler[2] = objRotationZ + radians(360) * round(objRotationZ / radians(360), 0)
            elif objRotationZ <= radians(360):
                obj.rotation_euler[2] = objRotationZ - radians(360) * round(objRotationZ / radians(360), 0)
            if objRotationY >= radians(360):
                obj.rotation_euler[1] = objRotationY + radians(360) * round(objRotationY / radians(360), 0)
            elif objRotationY <= radians(360):
                obj.rotation_euler[1] = objRotationY - radians(360) * round(objRotationY / radians(360), 0)
            if objRotationX >= radians(360):
                obj.rotation_euler[0] = objRotationX + radians(360) * round(objRotationX / radians(360), 0)
            elif objRotationX <= radians(360):
                obj.rotation_euler[0] = objRotationX - radians(360) * round(objRotationX / radians(360), 0)
 
            obj.select_set(False)
            
            loopCount += 1
            
        if bpy.context.scene.collectRotations == False:
            loopCount = 0
            while loopCount < objCount:
                objHolder[loopCount].select_set(state=True)
                loopCount += 1
    
        return {'FINISHED'}
    
class setPosZ(bpy.types.Operator):
    bl_idname = "custom.set_pos_z"
    bl_label = "Set Positive Z Rotation"
    bl_description = "Change Local Rotation"
    
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
            
            bpy.ops.transform.rotate(value=radians(90), orient_axis='Z', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)

            objRotationX = obj.rotation_euler[0]
            objRotationY = obj.rotation_euler[1]
            objRotationZ = obj.rotation_euler[2]
            
            if objRotationZ >= radians(360):
                obj.rotation_euler[2] = objRotationZ + radians(360) * round(objRotationZ / radians(360), 0)
            elif objRotationZ <= radians(360):
                obj.rotation_euler[2] = objRotationZ - radians(360) * round(objRotationZ / radians(360), 0)
            if objRotationY >= radians(360):
                obj.rotation_euler[1] = objRotationY + radians(360) * round(objRotationY / radians(360), 0)
            elif objRotationY <= radians(360):
                obj.rotation_euler[1] = objRotationY - radians(360) * round(objRotationY / radians(360), 0)
            if objRotationX >= radians(360):
                obj.rotation_euler[0] = objRotationX + radians(360) * round(objRotationX / radians(360), 0)
            elif objRotationX <= radians(360):
                obj.rotation_euler[0] = objRotationX - radians(360) * round(objRotationX / radians(360), 0)
     
            obj.select_set(False)
            
            loopCount += 1
            
        if bpy.context.scene.collectRotations == False:
            loopCount = 0
            while loopCount < objCount:
                objHolder[loopCount].select_set(state=True)
                loopCount += 1

        return {'FINISHED'}
    
class sendToUDK(bpy.types.Operator):
    bl_idname = "custom.send_to_udk"
    bl_label = "Send to UDK"
    bl_description = "Creates Object Data"

    
    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
    
    def execute(self, context):
        
        outputFile = '{}{}'.format(bpy.path.abspath(bpy.context.scene.conf_path), "Blender2UDK.csv")
        textUDK = ""
        
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
            
            # LOCATION XYZ
            # --------------------------------------------------------------------
            center = obj.location
            centerX, centerY, centerZ = center[0]*100, center[1]*100, center[2]*100
            d, e, f = round(-centerX, 6), round(centerY, 6), round(centerZ, 6),
            locationString = 'Location=(X={:f},Y={:f},Z={:f})'.format(d, e, f)
            
            # ROTATION XYZ 
            # --------------------------------------------------------------------
            orientationX = degrees(obj.rotation_euler.x)*-1
            orientationY = degrees(obj.rotation_euler.y)
            orientationZ = degrees(obj.rotation_euler.z)*-1
            a, b, c = round(orientationX * (65536 / 360)), round(orientationY * (65536 / 360)), round(orientationZ * (65536 / 360))
            rotationString = 'Rotation=(Pitch={},Yaw={},Roll={})'.format(b, c, a)

            # SCALE XYZ
            # --------------------------------------------------------------------
            objScaleX = round(obj.scale[0], 6)
            objScaleY = round(obj.scale[1], 6)
            objScaleZ = round(obj.scale[2], 6)
            scaleString = 'DrawScale3D=(X={},Y={},Z={})'.format(objScaleX, objScaleY, objScaleZ)
                        
            # PROJECT NAME
            # --------------------------------------------------------------------
            mapDirectory = bpy.context.scene['projectName'].split('.')
            mapName = mapDirectory[-2].split("\\")
            
            # STATICMESH NAME
            # --------------------------------------------------------------------
            objName = obj.name.split('.')
            staticString = "{}.{}".format(mapName[-1], objName[0])
            
            
            # MATERIAL LIST
            # --------------------------------------------------------------------
            materialCount = 0
            materialNames = ''
            
            if bpy.context.scene.collectMaterials == True:
                
                for objSlots in obj.material_slots:
                    materialSlots = objSlots.material.name.lstrip('"').rstrip('"').replace("'", "").lstrip("Material'")
                    materialString = "Materials({})=Material'{}'\n\t\t\t\t\t".format(materialCount, materialSlots)
                    materialCount += 1
                    materialNames += materialString
            
            # LAYER
            # --------------------------------------------------------------------
            layerString = 'Layer="{}"'.format(str(obj.users_collection[0].name.rstrip(".0123456789")))
            
            # TAG
            # --------------------------------------------------------------------
            tagString = 'Tag="{}"'.format(str(objName[0]).rstrip(".0123456789"))
            
            # PHYSICAL MATERIAL APPLIED
            # --------------------------------------------------------------------
            if bpy.context.scene.physMat == True:
                physString = "PhysMaterialOverride=PhysicalMaterial'PhysicalMaterials.Collision_Sticky'"
            else:
                physString = ''
                
            # FORMATTING FOR STATICMESH 
            # --------------------------------------------------------------------
            if ('StaticMesh' in str(objName)):
                num = str(bpy.context.scene.numberSequencer).zfill(10)
                textUDK += f"""
Begin Map
   Begin Level
      Begin Actor Class=StaticMeshActor Name={str(objName[0])}_{num} Archetype=StaticMeshActor'Engine.Default__StaticMeshActor'
         Begin Object Class=StaticMeshComponent Name=StaticMeshActor_{num} ObjName=StaticMeshComponent{num} Archetype=StaticMeshComponent'Engine.Default__StaticMeshActor:StaticMeshComponent0'
            StaticMesh=StaticMesh'{staticString}'
            VertexPositionVersionNumber=1
            {materialNames.rstrip()}
            ReplacementPrimitive=None
            bAllowApproximateOcclusion=True
            bAcceptsDynamicDecals=False
            bForceDirectLightMap=True
            bUsePrecomputedShadows=True
            bDisableAllRigidBody=False
            LightingChannels=(bInitialized=True,Static=True)
            {physString}
            Name="StaticMeshComponent"
            ObjectArchetype=StaticMeshComponent'Engine.Default__StaticMeshActor:StaticMeshComponent0'
         End Object
         StaticMeshComponent=StaticMeshComponent'StaticMeshComponent{num}'
         Components(0)=StaticMeshComponent'StaticMeshComponent{num}'
         {locationString}
         {rotationString}
         {scaleString}
         {tagString}
         {layerString}
         BlockRigidBody=True
         CreationTime=0
         CollisionComponent=StaticMeshComponent'StaticMeshComponent'
         Name="{str(objName[0])}_{num}"
         ObjectArchetype=StaticMeshActor'Engine.Default__StaticMeshActor'
      End Actor
   End Level
Begin Surface
End Surface
End Map
        """#.format(num, num, num, staticString, materialNames.rstrip(), physString, num, num, num, locationString, rotationString, scaleString, tagString, layerString, num)
            
            # FORMATTING FOR SPOTLIGHT 
            # --------------------------------------------------------------------
            elif ('Spot' in str(objName)):
                bpy.ops.custom.set_pos_y()
                # ROTATION XYZ FOR SPOTLIGHTS IS NEGATIVE 90 DEGREES IN UDK SO WE HAVE TO ADJUST IT.
                # --------------------------------------------------------------------
                orientationX = degrees(obj.rotation_euler.x)*-1
                orientationY = degrees(obj.rotation_euler.y)
                orientationZ = degrees(obj.rotation_euler.z)*-1
                a, b, c = round(orientationX * (65536 / 360)), round(orientationY * (65536 / 360)), round(orientationZ * (65536 / 360))
                
                rotationString = 'Rotation=(Pitch={},Yaw={},Roll={})'.format(b, c, a)
                
                bpy.ops.custom.set_neg_y()
                
                textUDK += f"""Begin Map
   Begin Level
      Begin Actor Class=SpotLightToggleable Name=SpotLightToggleable_1 Archetype=SpotLightToggleable'Engine.Default__SpotLightToggleable'
         Begin Object Class=DrawLightConeComponent Name=DrawInnerCone0 ObjName=DrawLightConeComponent_2 Archetype=DrawLightConeComponent'Engine.Default__SpotLightToggleable:DrawInnerCone0'
            ConeRadius=1024.000000
            ConeAngle=0.000000
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="DrawLightConeComponent_2"
            ObjectArchetype=DrawLightConeComponent'Engine.Default__SpotLightToggleable:DrawInnerCone0'
         End Object
         Begin Object Class=DrawLightConeComponent Name=DrawOuterCone0 ObjName=DrawLightConeComponent_3 Archetype=DrawLightConeComponent'Engine.Default__SpotLightToggleable:DrawOuterCone0'
            ConeColor=(B=255,G=255,R=200,A=255)
            ConeRadius=1024.000000
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="DrawLightConeComponent_3"
            ObjectArchetype=DrawLightConeComponent'Engine.Default__SpotLightToggleable:DrawOuterCone0'
         End Object
         Begin Object Class=DrawLightRadiusComponent Name=DrawLightRadius0 ObjName=DrawLightRadiusComponent_2 Archetype=DrawLightRadiusComponent'Engine.Default__SpotLightToggleable:DrawLightRadius0'
            SphereRadius=1024.000000
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="DrawLightRadiusComponent_2"
            ObjectArchetype=DrawLightRadiusComponent'Engine.Default__SpotLightToggleable:DrawLightRadius0'
         End Object
         Begin Object Class=DrawLightRadiusComponent Name=DrawLightSourceRadius0 ObjName=DrawLightRadiusComponent_3 Archetype=DrawLightRadiusComponent'Engine.Default__SpotLightToggleable:DrawLightSourceRadius0'
            SphereColor=(B=0,G=239,R=231,A=255)
            SphereRadius=32.000000
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="DrawLightRadiusComponent_3"
            ObjectArchetype=DrawLightRadiusComponent'Engine.Default__SpotLightToggleable:DrawLightSourceRadius0'
         End Object
         Begin Object Class=SpotLightComponent Name=SpotLightComponent0 ObjName=SpotLightComponent_1 Archetype=SpotLightComponent'Engine.Default__SpotLightToggleable:SpotLightComponent0'
            PreviewInnerCone=DrawLightConeComponent'DrawLightConeComponent_2'
            PreviewOuterCone=DrawLightConeComponent'DrawLightConeComponent_3'
            CachedParentToWorld=(XPlane=(W=0.000000,X=0.000000,Y=0.000000,Z=-1.000000),YPlane=(W=0.000000,X=-0.000000,Y=1.000000,Z=-0.000000),ZPlane=(W=0.000000,X=1.000000,Y=0.000000,Z=0.000000),WPlane=(W=1.000000,X=-60.936401,Y=144.001099,Z=1035.462280))
            PreviewLightRadius=DrawLightRadiusComponent'DrawLightRadiusComponent_2'
            LightmassSettings=(LightSourceRadius=32.000000,IndirectLightingScale=0.000000)
            PreviewLightSourceRadius=DrawLightRadiusComponent'DrawLightRadiusComponent_3'
            LightGuid=(A=199097462,B=1258459027,C=-1227397451,D=-1066570931)
            LightmapGuid=(A=1471253091,B=1300878571,C=1949417371,D=346712220)
            CastDynamicShadows=False
            bPrecomputedLightingIsValid=False
            LightingChannels=(Dynamic=False)
            LightAffectsClassification=LAC_STATIC_AFFECTING
            Name="SpotLightComponent_1"
            ObjectArchetype=SpotLightComponent'Engine.Default__SpotLightToggleable:SpotLightComponent0'
         End Object
         Begin Object Class=SpriteComponent Name=Sprite ObjName=SpriteComponent_254 Archetype=SpriteComponent'Engine.Default__SpotLightToggleable:Sprite'
            Sprite=Texture2D'EditorResources.LightIcons.Light_Spot_Toggleable_Statics'
            SpriteCategoryName="Lighting"
            ReplacementPrimitive=None
            HiddenGame=True
            AlwaysLoadOnClient=False
            AlwaysLoadOnServer=False
            LightingChannels=(bInitialized=True,Dynamic=True)
            Scale=0.250000
            Name="SpriteComponent_254"
            ObjectArchetype=SpriteComponent'Engine.Default__SpotLightToggleable:Sprite'
         End Object
         Begin Object Class=ArrowComponent Name=ArrowComponent0 ObjName=ArrowComponent_72 Archetype=ArrowComponent'Engine.Default__SpotLightToggleable:ArrowComponent0'
            ArrowColor=(B=255,G=200,R=150,A=255)
            bTreatAsASprite=True
            SpriteCategoryName="Lighting"
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="ArrowComponent_72"
            ObjectArchetype=ArrowComponent'Engine.Default__SpotLightToggleable:ArrowComponent0'
         End Object
         LightComponent=SpotLightComponent'SpotLightComponent_1'
         Components(0)=SpriteComponent'SpriteComponent_254'
         Components(1)=DrawLightRadiusComponent'DrawLightRadiusComponent_2'
         Components(2)=DrawLightConeComponent'DrawLightConeComponent_2'
         Components(3)=DrawLightConeComponent'DrawLightConeComponent_3'
         Components(4)=DrawLightRadiusComponent'DrawLightRadiusComponent_3'
         Components(5)=SpotLightComponent'SpotLightComponent_1'
         Components(6)=ArrowComponent'ArrowComponent_72'
         {locationString}
         {rotationString}
         {scaleString}
         CreationTime=953.067566
         {tagString}
         {layerString}
         Name="SpotLightToggleable_1"
         ObjectArchetype=SpotLightToggleable'Engine.Default__SpotLightToggleable'
      End Actor
   End Level
Begin Surface
End Surface
End Map"""

            elif ('GoalVolume' in str(objName)):
                
                bpy.ops.custom.send_to_t3d()
                
                num = str(bpy.context.scene.numberSequencer).zfill(10)
                
                textUDK += f"""
Begin Map
   Begin Level
      Begin Actor Class=GoalVolume_TA Name=GoalVolume_TA_{num} Archetype=GoalVolume_TA'tagame.Default__GoalVolume_TA'
         Begin Object Class=Polys Name=Polys_{num}
            Name="Polys_{num}"
            ObjectArchetype=Polys'Engine.Default__Polys'
         End Object
         Begin Object Class=Goal_TA Name=DefaultGoal ObjName=Goal_TA_{num} Archetype=Goal_TA'tagame.Default__GoalVolume_TA:DefaultGoal'
            Name="Goal_TA_{num}"
            ObjectArchetype=Goal_TA'tagame.Default__GoalVolume_TA:DefaultGoal'
         End Object
         Begin Object Class=BrushComponent Name=BrushComponent0 ObjName=BrushComponent_{num} Archetype=BrushComponent'tagame.Default__GoalVolume_TA:BrushComponent0'
            Brush=Model'Model_{num}'
            ReplacementPrimitive=None
            bAcceptsLights=True
            CollideActors=True
            BlockNonZeroExtent=True
            bDisableAllRigidBody=True
            AlwaysLoadOnClient=True
            AlwaysLoadOnServer=True
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="BrushComponent_{num}"
            ObjectArchetype=BrushComponent'tagame.Default__GoalVolume_TA:BrushComponent0'
         End Object
         Goal=Goal_TA'Goal_TA_{num}'
         Begin Brush Name=Model_{num}
            {bpy.context.scene.textT3d}
         End Brush
         Brush=Model'Model_{num}'
         BrushComponent=BrushComponent'BrushComponent_{num}'
         Components(0)=BrushComponent'BrushComponent_{num}'
         {locationString}
         {rotationString}
         {scaleString}
         CreationTime=0
         {tagString}
         CollisionComponent=BrushComponent'BrushComponent_{num}'
         Name="GoalVolume_TA_{num}"
         ObjectArchetype=GoalVolume_TA'tagame.Default__GoalVolume_TA'
      End Actor
   End Level
Begin Surface
End Surface
End Map
"""
            elif ('DynamicTrigger' in str(objName)):
                    
                bpy.ops.custom.send_to_t3d()
                
                num = str(bpy.context.scene.numberSequencer).zfill(10)
                
                textUDK += f"""Begin Map
   Begin Level
      Begin Actor Class=DynamicTriggerVolume Name={str(objName[0])}_{num} Archetype=DynamicTriggerVolume'Engine.Default__DynamicTriggerVolume'
         Begin Object Class=Polys Name=Polys_{num}
            Name="Polys_{num}"
            ObjectArchetype=Polys'Engine.Default__Polys'
         End Object
         Begin Object Class=BrushComponent Name=BrushComponent0 ObjName=BrushComponent_{num} Archetype=BrushComponent'Engine.Default__DynamicTriggerVolume:BrushComponent0'
            Brush=Model'Model_{num}'
            ReplacementPrimitive=None
            bAcceptsLights=True
            CollideActors=True
            BlockNonZeroExtent=True
            bDisableAllRigidBody=True
            AlwaysLoadOnClient=True
            AlwaysLoadOnServer=True
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="BrushComponent_{num}"
            ObjectArchetype=BrushComponent'Engine.Default__DynamicTriggerVolume:BrushComponent0'
         End Object
         Begin Brush Name=Model_{num}
            {bpy.context.scene.textT3d}
         End Brush
         Brush=Model'Model_{num}'
         BrushComponent=BrushComponent'BrushComponent_{num}'
         Components(0)=BrushComponent'BrushComponent_{num}'
         {locationString}
         {rotationString}
         {scaleString}
         CreationTime=0
         {tagString}
         CollisionComponent=BrushComponent'BrushComponent_{num}'
         Name="{str(objName[0])}_{num}"
         ObjectArchetype=DynamicTriggerVolume'Engine.Default__DynamicTriggerVolume'
      End Actor
   End Level
Begin Surface
End Surface
End Map"""

            # FORMATTTING FOR EVERYTHING ELSE 
            # --------------------------------------------------------------------
            else:
                textUDK += f"""
Begin Map
   Begin Level
      Begin Actor Class=StaticMeshActor Name={str(objName[0])}_{num} Archetype=StaticMeshActor'Engine.Default__StaticMeshActor'
         Begin Object Class=StaticMeshComponent Name=StaticMeshComponent{num} ObjName=StaticMeshComponent Archetype=StaticMeshComponent'Engine.Default__StaticMeshActor:StaticMeshComponent{num}'
            StaticMesh=StaticMesh'{staticString}'
            VertexPositionVersionNumber=1
            {materialNames.rstrip()}
            ReplacementPrimitive=None
            bAllowApproximateOcclusion=True
            bAcceptsDynamicDecals=False
            bForceDirectLightMap=True
            bUsePrecomputedShadows=True
            bDisableAllRigidBody=False
            LightingChannels=(bInitialized=True,Static=True)
            {physString}
            Name="StaticMeshComponent"
            ObjectArchetype=StaticMeshComponent'Engine.Default__StaticMeshActor:StaticMeshComponent{num}'
         End Object
         StaticMeshComponent=StaticMeshComponent'StaticMeshComponent{num}'
         Components(0)=StaticMeshComponent'StaticMeshComponent{num}'
         {locationString}
         {rotationString}
         {scaleString}
         {tagString}
         {layerString}
         BlockRigidBody=True
         CreationTime=0
         CollisionComponent=StaticMeshComponent'StaticMeshComponent'
         Name="{str(objName[0])}_{num}"
         ObjectArchetype=StaticMeshActor'Engine.Default__StaticMeshActor'
      End Actor
   End Level
Begin Surface
End Surface
End Map
        """
        
            loopCount += 1
            
            bpy.context.scene.numberSequencer += 1


        f = open( outputFile, 'w' )
        f.writelines( textUDK.rstrip() )
        f.close()   
        pyperclip.copy(textUDK.rstrip())
        
        return {'FINISHED'}

class sendToT3d(bpy.types.Operator):
    bl_idname = "custom.send_to_t3d"
    bl_label = "Send to T3d"
    bl_description = "Creates T3d File for UDK"

    
    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
    
    def execute(self, context):
        
        objectString = bpy.context.active_object
        
        objectStringName = objectString.name.rstrip('.0123456789')
        
        bpy.context.scene.textT3d = 'Begin PolyList'
        
        linkCount = 0
        
        for f in objectString.data.polygons:
            
            verticeList = [linkCount]
            
            originShort = objectString.data.vertices[f.vertices[0]].co
            
            originList = [originShort.x, originShort.y, originShort.z]
            
            for origin in originList:
                    
                if ('-' in str(origin)):
                    idxorigin = str(round(origin * 100, 6)).lstrip('-').split('.')
                    idxoriginString = '-' + idxorigin[0].zfill(5) + '.' + idxorigin[1].ljust(6, '0')
                else:
                    idxorigin = str(round(origin * 100, 6)).split('.')
                    idxoriginString = '+' + idxorigin[0].zfill(5) + '.' + idxorigin[1].ljust(6, '0')
                
                verticeList.append(idxoriginString)
            
            polyList = [f.normal.x, f.normal.y, f.normal.z]
            
            for polyIdx in polyList:
            
                if ('-' in str(polyIdx)):
                    polySplit = str(round(polyIdx, 6)).lstrip('-').split('.')
                    polyString = '-' + polySplit[0].zfill(5) + '.' + polySplit[1].ljust(6, '0')
                else:
                    polySplit = str(round(polyIdx, 6)).split('.')
                    polyString = '+' + polySplit[0].zfill(5) + '.' + polySplit[1].ljust(6, '0')
                
                verticeList.append(polyString)
            
            if f.normal.x != 0:
                verticeList.extend(['+00000.000000','+00001.000000','+00000.000000'])
                verticeList.extend(['+00000.000000','+00000.000000','+00001.000000'])
            elif f.normal.y !=0:
                verticeList.extend(['+00001.000000','+00000.000000','+00000.000000'])
                verticeList.extend(['+00000.000000','+00000.000000','+00001.000000'])
            else:
                verticeList.extend(['+00001.000000','+00000.000000','+00000.000000'])
                verticeList.extend(['+00000.000000','+00001.000000','+00000.000000'])
            
            for idx in f.vertices:

                idxList = [objectString.data.vertices[idx].co.x, objectString.data.vertices[idx].co.y, objectString.data.vertices[idx].co.z]

                for coord in idxList:
                    
                    if ('-' in str(coord)):
                        idxCoord = str(round(coord * 100, 6)).lstrip('-').split('.')
                        idxCoordString = '-' + idxCoord[0].zfill(5) + '.' + idxCoord[1].ljust(6, '0')
                    else:
                        idxCoord = str(round(coord * 100, 6)).split('.')
                        idxCoordString = '+' + idxCoord[0].zfill(5) + '.' + idxCoord[1].ljust(6, '0')
                    
                    verticeList.append(idxCoordString)

            linkCount += 1
            
            bpy.context.scene.textT3d += """\n\tBegin Polygon Flags=3584 Link={}
        Origin   {},{},{}
        Normal   {},{},{}
        TextureU {},{},{}
        TextureV {},{},{}
        Vertex   {},{},{}
        Vertex   {},{},{}
        Vertex   {},{},{}
        Vertex   {},{},{}
    End Polygon""".format(*verticeList)

        bpy.context.scene.textT3d += '\nEnd PolyList'
        fileName = '{}{}'.format(objectStringName, '.t3d')
        outputT3d = '{}{}'.format(bpy.path.abspath(bpy.context.scene.conf_path), fileName)
       
        f = open( outputT3d, 'w' )
        f.writelines( bpy.context.scene.textT3d.rstrip() )
        f.close()   
        pyperclip.copy(bpy.context.scene.textT3d.rstrip())
        
        return {'FINISHED'}
    
class defaultObjects(bpy.types.Operator):
    bl_idname = "custom.default_objects"
    bl_label = "Default UDK Objects"
    bl_description = "Creates Default UDK Objects"

    
    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
    
    def execute(self, context):
        
        num = str(bpy.context.scene.numberSequencer).zfill(10)
        
        outputFile = '{}{}'.format(bpy.path.abspath(bpy.context.scene.conf_path), "udkDefaultObjects.csv")
        textDefUDK = ""
            
        if bpy.context.scene.defGoals == True:
            

            textDefUDK += f""""""
                
            loopCount += 1
            bpy.context.scene.numberSequencer += 1
                        
        if bpy.context.scene.defSpawns == True:
            # MAKE SPAWNS TEXT
            textDefUDK += f""""""
            bpy.context.scene.numberSequencer += 1
            
        if bpy.context.scene.defBoost == True:
            # MAKE SPAWNS TEXT
            textDefUDK += f""""""
            bpy.context.scene.numberSequencer += 1
            
        if bpy.context.scene.defPillar == True:
            # MAKE PILLAR TEXT
            textDefUDK += f""""""
            bpy.context.scene.numberSequencer += 1
                    
        f = open( outputFile, 'w' )
        f.writelines( textDefUDK.rstrip() )
        f.close()   
        pyperclip.copy(textDefUDK.rstrip())
        
        return {'FINISHED'}

#this function is called on plugin loading(installing), adding class definitions into blender
#to be used, drawed and called
def register():
    #register the classes with the correct function
    bpy.types.Scene.collectionHolder = bpy.props.StringProperty(name="", default = "", description = "")
    bpy.types.Scene.projectName = bpy.props.StringProperty(name="UDK", default = "", description = "Select the UDK file you're currently working on.", subtype='FILE_PATH')
    bpy.types.Scene.textT3d = bpy.props.StringProperty(name="", default = "", description = "")
    bpy.types.Scene.prefabOBJ = bpy.props.PointerProperty(name="Object", type=bpy.types.Object)
    bpy.types.Scene.prefabPLANE = bpy.props.PointerProperty(name="Plane", type=bpy.types.Object)
    bpy.types.Scene.scaleFACES = bpy.props.BoolProperty(name="Scale Prefab To Plane")
    bpy.types.Scene.collectRotations = bpy.props.BoolProperty(name="Auto Collect Objects", default=True)
    bpy.types.Scene.collectData = bpy.props.BoolProperty(name="Auto Collect Objects", default=True)
    bpy.types.Scene.collectMaterials = bpy.props.BoolProperty(name="Collect Materials", default=True)
    bpy.types.Scene.collectT3d = bpy.props.BoolProperty(name="Auto Collect Objects", default=True)
    bpy.types.Scene.physMat = bpy.props.BoolProperty(name="Apply StickyWalls", default=True)
    bpy.types.Scene.defPillar = bpy.props.BoolProperty(name="Default Pillar", default=True)
    bpy.types.Scene.defGoals = bpy.props.BoolProperty(name="Default Goals", default=True)
    bpy.types.Scene.defSpawns = bpy.props.BoolProperty(name="Default Spawns", default=True)
    bpy.types.Scene.defBoost = bpy.props.BoolProperty(name="Default Boost", default=True)
    bpy.types.Scene.conf_path = bpy.props.StringProperty(name="CSV", default = "", description = "Define export directory for CSV file", subtype='FILE_PATH')
    bpy.types.Scene.numberSequencer = bpy.props.IntProperty(name="", default=0, min=0, max=1000000000)
    bpy.utils.register_class(setPosZ)
    bpy.utils.register_class(setNegZ)
    bpy.utils.register_class(setPosY)
    bpy.utils.register_class(setNegY)
    bpy.utils.register_class(setPosX)
    bpy.utils.register_class(setNegX)
    bpy.utils.register_class(sendToUDK)
    bpy.utils.register_class(sendToT3d)
    bpy.utils.register_class(defaultObjects)
    bpy.utils.register_class(RLMMPJ_PT_Panel)
    bpy.utils.register_class(RLMM_PT_Panel)
    bpy.utils.register_class(RLMMBRUSHES_PT_Panel)
    bpy.utils.register_class(UDKDEFAULT_PT_Panel)
    bpy.utils.register_class(setParent)
    bpy.utils.register_class(makeInstancesReal)

#same as register but backwards, deleting references
def unregister():
    #now we can continue to unregister classes normally
    bpy.utils.unregister_class(setPosZ)
    bpy.utils.unregister_class(setNegZ)
    bpy.utils.unregister_class(setPosY)
    bpy.utils.unregister_class(setNegY)
    bpy.utils.unregister_class(setPosX)
    bpy.utils.unregister_class(setNegX)       
    bpy.utils.unregister_class(sendToUDK)
    bpy.utils.unregister_class(sendToT3d)
    bpy.utils.unregister_class(defaultObjects)
    bpy.utils.unregister_class(RLMMPJ_PT_Panel)
    bpy.utils.unregister_class(RLMM_PT_Panel)
    bpy.utils.unregister_class(RLMMBRUSHES_PT_Panel)
    py.utils.register_class(UDKDEFAULT_PT_Panel)
    bpy.utils.unregister_class(setParent)    
    bpy.utils.unregister_class(makeInstancesReal) 

#NOTE: during testing if this addon was installed from a file then that current version
#of that file will be copied over to the blender addons directory
#if you want to see what changes occour you HAVE TO REINSTALL from the new file for it to register
    
#a quick line to autorun the script from the text editor when we hit 'run script'
if __name__ == '__main__':
    register()