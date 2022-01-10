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
        
        num = str(bpy.context.scene.numberSequencer).zfill(10)
        
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
                
                textDefUDK += pointString.format(num, pointLoc[0], pointLoc[1], pointLoc[2], pointRot[0], pointRot[1], pointRot[2])
                
                goalLoc = defCurrentGoal[3]
                
                textDefUDK += goalString.format(num, defCurrentGoal[2], defaultGoalT3d, goalLoc[0], goalLoc[1], goalLoc[2], '0', '0', '0')
                    
                num += 1
                
                goalCreatedList.append(f"""GoalVolume_TA_{num}""")
            
        if bpy.context.scene.defSpawns == True:

            playerDefaultStarts = [playerStart0, playerStart1, playerStart2, playerStart3, playerStart4, playerStart5, playerStart6, playerStart7, playerStart8]
            
            playerCreatedList = []
            
            for defCurrentSpawn in playerDefaultStarts:
            
                playerLoc = defCurrentSpawn[0]
                playerRot = defCurrentSpawn[1]
            
                textDefUDK += playerString.format(num, playerLoc[0], playerLoc[1], playerLoc[2], playerRot[0], playerRot[1], playerRot[2])
                
                num += 1
                
                playerCreatedList.append(f"""PlayerStart_TA_{num}""")

        if bpy.context.scene.defPillar == True:
            
            textDefUDK += pillarString.format(num, goalCreatedList, playerCreatedList)

            num += 1
            
        if bpy.context.scene.defBoost == True:

            for boostList in boostLocList:
            
                boostDupeLoc = boostList[0]
                
                for boostDupe in boostList[1]:
                
                    if boostDupeLoc[2] == 70.0:
                    
                        textDefUDK += boostFxString.format(num, '0', boostDupe[2], '0', boostDupeLoc[0] * boostDupe[0], boostDupeLoc[1] * boostDupe[1], boostDupeLoc[2] - 64, 'Pad')
                        
                        textDefUDK += boostPickupString.format(num, 'Pad', boostDupeLoc[0] * boostDupe[0], boostDupeLoc[1] * boostDupe[1], boostDupeLoc[2], '0', boostDupe[2], '0', 'Small')
                        
                        num += 1
                        
                    else:
                    
                        textDefUDK += boostFxString.format(num, '0', boostDupe[2], '0', boostDupeLoc[0] * boostDupe[0], boostDupeLoc[1] * boostDupe[1], boostDupeLoc[2] - 69, 'Pill')
                        
                        textDefUDK += boostPickupString.format(num, 'Pill', boostDupeLoc[0] * boostDupe[0], boostDupeLoc[1] * boostDupe[1], boostDupeLoc[2], '0', boostDupe[2], '0', 'Large')
                        
                        textDefUDK += staticMeshString.format(num, str(boostLgMesh).rstrip("']").lstrip("['"), boostLgMaterials, '', boostDupeLoc[0] * boostDupe[0], boostDupeLoc[1] * boostDupe[1], boostDupeLoc[2] - 66, '0', boostDupe[2], '0', '1.0', '1.0', '1.0', 'LargeBoostMesh', 'Field,Boost', 'LargeBoost')

                        num += 1
            
            for boostSmMesh in boostSmStaticLoc:
            
                boostSmLoc = boostSmMesh[0]

                textDefUDK += staticMeshString.format(num, str(boostSmMesh[1]).rstrip("']").lstrip("['"), boostSmMaterials, '', boostSmLoc[0], boostSmLoc[1], boostSmLoc[2], '0.0', '0.0', '0.0', '1.0', '1.0', '1.0', 'SmallBoostMesh', 'Field,Boost', 'SmallBoost')

                num += 1
    
    
        f = open( outputFile, 'w' )
        f.writelines( textDefUDK.rstrip() )
        f.close()   
        pyperclip.copy(textDefUDK.rstrip())

        return {'FINISHED'}