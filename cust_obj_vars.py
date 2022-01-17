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

# import bpy
# DYNAMIC TRIGGER STRING
# ---------------------------------------------
dynamicTriggerString = """Begin Map
   Begin Level
      Begin Actor Class=DynamicTriggerVolume Name=DynamicTriggerVolume_{0} Archetype=DynamicTriggerVolume'Engine.Default__DynamicTriggerVolume'
         Begin Object Class=Polys Name=Polys_{0}
            Name="Polys_{0}"
            ObjectArchetype=Polys'Engine.Default__Polys'
         End Object
         Begin Object Class=BrushComponent Name=BrushComponent0 ObjName=BrushComponent_{0} Archetype=BrushComponent'Engine.Default__DynamicTriggerVolume:BrushComponent0'
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
            ObjectArchetype=BrushComponent'Engine.Default__DynamicTriggerVolume:BrushComponent0'
         End Object
         Begin Brush Name=Model_{0}
            {1}
         End Brush
         Brush=Model'Model_{0}'
         BrushComponent=BrushComponent'BrushComponent_{0}'
         Components(0)=BrushComponent'BrushComponent_{0}'
         Location=(X={2[0]:.6f},Y={2[1]:.6f},Z={2[2]:.6f})
         Rotation=(Pitch={3[0]:.6f},Yaw={3[1]:.6f},Roll={3[2]:.6f})
         DrawScale3D=(X={4[0]:.6f},Y={4[1]:.6f},Z={4[2]:.6f})
         CreationTime=0
         Tag="{5}"
         Layer="{6}"
         CollisionComponent=BrushComponent'BrushComponent_{0}'
         Name="{5}_{0}"
         ObjectArchetype=DynamicTriggerVolume'Engine.Default__DynamicTriggerVolume'
      End Actor
   End Level
Begin Surface
End Surface
End Map"""


# SPOTLIGHT STRING
# ---------------------------------------------        
spotLightString = """Begin Map
   Begin Level
      Begin Actor Class=SpotLightToggleable Name=SpotLightToggleable_{0} Archetype=SpotLightToggleable'Engine.Default__SpotLightToggleable'
         Begin Object Class=DrawLightConeComponent Name=DrawInnerCone0 ObjName=DrawLightConeComponent_2_{0} Archetype=DrawLightConeComponent'Engine.Default__SpotLightToggleable:DrawInnerCone0'
            ConeRadius=1024.000000
            ConeAngle=0.000000
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="DrawLightConeComponent_2_{0}"
            ObjectArchetype=DrawLightConeComponent'Engine.Default__SpotLightToggleable:DrawInnerCone0'
         End Object
         Begin Object Class=DrawLightConeComponent Name=DrawOuterCone0 ObjName=DrawLightConeComponent_3_{0} Archetype=DrawLightConeComponent'Engine.Default__SpotLightToggleable:DrawOuterCone0'
            ConeColor=(B=255,G=255,R=200,A=255)
            ConeRadius=1024.000000
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="DrawLightConeComponent_3_{0}"
            ObjectArchetype=DrawLightConeComponent'Engine.Default__SpotLightToggleable:DrawOuterCone0'
         End Object
         Begin Object Class=DrawLightRadiusComponent Name=DrawLightRadius0 ObjName=DrawLightRadiusComponent_2_{0} Archetype=DrawLightRadiusComponent'Engine.Default__SpotLightToggleable:DrawLightRadius0'
            SphereRadius=1024.000000
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="DrawLightRadiusComponent_2_{0}"
            ObjectArchetype=DrawLightRadiusComponent'Engine.Default__SpotLightToggleable:DrawLightRadius0'
         End Object
         Begin Object Class=DrawLightRadiusComponent Name=DrawLightSourceRadius0 ObjName=DrawLightRadiusComponent_3_{0} Archetype=DrawLightRadiusComponent'Engine.Default__SpotLightToggleable:DrawLightSourceRadius0'
            SphereColor=(B=0,G=239,R=231,A=255)
            SphereRadius=32.000000
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="DrawLightRadiusComponent_3_{0}"
            ObjectArchetype=DrawLightRadiusComponent'Engine.Default__SpotLightToggleable:DrawLightSourceRadius0'
         End Object
         Begin Object Class=SpotLightComponent Name=SpotLightComponent0 ObjName=SpotLightComponent_{0} Archetype=SpotLightComponent'Engine.Default__SpotLightToggleable:SpotLightComponent0'
            PreviewInnerCone=DrawLightConeComponent'DrawLightConeComponent_2_{0}'
            PreviewOuterCone=DrawLightConeComponent'DrawLightConeComponent_3_{0}'
            CachedParentToWorld=(XPlane=(W=0.000000,X=0.000000,Y=0.000000,Z=-1.000000),YPlane=(W=0.000000,X=-0.000000,Y=1.000000,Z=-0.000000),ZPlane=(W=0.000000,X=1.000000,Y=0.000000,Z=0.000000),WPlane=(W=1.000000,X=-60.936401,Y=144.001099,Z=1035.462280))
            PreviewLightRadius=DrawLightRadiusComponent'DrawLightRadiusComponent_2_{0}'
            LightmassSettings=(LightSourceRadius=32.000000,IndirectLightingScale=0.000000)
            PreviewLightSourceRadius=DrawLightRadiusComponent'DrawLightRadiusComponent_3_{0}'
            LightGuid=(A=199097462,B=1258459027,C=-1227397451,D=-1066570931)
            LightmapGuid=(A=1471253091,B=1300878571,C=1949417371,D=346712220)
            CastDynamicShadows=False
            bPrecomputedLightingIsValid=False
            LightingChannels=(Dynamic=False)
            LightAffectsClassification=LAC_STATIC_AFFECTING
            Name="SpotLightComponent_{0}"
            ObjectArchetype=SpotLightComponent'Engine.Default__SpotLightToggleable:SpotLightComponent0'
         End Object
         Begin Object Class=SpriteComponent Name=Sprite ObjName=SpriteComponent_{0} Archetype=SpriteComponent'Engine.Default__SpotLightToggleable:Sprite'
            Sprite=Texture2D'EditorResources.LightIcons.Light_Spot_Toggleable_Statics'
            SpriteCategoryName="Lighting"
            ReplacementPrimitive=None
            HiddenGame=True
            AlwaysLoadOnClient=False
            AlwaysLoadOnServer=False
            LightingChannels=(bInitialized=True,Dynamic=True)
            Scale=0.250000
            Name="SpriteComponent_{0}"
            ObjectArchetype=SpriteComponent'Engine.Default__SpotLightToggleable:Sprite'
         End Object
         Begin Object Class=ArrowComponent Name=ArrowComponent0 ObjName=ArrowComponent_72_{0} Archetype=ArrowComponent'Engine.Default__SpotLightToggleable:ArrowComponent0'
            ArrowColor=(B=255,G=200,R=150,A=255)
            bTreatAsASprite=True
            SpriteCategoryName="Lighting"
            ReplacementPrimitive=None
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="ArrowComponent_72_{0}"
            ObjectArchetype=ArrowComponent'Engine.Default__SpotLightToggleable:ArrowComponent0'
         End Object
         LightComponent=SpotLightComponent'SpotLightComponent_{0}'
         Components(0)=SpriteComponent'SpriteComponent_{0}'
         Components(1)=DrawLightRadiusComponent'DrawLightRadiusComponent_2_{0}'
         Components(2)=DrawLightConeComponent'DrawLightConeComponent_2_{0}'
         Components(3)=DrawLightConeComponent'DrawLightConeComponent_3_{0}'
         Components(4)=DrawLightRadiusComponent'DrawLightRadiusComponent_3_{0}'
         Components(5)=SpotLightComponent'SpotLightComponent_{0}'
         Components(6)=ArrowComponent'ArrowComponent_72_{0}'
         Location=(X={1[0]:.6f},Y={1[1]:.6f},Z={1[2]:.6f})
         Rotation=(Pitch={2[0]:.6f},Yaw={2[1]:.6f},Roll={2[2]:.6f})
         DrawScale3D=(X={3[0]:.6f},Y={3[1]:.6f},Z={3[2]:.6f})
         CreationTime=0
         Tag="{4}"
         Layer="{5}"
         Name="{4}_{0}"
         ObjectArchetype=SpotLightToggleable'Engine.Default__SpotLightToggleable'
      End Actor
   End Level
Begin Surface
End Surface
End Map"""

customBoostFxString = """Begin Map
   Begin Level
      Begin Actor Class=FXActor_Boost_TA Name=FXActor_Boost_TA_{0} Archetype=FXActor_Boost_TA'tagame.Default__FXActor_Boost_TA'
         Begin Object Class=StaticMeshComponent Name=StaticMeshComponent_{0} ObjName=StaticMeshComponent_{0}
            StaticMesh=StaticMesh'{1}'
            Materials(0)=Material'Park_P.pickup_boost.BoostPad_Mat'
            Materials(1)=Material'Park_P.pickup_boost.BoostPad_LightCone_03_Mat'
            ReplacementPrimitive=None
            Name="StaticMeshComponent_{0}"
            ObjectArchetype=StaticMeshComponent'Engine.Default__StaticMeshComponent'
         End Object
         Begin Object Class=ParticleSystemComponent Name=ParticleSystemComponent_{0} ObjName=ParticleSystemComponent_{0}
            Template=ParticleSystem'Park_P.pickup_boost.BoostPad_Used_PS'
            ReplacementPrimitive=None
            Name="ParticleSystemComponent_{0}"
            ObjectArchetype=ParticleSystemComponent'Engine.Default__ParticleSystemComponent'
         End Object{5}
         Begin Object Class=ParameterDispenser_X Name=DefaultParameters ObjName=ParameterDispenser_X_{0} Archetype=ParameterDispenser_X'tagame.Default__FXActor_Boost_TA:DefaultParameters'
            Name="ParameterDispenser_X_{0}"
            ObjectArchetype=ParameterDispenser_X'tagame.Default__FXActor_Boost_TA:DefaultParameters'
         End Object
         Begin Object Class=SpriteComponent Name=Sprite ObjName=SpriteComponent_{0} Archetype=SpriteComponent'tagame.Default__FXActor_Boost_TA:Sprite'
            Sprite=Texture2D'EditorResources.MatIcon_FX'
            SpriteCategoryName="FXActor"
            ReplacementPrimitive=None
            HiddenGame=True
            AlwaysLoadOnClient=False
            AlwaysLoadOnServer=False
            LightingChannels=(bInitialized=True,Dynamic=True)
            Scale=2.000000
            Name="SpriteComponent_{0}"
            ObjectArchetype=SpriteComponent'tagame.Default__FXActor_Boost_TA:Sprite'
         End Object
         Attachments(0)=(Name="BaseMesh",Component=StaticMeshComponent'StaticMeshComponent_{0}',AttachAny=(FXActorEvent_X'FXActorEvents.Spawned'),DetachAny=(FXActorEvent_X'FXActorEvents.PickedUp'))
         Attachments(1)=(Name="PickupPSC",Component=ParticleSystemComponent'ParticleSystemComponent_{0}',AttachAny=(FXActorEvent_X'FXActorEvents.PickedUp')){6}
         Parameters=ParameterDispenser_X'ParameterDispenser_X_{0}'
         Components(0)=SpriteComponent'SpriteComponent_{0}'
         Location=(X={2[0]:.6f},Y={2[1]:.6f},Z={2[2]:.6f})
         Rotation=(Pitch={3[0]:.6f},Yaw={3[1]:.6f},Roll={3[2]:.6f})
         Tag="Boost_{4}"
         Layer="Field, Boost"
         bNoDelete=True
         Tag="FXActor_Boost_TA"
         Name="FXActor_Boost_TA_{0}"
         ObjectArchetype=FXActor_Boost_TA'tagame.Default__FXActor_Boost_TA'
      End Actor
   End Level
Begin Surface
End Surface
End Map"""

customLargeBoostFx = """\n         Begin Object Class=ParticleSystemComponent Name=ParticleSystemComponent_2_{0} ObjName=ParticleSystemComponent_2_{0}
            Template=ParticleSystem'Park_P.pickup_boost.BoostOrb_PS'
            ReplacementPrimitive=None
            Name="ParticleSystemComponent_2_{0}"
            ObjectArchetype=ParticleSystemComponent'Engine.Default__ParticleSystemComponent'
         End Object"""
         
customLargeBoostAttach = """\n         Attachments(2)=(Name="BoostOrb_PSC",Component=ParticleSystemComponent'ParticleSystemComponent_2_{0}',AttachAny=(FXActorEvent_X'FXActorEvents.Spawned'),DetachAny=(FXActorEvent_X'FXActorEvents.PickedUp'))"""
      
customPickUpString = """Begin Map
   Begin Level
      Begin Actor Class=VehiclePickup_Boost_TA Name=VehiclePickup_Boost_TA_{0} Archetype=VehiclePickup_Boost_TA'tagame.Default__VehiclePickup_Boost_TA'
         Begin Object Class=CylinderComponent Name=DefaultCollisionCylinder ObjName=CylinderComponent_{0} Archetype=CylinderComponent'tagame.Default__VehiclePickup_Boost_TA:DefaultCollisionCylinder'
            CollisionHeight=64.000000
            CollisionRadius={6}
            ReplacementPrimitive=None
            CollideActors=True
            LightingChannels=(bInitialized=True,Dynamic=True)
            Name="CylinderComponent_{0}"
            ObjectArchetype=CylinderComponent'tagame.Default__VehiclePickup_Boost_TA:DefaultCollisionCylinder'
         End Object
         Begin Object Class=SpriteComponent Name=Sprite ObjName=SpriteComponent_{0} Archetype=SpriteComponent'tagame.Default__VehiclePickup_Boost_TA:Sprite'
            Sprite=Texture2D'EditorResources.S_KVehFact'
            SpriteCategoryName="VehiclePickupBoost"
            ReplacementPrimitive=None
            HiddenGame=True
            AlwaysLoadOnClient=False
            AlwaysLoadOnServer=False
            LightingChannels=(bInitialized=True,Dynamic=True)
            Scale=2.000000
            Name="SpriteComponent_{0}"
            ObjectArchetype=SpriteComponent'tagame.Default__VehiclePickup_Boost_TA:Sprite'
         End Object
         BoostAmount={3}
         BoostType=BoostType_{4}
         RespawnDelay={5}
         FXActorArchetype=FXActor_Boost_TA'FXActor_Boost_TA_{0}'
         CylinderComponent=CylinderComponent'CylinderComponent_{0}'
         Components(0)=CylinderComponent'CylinderComponent_{0}'
         Components(1)=()
         Components(2)=SpriteComponent'SpriteComponent_{0}'
         Location=(X={1[0]:.6f},Y={1[1]:.6f},Z={1[2]:.6f})
         Rotation=(Pitch={2[0]:.6f},Yaw={2[1]:.6f},Roll={2[2]:.6f})
         Tag="VehiclePickup_Boost_TA"
         Layer="Field, Boost"
         CollisionComponent=CylinderComponent'CylinderComponent_{0}'
         Name="VehiclePickup_Boost_TA_{0}"
         ObjectArchetype=VehiclePickup_Boost_TA'tagame.Default__VehiclePickup_Boost_TA'
      End Actor
   End Level
Begin Surface
End Surface
End Map"""