import bpy
import bmesh
import pyperclip


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
            
            stringList = [linkCount]
            
            originShort = objectString.data.vertices[f.vertices[0]].co
            
            originList = [originShort.x, originShort.y, originShort.z]
            
            stringList.extend(self.stringFormatter(originList, 100))
            
            polyList = [f.normal.x, f.normal.y, f.normal.z]
            
            stringList.extend(self.stringFormatter(polyList, 1))
            
            if f.normal.x != 0:
                stringList.extend(['+00000.000000','+00001.000000','+00000.000000','+00000.000000','+00000.000000','+00001.000000'])
            elif f.normal.y !=0:
                stringList.extend(['+00001.000000','+00000.000000','+00000.000000','+00000.000000','+00000.000000','+00001.000000'])
            else:
                stringList.extend(['+00001.000000','+00000.000000','+00000.000000','+00000.000000','+00001.000000','+00000.000000'])
            
            for idx in f.vertices:

                idxList = [objectString.data.vertices[idx].co.x, objectString.data.vertices[idx].co.y, objectString.data.vertices[idx].co.z]

                stringList.extend(self.stringFormatter(idxList, 100))

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
    End Polygon""".format(*stringList)

        bpy.context.scene.textT3d += '\nEnd PolyList'
        print(bpy.context.scene.textT3d)
        fileName = '{}{}'.format(objectStringName, '.t3d')
        outputT3d = '{}{}'.format(bpy.path.abspath(bpy.context.scene.conf_path), fileName)
       
        f = open( outputT3d, 'w' )
        f.writelines( bpy.context.scene.textT3d.rstrip() )
        f.close()   
        pyperclip.copy(bpy.context.scene.textT3d.rstrip())
        
        return {'FINISHED'}
    
    def stringFormatter(self, inVar, multiple):
        
        outVar = []
        
        for var in inVar:
            
            if ('-' in str(var)):
                idxVar = str(round(var * multiple, 6)).lstrip('-').split('.')
                idxVarString = '-' + idxVar[0].zfill(5) + '.' + idxVar[1].ljust(6, '0')
            else:
                idxVar = str(round(var * multiple, 6)).split('.')
                idxVarString = '+' + idxVar[0].zfill(5) + '.' + idxVar[1].ljust(6, '0')

            outVar.append(idxVarString)
            
        return outVar
