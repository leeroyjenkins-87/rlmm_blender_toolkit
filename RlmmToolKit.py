bl_info = {
    "name": "RLMM Toolkit",
    "author": "LeeroyJenkins0G",
    "version": (1, 0, 13),   # addon plugin version
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
    bl_label = "Project Name"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'

#create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):
        
        layout = self.layout

        boxLayout1 = layout.box()
        boxLayout1.label(text="Project Name",icon='DESKTOP')
        
        row1 = boxLayout1.row()
        row1.prop(context.scene, 'projectName')


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
        
        row3 = boxlayout5.row()
        row3.prop(context.scene, 'conf_path')
        row2 = boxlayout5.row()
        row2.operator('custom.send_to_udk', text="Send to UDK")
        
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

        boxLayout9 = layout.box()
        boxLayout9.label(text="T3D File",icon='CUBE')
        boxLayout9.operator('custom.send_to_t3d', text="Create Custom Brush")

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
        
        if bpy.context.scene.collectData == True:
            objectString = bpy.data.collections[bpy.context.scene.collectionHolder].objects[:]
        else:
            objectString = bpy.context.selected_objects
            
        for obj in objectString:    
            if obj.type != 'MESH':
                continue
            
            # LOCATION XYZ
            # --------------------------------------------------------------------
            center = obj.location
            centerX, centerY, centerZ = center[0]*100, center[1]*100, center[2]*100
            d, e, f = round(-centerX, 6), round(centerY, 6), round(centerZ, 6),
            locationString = 'Location=(X={},Y={},Z={})'.format(d, e, f)
            
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
                physString = "PhysMaterialOverride=PhysicalMaterial'{}.Materials.StickyWalls'".format(mapName[-1].lower())
            else:
                physString = ''
            
            textUDK += """
        Begin Map
           Begin Level
              Begin Actor Class=StaticMeshActor Name=StaticMeshActor_4 Archetype=StaticMeshActor'Engine.Default__StaticMeshActor'
                 Begin Object Class=StaticMeshComponent Name=StaticMeshComponent0 ObjName=StaticMeshComponent Archetype=StaticMeshComponent'Engine.Default__StaticMeshActor:StaticMeshComponent0'
                    StaticMesh=StaticMesh'{}'
                    VertexPositionVersionNumber=1
                    {}
                    ReplacementPrimitive=None
                    bAllowApproximateOcclusion=True
                    bAcceptsDynamicDecals=False
                    bForceDirectLightMap=True
                    bUsePrecomputedShadows=True
                    bDisableAllRigidBody=False
                    LightingChannels=(bInitialized=True,Static=True)
                    {}
                    Name="StaticMeshComponent"
                    ObjectArchetype=StaticMeshComponent'Engine.Default__StaticMeshActor:StaticMeshComponent0'
                 End Object
                 StaticMeshComponent=StaticMeshComponent'StaticMeshComponent0'
                 Components(0)=StaticMeshComponent'StaticMeshComponent0'
                 {}
                 {}
                 {}
                 {}
                 {}
                 BlockRigidBody=True
                 CreationTime=0
                 Tag="StaticMeshActor"
                 CollisionComponent=StaticMeshComponent'StaticMeshComponent'
                 Name="StaticMeshActor"
                 ObjectArchetype=StaticMeshActor'Engine.Default__StaticMeshActor'
              End Actor
           End Level
        Begin Surface
        End Surface
        End Map
        """.format(staticString, materialNames.rstrip(), physString, locationString, rotationString, scaleString, tagString, layerString)

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
        
        textT3d = 'Begin PolyList\n'
        
        for f in objectString.data.polygons:
            
            polyNormal = f.normal
            
            if ('-' in str(polyNormal.x)):
                polyX = str(polyNormal.x).lstrip('-').split('.')
                polyXString = '-' + polyX[0].zfill(5) + '.' + polyX[1].ljust(6, '0')
            else:
                polyX = str(polyNormal.x).split('.')
                polyXString = '+' + polyX[0].zfill(5) + '.' + polyX[1].ljust(6, '0')
                
            if ('-' in str(polyNormal.y)):
                polyY = str(polyNormal.y).lstrip('-').split('.')
                polyYString = '-' + polyY[0].zfill(5) + '.' + polyY[1].ljust(6, '0')
            else:
                polyY = str(polyNormal.y).split('.')
                polyYString = '+' + polyY[0].zfill(5) + '.' + polyY[1].ljust(6, '0')
                
            if ('-' in str(polyNormal.z)):
                polyZ = str(polyNormal.z).lstrip('-').split('.')
                polyZString = '-' + polyZ[0].zfill(5) + '.' + polyZ[1].ljust(6, '0')
            else:
                polyZ = str(polyNormal.z).split('.')
                polyZString = '+' + polyZ[0].zfill(5) + '.' + polyZ[1].ljust(6, '0')
            
            polyString = '\t\tNormal   {},{},{}'.format(polyXString, polyYString, polyZString)
            
            if f.normal.x != 0:
                uString = '\t\tTextureU +00000.000000,+00001.000000,+00000.000000'
                vString = '\t\tTextureV +00000.000000,+00000.000000,+00001.000000'
            elif f.normal.y !=0:
                uString = '\t\tTextureU +00001.000000,+00000.000000,+00000.000000'
                vString = '\t\tTextureV +00000.000000,+00000.000000,+00001.000000'
            else:
                uString = '\t\tTextureU +00001.000000,+00000.000000,+00000.000000'
                vString = '\t\tTextureV +00000.000000,+00001.000000,+00000.000000'
            
            verticeString = ''
            
            for idx in f.vertices:
                if ('-' in str(objectString.data.vertices[idx].co.x)):
                    idxX = str(objectString.data.vertices[idx].co.x * 100).lstrip('-').split('.')
                    idxXString = '-' + idxX[0].zfill(5) + '.' + idxX[1].ljust(6, '0')
                else:
                    idxX = str(objectString.data.vertices[idx].co.x * 100).split('.')
                    idxXString = '+' + idxX[0].zfill(5) + '.' + idxX[1].ljust(6, '0')
                    
                if ('-' in str(objectString.data.vertices[idx].co.y)):
                    idxY = str(objectString.data.vertices[idx].co.y * 100).lstrip('-').split('.')
                    idxYString = '-' + idxY[0].zfill(5) + '.' + idxY[1].ljust(6, '0')
                else:
                    idxY = str(objectString.data.vertices[idx].co.y * 100).split('.')
                    idxYString = '+' + idxY[0].zfill(5) + '.' + idxY[1].ljust(6, '0')
                    
                if ('-' in str(objectString.data.vertices[idx].co.z)):
                    idxZ = str(objectString.data.vertices[idx].co.z * 100).lstrip('-').split('.')
                    idxZString = '-' + idxZ[0].zfill(5) + '.' + idxZ[1].ljust(6, '0')
                else:
                    idxZ = str(objectString.data.vertices[idx].co.z * 100).split('.')
                    idxZString = '+' + idxZ[0].zfill(5) + '.' + idxZ[1].ljust(6, '0')
              
                verticeString += '\t\tVertex   {},{},{}\n'.format(idxXString, idxYString, idxZString)


            polyOrigin = verticeString.split('\n') 
            
            polyOriginString = polyOrigin[0].replace('Vertex', 'Origin')
            
            startString = '\tBegin Polygon Texture=EngineMaterials.DefaultMaterial Flags=3584'
            
            endString = '\tEnd Polygon'
            
            textT3d += '{}\n{}\n{}\n{}\n{}\n{}{}\n'.format(startString, polyOriginString, polyString, uString, vString, verticeString, endString)

        textT3d += 'End PolyList'
        fileName = '{}{}'.format(objectStringName, '.t3d')
        outputT3d = '{}{}'.format(bpy.path.abspath(bpy.context.scene.conf_path), fileName)
       
        f = open( outputT3d, 'w' )
        f.writelines( textT3d.rstrip() )
        f.close()   
        pyperclip.copy(textT3d.rstrip())
        
        return {'FINISHED'}

#this function is called on plugin loading(installing), adding class definitions into blender
#to be used, drawed and called
def register():
    #register the classes with the correct function
    bpy.types.Scene.collectionHolder = bpy.props.StringProperty(name="", default = "", description = "")
    bpy.types.Scene.projectName = bpy.props.StringProperty(name="", default = "", description = "Define export directory for CSV file", subtype='FILE_PATH')
    bpy.types.Scene.prefabOBJ = bpy.props.PointerProperty(name="Object", type=bpy.types.Object)
    bpy.types.Scene.prefabPLANE = bpy.props.PointerProperty(name="Plane", type=bpy.types.Object)
    bpy.types.Scene.scaleFACES = bpy.props.BoolProperty(name="Scale Prefab To Plane")
    bpy.types.Scene.collectRotations = bpy.props.BoolProperty(name="Auto Collect Objects", default=True)
    bpy.types.Scene.collectData = bpy.props.BoolProperty(name="Auto Collect Objects", default=True)
    bpy.types.Scene.collectMaterials = bpy.props.BoolProperty(name="Collect Materials", default=True)
    bpy.types.Scene.collectT3d = bpy.props.BoolProperty(name="Auto Collect Objects", default=True)
    bpy.types.Scene.physMat = bpy.props.BoolProperty(name="Apply StickyWalls", default=True)
    bpy.types.Scene.conf_path = bpy.props.StringProperty(name="CSV", default = "", description = "Define export directory for CSV file", subtype='FILE_PATH')
    bpy.utils.register_class(setPosZ)
    bpy.utils.register_class(setNegZ)
    bpy.utils.register_class(setPosY)
    bpy.utils.register_class(setNegY)
    bpy.utils.register_class(setPosX)
    bpy.utils.register_class(setNegX)
    bpy.utils.register_class(sendToUDK)
    bpy.utils.register_class(sendToT3d)
    bpy.utils.register_class(RLMMPJ_PT_Panel)
    bpy.utils.register_class(RLMM_PT_Panel)
    bpy.utils.register_class(RLMMBrushes_PT_Panel)
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
    bpy.utils.unregister_class(RLMMPJ_PT_Panel)
    bpy.utils.unregister_class(RLMM_PT_Panel)
    bpy.utils.unregister_class(RLMMBrushes_PT_Panel)
    bpy.utils.unregister_class(setParent)    
    bpy.utils.unregister_class(makeInstancesReal) 

#NOTE: during testing if this addon was installed from a file then that current version
#of that file will be copied over to the blender addons directory
#if you want to see what changes occour you HAVE TO REINSTALL from the new file for it to register
    
#a quick line to autorun the script from the text editor when we hit 'run script'
if __name__ == '__main__':
    register()