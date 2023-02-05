## Move an object to the center of scene by selected face's center
## Generally used for objects to stand on a flat surface on game design
## by Arda Erdikmen https://github.com/ref-xx

bl_info = {
    "name": "Origin to Face and Move",
    "description": "Move origin to active face and move object to scene center",
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
from bpy.types import Operator
from bpy_extras.object_utils import world_to_camera_view

class MoveCursorToFaceCenterOperator(Operator):
    bl_idname = "object.move_cursor_to_face_center"
    bl_label = "Set Origin and Move to Center"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.object
        
        # Make sure the object is in Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)
        active_face = bm.faces.active
        center=None
        if active_face and bpy.context.tool_settings.mesh_select_mode[2] == True:
            center = active_face.calc_center_median()
        
        if center==None:    
            # blender doesn't have bm.edges.active?!?!!!?
            active_edge = [v for v in bm.edges if v.select]
            if len(active_edge) > 0:
                edge = active_edge[-1]        
                if edge and bpy.context.tool_settings.mesh_select_mode[1] == True:
                    start_vert = edge.verts[0]
                    end_vert = edge.verts[1]
                    center = (start_vert.co + end_vert.co) / 2

        if center==None:    
            active_vert = [v for v in bm.verts if v.select]
            if len(active_vert) > 0:
                active_vert = active_vert[-1]             
                if active_vert and bpy.context.tool_settings.mesh_select_mode[0] == True:
                    center = active_vert.co

        if center==None:    
            self.report({'INFO'},"Cannot set origin. Please select a face/edge/vertex first.")
            return {'FINISHED'}

                
        bpy.context.scene.cursor.location = obj.matrix_world @ center
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
        obj.location = bpy.context.scene.cursor.location
        return {'FINISHED'}
    



def menu_func(self, context):
    self.layout.operator(MoveCursorToFaceCenterOperator.bl_idname)

def register():
    bpy.utils.register_class(MoveCursorToFaceCenterOperator)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    bpy.utils.unregister_class(MoveCursorToFaceCenterOperator)

if __name__ == "__main__":
    register()
