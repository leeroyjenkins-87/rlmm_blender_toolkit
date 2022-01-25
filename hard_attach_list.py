import bpy

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       CollectionProperty,
                       PointerProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)

# -------------------------------------------------------------------
#   Operators
# -------------------------------------------------------------------

class hardAttachUpDown(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "custom.hard_attach_up_down"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}
    
    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.hard_index

        try:
            item = scn.hard_collection[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.hard_collection) - 1:
                item_next = scn.hard_collection[idx+1].name
                scn.hard_collection.move(idx, idx+1)
                scn.hard_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.hard_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.hard_collection[idx-1].name
                scn.hard_collection.move(idx, idx-1)
                scn.hard_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.hard_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scn.hard_collection[idx].name)
                scn.hard_index -= 1
                scn.hard_collection.remove(idx)
                self.report({'INFO'}, info)
                
        if self.action == 'ADD':
            if context.object:
                item = scn.hard_collection.add()
                item.name = context.object.name
                item.obj = context.object
                scn.hard_index = len(scn.hard_collection)-1
                info = '"%s" added to list' % (item.name)
                self.report({'INFO'}, info)
            else:
                self.report({'INFO'}, "Nothing selected in the Viewport")
        return {"FINISHED"}
    
    
class removeDuplicates(Operator):
    """Remove all duplicates"""
    bl_idname = "custom.remove_duplicates"
    bl_label = "Remove Duplicates"
    bl_description = "Remove all duplicates"
    bl_options = {'INTERNAL'}

    def find_duplicates(self, context):
        """find all duplicates by name"""
        name_lookup = {}
        for c, i in enumerate(context.scene.hard_collection):
            name_lookup.setdefault(i.obj.name, []).append(c)
        duplicates = set()
        for name, indices in name_lookup.items():
            for i in indices[1:]:
                duplicates.add(i)
        return sorted(list(duplicates))
        
    @classmethod
    def poll(cls, context):
        return bool(context.scene.hard_collection)
        
    def execute(self, context):
        scn = context.scene
        removed_items = []
        # Reverse the list before removing the items
        for i in self.find_duplicates(context)[::-1]:
            scn.hard_collection.remove(i)
            removed_items.append(i)
        if removed_items:
            scn.hard_index = len(scn.hard_collection)-1
            info = ', '.join(map(str, removed_items))
            self.report({'INFO'}, "Removed indices: %s" % (info))
        else:
            self.report({'INFO'}, "No duplicates")
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)