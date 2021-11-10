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


import os
import sys
import subprocess
from collections import namedtuple


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


if "bpy" in locals():
    import importlib
    importlib.reload(make_instances_real)
    importlib.reload(send_to_t3d)
    importlib.reload(send_to_udk)
    importlib.reload(set_parent)
    importlib.reload(set_rotation)


else:
    from . import make_instances_real
    from . import send_to_t3d
    from . import send_to_udk
    from . import set_parent
    from . import set_rotation


import bpy
from bpy.types import (
        Menu,
        AddonPreferences,
        )
from bpy.props import (
        StringProperty,
        BoolProperty,
        )



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


class RLMM_PT_warning_panel(bpy.types.Panel):
    bl_label = "Example Warning"
    bl_category = "Example Tab"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return not dependencies_installed

    def draw(self, context):
        layout = self.layout

        lines = [f"Please install the missing dependencies for the \"{bl_info.get('name')}\" add-on.",
                 f"1. Open the preferences (Edit > Preferences > Add-ons).",
                 f"2. Search for the \"{bl_info.get('name')}\" add-on.",
                 f"3. Open the details section of the add-on.",
                 f"4. Click on the \"{EXAMPLE_OT_install_dependencies.bl_label}\" button.",
                 f"   This will download and install the missing Python packages, if Blender has the required",
                 f"   permissions.",
                 f"If you're attempting to run the add-on from the text editor, you won't see the options described",
                 f"above. Please install the add-on properly through the preferences.",
                 f"1. Open the add-on preferences (Edit > Preferences > Add-ons).",
                 f"2. Press the \"Install\" button.",
                 f"3. Search for the add-on file.",
                 f"4. Confirm the selection by pressing the \"Install Add-on\" button in the file browser."]

        for line in lines:
            layout.label(text=line)


class RLMM_OT_install_dependencies(bpy.types.Operator):
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

        # Register the panels, operators, etc. since dependencies are installed
        for cls in classes:
            bpy.utils.register_class(cls)

        return {"FINISHED"}


class RLMM_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator(RLMM_OT_install_dependencies.bl_idname, icon="CONSOLE")


class RLMMPJ_PT_Panel(bpy.types.Panel):
    bl_idname = "RLMMPJ_PT_Panel"
    bl_label = "Project Name"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'

#create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):
        
        layout = self.layout

        boxLayout1 = layout.box()
        boxLayout1.label(text="Project Name",icon='DESKTOP')
        
        row1 = boxLayout1.row()
        row1.prop(context.scene, 'projectName')


class RLMM_PT_Panel(bpy.types.Panel):
    bl_idname = "RLMM_PT_Panel"
    bl_label = "Objects: Location/Rotation"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'

#create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):
        
        layout = self.layout

        boxLayout1 = layout.row().box()
        # ICON OBJECT_DATA IS THE SQUARE INSIDE THE SELECT BOX
        boxLayout1.label(text="Select Array Objects",icon='EYEDROPPER')   
        boxLayout1.prop_search(context.scene, "prefabOBJ", context.scene, "objects")
        boxLayout1.prop_search(context.scene, "prefabPLANE", context.scene, "objects")
        
        boxLayout2 = layout.row().box()  
        boxLayout2.label(text="Object Instances",icon='LINKED')
        boxlayout7 = boxLayout2.box()
        boxlayout7.prop(context.scene, "scaleFACES")
        boxlayout7.operator('custom.set_parent', text="Set Parent/Scale")
        boxlayout7.operator('custom.make_instances_real', text="Make Instances Real")
        
        boxLayout3 = layout.box()
        boxLayout3.label(text="Set Rotation",icon='ORIENTATION_LOCAL')
        boxlayout8 = boxLayout3.box()
        boxlayout8.prop(context.scene, "collectRotations")
        
        subrow = boxlayout8.row(align=True)
        subrow.operator('custom.set_neg_x', text="-X")
        subrow.operator('custom.set_pos_x', text="+X")
        subrow.operator('custom.set_neg_y', text="-Y")
        subrow.operator('custom.set_pos_y', text="+Y")
        subrow.operator('custom.set_neg_z', text="-Z")
        subrow.operator('custom.set_pos_z', text="+Z")
        
        boxLayout4 = layout.box()
        boxLayout4.label(text="Export Data",icon='EXPORT')
        boxlayout5 = boxLayout4.box()
        boxlayout5.prop(context.scene, "collectData")
        boxlayout5.prop(context.scene, "collectMaterials")
        boxlayout5.prop(context.scene, "physMat")
        
        row3 = boxlayout5.row()
        row3.prop(context.scene, 'conf_path')
        row2 = boxlayout5.row()
        row2.operator('custom.send_to_udk', text="Send to UDK")
        
class RLMMBrushes_PT_Panel(bpy.types.Panel):
    bl_idname = "RLMMBrushes_PT_Panel"
    bl_label = "Brushes"
    bl_category = "RLMM Toolkit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = 'objectmode'

#create a panel (class) by deriving from the bpy Panel, this be the UI
    def draw(self, context):
        
        layout = self.layout

        boxLayout9 = layout.box()
        boxLayout9.label(text="T3D File",icon='CUBE')
        boxLayout9.operator('custom.send_to_t3d', text="Create Custom Brush")


preference_classes = (RLMM_PT_warning_panel,
                      RLMM_OT_install_dependencies,
                      RLMM_preferences)

classes = (setPosZ,
           setNegZ,
           setPosY,
           setNegY,
           setPosX,
           setNegX,
           sendToUDK,
           sendToT3d,
           RLMMPJ_PT_Panel,
           RLMM_PT_Panel,
           RLMMBrushes_PT_Panel,
           setParent,
           makeInstancesReal)

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

    #register the classes with the correct function
    bpy.types.Scene.collectionHolder = bpy.props.StringProperty(name="", default = "", description = "")
    bpy.types.Scene.projectName = bpy.props.StringProperty(name="", default = "", description = "Define export directory for CSV file", subtype='FILE_PATH')
    bpy.types.Scene.prefabOBJ = bpy.props.PointerProperty(name="Object", type=bpy.types.Object)
    bpy.types.Scene.prefabPLANE = bpy.props.PointerProperty(name="Plane", type=bpy.types.Object)
    bpy.types.Scene.scaleFACES = bpy.props.BoolProperty(name="Scale Prefab To Plane")
    bpy.types.Scene.collectRotations = bpy.props.BoolProperty(name="Auto Collect Objects", default=True)
    bpy.types.Scene.collectData = bpy.props.BoolProperty(name="Auto Collect Objects", default=True)
    bpy.types.Scene.collectMaterials = bpy.props.BoolProperty(name="Collect Materials", default=True)
    bpy.types.Scene.collectT3d = bpy.props.BoolProperty(name="Auto Collect Objects", default=True)
    bpy.types.Scene.physMat = bpy.props.BoolProperty(name="Apply StickyWalls", default=True)
    bpy.types.Scene.conf_path = bpy.props.StringProperty(name="CSV", default = "", description = "Define export directory for CSV file", subtype='FILE_PATH')

    for cls in classes:
        bpy.utils.register_class(cls)


#same as register but backwards, deleting references
def unregister():
    for cls in preference_classes:
        bpy.utils.unregister_class(cls)

    #now we can continue to unregister classes normally
    if dependencies_installed:
        for cls in classes:
            bpy.utils.unregister_class(cls)

#NOTE: during testing if this addon was installed from a file then that current version
#of that file will be copied over to the blender addons directory
#if you want to see what changes occour you HAVE TO REINSTALL from the new file for it to register

#a quick line to autorun the script from the text editor when we hit 'run script'
if __name__ == '__main__':
    register()