import bpy
import logging
import os

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
        # Check that it is not a nonetype object
        if obj.type != 'EMPTY':
            # Rename the data to match the object name
            obj.data.name = obj.name
    
    # End
    msgs.append("Renamed data blocks")
    return msgs


# Conversion operation
def particles_to_curves(input_particle_system,**kwargs):
    # Initiate logging
    msgs = []
    # Get settings
    nodegroupname = kwargs.get('nodegroupname', "Hair Preset")
    attachmentuvmap = kwargs.get('attachmentuvmap', "UVMap")
    attachcurves =  kwargs.get('attachcurves', True)
    skipchild =  kwargs.get('skipchild', True)
    #--------------------------------------------------------------------------------------------
    
    # Store original mode
    originalmode = bpy.context.mode
    
    # Set mode to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Get particle system
    particle_system = input_particle_system
    
    # Get the surface object from the particle system
    surface_object = particle_system.id_data
        
    # Change active particle system
    surface_object.particle_systems.active_index = surface_object.particle_systems.find(particle_system.name)
    
    # Save particle system child type, we set it back at the end
    particle_system_childtype = particle_system.settings.child_type
    
    if skipchild == True:
        # Set active particle system child type to NONE
        particle_system.settings.child_type = 'NONE'
    
    # Get particle system modifier in case it has a different name
    for modifier in surface_object.modifiers:
        if modifier.type == "PARTICLE_SYSTEM":
            if modifier.particle_system == particle_system:
                particle_system_modifier = modifier
                # OCD rename modifiers to particle system name sorry if u didnt want lol
                particle_system_modifier.name = particle_system.name
    
    
    # Force set particle system to visible
    particle_system_modifier.show_viewport = True
    
    #--------------------------------------------------------------------------------------------
    # Handle pre-existing object
    preexisting = False
    # Detect pre-exising curves object
    if bpy.data.objects.get(particle_system.name):
        # Found pre existing
        preexisting = True
        
        # Save old object
        haircurvesobjectold = bpy.data.objects.get(particle_system.name)
        
        # Rename old hair curves object to indicate its old
        haircurvesobjectold.name = particle_system.name + "_Old"
        
        # Get collections from old hair curves object
        haircollections = haircurvesobjectold.users_collection
    
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
    # Import the default node groups if missing
    # Check if the node groups already exist.
    if bpy.data.node_groups.get("Set Hair Curve Profile") == None:

        # Report that import is necessary
        logging.info(f"Hair Curve Profile node group is missing. Importing it now.")

        # Get the blender directory of the current version
        blender_directory = bpy.utils.resource_path('LOCAL')

        # File path
        source_file = source_file = os.path.join(blender_directory, "datafiles", "assets\\geometry_nodes\\procedural_hair_node_assets.blend")

        # Node group to import
        node_group_name = "Set Hair Curve Profile"
        
        # Import the node group
        # Check if the file exists
        if not os.path.isfile(source_file):
            # Report failure to find the asset file
            msgs.append("Failed to find the node group assets file. Append the hair curve profile node manually.")
            return msgs
        else:
            # Load the custom node group from the blend file
            with bpy.data.libraries.load(source_file, link=False) as (data_from, data_to):
                if node_group_name in data_from.node_groups:
                    data_to.node_groups = [node_group_name]

            # Check if the node group was successfully loaded
            if not data_to.node_groups or not data_to.node_groups[0]:
                msgs.append("Failed to load the node group. Append the hair curve profile node manually.")
                return msgs
            else:
                #Clear the fake user flag and asset flag
                imported_node_group = bpy.data.node_groups[node_group_name]
                imported_node_group.asset_clear()
                imported_node_group.use_fake_user = False

            # Report successful import
            logging.info("Succesfully imported the hair curve profile node group")
    
    #--------------------------------------------------------------------------------------------
    # Apply visual profile to new hair curves object for easier viewing
    # Curves have a large radius by default so this is just for the viewport while the curves have their modifiers off.
    # Add profile modifier
    modifier_profile = haircurvesobjectnew.modifiers.new(name="Set Hair Curve Profile", type='NODES')
    modifier_profile.node_group = bpy.data.node_groups.get("Set Hair Curve Profile")
    
    #Copy radius from particle system
    modifier_profile["Input_3"] = particle_system.settings.root_radius * particle_system.settings.radius_scale * 0.5
    modifier_profile["Input_2"] = ((particle_system.settings.shape - -1) / (1 - -1)) * (1 - 0) + 0
    
    # Apply profile modifier
    bpy.ops.object.modifier_apply(modifier="Set Hair Curve Profile")
    
    #--------------------------------------------------------------------------------------------
    # Add hair curves geometry nodes preset
    if preexisting == False and (nodegroupname != "" and nodegroupname != "None" and nodegroupname != "none"):
        if bpy.data.node_groups.get(nodegroupname):
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
            
            #Hide modifier in viewport for performance
            new_modifier.show_viewport = False
            
            # For now hair curves objects can only have geometry nodes modifiers so this is probably safe
            new_modifier.node_group = modifier.node_group
            
            # Copy all the inputs starting from the second one because the first is geometry and can't be copied
            for i in modifier.node_group.interface.items_tree:
                #check that it is a socket and not a panel, check that its an input, and check that its not geometry
                if i.item_type == 'SOCKET' and i.in_out == 'INPUT' and  i.socket_type != 'NodeSocketGeometry':
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
    
    # Set the parent to the surface object
    if surface_object.parent:
        haircurvesobjectnew.parent = surface_object.parent
    
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


# Function for converting one particle system
def convert_particles_to_curves(**kwargs):
    # Initiate logging
    msgs = []
    
    # Get settings
    input_nodegroupname = kwargs.get('nodegroupname', "Hair Preset")
    input_attachmentuvmap = kwargs.get('attachmentuvmap', "UVMap")
    input_attachcurves =  kwargs.get('attachcurves', True)
    input_skipchild =  kwargs.get('skipchild', True)
    
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
    if not surface_object.data.uv_layers.get(input_attachmentuvmap):
        msgs.append("Object has no UV map by specified name")
        return msgs
    
    # Check that the object has particle systems
    if not surface_object.particle_systems:
        msgs.append("Object has no particle systems")
        return msgs
    
    # Get active particle system
    particle_system = surface_object.particle_systems.active
    
    result = particles_to_curves(particle_system,nodegroupname = input_nodegroupname, attachmentuvmap = input_attachmentuvmap, attachcurves = input_attachcurves, skipchild = input_skipchild)
    msgs.append(result)
    
    return msgs
    

# Function to convert all particle systems directly into equivalent curves objects
def convert_particles_all(**kwargs):
    # Initiate logging
    msgs = []
    converted_count = 0  # Counter for converted particle systems
    
    # Get settings
    input_nodegroupname = kwargs.get('nodegroupname', "Hair Preset")
    input_attachmentuvmap = kwargs.get('attachmentuvmap', "UVMap")
    input_attachcurves = kwargs.get('attachcurves', True)
    input_skipchild = kwargs.get('skipchild', True)
    
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
    
    # Check that the object has a UV map by that name
    if not surface_object.data.uv_layers.get(input_attachmentuvmap):
        msgs.append("Object has no UV map by specified name")
        return msgs
    
    # Check that the object has particle systems
    if not surface_object.particle_systems:
        msgs.append("Object has no particle systems")
        return msgs
    
    # Iterate through all particle systems and convert them to curves
    for particle_system in surface_object.particle_systems:
        result = particles_to_curves(
            particle_system,
            nodegroupname=input_nodegroupname,
            attachmentuvmap=input_attachmentuvmap,
            attachcurves=input_attachcurves,
            skipchild=input_skipchild
        )
        
        # Log count
        converted_count += 1
    
    # Add a final message with the total count
    msgs.append(f"Total particle systems converted: {converted_count}")
    
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
# WIP
def select_model_half(**kwargs):
    # Initiate logging
    msgs = []
    
    # Get settings
    selectcenter = kwargs.get('selectcenter', False)
    symmetryaxis = kwargs.get('symmetryaxis', "+X")
    
    return "WIP"


# Function to select asymmetric vertices
# WIP
def select_asymmetrical_vertices(**kwargs):
    # Initiate logging
    msgs = []
    
    # Get settings
    symmetryaxis = kwargs.get('symmetryaxis', "+X")
    
    return "WIP"


# Function to select half of the vertices of a model
# WIP
def select_mergeable_vertices():
    # Initiate logging
    msgs = []
    return "WIP"


# Function to find groups that contain a certain node group
def node_group_list_parents(**kwargs):
    # Initiate logging
    msgs = []
    
    # Get settings
    nodegroupname = kwargs.get('nodegroupname', "None")
    
    # Start, check that node exists
    logging.info(f"----------------------------------------------------------------------------------")
    if bpy.data.node_groups.get(nodegroupname):
        # Get the node group by name
        target_nodegroup = bpy.data.node_groups.get(nodegroupname)
    else:
        logging.info("Node group not found")
        msgs.append("Node group not found")
        return msgs
    
    # Start list
    logging.info(f"Listing parents for '{target_nodegroup.name}'")
    logging.info(f"")
    
    # Log number of owners
    counter = 0
    
    # Iterate over every existing node group
    for nodegroup in bpy.data.node_groups:
        if target_nodegroup != nodegroup:
            for node in nodegroup.nodes:
                if node.bl_rna.identifier == 'GeometryNodeGroup' or node.bl_rna.identifier == 'ShaderNodeGroup':
                    if node.node_tree == target_nodegroup:
                        logging.info(f"Node group '{nodegroup.name}' contains '{target_nodegroup.name}'")
                        counter = counter + 1
    
    # Check materials
    for nodegroup in bpy.data.materials:
        if nodegroup.node_tree and nodegroup.node_tree.nodes:
            for node in nodegroup.node_tree.nodes:
                if node.bl_rna.identifier == 'GeometryNodeGroup' or node.bl_rna.identifier == 'ShaderNodeGroup':
                    if node.node_tree == target_nodegroup:
                        logging.info(f"Material '{nodegroup.name}' contains '{target_nodegroup.name}'")
                        counter = counter + 1
            
    
    # Finalize
    logging.info(f"")
    logging.info(f"There are {counter} instances containing '{target_nodegroup.name}'")
    
    msgs.append(f"Found {counter} results, check console for detailed list.")
    return msgs


# Function to replace duplicate node groups that end in .001 with the original
# WIP
def node_group_merge_duplicates(**kwargs):
    # Initiate logging
    msgs = []
    
    # Get settings
    priority = kwargs.get('prioritymode', "Oldest")

    for nodegroup in bpy.data.node_groups:
        if nodegroup.name[-4] == '.' and nodegroup.name[-3:].isdigit():
            print("Node group is a duplicate")
    
    return "WIP"


# Function to select similar nodes in the current editor
def nodes_select_similar():
    # Initiate logging
    msgs = []
    
    # get all node editor windows and the node groups open in them
    nodegroups = [editor.spaces.active.edit_tree.nodes for editor in bpy.context.window_manager.windows[0].screen.areas if editor.type == 'NODE_EDITOR']
    
    # iterate over every node group
    for nodegroup in nodegroups:
        activenode = nodegroup.active
        activenode_type = activenode.bl_rna.identifier
        
        # iterate over every node inside
        for node in nodegroup:
            # check if node has the same identifier type
            if node.bl_rna.identifier == activenode_type:
                # check if it's a node group and if so only select it if it has the same group
                print(activenode_type)
                if activenode_type == 'GeometryNodeGroup' or activenode_type == 'ShaderNodeGroup':
                    if node.node_tree == activenode.node_tree:
                        node.select = True
                # if its not a node group node, just select all similar
                else:
                    node.select = True
    return "Selected all similar nodes"


# Function to merge selected objects with a geometry nodes group
# WIP
def join_selected_objects_with_geometry_nodes(**kwargs):
    # Initiate logging
    msgs = []
    
    # Retrieve the keyword argument for differentiating materials, default to True
    differentiate_materials = kwargs.get('DifferentiateMaterials', True)
    
    # Get the active object
    active_obj = bpy.context.view_layer.objects.active
    
    # Get all selected objects
    selected_objects = [obj for obj in bpy.context.selected_objects]
    
    # Check if we have an active object and at least one selected object
    if not active_obj or not selected_objects:
        msgs.append("Please ensure there is an active object and other selected objects.")
        return msgs
    
    # Dictionary to hold objects grouped by their materials
    material_objects_dict = {}
    
    # Put then into dictionary sorted by material
    if differentiate_materials:
        # Organize objects by material
        for obj in selected_objects:
            for mat in obj.data.materials:
                if mat.name not in material_objects_dict:
                    material_objects_dict[mat.name] = []
                material_objects_dict[mat.name].append(obj)
    else:
        # If not differentiating materials, treat all objects as having the same material
        material_objects_dict['Combined'] = selected_objects
    
    # List to hold all combined objects created
    combined_objects = []
    
    # Process each group of objects by their material
    for mat_name, objs in material_objects_dict.items():
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        # Select the first object in the current material group
        objs[0].select_set(True)
        # Make it the active object
        bpy.context.view_layer.objects.active = objs[0]
        # Duplicate the active object
        bpy.ops.object.duplicate()
        # The duplicated object is now the active object
        combined_obj = bpy.context.view_layer.objects.active
        # Rename the duplicated object to indicate it is combined with a specific material
        combined_obj.name = "Combined_" + mat_name
        # Add the combined object to our list
        combined_objects.append(combined_obj) # why do we need to do this?
        
        # Remove any modifiers the duplicated object had
        while combined_obj.modifiers:
            bpy.ops.object.modifier_remove(modifier=combined_obj.modifiers[0].name)
        
        # Add a Geometry Nodes modifier to the duplicated object and name it "Join Curves"
        modifier = combined_obj.modifiers.new(name="Join Curves", type='NODES')
        
        # Create a new node group if it doesn't already exist
        if not modifier.node_group:
            node_group = bpy.data.node_groups.new(name="GeometryNodesGroup_" + mat_name, type='GeometryNodeTree')
            modifier.node_group = node_group

        # Clear existing nodes in the node group
        node_group.nodes.clear()
        
        # Create a Join Geometry node to join multiple geometries
        join_geometry_node = node_group.nodes.new(type='GeometryNodeJoinGeometry')
        # Create an Output node to output the final geometry
        output_node = node_group.nodes.new(type='NodeGroupOutput')
        # Create an Input node to accept input geometries
        group_input = node_group.nodes.new(type='NodeGroupInput')
        
        # Position the nodes for better visual arrangement
        group_input.location = (-600, 0)
        join_geometry_node.location = (0, 0)
        output_node.location = (300, 0)
        
        # Link the Join Geometry node to the Output node
        #node_group.links.new(join_geometry_node.outputs["Geometry"], output_node.inputs["Geometry"])
        
        # Only add Object Info nodes and connect them to the Join Geometry node
        for i, obj in enumerate(objs):
            # Create an Object Info node to get geometry from each object
            obj_info_node = node_group.nodes.new(type='GeometryNodeObjectInfo')
            # Position the Object Info node
            obj_info_node.location = (-200, -i*200)
            # Set the object for the Object Info node
            obj_info_node.inputs[0].default_value = obj
            # Link the Object Info node's Geometry output to the Join Geometry node's inputs
            node_group.links.new(obj_info_node.outputs["Geometry"], join_geometry_node.inputs[0])
        
        #Link to output node desu
        node_group.links.new(join_geometry_node.outputs[0],output_node.inputs[0])
        
        # If differentiating materials, assign the current material to the combined object
        if differentiate_materials:
            combined_obj.data.materials.append(bpy.data.materials[mat_name])
    
    # Hide the original selected objects and disable them from rendering
    for obj in selected_objects:
        obj.hide_set(True)
        obj.hide_render = True
    
    # Print a message indicating the number of combined objects created
    msgs.append(f"Created {len(combined_objects)} combined objects for unique materials and hid the original objects.")
    
    return msgs


# Hi
