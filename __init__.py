bl_info = {
	"name": "Import Sidewinder V Models format",
	"description": "Import Sidewinder V Model",
	"author": "GreenTrafficLight",
	"version": (1, 0),
	"blender": (2, 92, 0),
	"location": "File > Import > Sidewinder V Importer",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"support": "COMMUNITY",
	"category": "Import-Export"}

import bpy

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator

class ImportSidewinderV(Operator, ImportHelper):
    """Load a Sidewinder V model file"""
    bl_idname = "import_scene.sidewinderv_data"
    bl_label = "Import Sidewinder V Data"

    filename_ext = ""
    filter_glob: StringProperty(default="*", options={'HIDDEN'}, maxlen=255,)

    # Selected files
    files: CollectionProperty(type=bpy.types.PropertyGroup)

    clear_scene: BoolProperty(
        name="Clear scene",
        description="Clear everything from the scene",
        default=False,
    )

    def execute(self, context):
        from . import  import_sidewinderv
        import_sidewinderv.main(self.filepath, self.files, self.clear_scene)
        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(ImportSidewinderV.bl_idname, text="Sidewinder V")


def register():
    bpy.utils.register_class(ImportSidewinderV)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportSidewinderV)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()