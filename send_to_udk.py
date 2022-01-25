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
from mathutils import Matrix

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
        
        if bpy.context.scene.projectName == '':
            bpy.context.scene.errorCode = 3
            bpy.ops.custom.error_message('INVOKE_DEFAULT')
        else:
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
        
        outputFile = '{}{}'.format(bpy.path.abspath(bpy.context.scene.conf_path), "Blender2UDK.csv")
        
        textUDK_input = ""
        textUDK = ""
           
        loopCount = 0
        
        while loopCount < objCount:
            
            if bpy.context.scene.collectData == True: 
                obj = bpy.data.collections[bpy.context.scene.collectionHolder].objects[loopCount]
            else:
                obj = objHolder[loopCount]

            if bpy.context.scene.ishardAttach == True:
                textUDK += self.pushSend(obj, textUDK_input, self.createHardAttach(True, obj), False, '', '', '')
                
                attachCount = 0
                
                for attachIDX in reversed(range(bpy.context.scene.hard_index, -1, -1)):    
                    attachOBJ = bpy.context.scene.hard_collection[attachIDX].obj
                    textUDK += self.pushSend(attachOBJ, textUDK_input, self.createHardAttach(False, obj), True, self.getLoc(obj.location), self.getRot(obj.rotation_euler), attachCount)
                    attachCount += 1

                loopCount += 1
                bpy.context.scene.numberSequencer += 1
            else:
                textUDK += self.pushSend(obj, textUDK_input, '', False, '', '', '')
                loopCount += 1
                bpy.context.scene.numberSequencer += 1
        
        f = open( outputFile, 'w' )
        f.writelines( textUDK.rstrip() )
        f.close()   
        pyperclip.copy(textUDK.rstrip())
        
        bpy.context.scene.errorCode = 5
        bpy.ops.custom.error_message('INVOKE_DEFAULT')
        
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
        
    def getLoc(self, inVar):
        tempList = []
        locCount = 0
    
        for idxLoc in inVar:   
            if locCount == 0:
                idxLoc = -idxLoc
            tempList.append(round(idxLoc * 100, 6))
            locCount += 1
            
        outVar = [tempList[0],tempList[1],tempList[2]]
        return outVar

    def setBoostLoc(self, inVar1, inVar2):
    
        loc = Matrix.Translation((inVar2[0], inVar2[1], inVar2[2]))
        inVar1.matrix_basis @= loc
        
        return
        
    def pushSend(self, inVar1, inVar2, inVar3, inVar4, inVar5, inVar6, inVar7):
    
        obj = inVar1
        textUDK = inVar2
        hardAttach = inVar3
        isAttachChild = inVar4

        num = str(bpy.context.scene.numberSequencer).zfill(10)
        
        obj.select_set(True)
            
        bpy.context.view_layer.objects.active = obj
        
        # LOCATION XYZ
        # --------------------------------------------------------------------
        if isAttachChild == True:
            locList = inVar5
        else:
            locList = self.getLoc(obj.location)
        
        # ROTATION XYZ 
        # --------------------------------------------------------------------
        if isAttachChild == True:
            rotList = inVar6
        else:
            rotList = self.getRot(obj.rotation_euler)

        # SCALE XYZ
        # --------------------------------------------------------------------
        scaleList = []
        
        for objScale in obj.scale:
            scaleList.append(round(objScale, 6))

        # PROJECT NAME
        # --------------------------------------------------------------------
        if ('.' in str(bpy.context.scene.projectName)):
            mapDirectory = bpy.context.scene.projectName.split('.')
            mapName = mapDirectory[-2].split("\\")
        else:
            mapName = bpy.context.scene.projectName
            
        # STATICMESH NAME
        # --------------------------------------------------------------------
        objName = obj.name.split('.')
        staticString = "{}".format(objName[0])
        
        # ArcheType
        if bpy.context.scene.isArchetype == True:
            archetype = "{}.{}.{}".format(mapName[-1], 'archetypes', objName[0])
        else:
            archetype = defStaticArch
        
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
        
            if isAttachChild == True:
                num = str(bpy.context.scene.numberSequencer).zfill(10) + '_' + str(inVar7)
                
            textUDK += staticMeshString.format(num, staticString, materialNames.rstrip(), physString, locList, rotList, scaleList, tagString, layerString, archetype, hardAttach)
        
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
        # AS FAR AS I CAN TELL YOU CAN'T DO AN ARCHETYPE FOR THIS
        # --------------------------------------------------------------------
        elif ('GoalVolume' in str(objName)):
            
            teamNum = 0
            
            bpy.context.scene.isT3dFromSend2UDK = True
            bpy.ops.custom.send_to_t3d()

            #IF LOCATION == NEGATIVE Y SET TO TEAM NUMBER 1
            if locList[1] < 0:
                teamNum = 1

            textUDK += goalString.format(num, teamNum, bpy.context.scene.textT3d, locList, rotList, scaleList, layerString)
            
        # FORMATTING FOR DYNAMIC TRIGGER 
        # AS FAR AS I CAN TELL YOU CAN'T DO AN ARCHETYPE FOR THIS 
        # --------------------------------------------------------------------                
        elif ('DynamicTrigger' in str(objName)):
            
            bpy.context.scene.isT3dFromSend2UDK = True
            bpy.ops.custom.send_to_t3d()
            
            if isAttachChild == True:
                num = str(bpy.context.scene.numberSequencer).zfill(10) + '_' + str(inVar7)

            textUDK += dynamicTriggerString.format(num, bpy.context.scene.textT3d, locList, rotList, scaleList, tagString, layerString, hardAttach)
            
        # FORMATTING FOR CUSTOM BOOST
        # --------------------------------------------------------------------
        elif ('Boost' in str(objName)):
            
            if bpy.context.scene.customBoostMesh == True:
                textUDK += staticMeshString.format(num, staticString, materialNames.rstrip(), physString, locList, rotList, scaleList, tagString, layerString, archetype)
            elif ("Large" in str(objName)):
                textUDK += staticMeshString.format(num, boostLgMesh, materialNames.rstrip(), physString, locList, rotList, scaleList, tagString, layerString, archetype)
            else:
                textUDK += staticMeshString.format(num, boostSmMesh, materialNames.rstrip(), physString, locList, rotList, scaleList, tagString, layerString, archetype)
          
            fxLoc = [0.0, 0.0, 0.05]
            self.setBoostLoc(obj, fxLoc)    
            fxList = self.getLoc(obj.location)
            
            pickupLoc = [0.0, 0.0, 0.67]
            self.setBoostLoc(obj, pickupLoc)
            pickupList = self.getLoc(obj.location)
            
            if ('Large' in str(objName)):
                boostSize = 'Pill'
                boostAmount = 9999.000000
                boostDelay = 10.0
                CollisionRadius = 96.0   
                largeBoostOrb = customLargeBoostFx.format(num)
                largeBoostAttach = customLargeBoostAttach.format(num)
                
            else:
                boostSize = 'Pad'
                boostAmount = 0.120000
                boostDelay = 4.0
                CollisionRadius = 160.0 
                largeBoostOrb = ''
                largeBoostAttach = ''
            
            if bpy.context.scene.customBoostParticles == True:
                textUDK += customBoostFxString.format(num, tagString + '_Particles', fxList, rotList, boostSize, largeBoostOrb, largeBoostAttach)
                textUDK += customPickUpString.format(num, pickupList, rotList, boostAmount, boostSize, boostDelay, CollisionRadius)
                
            else:
                textUDK += boostFxString.format(num, rotList, fxList, boostSize)
                textUDK += boostPickupString.format(num, boostSize, pickupList, rotList, boostSize)
            
            orgLoc = [0.0, 0.0, -0.72]
            self.setBoostLoc(obj, orgLoc)

        # SKIP PARTICLES MESHES
        # --------------------------------------------------------------------
        elif ('Particles' in str(objName)):
            textUDK += ''
            
        # FORMATTING FOR PILLAR
        # --------------------------------------------------------------------    
        elif ('Pillar' in str(objName)):
            textUDK += pillarString.format(num, '', '', locList)
            
        # FORMATTING FOR PLAYERSTART
        # --------------------------------------------------------------------    
        elif ('Player' in str(objName)):
            textUDK += playerString.format(num, locList, rotList)
            
        # FORMATTING FOR Interp
        # --------------------------------------------------------------------    
        elif ('Interp' in str(objName)):
            textUDK += ''
            
        # FORMATTING FOR Kactor
        # --------------------------------------------------------------------    
        elif ('KActor' in str(objName)):
        
            if isAttachChild == True:
                num = str(bpy.context.scene.numberSequencer).zfill(10) + '_' + str(inVar7)
                
            textUDK += customKactorString.format(num, staticString, materialNames.rstrip(), locList, rotList, scaleList, tagString, layerString, hardAttach)
            
        # FORMATTTING FOR EVERYTHING ELSE 
        # --------------------------------------------------------------------
        else:
        
            if isAttachChild == True:
                num = str(bpy.context.scene.numberSequencer).zfill(10) + '_' + str(inVar7)
                
            textUDK += staticMeshString.format(num, staticString, materialNames.rstrip(), physString, locList, rotList, scaleList, tagString, layerString, archetype, hardAttach)
            
        return textUDK
        
    def createHardAttach(self, inVar1, inVar2):
        # NEED TO INCREMENT NAMES OF MULTIPLE OF THE SAME TYPE
         # Attached(0)=DynamicTriggerVolume'DynamicTriggerVolume_0000000093'
         # Attached(1)=DynamicTriggerVolume'DynamicTriggerVolume_0000000093'
        hardAttach = ''
        num = str(bpy.context.scene.numberSequencer).zfill(10)
        count = 0
        
        if inVar1 == True:
            for attachIDX in reversed(range(bpy.context.scene.hard_index, -1, -1)):    
                attachOBJ = bpy.context.scene.hard_collection[attachIDX].obj
                
                objName = attachOBJ.name.split('.')
                                
                if ('KActor' in str(objName)):
                    typeString = 'KActor'
                    nameString = 'KActor_{0}'.format(num + '_' + str(count))
                elif ('DynamicTrigger' in str(objName)):
                    typeString = 'DynamicTriggerVolume'
                    nameString = 'DynamicTriggerVolume_{0}'.format(num + '_' + str(count))
                else:
                    typeString = 'StaticMeshActor'
                    nameString = 'StaticMeshActor_{0}'.format(num + '_' + str(count))
                    
                hardAttach += customAttachParentString.format(attachIDX, typeString, nameString)
                count += 1
        else:
            objName = inVar2.name.split('.')
            
            if ('KActor' in str(objName)):
                typeString = 'KActor'
                nameString = 'KActor_{0}'.format(num)
            elif ('DynamicTrigger' in str(objName)):
                typeString = 'DynamicTriggerVolume'
                nameString = 'DynamicTriggerVolume_{0}'.format(num)
            else:
                typeString = 'StaticMeshActor'
                nameString = 'StaticMeshActor_{0}'.format(num)
                
            hardAttach = customAttachChildString.format(typeString, nameString)
    
        return hardAttach