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
    if not object.data.shape_keys:
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


# Function to rename data blocks to their objects name
def sync_data_block_names():
    # Initiate logging
    msgs = []
    
    # Get a list of all objects
    for obj in bpy.data.objects:
        # Rename the data to match the object name
        obj.data.name = obj.name
    
    # End
    msgs.append("Renamed data blocks")
    return msgs


# Function to remove duplicate node groups
def merge_duplicate_node_groups():
    # Initiate logging
    msgs = []
    
    return "WIP"


# Function to convert particle systems to a curve object with automatically set surface, uv map, and node group
def convert_particles_to_curves(**kwargs):
    # Initiate logging
    msgs = []
    
    # Get settings
    nodegroupname = kwargs.get('nodegroupname', "Hair Preset")
    attachmentuvmap = kwargs.get('attachmentuvmap', "UVMap")
    attachcurves =  kwargs.get('attachcurves', True)
    
    #--------------------------------------------------------------------------------------------
    
    # Store original mode
    originalmode = bpy.context.mode
    
    # Set mode to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Check that an active object is selected
    if not bpy.context.active_object:
        msgs.append("No active object")
        return msgs
    
    # Get selected object
    surface_object = bpy.context.active_object
    
    # Check that the object is a mesh
    if surface_object.type != 'MESH':
        msgs.append("Active object must be a mesh")
        return msgs
    
    # Check that the object has an UV map by that name
    if not surface_object.data.uv_layers.get(attachmentuvmap):
        msgs.append("Object has no UV map by specified name")
        return msgs
    
    # Check that the object has particle systems
    if not surface_object.particle_systems:
        msgs.append("Object has no particle systems")
        return msgs
    
    # Get active particle system
    particle_system = surface_object.particle_systems.active
    
    # Save particle system child type, we set it back at the end
    particle_system_childtype = particle_system.settings.child_type
    
    # Set active particle system child type to NONE
    particle_system.settings.child_type = 'NONE'
    
    # Get particle system modifier in case it has a different name
    for modifier in surface_object.modifiers:
        if modifier.type == "PARTICLE_SYSTEM":
            if modifier.particle_system == particle_system:
                particle_system_modifier = modifier
    
    
    # Force set particle system to visible
    particle_system_modifier.show_viewport = True
    
    #--------------------------------------------------------------------------------------------
    # Handle pre-existing object
    preexisting = False
    # Detect pre-exising curves object
    if bpy.data.objects.get(particle_system.name):
        preexisting = True
        haircurvesobjectold = bpy.data.objects.get(particle_system.name)
        
        # Rename old hair curves object
        haircurvesobjectold.name = particle_system.name + "_Old"
        
        # Get collections from old hair curves object
        haircollections = haircurvesobjectold.users_collection
        
        # Get hair preset name from old hair curves object
        nodegroupname = haircurvesobjectold.modifiers[0].node_group.name
    
    if preexisting == False:
        # Check that the default hair preset exists
        # Skip if string is empty
        if nodegroupname != "" and nodegroupname != "None" and nodegroupname != "none":
            if not bpy.data.node_groups.get(nodegroupname):
                msgs.append("Could not find node group")
                return msgs
    
    #--------------------------------------------------------------------------------------------
    # New hair curves object setup
    # Create new hair curves object
    bpy.ops.curves.convert_from_particle_system()
    
    # Get new hair curves object
    haircurvesobjectnew = bpy.data.objects.get(particle_system.name)
    
    # If it exists, clear collections and set them. Otherwise, just leave it as the active collection.
    if preexisting == True:
        # Remove from collections
        for collection in haircurvesobjectnew.users_collection:
            collection.objects.unlink(haircurvesobjectnew)
        
        # Set collection
        for collection in haircollections:
            collection.objects.link(haircurvesobjectnew)
    
    #--------------------------------------------------------------------------------------------
    # Set new hair curves object data
    
    # Set new hair curves object surface
    haircurvesobjectnew.data.surface = surface_object
    
    # Set new hair curves object UV map
    haircurvesobjectnew.data.surface_uv_map = attachmentuvmap
    
    #--------------------------------------------------------------------------------------------
    # Attach hair curves to surface
    # We attach the curves to the surface in sculpt mode so that 
    if attachcurves == True:
        bpy.ops.object.mode_set(mode='SCULPT_CURVES')
        bpy.ops.curves.snap_curves_to_surface(attach_mode='NEAREST')
        bpy.ops.curves.sculptmode_toggle()
    
    #--------------------------------------------------------------------------------------------
    # Apply visual profile to new hair curves object for easier viewing
    # Curves have a large radius by default so this is just for the viewport while the curves have their modifiers off.
    # Add profile modifier
    modifier_profile = haircurvesobjectnew.modifiers.new(name="Set Hair Curve Profile", type='NODES')
    modifier_profile.node_group = bpy.data.node_groups.get("Set Hair Curve Profile")
    modifier_profile["Input_3"] = 0.0005
    
    # Apply profile modifier
    bpy.ops.object.modifier_apply(modifier="Set Hair Curve Profile")
    
    #--------------------------------------------------------------------------------------------
    # Add hair curves geometry nodes preset
    if preexisting == False and (nodegroupname != "" and nodegroupname != "None" and nodegroupname != "none"):
        # Add new hair curves object geometry nodes preset
        modifier_nodes_new = haircurvesobjectnew.modifiers.new(name=nodegroupname, type='NODES')
        modifier_nodes_new.node_group = bpy.data.node_groups.get(nodegroupname)
    
    #--------------------------------------------------------------------------------------------
    # Get data to copy
    if preexisting == True:
        # Copy all modifiers from old curves object to new curves object
        for modifier in haircurvesobjectold.modifiers:
            # Create a new modifier in the new curves and copy the types
            new_modifier = haircurvesobjectnew.modifiers.new(name=modifier.name, type=modifier.type)
            # For now hair curves objects can only have geometry nodes modifiers so this is probably safe
            new_modifier.node_group = modifier.node_group
            # Copy all the inputs starting from the second one because the first is geometry and can't be copied
            for i in modifier.node_group.inputs[1::]:
                new_modifier[i.identifier] = modifier[i.identifier]
        
        # Copy all materials
        materialnum = 0
        for materialslot in haircurvesobjectold.material_slots:
            bpy.ops.object.material_slot_add()
            haircurvesobjectnew.data.materials[materialnum] = materialslot.material
            materialnum = materialnum + 1
        
        # Delete old hair curves object
        bpy.data.objects.remove(haircurvesobjectold)
        
    if preexisting == False:
        # Get particle settings material
        particle_system_material = surface_object.material_slots[surface_object.particle_systems.active.settings.material - 1].material
        
        # Add a slot
        bpy.ops.object.material_slot_add()
        
        # Set the material
        haircurvesobjectnew.data.materials[0] = particle_system_material
    
    #--------------------------------------------------------------------------------------------
    # Finalize & cleanup
    
    # Hide curves object modifiers for performance
    for modifier in bpy.context.object.modifiers:
        modifier.show_viewport = False
    
    # Set active object back to surface object
    bpy.context.view_layer.objects.active = surface_object
    
    # Set active particle system child type back to original
    particle_system.settings.child_type = particle_system_childtype
    
    # Set particle system to hidden
    particle_system_modifier.show_viewport = False
    
    # Set mode back to original mode
    bpy.ops.object.mode_set(mode=originalmode)
    
    logging.info("finished conversion")
    msgs.append("Converted particle system to curves")
    return msgs


# Function to convert curves back to a particle system and automatically make one if there  isn't one
def convert_curves_to_particles():
    # Initiate logging
    msgs = []
    
    return "WIP"


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


# Function to convert scale transforms into location transforms
def convert_scale_to_loc():
    """Automatically convert scaled bones into equivalent visual location transforms"""
    # Initiate logging
    msgs = []
    logging.info(f"converting scale transforms to visual location")
    
    # Check if there is an active object
    if not bpy.context.active_object:
        msgs.append("No active object")
        return msgs
    
    # Check if the active object is a valid armature
    if bpy.context.active_object.type != 'ARMATURE':
        # Object is not an armature. Cancelling.
        msgs.append(f"No armature selected.")
        return msgs
    
    # Store current mode
    original_mode = bpy.context.mode
    # For some reason it doesn't recognize edit_armature as a valid mode to switch to so we change it to just edit. Blender moment
    if original_mode == 'EDIT_ARMATURE':
        original_mode = 'EDIT'
    #Set to pose mode
    bpy.ops.object.mode_set(mode='POSE')

    # Get the armature
    armature = bpy.context.object
    logging.info(f"armature: {armature.name}")
    
    # Initiate logging variable
    editnumber = 0
    
    # Initiate list of any bones that are not at their armaturespace rest location
    posebone_list = []
    posebone_data = {}
    
    # We get a list of all bones not in their rest positions in armaturespace
    for p_bone in armature.pose.bones:
        
        posebone_rotation = p_bone.rotation_quaternion.copy()
        
        p_bone.rotation_quaternion = (1,0,0,0)
        bpy.context.view_layer.update()
        
        #We copy all data in case we need parent data
        posebone_data[p_bone] = [p_bone.bone.head_local.copy(),p_bone.head.copy(),p_bone.location.copy(),posebone_rotation]
        posebone_list.append(p_bone)
        logging.info(f"{p_bone.name} rest pos: {p_bone.bone.head_local}")
        logging.info(f"{p_bone.name} pose pos: {p_bone.head}")
            
    
    #Clear scale of all bones
    for p_bone in armature.pose.bones:
        p_bone.scale = (1,1,1)
        p_bone.location = (0,0,0)
        
    
    #Clear scale and set location
    logging.info(f"Setting location of pose bones:")
    for p_bone in posebone_list:
        logging.info(f"posed bone: {p_bone}")
        # Update positions
        bpy.context.view_layer.update()
        
        if p_bone.parent != None:
            # Bone_rest offset from Parent_rest
            rest_offset = posebone_data[p_bone][0] - posebone_data[p_bone.parent][0]
            
            # Bone_pose offset from Parent_pose
            pose_offset = posebone_data[p_bone][1] - posebone_data[p_bone.parent][1]
        
            calc_offset = pose_offset - rest_offset
        
            p_bone.matrix.translation = p_bone.matrix.translation + calc_offset
        
        else:
            p_bone.matrix.translation = p_bone.matrix.translation + (posebone_data[p_bone][1] - posebone_data[p_bone][0])
        
        editnumber = editnumber + 1
    
    for p_bone in posebone_list:
        p_bone.rotation_quaternion = posebone_data[p_bone][3]
        
    
    if editnumber > 0:
        msgs.append(f"Moved {editnumber} bones to their visual locations and reset scales")
    else:
        msgs.append(f"No bones required movement.")
    
    #Return to original mode
    bpy.ops.object.mode_set(mode=original_mode)
    
    return msgs


# Function to select half of the vertices of a model
def select_model_half(**kwargs):
    # Initiate logging
    msgs = []
    
    # Get settings
    selectcenter = kwargs.get('selectcenter', False)
    symmetryaxis = kwargs.get('symmetryaxis', "+X")
    
    return "WIP"


# Function to select asymmetric vertices
def select_asymmetrical_vertices(**kwargs):
    # Initiate logging
    msgs = []
    
    # Get settings
    symmetryaxis = kwargs.get('symmetryaxis', "+X")
    
    return "WIP"


# Function to select half of the vertices of a model
def select_mergeable_vertices():
    # Initiate logging
    msgs = []
    return "WIP"