import bpy
import logging

# Function to toggle all shape keys
def toggle_shape_keys(**kwargs):
    # Initiate logging
    msgs = []
    
    # Get settings
    toggleindividual = kwargs.get('toggleindividual', True)
    
    # Check if there is an active object
    if not bpy.context.active_object:
        msgs.append("No active object")
        return msgs
    
    # Get active object:
    object = bpy.context.active_object
    
    # Check that object is a mesh
    if object.type != 'MESH':
        msgs.append("Active object must be a mesh")
        return msgs
    
    # Check that object has shape keys
    if object.data.shape_keys == False:
        msgs.append("Active object has no shape keys")
        return msgs
    
    #Toggle all key status
    if toggleindividual == True:
        for key in object.data.shape_keys.key_blocks:
            key.mute = not key.mute
    else:
        mutestatus = not object.data.shape_keys.key_blocks[0].mute
        for key in object.data.shape_keys.key_blocks:
            key.mute = mutestatus
    
    msgs.append("Toggled shape keys")
    return msgs


# Function to apply all armature modifers of all children objects of an armature, and re-add them (Optional)
def apply_armature_modifiers(**kwargs):
    # Initiate logging
    msgs = []
    
    # Settings
    copymodifier = kwargs.get('restoremodifier', True)
    applyrestpose = kwargs.get('applyrestpose', False)
    
    # Check if there is an active object
    if not bpy.context.active_object:
        msgs.append("No active object")
        return msgs
    
    # Check if the active object is a valid armature
    if bpy.context.active_object.type != 'ARMATURE':
        # Object is not an armature. Cancelling.
        msgs.append(f"No armature selected.")
        return msgs

    # Get the armature
    armature = bpy.context.object
    logging.info(f"armature: {armature.name}")
    
    # Store current mode
    original_mode = bpy.context.mode
    # For some reason it doesn't recognize edit_armature as a valid mode to switch to so we change it to just edit. Blender moment
    if original_mode == 'EDIT_ARMATURE':
        original_mode = 'EDIT'
    
    #Start
    logging.info(f"applying armature modifiers of children objects")
    armaturechildren = []
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create list of armature children
    for ob in bpy.context.view_layer.objects: 
        if ob.parent == armature and ob.type == 'MESH' and ob.modifiers:
            if ob.data.shape_keys:
                msgs.append(f"Warning: {ob.name} has shape keys")
                return msgs
            armaturechildren.append(ob)
    
    for ob in armaturechildren:
        bpy.context.view_layer.objects.active = ob
        # Check if they are parented to the armature, are a mesh, and have modifiers
        modifier_list = []
        #Create a list of current armature modifiers in the object
        for modifier in ob.modifiers:
            if modifier.type == 'ARMATURE':
                modifier_list.append(modifier)
        for modifier in modifier_list:
            # Apply the armature modifier
            if copymodifier == True:
                bpy.ops.object.modifier_copy(modifier=modifier.name)
            bpy.ops.object.modifier_apply(modifier=modifier.name)
    

    bpy.context.view_layer.objects.active = armature
    
    if applyrestpose == True:
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply()
    
    bpy.ops.object.mode_set(mode=original_mode)
    msgs.append(f"Finished applying armature modifiers")
    return msgs