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
import pyperclip
from math import degrees#, radians, pi
from .def_obj_vars import *
from .cust_obj_vars import *

class sendToUDK(bpy.types.Operator):
    bl_idname = "custom.send_to_udk"
    bl_label = "Send to UDK"
    bl_description = "Creates Object Data"

    
    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
    
    def execute(self, context):
   
        objCount = 0
        objHolder = []
        
        if bpy.context.scene.collectData == True:
            if bpy.context.scene.collectionHolder != '':
                objCount = len(bpy.data.collections[bpy.context.scene.collectionHolder].objects[:])
                self.runSend(objCount, objHolder)
            else:
                bpy.context.scene.errorCode = 2
                bpy.ops.custom.error_message('INVOKE_DEFAULT')                
        else:
            if len(bpy.context.selected_objects) < 1:
                bpy.context.scene.errorCode = 1
                bpy.ops.custom.error_message('INVOKE_DEFAULT')
            else:
                objHolder = bpy.context.selected_objects
                objCount = len(bpy.context.selected_objects[:])
                self.runSend(objCount, objHolder)
            
        return{'FINISHED'}
        
    def runSend(self, inVar1, inVar2):
        for selectedObj in bpy.context.selected_objects:
            selectedObj.select_set(False)
            
        objCount = inVar1
        objHolder = inVar2
        
        num = str(bpy.context.scene.numberSequencer).zfill(10)
        outputFile = '{}{}'.format(bpy.path.abspath(bpy.context.scene.conf_path), "Blender2UDK.csv")
        textUDK = ""
            
        loopCount = 0
        
        while loopCount < objCount:
            
            if bpy.context.scene.collectData == True: 
                obj = bpy.data.collections[bpy.context.scene.collectionHolder].objects[loopCount]
            else:
                obj = objHolder[loopCount]
        
            obj.select_set(True)
            
            bpy.context.view_layer.objects.active = obj
            
            # LOCATION XYZ
            # --------------------------------------------------------------------
            locCount = 0
            locList = []
            
            for idxLoc in obj.location:
                if locCount == 0:
                    idxLoc = -idxLoc
                locList.append(round(idxLoc * 100, 6))
                locCount += 1
            
            # ROTATION XYZ 
            # --------------------------------------------------------------------
            rotList = self.getRot(obj.rotation_euler)

            # SCALE XYZ
            # --------------------------------------------------------------------
            scaleList = []
            
            for objScale in obj.scale:
                scaleList.append(round(objScale, 6))

            # PROJECT NAME
            # --------------------------------------------------------------------
            
            if bpy.context.scene.projectName == '':
                bpy.context.scene.errorCode = 3
                bpy.ops.custom.error_message('INVOKE_DEFAULT')

            else:
                mapDirectory = bpy.context.scene.projectName.split('.')
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
                
                layerString = str(obj.users_collection[0].name.rstrip(".0123456789"))
                
                # TAG
                # --------------------------------------------------------------------
                tagString = str(objName[0]).rstrip(".0123456789")
                
                # PHYSICAL MATERIAL APPLIED
                # --------------------------------------------------------------------
                if bpy.context.scene.physMat == True:
                    physString = 'PhysicalMaterials.Collision_Sticky'
                else:
                    physString = ''
                    
                # FORMATTING FOR STATICMESH 
                # --------------------------------------------------------------------
                if ('StaticMesh' in str(objName)):                
                    textUDK += staticMeshString.format(num, staticString, materialNames.rstrip(), physString, locList, rotList, scaleList, tagString, layerString)
                
                # FORMATTING FOR SPOTLIGHT 
                # --------------------------------------------------------------------
                elif ('Spot' in str(objName)):
                
                    # ROTATION XYZ FOR SPOTLIGHTS IS NEGATIVE 90 DEGREES IN UDK SO WE HAVE TO ADJUST IT.
                    bpy.ops.custom.set_pos_y()

                    rotList = self.getRot(obj.rotation_euler)
                    
                    # ADUJUST ROTATION BACK 90 DEGREES
                    bpy.ops.custom.set_neg_y()
                    
                    textUDK += spotLightString.format(num, locList, rotList, scaleList, tagString, layerString)
                    
                # FORMATTING FOR CUSTOM GOAL 
                # --------------------------------------------------------------------
                elif ('GoalVolume' in str(objName)):
                    teamNum = 0
                    
                    bpy.ops.custom.send_to_t3d()

                    #IF LOCATION == NEGATIVE Y SET TO TEAM NUMBER 1
                    if locList[1] < 0:
                        teamNum = 1

                    textUDK += goalString.format(num, teamNum, bpy.context.scene.textT3d, locList, rotList, scaleList, layerString)
                    
                elif ('DynamicTrigger' in str(objName)):
                        
                    bpy.ops.custom.send_to_t3d()

                    textUDK += dynamicTriggerString.format(num, bpy.context.scene.textT3d, locList, rotList, scaleList, tagString, layerString)

                # FORMATTTING FOR EVERYTHING ELSE 
                # --------------------------------------------------------------------
                else:
                    textUDK += staticMeshString.format(num, staticString, materialNames.rstrip(), physString, locList, rotList, scaleList, tagString, layerString)
            
                loopCount += 1
                
                bpy.context.scene.numberSequencer += 1

            f = open( outputFile, 'w' )
            f.writelines( textUDK.rstrip() )
            f.close()   
            pyperclip.copy(textUDK.rstrip())
        
            return {'FINISHED'}
        
    def getRot(self, inVar):
        tempList = []
        flipRot = [-1,1,-1]
        count = 0
        
        for idxRot in inVar:
            multRot = round((degrees(idxRot) * flipRot[count]) * (65536 / 360))
            tempList.append(multRot)
            count += 1

        outVar = [tempList[1],tempList[2],tempList[0]]
        return outVar