# STATICMESH STRING
# ---------------------------------------------
staticMeshString = """
Begin Map
   Begin Level
      Begin Actor Class=StaticMeshActor Name=StaticMeshActor_{0} Archetype=StaticMeshActor'Engine.Default__StaticMeshActor'
         Begin Object Class=StaticMeshComponent Name=StaticMeshComponent{0} ObjName=StaticMeshComponent_{0} Archetype=StaticMeshComponent'Engine.Default__StaticMeshActor:StaticMeshComponent0'
            StaticMesh=StaticMesh'{1}'
            VertexPositionVersionNumber=1
            {2}
            ReplacementPrimitive=None
            bAllowApproximateOcclusion=True
            bAcceptsDynamicDecals=False
            bForceDirectLightMap=True
            bUsePrecomputedShadows=True
            bDisableAllRigidBody=False
            LightingChannels=(bInitialized=True,Static=True)
            PhysMaterialOverride=PhysicalMaterial'{3}'
            Name="StaticMeshComponent_{0}"
            ObjectArchetype=StaticMeshComponent'Engine.Default__StaticMeshActor:StaticMeshComponent0'
         End Object
         StaticMeshComponent=StaticMeshComponent'StaticMeshComponent_{0}'
         Components(0)=StaticMeshComponent'StaticMeshComponent_{0}'
         Location=(X={4[0]},Y={4[1]},Z={4[2]})
         Rotation=(Pitch={5[0]},Yaw={5[1]},Roll={5[2]})
         DrawScale3D=(X={6[0]},Y={6[1]},Z={6[2]})
         Tag="{7}"
         Layer="{8}"
         BlockRigidBody=True
         CreationTime=0
         CollisionComponent=StaticMeshComponent'StaticMeshComponent_{0}'
         Name="{7}_{0}"
         ObjectArchetype=StaticMeshActor'Engine.Default__StaticMeshActor'
      End Actor
   End Level
Begin Surface
End Surface
End Map
        """
        
# -------- How to WRITE MESH STRING ------

#blah = staticMeshString.format(num, staticString, materialNames.rstrip(), physString, locList, rotList, scaleList, tagString, layerString, objName)


# DEFAULT BOOST LOCATIONS/ROTATIONS
# ---------------------------------

# [[[LocationX, LocationY, LocationZ], [[DuplicateX1, DuplicateY1, Yaw1], [DuplicateX2, DuplicateY2, Yaw2], [DuplicateX3, DuplicateY3, Yaw3], [DuplicateX4, DuplicateY4, Yaw4]]]
boostLocList = [
 [[3584.0, 2484.0, 70.0], [[1 ,1, 32768], [-1, 1, 32768], [1, -1, 0], [-1, -1, 0]]],
 [[1788.0, 2300.0, 70.0], [[1 ,1, -40960], [-1, 1, 40960], [1, -1, 8192], [-1, -1, -8192]]], 
 [[1792.0,4184.0,70.0], [[1 ,1, -32768], [-1, 1, 32768], [1, -1, 0], [-1, -1, 0]]], 
 [[940.0, 3308.0, 70.0], [[1 ,1, 32768], [-1, 1, 32768], [1, -1, 0], [-1, -1, 0]]], 
 [[2048.0, 1036.0, 70.0], [[1 ,1, 32768], [-1, 1, 32768], [1, -1, 0], [-1, -1, 0]]], 
 [[0.0, 1024.0, 70.0], [[1 ,1, 0], [1, -1, 32768]]], 
 [[0.0, 2816.0, 70.0], [[1 ,1, 32768], [1, -1, 0]]], 
 [[0.0, 4240.0, 70.0], [[1 ,1, 32768], [1, -1, 0]]], 
 [[1024.0, 0.0, 70.0], [[1 ,1, 49152], [-1, 1, -49152]]], 
 [[3072, 4096.0, 73.0], [[1 ,1, -8192], [-1, 1, 8192], [1, -1, -2732], [-1, -1, 2728]]], 
 [[3584.0, 0.0, 73.0], [[1 ,1, -16384], [-1, 1, 16384]]]
 ]
 
boostScale = [1, 1, 1]

boostFxString = """
Begin Map
   Begin Level
        Begin Actor Class=FXActor_TA Name=FXActor_Boost_TA_{0} Archetype=FXActor_TA'Park_P.pickup_boost.Boost{3}_FXActor'
         Begin Object Class=ParameterDispenser_X Name=DefaultParameters_{0} ObjName=ParameterDispenser_X_{0} Archetype=ParameterDispenser_X'Park_P.pickup_boost.Boost{3}_FXActor:DefaultParameters'
            Name="ParameterDispenser_X_{0}"
            ObjectArchetype=ParameterDispenser_X'Park_P.pickup_boost.Boost{3}_FXActor:DefaultParameters'
         End Object
         Begin Object Class=SpriteComponent Name=Sprite ObjName=SpriteComponent_29 Archetype=SpriteComponent'Park_P.pickup_boost.Boost{3}_FXActor:Sprite'
            Sprite=Texture2D'EditorResources.MatIcon_FX'
            SpriteCategoryName="FXActor"
            ReplacementPrimitive=None
            HiddenGame=True
            AlwaysLoadOnClient=False
            AlwaysLoadOnServer=False
            LightingChannels=(bInitialized=True,Dynamic=True)
            Scale=2.000000
            Name="SpriteComponent_{0}"
            ObjectArchetype=SpriteComponent'Park_P.pickup_boost.Boost{3}_FXActor:Sprite'
         End Object
         Parameters=ParameterDispenser_X'ParameterDispenser_X_{0}'
         Components(0)=SpriteComponent'SpriteComponent_{0}'
         Location=(X={2[0]},Y={2[1]},Z={2[2]})
         Rotation=(Pitch={1[0]},Yaw={1[1]},Roll={1[2]})
         bNoDelete=True
         Tag="Boost_Small"
         Layer="Field, Boost"
         Name="FXActor_Boost_TA_{0}"
         ObjectArchetype=FXActor_TA'Park_P.pickup_boost.Boost{3}_FXActor'
        End Actor
   End Level
End Map"""

boostPickupString = """
Begin Map
   Begin Level
      Begin Actor Class=VehiclePickup_Boost_TA Name=VehiclePickup_Boost_TA_{0} Archetype=VehiclePickup_Boost_TA'Park_P.archetypes.vehiclepickup.VehiclePickup_Boost{1}'
         Begin Object Class=CylinderComponent Name=DefaultCollisionCylinder_{0} ObjName=CylinderComponent_{0} Archetype=CylinderComponent'Park_P.archetypes.vehiclepickup.VehiclePickup_Boost{1}:DefaultCollisionCylinder'
            CollisionHeight=100
            CollisionRadius=100
            ReplacementPrimitive=None
            CollideActors=True
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="CylinderComponent_{0}"
            ObjectArchetype=CylinderComponent'Park_P.archetypes.vehiclepickup.VehiclePickup_Boost{1}:DefaultCollisionCylinder'
         End Object
         Begin Object Class=SpriteComponent Name=Sprite_{0} ObjName=SpriteComponent_{0} Archetype=SpriteComponent'Park_P.archetypes.vehiclepickup.VehiclePickup_Boost{1}:Sprite'
            Sprite=Texture2D'EditorResources.S_KVehFact'
            SpriteCategoryName="VehiclePickupBoost"
            ReplacementPrimitive=None
            HiddenGame=True
            AlwaysLoadOnClient=False
            AlwaysLoadOnServer=False
            LightingChannels=(bInitialized=True,Dynamic=True)
            Scale=2.000000
            Name="SpriteComponent_{0}"
            ObjectArchetype=SpriteComponent'Park_P.archetypes.vehiclepickup.VehiclePickup_Boost{1}:Sprite'
         End Object
         FXActorArchetype=FXActor_TA'FXActor_Boost_TA_{0}'
         CylinderComponent=CylinderComponent'CylinderComponent_{0}'
         Components(0)=CylinderComponent'CylinderComponent_{0}'
         Components(1)=()
         Components(2)=SpriteComponent'SpriteComponent_{0}'
         Location=(X={2[0]},Y={2[1]},Z={2[2]})
		 Rotation=(Pitch={3[0]},Yaw={3[1]},Roll={3[2]})
         Tag="{4}_VehiclePickup_Boost_TA_{0}"
         CollisionComponent=CylinderComponent'CylinderComponent_{0}'
         Name="VehiclePickup_Boost_TA_{0}"
         ObjectArchetype=VehiclePickup_Boost_TA'Park_P.archetypes.vehiclepickup.VehiclePickup_Boost{1}'
      End Actor
   End Level
Begin Surface
End Surface
End Map"""

boostSmStaticLoc = [
[[0.0, -3257, 8.965], ['Park_P.park_assets.Meshes.BoostPads_01_Combined']], 
[[0.0, 0.0, 8.965], ['Park_P.park_assets.Meshes.BoostPads_02_Combined']], 
[[0.0, 3257, 8.965], ['Park_P.park_assets.Meshes.BoostPads_03_Combined']]
]

boostSmMaterials = """Materials(0)=MaterialInstanceConstant'HoopsStadium_P.pickup_boost.Materials.BoostPad_Small_MIC'"""
boostLgMaterials = """Materials(0)=Material'Park_P.pickup_boost.Materials.BoostPad_Mat'"""
boostLgMesh = 'Park_P.pickup_boost.BoostPad_Large'

# DEFAULT POINT IN SPACE STRING
# ----------------------------------------------

pointString = """
Begin Map
Begin Level
  Begin Actor Class=PointInSpace_TA Name=PointInSpace_TA_{0} Archetype=PointInSpace_TA'tagame.Default__PointInSpace_TA'
     Begin Object Class=SpriteComponent Name=Sprite ObjName=SpriteComponent_{0} Archetype=SpriteComponent'tagame.Default__PointInSpace_TA:Sprite'
        ReplacementPrimitive=None
        HiddenGame=True
        AlwaysLoadOnClient=False
        AlwaysLoadOnServer=False
        LightingChannels=(bInitialized=True,Dynamic=True)
        Name="SpriteComponent_{0}"
        ObjectArchetype=SpriteComponent'tagame.Default__PointInSpace_TA:Sprite'
     End Object
     Begin Object Class=ArrowComponent Name=Arrow ObjName=ArrowComponent_2 Archetype=ArrowComponent'tagame.Default__PointInSpace_TA:Arrow'
        ReplacementPrimitive=None
        LightingChannels=(bInitialized=True,Dynamic=True)
        Name="ArrowComponent_2"
        ObjectArchetype=ArrowComponent'tagame.Default__PointInSpace_TA:Arrow'
     End Object
     Components(0)=SpriteComponent'SpriteComponent_{0}'
     Components(1)=ArrowComponent'ArrowComponent_2'
     Location=(X={1[0]},Y={1[1]},Z={1[2]})
     Rotation=(Pitch={2[0]},Yaw={2[1]},Roll={2[2]})
     DrawScale=1
     CreationTime=0
     Tag=PointInSpace_TA
     Name="PointInSpace_TA_{0}"
     ObjectArchetype=PointInSpace_TA'tagame.Default__PointInSpace_TA'
  End Actor
End Level
Begin Surface
End Surface
End Map"""

# DEFAULT GOAL STRING
# -----------------------------------------------

goalString = """
Begin Map
   Begin Level
      Begin Actor Class=GoalVolume_TA Name=GoalVolume_TA_{0} Archetype=GoalVolume_TA'tagame.Default__GoalVolume_TA'
         Begin Object Class=Polys Name=Polys_{0}
            Name="Polys_{0}"
            ObjectArchetype=Polys'Engine.Default__Polys'
         End Object
         Begin Object Class=Goal_TA Name=DefaultGoal ObjName=Goal_TA_{0} Archetype=Goal_TA'tagame.Default__GoalVolume_TA:DefaultGoal'
            GoalOrientation=PointInSpace_TA'PointInSpace_TA_{0}'
            TeamNum={1}
            Name="Goal_TA_{0}"
            ObjectArchetype=Goal_TA'tagame.Default__GoalVolume_TA:DefaultGoal'
         End Object
         Begin Object Class=BrushComponent Name=BrushComponent0 ObjName=BrushComponent_{0} Archetype=BrushComponent'tagame.Default__GoalVolume_TA:BrushComponent0'
            Brush=Model'Model_{0}'
            ReplacementPrimitive=None
            bAcceptsLights=True
            CollideActors=True
            BlockNonZeroExtent=True
            bDisableAllRigidBody=True
            AlwaysLoadOnClient=True
            AlwaysLoadOnServer=True
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="BrushComponent_{0}"
            ObjectArchetype=BrushComponent'tagame.Default__GoalVolume_TA:BrushComponent0'
         End Object
         Goal=Goal_TA'Goal_TA_{0}'
         Begin Brush Name=Model_{0}
            {2}
         End Brush
         Brush=Model'Model_{0}'
         BrushComponent=BrushComponent'BrushComponent_{0}'
         Components(0)=BrushComponent'BrushComponent_{0}'
         Location=(X={3[0]},Y={3[1]},Z={3[2]})
		 Rotation=(Pitch={4[0]},Yaw={4[1]},Roll=4[2])
         DrawScale3D=(X={5[0]},Y={5[1]},Z={5[2]})
         CreationTime=0
         Tag="GoalVolume_Team_#{1}"
         Layer="{6}"
         CollisionComponent=BrushComponent'BrushComponent_{0}'
         Name="GoalVolume_TA_{0}"
         ObjectArchetype=GoalVolume_TA'tagame.Default__GoalVolume_TA'
      End Actor
   End Level
Begin Surface
End Surface
End Map"""

# DEFAULT PROPERTIES OF BLUE GOAL
# -------------------------------------------------------------------------

defaultBluePointInSpaceLocation = [0.0, 5120.0, 320.0]

defaultBluePointInSpaceRotation = [0, 49152, 0]

defaultBlueTeamNumber = 0

defaultBlueGoalLocation = [0.0, 5570.0, 320.0]

goalRot = [0, 0, 0]

goalScale = [1, 1, 1]

# DEFAULT PROPERTIES OF ORANGE GOAL
# -------------------------------------------------------------------------

defaultOrangePointInSpaceLocation = [0.0, -5120.0, 320.0]

defaultOrangePointInSpaceRotation = [0, 81920, 0]

defaultOrangeTeamNumber = 1

defaultOrangeGoalLocation = [0.0, -5570.0, 320.0]

# DEFAULT PROPERTIES OF GOAL BRUSH
# -------------------------------------------------------------------------
defaultGoalT3d = """
Begin PolyList
    Begin Polygon Flags=3584 Link=0
        Origin   -00979.130744934082,-00450.000000,-00320.0000047683716
        Normal   -00001.000000,-00000.000000,+00000.000000
        TextureU +00000.000000,+00001.000000,+00000.000000
        TextureV +00000.000000,+00000.000000,+00001.000000
        Vertex   -00979.130744934082,-00450.000000,-00320.0000047683716
        Vertex   -00979.130744934082,-00450.000000,+00320.0000047683716
        Vertex   -00979.130744934082,+00450.000000,+00320.0000047683716
        Vertex   -00979.130744934082,+00450.000000,-00320.0000047683716
    End Polygon
    Begin Polygon Flags=3584 Link=1
        Origin   -00979.130744934082,+00450.000000,-00320.0000047683716
        Normal   +00000.000000,+00000.9999999403953552,+00000.000000
        TextureU +00001.000000,+00000.000000,+00000.000000
        TextureV +00000.000000,+00000.000000,+00001.000000
        Vertex   -00979.130744934082,+00450.000000,-00320.0000047683716
        Vertex   -00979.130744934082,+00450.000000,+00320.0000047683716
        Vertex   +00979.130744934082,+00450.000000,+00320.0000047683716
        Vertex   +00979.130744934082,+00450.000000,-00320.0000047683716
    End Polygon
    Begin Polygon Flags=3584 Link=2
        Origin   +00979.130744934082,+00450.000000,-00320.0000047683716
        Normal   +00001.000000,-00000.000000,+00000.000000
        TextureU +00000.000000,+00001.000000,+00000.000000
        TextureV +00000.000000,+00000.000000,+00001.000000
        Vertex   +00979.130744934082,+00450.000000,-00320.0000047683716
        Vertex   +00979.130744934082,+00450.000000,+00320.0000047683716
        Vertex   +00979.130744934082,-00450.000000,+00320.0000047683716
        Vertex   +00979.130744934082,-00450.000000,-00320.0000047683716
    End Polygon
    Begin Polygon Flags=3584 Link=3
        Origin   +00979.130744934082,-00450.000000,-00320.0000047683716
        Normal   +00000.000000,-00000.9999999403953552,+00000.000000
        TextureU +00001.000000,+00000.000000,+00000.000000
        TextureV +00000.000000,+00000.000000,+00001.000000
        Vertex   +00979.130744934082,-00450.000000,-00320.0000047683716
        Vertex   +00979.130744934082,-00450.000000,+00320.0000047683716
        Vertex   -00979.130744934082,-00450.000000,+00320.0000047683716
        Vertex   -00979.130744934082,-00450.000000,-00320.0000047683716
    End Polygon
    Begin Polygon Flags=3584 Link=4
        Origin   -00979.130744934082,+00450.000000,-00320.0000047683716
        Normal   +00000.000000,+00000.000000,-00001.000000
        TextureU +00001.000000,+00000.000000,+00000.000000
        TextureV +00000.000000,+00001.000000,+00000.000000
        Vertex   -00979.130744934082,+00450.000000,-00320.0000047683716
        Vertex   +00979.130744934082,+00450.000000,-00320.0000047683716
        Vertex   +00979.130744934082,-00450.000000,-00320.0000047683716
        Vertex   -00979.130744934082,-00450.000000,-00320.0000047683716
    End Polygon
    Begin Polygon Flags=3584 Link=5
        Origin   +00979.130744934082,+00450.000000,+00320.0000047683716
        Normal   +00000.000000,-00000.000000,+00001.000000
        TextureU +00001.000000,+00000.000000,+00000.000000
        TextureV +00000.000000,+00001.000000,+00000.000000
        Vertex   +00979.130744934082,+00450.000000,+00320.0000047683716
        Vertex   -00979.130744934082,+00450.000000,+00320.0000047683716
        Vertex   -00979.130744934082,-00450.000000,+00320.0000047683716
        Vertex   +00979.130744934082,-00450.000000,+00320.0000047683716
    End Polygon
End PolyList"""

# DEFAULT PLAYER START STRING
# ----------------------------------------

playerString = """
Begin Map
   Begin Level
      Begin Actor Class=PlayerStart_TA Name=PlayerStart_TA_{0} Archetype=PlayerStart_TA'tagame.Default__PlayerStart_TA'
         Begin Object Class=CylinderComponent Name=CollisionCylinder ObjName=CylinderComponent_{0} Archetype=CylinderComponent'tagame.Default__PlayerStart_TA:CollisionCylinder'
            CollisionHeight=80.000000
            CollisionRadius=40.000000
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="CylinderComponent_{0}"
            ObjectArchetype=CylinderComponent'tagame.Default__PlayerStart_TA:CollisionCylinder'
         End Object
         Begin Object Class=SpriteComponent Name=Sprite_{0} ObjName=SpriteComponent_{0} Archetype=SpriteComponent'tagame.Default__PlayerStart_TA:Sprite'
            Sprite=Texture2D'EditorResources.S_Player'
            SpriteCategoryName="PlayerStart"
            ReplacementPrimitive=None
            HiddenGame=True
            AlwaysLoadOnClient=False
            AlwaysLoadOnServer=False
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="SpriteComponent_{0}"
            ObjectArchetype=SpriteComponent'tagame.Default__PlayerStart_TA:Sprite'
         End Object
         Begin Object Class=SpriteComponent Name=Sprite2_{0} ObjName=SpriteComponent_{0}_2 Archetype=SpriteComponent'tagame.Default__PlayerStart_TA:Sprite2'
            Sprite=Texture2D'EditorResources.Bad'
            SpriteCategoryName="Navigation"
            ReplacementPrimitive=None
            HiddenGame=True
            HiddenEditor=True
            AlwaysLoadOnClient=False
            AlwaysLoadOnServer=False
            LightingChannels=(bInitialized=True,Dynamic=True)
            Scale=0.250000
            Name="SpriteComponent_{0}_2"
            ObjectArchetype=SpriteComponent'tagame.Default__PlayerStart_TA:Sprite2'
         End Object
         Begin Object Class=ArrowComponent Name=Arrow_{0} ObjName=ArrowComponent_{0} Archetype=ArrowComponent'tagame.Default__PlayerStart_TA:Arrow'
            ArrowColor=(B=255,G=200,R=150,A=255)
            ArrowSize=0.500000
            bTreatAsASprite=True
            SpriteCategoryName="Navigation"
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="ArrowComponent_{0}"
            ObjectArchetype=ArrowComponent'tagame.Default__PlayerStart_TA:Arrow'
         End Object
         Begin Object Class=PathRenderingComponent Name=PathRenderer_{0} ObjName=PathRenderingComponent_{0} Archetype=PathRenderingComponent'tagame.Default__PlayerStart_TA:PathRenderer'
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="PathRenderingComponent_{0}"
            ObjectArchetype=PathRenderingComponent'tagame.Default__PlayerStart_TA:PathRenderer'
         End Object
         TeamIndex=1
         bPathsChanged=True
         bDestinationOnly=True
         CylinderComponent=CylinderComponent'CylinderComponent_{0}'
         Components(0)=SpriteComponent'SpriteComponent_{0}'
         Components(1)=SpriteComponent'SpriteComponent_{0}_2'
         Components(2)=ArrowComponent'ArrowComponent_{0}'
         Components(3)=CylinderComponent'CylinderComponent_{0}'
         Components(4)=PathRenderingComponent'PathRenderingComponent_{0}'
         Location=(X={1[0]},Y={1[1]},Z={1[2]})
		 Rotation=(Pitch={2[0]},Yaw={2[1]},Roll={2[2]})
         DrawScale=4.000000
         Base=StaticMeshActor'StaticMeshActor_5'
         Tag="PlayerStart_TA_{0}"
         CollisionComponent=CylinderComponent'CylinderComponent_{0}'
         Name="PlayerStart_TA_{0}"
         ObjectArchetype=PlayerStart_TA'tagame.Default__PlayerStart_TA'
      End Actor
   End Level
Begin Surface
End Surface
End Map"""


#  DEFAULT PLAYER START LOCATIONS/ROTATIONS
# -------------------------------------------------------------------------
playerStart0 = [[2688.0, -4608.0, 82.99560], [0, 81920, 0]]

playerStart1 = [[-2048.0, -2560.0, 82.99560], [0, 73728, 0]]

playerStart2 = [[2048.0, -2560.0, 82.99560], [0, 90112, 0]]

playerStart3 = [[-256.0, -3840.0, 82.99560], [0, 81920, 0]]

playerStart4 = [[-2688.0, -4608.0, 82.99560], [0, 81920, 0]]

playerStart5 = [[-2304.0, -4608.0, 82.99560], [0, 81920, 0]]

playerStart6 = [[2304.0, -4608.0, 82.99560], [0, 81920, 0]]

playerStart7 = [[0.0, -4608.0, 82.99560], [0, 81920, 0]]

playerStart8 = [[256.0, -3840.0, 82.99560], [0, 81920, 0]]


# DEFAULT PILLAR STRING
# -----------------------------------------------

pillarString = """
Begin Map
   Begin Level
      Begin Actor Class=Pylon_Soccar_TA Name=Pylon_Soccar_TA_{0} Archetype=Pylon_Soccar_TA'tagame.Default__Pylon_Soccar_TA'
         Begin Object Class=NavigationMeshBase Name=NavigationMeshBase_{0}
            Name="NavigationMeshBase_{0}"
            ObjectArchetype=NavigationMeshBase'Engine.Default__NavigationMeshBase'
         End Object
         Begin Object Class=NavigationMeshBase Name=NavigationMeshBase_{0}_2
            Name="NavigationMeshBase_{0}_2"
            ObjectArchetype=NavigationMeshBase'Engine.Default__NavigationMeshBase'
         End Object
         Begin Object Class=Goal_TA Name={1[0]} ObjName={1[0]} Archetype=Goal_TA'tagame.Default__Pylon_Soccar_TA:Goal_TA_0'
            Name="{1[0]}"
            ObjectArchetype=Goal_TA'tagame.Default__Pylon_Soccar_TA:Goal_TA_0'
         End Object
         Begin Object Class=Goal_TA Name={1[1]} ObjName={1[1]} Archetype=Goal_TA'tagame.Default__Pylon_Soccar_TA:Goal_TA_1'
            TeamNum=1
            Name="{1[1]}"
            ObjectArchetype=Goal_TA'tagame.Default__Pylon_Soccar_TA:Goal_TA_1'
         End Object
         Begin Object Class=DrawPylonRadiusComponent Name=DrawPylonRadius_{0} ObjName=DrawPylonRadiusComponent_{0} Archetype=DrawPylonRadiusComponent'tagame.Default__Pylon_Soccar_TA:DrawPylonRadius0'
            SphereRadius=2048.000000
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="DrawPylonRadiusComponent_{0}"
            ObjectArchetype=DrawPylonRadiusComponent'tagame.Default__Pylon_Soccar_TA:DrawPylonRadius0'
         End Object
         Begin Object Class=NavMeshRenderingComponent Name=NavMeshRenderer_{0} ObjName=NavMeshRenderingComponent_{0} Archetype=NavMeshRenderingComponent'tagame.Default__Pylon_Soccar_TA:NavMeshRenderer'
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="NavMeshRenderingComponent_{0}"
            ObjectArchetype=NavMeshRenderingComponent'tagame.Default__Pylon_Soccar_TA:NavMeshRenderer'
         End Object
         Begin Object Class=SpriteComponent Name=Sprite{0}_1 ObjName=SpriteComponent_{0}_1 Archetype=SpriteComponent'tagame.Default__Pylon_Soccar_TA:Sprite3'
            Sprite=Texture2D'EditorResources.BadPylon'
            SpriteCategoryName="Navigation"
            ReplacementPrimitive=None
            HiddenGame=True
            HiddenEditor=True
            AlwaysLoadOnClient=False
            AlwaysLoadOnServer=False
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="SpriteComponent_{0}_1"
            ObjectArchetype=SpriteComponent'tagame.Default__Pylon_Soccar_TA:Sprite3'
         End Object
         Begin Object Class=CylinderComponent Name=CollisionCylinder{0} ObjName=CylinderComponent_{0} Archetype=CylinderComponent'tagame.Default__Pylon_Soccar_TA:CollisionCylinder'
            CollisionHeight=50.000000
            CollisionRadius=50.000000
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="CylinderComponent_{0}"
            ObjectArchetype=CylinderComponent'tagame.Default__Pylon_Soccar_TA:CollisionCylinder'
         End Object
         Begin Object Class=SpriteComponent Name=Sprite_{0}_2 ObjName=SpriteComponent_{0}_2 Archetype=SpriteComponent'tagame.Default__Pylon_Soccar_TA:Sprite'
            Sprite=Texture2D'EditorResources.Pylon'
            SpriteCategoryName="Navigation"
            ReplacementPrimitive=None
            HiddenGame=True
            AlwaysLoadOnClient=False
            AlwaysLoadOnServer=False
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="SpriteComponent_{0}_2"
            ObjectArchetype=SpriteComponent'tagame.Default__Pylon_Soccar_TA:Sprite'
         End Object
         Begin Object Class=SpriteComponent Name=Sprite_{0}_3 ObjName=SpriteComponent_{0}_3 Archetype=SpriteComponent'tagame.Default__Pylon_Soccar_TA:Sprite2'
            Sprite=Texture2D'EditorResources.Bad'
            SpriteCategoryName="Navigation"
            ReplacementPrimitive=None
            HiddenGame=True
            HiddenEditor=True
            AlwaysLoadOnClient=False
            AlwaysLoadOnServer=False
            LightingChannels=(bInitialized=True,Dynamic=True)
            Scale=0.250000
            Name="SpriteComponent_{0}_3"
            ObjectArchetype=SpriteComponent'tagame.Default__Pylon_Soccar_TA:Sprite2'
         End Object
         Begin Object Class=ArrowComponent Name=Arrow_{0} ObjName=ArrowComponent_{0} Archetype=ArrowComponent'tagame.Default__Pylon_Soccar_TA:Arrow'
            ArrowColor=(B=255,G=200,R=150,A=255)
            ArrowSize=0.500000
            bTreatAsASprite=True
            SpriteCategoryName="Navigation"
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="ArrowComponent_{0}"
            ObjectArchetype=ArrowComponent'tagame.Default__Pylon_Soccar_TA:Arrow'
         End Object
         Begin Object Class=PathRenderingComponent Name=PathRenderer_{0} ObjName=PathRenderingComponent_{0} Archetype=PathRenderingComponent'tagame.Default__Pylon_Soccar_TA:PathRenderer'
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="PathRenderingComponent_{0}"
            ObjectArchetype=PathRenderingComponent'tagame.Default__Pylon_Soccar_TA:PathRenderer'
         End Object
         FieldOrientation=(Pitch=0,Yaw=16384,Roll=0)
         FieldSize=(X=10000.000000,Y=15000.000000,Z=5000.000000)
         FieldExtent=(X=10000.000000,Y=15000.000000,Z=100.000000)
         FieldCenter=(X=0.000000,Y=0.000000,Z=100.000000)
         Goals(0)=Goal_TA'{1[0]}'
         Goals(1)=Goal_TA'{1[1]}'
         SpawnPoints(0)=PlayerStart_TA'{2[0]}'
         SpawnPoints(1)=PlayerStart_TA'{2[1]}'
         SpawnPoints(2)=PlayerStart_TA'{2[2]}'
         SpawnPoints(3)=PlayerStart_TA'{2[3]}'
         SpawnPoints(4)=PlayerStart_TA'{2[4]}'
         SpawnPoints(5)=PlayerStart_TA'{2[5]}'
         SpawnPoints(6)=PlayerStart_TA'{2[6]}'
         SpawnPoints(7)=PlayerStart_TA'{2[7]}'
         SpawnPoints(8)=PlayerStart_TA'{2[8]}
         GroundZ=-1000.000000
         PylonRadiusPreview=DrawPylonRadiusComponent'DrawPylonRadiusComponent_{0}'
         RenderingComp=NavMeshRenderingComponent'NavMeshRenderingComponent_{0}'
         NavMeshGenerator=1
         bPathsChanged=True
         nextNavigationPoint=PlayerStart_TA'PlayerStart_TA_2'
         CylinderComponent=CylinderComponent'CylinderComponent_{0}'
         NavGuid=(A=-1450235986,B=1184243848,C=797072292,D=-370696684)
         Components(0)=SpriteComponent'SpriteComponent_{0}_2'
         Components(1)=SpriteComponent'SpriteComponent_{0}_3'
         Components(2)=ArrowComponent'ArrowComponent_{0}'
         Components(3)=CylinderComponent'CylinderComponent_{0}'
         Components(4)=PathRenderingComponent'PathRenderingComponent_{0}'
         Components(5)=NavMeshRenderingComponent'NavMeshRenderingComponent_{0}'
         Components(6)=DrawPylonRadiusComponent'DrawPylonRadiusComponent_{0}'
         Components(7)=SpriteComponent'SpriteComponent_{0}_1'
         Location=(X=0,Y=0,Z=52)
         Rotation=(Pitch=0,Yaw=16384,Roll=0)
         DrawScale=3.000000
         Base=StaticMeshActor'StaticMeshActor_5'
         Tag="Pylon_Soccar_TA"
         RelativeLocation=(X=0,Y=0,Z=52)
         CollisionComponent=CylinderComponent'CylinderComponent_{0}'
         Name="Pylon_Soccar_TA_{0}"
         ObjectArchetype=Pylon_Soccar_TA'tagame.Default__Pylon_Soccar_TA'
      End Actor
   End Level
Begin Surface
End Surface
End Map"""