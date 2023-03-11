# My Custom Blender Addons
Various blender addons for extra functionality by Ref

Following add-ons are replacing a set of commands with a single one. Normally to change object origin, you have to go to edit mode, select a vertex, change 3d cursor to there, then go back to object mode, then set origin to cursor, and reset cursor back to center position. following add-ons make it one click.

Set Origin to Active Face and Move to Center:
---
This add-on is executed from in right click menu in edit mode. 
When you select a face/edge/vertex and execute this script, it will change your object origin to the center of selected active face.
This is only works for last selected (active) item.  at the end the mode will changed to Object Mode. This is by design as you generally move on to other tasks.

Set Origin to Selected
---
This uses different method to get vertex data, thus it doesn't care last selected item in the mesh. It will consider every vertex selected and set the object origin to center of these vertices. You can select groups of vertices, edges or faces. At the end, mode will stay in Edit mode.
