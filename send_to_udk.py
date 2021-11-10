


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