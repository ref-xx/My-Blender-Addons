## Move an object to the center of scene by selected face's center
## Generally used for objects to stand on a flat surface on game design
## by Arda Erdikmen https://github.com/ref-xx

bl_info = {
    "name": "Origin to Here",
    "description": "Set origin to center of selected vertices",
    "author": "Arda Erdikmen",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > Edit Mode > Right-click menu",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url": "https://github.com/ref-xx",
    "tracker_url": "https://github.com/ref-xx",
    "support": "COMMUNITY",
    "category": "Mesh",
}


import bpy
import bmesh
import mathutils
from bpy.types import Operator
from bpy_extras.object_utils import world_to_camera_view

class SetOriginToSelected(Operator):
    bl_idname = "object.set_origin_to_selected"
    bl_label = "Set Origin to Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.object
        
        if obj.mode == 'EDIT':    
            obj = bpy.context.object
            bm = bmesh.from_edit_mesh(obj.data)

            selected_verts = [v for v in bm.verts if v.select]
            center=None
            if selected_verts:
                center =  mathutils.Vector((0.0, 0.0, 0.0))
                for v in selected_verts:
                    center += v.co
                center /= len(selected_verts)
                
            if center!= None:

                backup=bpy.context.scene.cursor.location
                   
                bpy.context.scene.cursor.location = obj.matrix_world @ center
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                bpy.context.scene.cursor.rotation_euler = (0,0,0)
                
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.context.scene.cursor.location= backup
                bpy.context.view_layer.update()

            else:
                 self.report({'INFO'},"Cannot set origin. Please select a vertex first.")
               
            return {'FINISHED'}
        

def menu_func(self, context):
    self.layout.operator(SetOriginToSelected.bl_idname)

def register():
    bpy.utils.register_class(SetOriginToSelected)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    bpy.utils.unregister_class(SetOriginToSelected)

if __name__ == "__main__":
    register()


#bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
#obj.location = bpy.context.scene.cursor.location
#bpy.ops.view3d.snap_cursor_to_center()