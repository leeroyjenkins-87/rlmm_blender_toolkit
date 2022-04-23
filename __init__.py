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

# Dependency code borrowed from https://github.com/robertguetzkow/blender-python-examples/tree/master/add_ons/install_dependencies
bl_info = {
    "name": "RLMM Toolkit",
    "author": "LeeroyJenkins0G",
    "version": (1, 1, 0),   # addon plugin version
    "blender": (2, 80, 0),  # minimum blender version
    "location": "View3D > Sidebar > Gen Tab",
    "description": "RLMM Toolkit: Blender to UDK",
    "warning": "Requires pyperclip package, see below",
    "wiki_url": "https://rocketleaguemapmaking.com",
    "support": "COMMUNITY",
    "category": "View 3D",
}

import bpy
import importlib
import os
import sys
import subprocess
from collections import namedtuple

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       CollectionProperty,
                       PointerProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList,
                       Object,
                       AddonPreferences,
                       Scene)

Dependency = namedtuple("Dependency", ["module", "package", "name"])

# Declare all modules that this add-on depends on, that may need to be installed. The package and (global) name can be
# set to None, if they are equal to the module name. See import_module and ensure_and_import_module for the explanation
# of the arguments. DO NOT use this to import other parts of your Python add-on, import them as usual with an
# "import" statement.
dependencies = (Dependency(module="pyperclip", package=None, name=None),)

dependencies_installed = False


def import_module(module_name, global_name=None, reload=True):
    """
    Import a module.
    :param module_name: Module to import.
    :param global_name: (Optional) Name under which the module is imported. If None the module_name will be used.
       This allows to import under a different name with the same effect as e.g. "import numpy as np" where "np" is
       the global_name under which the module can be accessed.
    :raises: ImportError and ModuleNotFoundError
    """
    if global_name is None:
        global_name = module_name

    if global_name in globals():
        importlib.reload(globals()[global_name])
    else:
        # Attempt to import the module and assign it to globals dictionary. This allow to access the module under
        # the given name, just like the regular import would.
        globals()[global_name] = importlib.import_module(module_name)


def install_pip():
    """
    Installs pip if not already present. Please note that ensurepip.bootstrap() also calls pip, which adds the
    environment variable PIP_REQ_TRACKER. After ensurepip.bootstrap() finishes execution, the directory doesn't exist
    anymore. However, when subprocess is used to call pip, in order to install a package, the environment variables
    still contain PIP_REQ_TRACKER with the now nonexistent path. This is a problem since pip checks if PIP_REQ_TRACKER
    is set and if it is, attempts to use it as temp directory. This would result in an error because the
    directory can't be found. Therefore, PIP_REQ_TRACKER needs to be removed from environment variables.
    :return:
    """

    try:
        # Check if pip is already installed
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
    except subprocess.CalledProcessError:
        import ensurepip

        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)


def install_and_import_module(module_name, package_name=None, global_name=None):
    """
    Installs the package through pip and attempts to import the installed module.
    :param module_name: Module to import.
    :param package_name: (Optional) Name of the package that needs to be installed. If None it is assumed to be equal
       to the module_name.
    :param global_name: (Optional) Name under which the module is imported. If None the module_name will be used.
       This allows to import under a different name with the same effect as e.g. "import numpy as np" where "np" is
       the global_name under which the module can be accessed.
    :raises: subprocess.CalledProcessError and ImportError
    """
    if package_name is None:
        package_name = module_name

    if global_name is None:
        global_name = module_name

    # Blender disables the loading of user site-packages by default. However, pip will still check them to determine
    # if a dependency is already installed. This can cause problems if the packages is installed in the user
    # site-packages and pip deems the requirement satisfied, but Blender cannot import the package from the user
    # site-packages. Hence, the environment variable PYTHONNOUSERSITE is set to disallow pip from checking the user
    # site-packages. If the package is not already installed for Blender's Python interpreter, it will then try to.
    # The paths used by pip can be checked with `subprocess.run([bpy.app.binary_path_python, "-m", "site"], check=True)`

    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True, env=environ_copy)

    # The installation succeeded, attempt to import the module again
    import_module(module_name, global_name)


class RLMM_PT_warning_panel(Panel):
    bl_name = "rlmm.warning_panel"
    bl_label = "Install Dependencies"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return not dependencies_installed

    def draw(self, context):
        layout = self.layout
        boxLayout = layout.box()

        lines = ['Please install the missing module',
                 'for the "RLMM Toolkit".',
                 '1. Open the preferences',
                 '   (Edit > Preferences > Add-ons).',
                 '2. Search for the "RLMM Toolkit".',
                 '3. Open the details section of the',
                 '   add-on.',
                 '4. Click on the "Install',
                 '   Dependencies" button. This will',
                 '   download and install the',
                 '   missing Python packages, if',
                 '   Blender hasthe required',
                 '   permissions.']
                 
        for line in lines:
            boxLayout.label(text=line)


class RLMM_OT_install_dependencies(Operator):
    bl_idname = "rlmm.install_dependencies"
    bl_label = "Install dependencies"
    bl_description = ("Downloads and installs the required python packages for this add-on. "
                      "Internet connection is required. Blender may have to be started with "
                      "elevated permissions in order to install the package")
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return not dependencies_installed

    def execute(self, context):
        try:
            install_pip()
            for dependency in dependencies:
                install_and_import_module(module_name=dependency.module,
                                          package_name=dependency.package,
                                          global_name=dependency.name)
        except (subprocess.CalledProcessError, ImportError) as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        global dependencies_installed
        dependencies_installed = True
        
        finishRegister()

        return {"FINISHED"}


class RLMM_preferences(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator(RLMM_OT_install_dependencies.bl_idname, icon="CONSOLE")


preference_classes = [RLMM_PT_warning_panel,
                      RLMM_OT_install_dependencies,
                      RLMM_preferences]
                      
class objectCollection(PropertyGroup):
    #name: StringProperty() -> Instantiated by default
    obj: PointerProperty(
        name="Object",
        type=bpy.types.Object)
        
class Hard_Attach_UL_Items(UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        obj = item.obj
        split = layout.split(factor=0.155)
        split.label(text="[%d]:" % (index))
        split.prop(obj, "name", text="", emboss=False, translate=False)
            
    def invoke(self, context, event):
        pass

def finishRegister():

    if dependencies_installed == True:
    
        from . import cust_obj_vars, def_obj_vars, def_obj_loop, make_instances_real, send_to_t3d, send_to_udk, set_parent, set_rotation, ui, hard_attach_list
        
        modules = [send_to_udk,
                   send_to_t3d,
                   def_obj_loop,
                   ui,
                   set_parent,
                   make_instances_real,
                   set_rotation,
                   hard_attach_list]
                   
        for module in modules:
            importlib.reload(module)
                   
        classes = [send_to_udk.sendToUDK,
                   send_to_t3d.sendToT3d,
                   send_to_udk.NumberStorageItem,
                   def_obj_loop.defaultObjects,
                   ui.RLMMPJ_PT_Panel,
                   ui.RLMM_Parent_PT_Panel,
                   ui.RLMM_Attach_PT_Panel,
                   ui.RLMM_Rotate_PT_Panel,
                   ui.RLMM_PT_Panel,
                   ui.RLMMBRUSHES_PT_Panel,
                   ui.UDKDEFAULT_PT_Panel,
                   ui.errorMessage,
                   set_parent.setParent,
                   make_instances_real.makeInstancesReal,
                   set_rotation.errorCheckRotation,
                   set_rotation.setNegX,
                   set_rotation.setPosX,
                   set_rotation.setNegY,
                   set_rotation.setPosY,
                   set_rotation.setNegZ,
                   set_rotation.setPosZ,
                   hard_attach_list.hardAttachUpDown,
                   hard_attach_list.removeDuplicates,
                   Hard_Attach_UL_Items,
                   objectCollection]
        
        for cls in classes:
            bpy.utils.register_class(cls)

        # REGISTER THE GLOBAL STRING VARIABLES FOR THE ADDON
        Scene.collectionHolder = StringProperty(name="", default = "", description = "") # CONTAINER FOR TEMPORARILY STORING OBJECTS IN A COLLECTION
        Scene.projectName = StringProperty(name="UDK", default = "", description = "Select the UDK file you're currently working on.", subtype='FILE_PATH') # NAME OF UDK FILE
        Scene.textT3d = StringProperty(name="", default = "", description = "") # CONTAINER FOR STORING T3D STRING
        Scene.conf_path = StringProperty(name="CSV", default = "", description = "Define export directory for CSV file", subtype='FILE_PATH') # SELECTED PATH TO PLACE EXPORTED UDK AND T3D DATA
        Scene.axis = StringProperty(name="", default = "", description = "") # STRING PROPERTY FOR SETTING ROTATIONS
        Scene.tempName = StringProperty(name="", default = "", description = "") #tempName for Hard Attaches
        
        # REGISTER THE GLOBAL POINTER VARIABLES FOR THE ADDON
        Scene.prefabOBJ = PointerProperty(name="Object", type=Object) # SELECTOR FOR OBJ YOU WANT TO MANIPULATE
        Scene.prefabPLANE = PointerProperty(name="Plane", type=Object) # SELECTOR FOR THE PARENT OF THAT OBJ
        
        # REGISTER THE GLOBAL BOOLEAN VARIABLES FOR THE ADDON
        Scene.scaleFACES = BoolProperty(name="Scale Prefab To Plane") # UI BOOLEAN FOR SCALING THE OBJ TO PARENT
        Scene.collectRotations = BoolProperty(name="Auto Collect Objects", default=False)
        Scene.collectData = BoolProperty(name="Auto Collect Objects", default=False) # UI BOOLEAN TO COLLECT THE OBJECTS INSIDE THE ADDON CREATED COLLECTION
        Scene.collectMaterials = BoolProperty(name="Collect Materials", default=True) # UI BOOLEAN TO COLLECT THE MATERIALS ON THE OBJ
        #Scene.collectT3d = BoolProperty(name="Auto Collect Objects", default=True) # UI BOOLEAN TO COLLECT THE OBJECTS INSIDE THE ADDON CREATED COLLECTION
        Scene.physMat = BoolProperty(name="Apply StickyWalls", default=True) # UI BOOLEAN TO APPLY PHYS MATERIAL TO EXPORTED OBJ
        Scene.defPillar = BoolProperty(name="Default Pillar", default=True) # UI BOOLEAN TO MAKE PILLAR
        Scene.defGoals = BoolProperty(name="Default Goals", default=True) # UI BOOLEAN TO MAKE GOALS
        Scene.defSpawns = BoolProperty(name="Default Spawns", default=True) # UI BOOLEAN TO MAKE SPAWNS
        Scene.defBoost = BoolProperty(name="Default Boost", default=True) # UI BOOLEAN TO MAKE BOOST
        Scene.xBool = BoolProperty(name="") # BOOLEAN PROPERTY FOR SETTING ROTATIONS
        Scene.yBool = BoolProperty(name="") # BOOLEAN PROPERTY FOR SETTING ROTATIONS
        Scene.zBool = BoolProperty(name="") # BOOLEAN PROPERTY FOR SETTING ROTATIONS
        Scene.isArchetype = BoolProperty(name="Is Archetype") # BOOLEAN PROPERTY FOR SETTING ROTATIONS
        Scene.customBoostMesh = BoolProperty(name="Custom Mesh")
        Scene.customBoostParticles = BoolProperty(name="Custom Particle")
        Scene.isT3dFromSend2UDK = BoolProperty(name="isT3dFromSend2UDK")
        Scene.ishardAttach = BoolProperty(name="Hard Attach")
        
        # REGISTER THE GLOBAL INTEGAR VARIABLES FOR THE ADDON
        Scene.numberSequencer = IntProperty(name="", default=0, min=0, max=1000000000) # INT PROPERTIED FOR HOLDING NUMERIC VALUE OF CREATED OBJECTS
        Scene.numberStorage = CollectionProperty(type=send_to_udk.NumberStorageItem)
        Scene.value = IntProperty(name="", default=0, min=-90, max=90) # INT PROPERTY FOR SETTING ROTATIONS
        Scene.errorCode = IntProperty(name="ErrorCode", default=0, min=0, max=90)
        bpy.types.Scene.hard_index = IntProperty()
        
        # REGISTER THE COLLECTIONS FOR THE ADDON
        bpy.types.Scene.hard_collection = CollectionProperty(type=objectCollection)


    return
    
#this function is called on plugin loading(installing), adding class definitions into blender
#to be used, drawed and called
def register():
    global dependencies_installed
    dependencies_installed = False
    
    for cls in preference_classes:
        bpy.utils.register_class(cls)

    try:
        for dependency in dependencies:
            import_module(module_name=dependency.module, global_name=dependency.name)
        dependencies_installed = True
    except ModuleNotFoundError:
    # Don't register other panels, operators etc.
        return
    
    finishRegister()

#same as register but backwards, deleting references
def unregister():
    for cls in preference_classes:
        bpy.utils.unregister_class(cls)

    #now we can continue to unregister classes normally
    if dependencies_installed:
    
        classes = [send_to_udk.sendToUDK,
                   send_to_t3d.sendToT3d,
                   def_obj_loop.defaultObjects,
                   ui.RLMMPJ_PT_Panel,
                   ui.RLMM_Parent_PT_Panel,
                   ui.RLMM_Attach_PT_Panel,
                   ui.RLMM_Rotate_PT_Panel,
                   ui.RLMM_PT_Panel,
                   ui.RLMMBRUSHES_PT_Panel,
                   ui.UDKDEFAULT_PT_Panel,
                   ui.errorMessage,
                   set_parent.setParent,
                   make_instances_real.makeInstancesReal,
                   set_rotation.errorCheckRotation,
                   set_rotation.setNegX,
                   set_rotation.setPosX,
                   set_rotation.setNegY,
                   set_rotation.setPosY,
                   set_rotation.setNegZ,
                   set_rotation.setPosZ,
                   hard_attach_list.hardAttachUpDown,
                   hard_attach_list.removeDuplicates,
                   Hard_Attach_UL_Items,
                   objectCollection]
                   
        for cls in classes:
            bpy.utils.unregister_class(cls)

#NOTE: during testing if this addon was installed from a file then that current version
#of that file will be copied over to the blender addons directory
#if you want to see what changes occour you HAVE TO REINSTALL from the new file for it to register

#a quick line to autorun the script from the text editor when we hit 'run script'
# if __name__ == '__main__':
    # register()