import bpy
import pyperclip
from .def_obj_vars import *

class defaultObjects(bpy.types.Operator):
    bl_idname = "custom.default_objects"
    bl_label = "Default UDK Objects"
    bl_description = "Creates Default UDK Objects"

    
    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
    
    def execute(self, context):

        outputFile = '{}{}'.format(bpy.path.abspath(bpy.context.scene.conf_path), "udkDefaultObjects.csv")
        textDefUDK = ""

        if bpy.context.scene.defGoals == True:

            goalCreatedList = []

            defBlueGoalList = [defaultBluePointInSpaceLocation, defaultBluePointInSpaceRotation, defaultBlueTeamNumber, defaultBlueGoalLocation]

            defOrangeGoalList = [defaultOrangePointInSpaceLocation, defaultOrangePointInSpaceRotation, defaultOrangeTeamNumber, defaultOrangeGoalLocation]

            defGoalList = [defBlueGoalList,  defOrangeGoalList]

            for defCurrentGoal in defGoalList:
            
                pointLoc = defCurrentGoal[0]
                
                pointRot = defCurrentGoal[1]
                
                textDefUDK += pointString.format(str(bpy.context.scene.numberSequencer).zfill(10), pointLoc, pointRot)
                
                goalLoc = defCurrentGoal[3]
                
                teamNum = defCurrentGoal[2]
                
                textDefUDK += goalString.format(str(bpy.context.scene.numberSequencer).zfill(10), teamNum, defaultGoalT3d, goalLoc, goalRot, goalScale, 'GoalVolume')
  
                bpy.context.scene.numberSequencer += 1
                
                goalCreatedList.append("""GoalVolume_TA_{}""".format(str(bpy.context.scene.numberSequencer).zfill(10)))
            
        if bpy.context.scene.defSpawns == True:

            playerDefaultStarts = [playerStart0, playerStart1, playerStart2, playerStart3, playerStart4, playerStart5, playerStart6, playerStart7, playerStart8]
            
            playerCreatedList = []
            
            for defCurrentSpawn in playerDefaultStarts:
            
                playerLoc = defCurrentSpawn[0]
                playerRot = defCurrentSpawn[1]
            
                textDefUDK += playerString.format(str(bpy.context.scene.numberSequencer).zfill(10), playerLoc, playerRot)
                
                bpy.context.scene.numberSequencer += 1
                
                playerCreatedList.append("""PlayerStart_TA_{}""".format(str(bpy.context.scene.numberSequencer).zfill(10)))

        if bpy.context.scene.defPillar == True:
            
            textDefUDK += pillarString.format(str(bpy.context.scene.numberSequencer).zfill(10), goalCreatedList, playerCreatedList)

            bpy.context.scene.numberSequencer += 1
            
        if bpy.context.scene.defBoost == True:

            for boostList in boostLocList:
            
                boostDupeLoc = boostList[0]
                
                for boostDupe in boostList[1]:
                
                    if boostDupeLoc[2] == 70.0:
                    
                        rotList = [0, boostDupe[2], 0]
                        
                        locList = [boostDupeLoc[0] * boostDupe[0], boostDupeLoc[1] * boostDupe[1], boostDupeLoc[2] - 64]
                    
                        textDefUDK += boostFxString.format(str(bpy.context.scene.numberSequencer).zfill(10), rotList, locList, 'Pad')
                        
                        locList = [boostDupeLoc[0] * boostDupe[0], boostDupeLoc[1] * boostDupe[1], boostDupeLoc[2]]
                        
                        textDefUDK += boostPickupString.format(str(bpy.context.scene.numberSequencer).zfill(10), 'Pad', locList, rotList, 'Small')
                        
                        bpy.context.scene.numberSequencer += 1
                        
                    else:
                        rotList = [0, boostDupe[2], 0]
                        
                        locList = [boostDupeLoc[0] * boostDupe[0], boostDupeLoc[1] * boostDupe[1], boostDupeLoc[2] - 69]
                    
                        textDefUDK += boostFxString.format(str(bpy.context.scene.numberSequencer).zfill(10), rotList, locList, 'Pill')
                        
                        locList = [boostDupeLoc[0] * boostDupe[0], boostDupeLoc[1] * boostDupe[1], boostDupeLoc[2]]
                        
                        textDefUDK += boostPickupString.format(str(bpy.context.scene.numberSequencer).zfill(10), 'Pill', locList, rotList, 'Large')
                        
                        locList = [boostDupeLoc[0] * boostDupe[0], boostDupeLoc[1] * boostDupe[1], boostDupeLoc[2] - 66]
                        
                        textDefUDK += staticMeshString.format(str(bpy.context.scene.numberSequencer).zfill(10), str(boostLgMesh).rstrip("']").lstrip("['"), boostLgMaterials, '', locList, rotList, boostScale, 'LargeBoostMesh', 'Field,Boost', 'LargeBoost')

                        bpy.context.scene.numberSequencer += 1
            
            for boostSmMesh in boostSmStaticLoc:
            
                boostSmLoc = boostSmMesh[0]
                
                rotList = [0, 0, 0]

                textDefUDK += staticMeshString.format(str(bpy.context.scene.numberSequencer).zfill(10), str(boostSmMesh[1]).rstrip("']").lstrip("['"), boostSmMaterials, '', boostSmLoc, rotList, boostScale, 'SmallBoostMesh', 'Field,Boost', 'SmallBoost')

                bpy.context.scene.numberSequencer += 1
    
    
        f = open( outputFile, 'w' )
        f.writelines( textDefUDK.rstrip() )
        f.close()   
        pyperclip.copy(textDefUDK.rstrip())

        return {'FINISHED'}