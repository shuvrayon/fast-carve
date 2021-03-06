import bpy
from bpy.props import *

def select_active(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select = True
    bpy.context.scene.objects.active = obj
    
def is_apply_immediate():
    return (bpy.context.scene.apply_bool == True)

def bool_mod_and_apply(obj, bool_method):
    
    active_obj = bpy.context.scene.objects.active
    
    bool_mod = active_obj.modifiers.new(type="BOOLEAN", name="FC_BOOL")
    
    method = 'DIFFERENCE'
    
    if bool_method == 1:
        method = 'UNION'
    elif bool_method == 2:
        method = 'INTERSECT'
    
    bool_mod.operation = method
    #bool_mod.solver = 'CARVE'
    bool_mod.object = obj
    
    if is_apply_immediate() == True:
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    else:  
        if bool_method == 0 or bool_method == 2:
            obj.draw_type = 'WIRE'


def execute_slice_op(context, target_obj):
     
    # store active object
    current_obj = context.object
    bpy.ops.object.transform_apply(scale=True)
    
    # clone target
    clone_target = target_obj.copy()
    context.scene.objects.link(clone_target)
    
    # Intersect for clone
    select_active(clone_target)            
    bpy.ops.object.make_single_user(object=True, obdata=True)
    
    bool_mod_and_apply(current_obj, 2)
        
    # Difference for target
    select_active(target_obj)
    bpy.ops.object.make_single_user(object=False, obdata=True)
            
    bool_mod_and_apply(current_obj, 0)
        
    select_active(current_obj)
    
    
def execute_boolean_op(context, target_obj, bool_method = 0):
    
    '''
    function for bool operation
    @target_obj : target object of the bool operation
    @bool_method : 0 = difference, 1 = union, 2 = intersect  
    '''

    # store active object
    current_obj = context.object
    bpy.ops.object.transform_apply(scale=True)
    
    # make target the active object
    select_active(target_obj)
        
    bool_mod_and_apply(current_obj, bool_method)

    select_active(current_obj)
