


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