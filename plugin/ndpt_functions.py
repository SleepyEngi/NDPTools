import bpy

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