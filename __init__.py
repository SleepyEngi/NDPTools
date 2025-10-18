# Addon information. Displays addon information on older blender versions. 
bl_info = {
    "name" : "NDP Tools Addon",
    "description" : "Adds a set of buttons on the viewport for managing and cleaning up the scene, among other miscellaneous buttons.",
    "author" : "NDP",
    "version" : (1, 0, 0),
    "blender" : (4, 1, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "https://github.com/SleepyEngi/NDPTools",
    "tracker_url": "https://github.com/SleepyEngi/NDPTools/issues/new",
    "category" : "3D View"
}

# Blender Python
import bpy

# Operators & Panel
from bpy.types import Operator, Panel

# Import functions
from .plugin import ndpt_functions

# Debug Logging
#import logging



# --------------------------------------------------------------------------------
# Operators
# Adds the operators, which we add then to the F3 menu

# Toggle shape keys operator
class NDPT_OT_ToggleShapeKeys(bpy.types.Operator):
    """ Toggle the mute state of all shape keys """
    bl_idname = "ndptobject.toggleshapekeys"
    bl_label = "Toggle all shape keys"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    # Button is pressed
    def execute(self, context):
        self.report({'INFO'},f"Toggling shape keys")
        # Log settings
        #logging.info(f"toggling shape keys")
        #logging.info(f"settings:")
        #logging.info(f"toggle individually: {context.scene.ndpt.NDPT_OT_ToggleShapeKeys_ToggleAll}")
        
        # Run the function
        result = ndpt_functions.toggle_shape_keys(toggleindividual = context.scene.ndpt.NDPT_OT_ToggleShapeKeys_ToggleAll)
        report_results(self, result)
        
        return {'FINISHED'}


# Join with geometry nodes
class NDPT_OT_JoinGeometryNodes(bpy.types.Operator):
    """ Joins objects using a geometry nodes modifier, which allows joining different object types """
    bl_idname = "ndptobject.joinwithgeometrynodes"
    bl_label = "Join selected with geometry nodes"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Joining selected objects")
        #logging.info(f"Joining selected objects")
        #logging.info(f"settings:")
        #logging.info(f"Differentiate materials: {context.scene.ndpt.NDPT_OT_JoinGeometryNodes_DifferentiateMaterials}")
        
        # Run the function
        result = ndpt_functions.join_selected_objects_with_geometry_nodes(DifferentiateMaterials = context.scene.ndpt.NDPT_OT_JoinGeometryNodes_DifferentiateMaterials)
        report_results(self, result)
        
        return {'FINISHED'}


# Synchronize data block names operator
class NDPT_OT_SyncDataNames(bpy.types.Operator):
    """ Rename object data blocks to be the same as the object name """
    bl_idname = "ndptdata.syncdatanames"
    bl_label = "Rename data blocks to match object name"
    bl_options = {"REGISTER", "UNDO"}
    
    # Enable button condition
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Synchronizing data block names")
        #logging.info(f"synchronizing data block names")
        
        # Run the function
        result = ndpt_functions.sync_data_block_names()
        report_results(self, result)

        return {'FINISHED'}


# Convert particles to curves
class NDPT_OT_ConvertParticlesToCurves(bpy.types.Operator):
    """ Convert active particle system into a curves object """
    bl_idname = "ndpthair.convertparticlestocurves"
    bl_label = "Converts a particle system to curves"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Converting particle systems to curves")
        #logging.info(f"converting particle system to curves")
        #logging.info(f"settings:")
        #logging.info(f"node group name: {context.scene.ndpt.NDPT_OT_ConvertParticlesToCurves_DefaultNodeGroup}")
        #logging.info(f"attachment uv map: {context.scene.ndpt.NDPT_OT_ConvertParticlesToCurves_DefaultUVMap}")
        #logging.info(f"attach curves: {context.scene.ndpt.NDPT_OT_ConvertParticlesToCurves_AttachCurves}")
        #logging.info(f"only parents: {context.scene.ndpt.NDPT_OT_ConvertParticlesToCurves_OnlyParents}")
        
        # Run the function
        result = ndpt_functions.convert_particles_to_curves(nodegroupname = context.scene.ndpt.NDPT_OT_ConvertParticlesToCurves_DefaultNodeGroup,attachmentuvmap = context.scene.ndpt.NDPT_OT_ConvertParticlesToCurves_DefaultUVMap,attachcurves = context.scene.ndpt.NDPT_OT_ConvertParticlesToCurves_AttachCurves,skipchild = context.scene.ndpt.NDPT_OT_ConvertParticlesToCurves_OnlyParents)
        report_results(self, result)

        return {'FINISHED'}


# Convert particles to curves 
class NDPT_OT_ConvertParticlesAll(bpy.types.Operator):
    """ Convert all particle systems of the selected object to curves """
    bl_idname = "ndpthair.convertparticlesall"
    bl_label = "Convert all particle systems of an object to curves"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    # Button is pressed
    def execute(self, context):
        self.report({'INFO'},f"Converting particle system to visually identical curves object")
        #logging.info(f"converting particles to equivalent curves")
        
        # Run the function
        result = ndpt_functions.convert_particles_all(nodegroupname = context.scene.ndpt.NDPT_OT_ConvertParticlesToCurves_DefaultNodeGroup,attachmentuvmap = context.scene.ndpt.NDPT_OT_ConvertParticlesToCurves_DefaultUVMap,attachcurves = context.scene.ndpt.NDPT_OT_ConvertParticlesToCurves_AttachCurves,skipchild = context.scene.ndpt.NDPT_OT_ConvertParticlesToCurves_OnlyParents)
        report_results(self, result)
        
        return {'FINISHED'}


# Apply armature modifiers operator
class NDPT_OT_ApplyArmatureModifiers(bpy.types.Operator):
    """ Applies the armature modifiers of all children of an armature """
    bl_idname = "ndptarmature.applyarmaturemodifiers"
    bl_label = "Apply armature modifiers of all children objects of an armature"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        enabled = False
        if context.mode == "OBJECT" or context.mode == "POSE":
            enabled = True
        return enabled
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Applying armature modifiers")
        #logging.info(f"applying armature modifiers")
        #logging.info(f"settings:")
        #logging.info(f"restore modifiers: {context.scene.ndpt.NDPT_OT_ApplyArmatureModifiers_RestoreModifiers}")
        #logging.info(f"apply rest pose: {context.scene.ndpt.NDPT_OT_ApplyArmatureModifiers_ApplyPoseAsRestPose}")
        
        # Run the function
        result = ndpt_functions.apply_armature_modifiers(restoremodifier = context.scene.ndpt.NDPT_OT_ApplyArmatureModifiers_RestoreModifiers, applyrestpose = context.scene.ndpt.NDPT_OT_ApplyArmatureModifiers_ApplyPoseAsRestPose)
        report_results(self, result)

        return {'FINISHED'}


# Convert scale to location operator
class NDPT_OT_ConvertScaleToLocation(bpy.types.Operator):
    """ Converts scale bone pose transforms into location transforms in the same visual location. Can take a long time for large armatures """
    bl_idname = "ndptarmature.convertscaletopose"
    bl_label = "Convert bone scale transforms into location transforms. Can take a long time for large armatures"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        enabled = False
        if context.mode == "OBJECT" or context.mode == "POSE":
            enabled = True
        return enabled
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Converting scale to location")
        #logging.info(f"converting scale to location")
        
        # Run the function
        result = ndpt_functions.convert_scale_to_loc()
        report_results(self, result)

        return {'FINISHED'}


# Select half operator
class NDPT_OT_SelectHalf(bpy.types.Operator):
    """ Selects all the vertices on one half of the model """
    bl_idname = "ndptedit.selecthalf"
    bl_label = "Select all the vertices on one half of the model"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Selecting half")
        #logging.info(f"selecting half")
        #logging.info(f"settings:")
        #logging.info(f"select center: {context.scene.ndpt.NDPT_OT_SelectHalf_SelectCenter}")
        #logging.info(f"symmetry axis: {context.scene.ndpt.NDPT_OT_SelectHalf_SymmetryAxis}")
        
        # Run the function
        result = ndpt_functions.select_model_half(selectcenter = context.scene.ndpt.NDPT_OT_SelectHalf_SelectCenter, symmetryaxis = context.scene.ndpt.NDPT_OT_SelectHalf_SymmetryAxis)
        report_results(self, result)

        return {'FINISHED'}


# Select asymmetrical operator
class  NDPT_OT_SelectAsymmetrical(bpy.types.Operator):
    """ Selects vertices that aren't symmetric with the other half of the model """
    bl_idname = "ndptedit.selectasymmetrical"
    bl_label = "Selects vertices that do not have symmetry with the other half of the model"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Selecting asymmetrical vertices")
        #logging.info(f"selecting assymetrical vertices")
        #logging.info(f"settings:")
        #logging.info(f"symmetry axis: {context.scene.ndpt.NDPT_OT_SelectHalf_SymmetryAxis}")
        
        # Run the function
        result = ndpt_functions.select_asymmetrical_vertices(symmetryaxis = context.scene.ndpt.NDPT_OT_SelectHalf_SymmetryAxis)
        report_results(self, result)

        return {'FINISHED'}


# Select mergeable operator
class  NDPT_OT_SelectMergeable(bpy.types.Operator):
    """ Selects vertices that are in the same location as another vertex """
    bl_idname = "ndptedit.selectmergeable"
    bl_label = "Selects vertices that are in the same location as another vertex"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Selecting mergeable vertices")
        #logging.info(f"selecting mergeable vertices")
        
        # Run the function
        result = ndpt_functions.select_mergeable_vertices()
        report_results(self, result)
        
        return {'FINISHED'}


# Select similar operator
class NDPT_OT_SelectSimilarNodes(bpy.types.Operator):
    """ Selects all nodes of the same type """
    bl_idname = "ndptnodes.selectsimilar"
    bl_label = "Selects all nodes of the same type"
    bl_options = {"REGISTER", "UNDO"}
    
    # Enabled always
    @classmethod
    def poll(cls, context):
        return True
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Selecting similar nodes")
        #logging.info(f"selecting similar nodes")

        
        # Run the function
        result = ndpt_functions.nodes_select_similar()
        report_results(self, result)

        return {'FINISHED'}


# Merge duplicate node groups operator
class NDPT_OT_MergeDuplicateNodeGroups(bpy.types.Operator):
    """ Merges duplicate node groups across the scene """
    bl_idname = "ndptnodes.mergeduplicatenodegroups"
    bl_label = "Merges duplicate node groups across the scene"
    bl_options = {"REGISTER", "UNDO"}
    
    # Enable button condition
    @classmethod
    def poll(cls, context):
        return True
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Merging duplicate node groups")
        #logging.info(f"merging duplicate node groups")
        #logging.info(f"settings:")
        #logging.info(f"priority mode: {context.scene.ndpt.NDPT_OT_MergeDuplicateNodeGroups_PriorityMode}")
        
        # Run the function
        result = ndpt_functions.node_group_merge_duplicates(prioritymode = context.scene.ndpt.NDPT_OT_MergeDuplicateNodeGroups_PriorityMode)
        report_results(self, result)

        return {'FINISHED'}


# Merge duplicate node groups operator
class NDPT_OT_FindNodeParents(bpy.types.Operator):
    """ Find which node groups contain this node group """
    bl_idname = "ndptnodes.findnodeparents"
    bl_label = "Find which node groups contain this node group"
    bl_options = {"REGISTER", "UNDO"}
    
    # Enable button condition
    @classmethod
    def poll(cls, context):
        return True
    
    # Button is pressed
    def execute(self, context):
        # Start
        scene = context.scene
        nodegroupname = context.scene.ndpt.NDPT_OT_FindNodeParents_DefaultNodeGroup

        # Log settings
        self.report({'INFO'},f"Finding node parents")
        #logging.info(f"finding node parents")
        #logging.info(f"settings:")
        #logging.info(f"node group name: {nodegroupname}")

        # Clear previous results
        scene.ndpt.NDPT_OT_FindNodeParents_Results.clear()
        
        # Run the function
        results = ndpt_functions.node_group_list_parents(nodegroupname = context.scene.ndpt.NDPT_OT_FindNodeParents_DefaultNodeGroup)
        
        for r in results:
            item = scene.ndpt.NDPT_OT_FindNodeParents_Results.add()
            item.name = r
        
        self.report({'INFO'}, f"Found {len(results) - 1} results.")

        return {'FINISHED'}



# --------------------------------------------------------------------------------
# Helper functions

# Report results
def report_results(op, result):
    if isinstance(result, str):
        op.report({'INFO'}, result)
    elif isinstance(result, (list, tuple, set)):
        for item in result:
            op.report({'INFO'}, str(item))
    else:
        op.report({'INFO'}, str(result))

# Function to dynamically fetch all node groups in the scene
def get_node_groups(node_type="BOTH"):
    items = [("None", "None", "No node group selected")]  # Add "None" as the first option
    
    # Check the filtering option and gather appropriate node groups
    for node_group in bpy.data.node_groups:
        if node_type == "BOTH":
            items.append((node_group.name, node_group.name, ""))
        elif node_type == "GEOMETRY" and node_group.type == 'GEOMETRY':
            items.append((node_group.name, node_group.name, ""))
        elif node_type == "SHADER" and node_group.type == 'SHADER':
            items.append((node_group.name, node_group.name, ""))
    
    return items

# Get all node groups in the scene
def get_all_node_groups(self,context):
    items = get_node_groups(node_type = "BOTH")
    return items

# Get geometry nodes groups
def get_geometry_node_groups(self,context):
    items = get_node_groups(node_type = "GEOMETRY")
    return items
    
# Function to retrieve UV maps from the active object
def get_uv_maps(self, context):
    items = []
    obj = context.object
    
    # Check if the active object has mesh data and UV maps
    if obj and obj.type == 'MESH' and obj.data.uv_layers:
        for uv in obj.data.uv_layers:
            items.append((uv.name, uv.name, ""))
    else:
        items.append(("None", "None", "No UV maps found"))

    return items

# -------------------------------------------------------------------------------

# Data type for node parent search results
class NDPT_NodeParentResult(bpy.types.PropertyGroup):
    """Item representing a single node parent result"""
    name: bpy.props.StringProperty(name="Parent Node Group Name")

# UI List for showing node group parent results
class NDPT_UL_NodeParentResults(bpy.types.UIList):
    """UI list to show node group parents"""
    bl_idname = "NDPT_UL_NodeParentResults"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.label(text=item.name)

# --------------------------------------------------------------------------------
# Panels
# Adds panels and buttons in the siderbar that when pressed, run operators and their settings


# Sidebar panels definition
class NDPT_PT_Sidebar_Object(bpy.types.Panel):
    """Creates a new tab in the sidebar"""
    bl_label = "NDPTools: Object"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "NDP Tools"
    
    # Draw
    def draw(self, context):
        # Define Colums
        col = self.layout.column(align=True)
        
        #--------------------------------------------------------------------------------------
        # Object
        
        # Create a box for separation
        box = col.box()
        box.label(text="Object")
        
        # Button
        prop = box.operator(NDPT_OT_ToggleShapeKeys.bl_idname, text="Toggle shape keys")
        
        # Button Settings
        box.prop(context.scene.ndpt, "NDPT_OT_ToggleShapeKeys_ToggleAll")
        
        # Separate
        col.separator()
        
        # Button
        prop = box.operator(NDPT_OT_JoinGeometryNodes.bl_idname, text="Join with geometry nodes")
        
        # Button Settings
        box.prop(context.scene.ndpt, "NDPT_OT_JoinGeometryNodes_DifferentiateMaterials")
        
        # Separate
        col.separator()

        #--------------------------------------------------------------------------------------
        # Data
        
        # Create a box for separation
        box = col.box()
        box.label(text="Data")
        
        # Button
        prop = box.operator(NDPT_OT_SyncDataNames.bl_idname, text="Sync data block names")
        
        # Separate
        col.separator()

        #--------------------------------------------------------------------------------------
        # Edit
        
        # Create a box for separation
        box = col.box()
        box.label(text="Edit mode")
        
        # Button
        prop = box.operator(NDPT_OT_SelectHalf.bl_idname, text="Select half")
        
        # Button settings
        box.prop(context.scene.ndpt, "NDPT_OT_SelectHalf_SelectCenter")
        
        # Label
        box.label(text="Symmetry axis:")
        
        # Button settings
        box.prop(context.scene.ndpt, "NDPT_OT_SelectHalf_SymmetryAxis")
        
        # Separate
        col.separator()
        
        # Button
        prop = box.operator(NDPT_OT_SelectAsymmetrical.bl_idname, text="Select asymmetrical vertices")
        
        # Separate
        col.separator()
        
        # Button
        prop = box.operator(NDPT_OT_SelectMergeable.bl_idname, text="Select mergeable vertices")
        
        # Separate
        col.separator()

class NDPT_PT_Sidebar_Hair(bpy.types.Panel):
    """Creates a new tab in the sidebar"""
    bl_label = "NDPTools: Hair"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "NDP Tools"
    
    # Draw
    def draw(self, context):
        #--------------------------------------------------------------------------------------
        # Convert Hair

        # Define Colums
        col = self.layout.column(align=True)
        
        # Create a box for separation
        box = col.box()
        box.label(text="Convert Hair")
        
        # Button
        prop = box.operator(NDPT_OT_ConvertParticlesToCurves.bl_idname, text="Convert particles to curves")
        
        # Label
        box.label(text="Default node group:")
        
        # Button settings
        box.prop(context.scene.ndpt, "NDPT_OT_ConvertParticlesToCurves_DefaultNodeGroup")
        
        # Label
        box.label(text="Attachment UV map:")
        
        # Button settings
        box.prop(context.scene.ndpt, "NDPT_OT_ConvertParticlesToCurves_DefaultUVMap")
        
        # Button settings
        box.prop(context.scene.ndpt, "NDPT_OT_ConvertParticlesToCurves_AttachCurves")
        
        # Button settings
        box.prop(context.scene.ndpt, "NDPT_OT_ConvertParticlesToCurves_OnlyParents")
        
        # Separate
        col.separator()
        
        # Button
        prop = box.operator(NDPT_OT_ConvertParticlesAll.bl_idname, text="Convert all particle systems to curves")
        
        # Separate
        col.separator()

class NDPT_PT_Sidebar_Armature(bpy.types.Panel):
    """Creates a new tab in the sidebar"""
    bl_label = "NDPTools: Armature"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "NDP Tools"
    
    # Draw
    def draw(self, context):
        #--------------------------------------------------------------------------------------
        # Armature

        # Define Colums
        col = self.layout.column(align=True)
        
        # Create a box for separation
        box = col.box()
        box.label(text="Armature")
        
        # Button
        prop = box.operator(NDPT_OT_ApplyArmatureModifiers.bl_idname, text="Apply armature modifiers")
        
        # Button settings
        box.prop(context.scene.ndpt, "NDPT_OT_ApplyArmatureModifiers_RestoreModifiers")
        
        # Button settings
        box.prop(context.scene.ndpt, "NDPT_OT_ApplyArmatureModifiers_ApplyPoseAsRestPose")
        
        # Separate
        col.separator()
        
        # Button
        prop = box.operator(NDPT_OT_ConvertScaleToLocation.bl_idname, text="Convert scale to location")
        
        # Separate
        col.separator()

class NDPT_PT_Sidebar_Nodes(bpy.types.Panel):
    """Creates a new tab in the sidebar"""
    bl_label = "NDPTools: Nodes"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "NDP Tools"
    
    # Draw
    def draw(self, context):
        
        #--------------------------------------------------------------------------------------
        # Geometry nodes
        
        # Define Colums
        col = self.layout.column(align=True)

        # Create a box for separation
        box = col.box()
        box.label(text="Nodes")
        
        # Button
        prop = box.operator(NDPT_OT_SelectSimilarNodes.bl_idname, text="Select similar nodes")
        
        # Separate
        col.separator()
        
        # Button
        prop = box.operator(NDPT_OT_FindNodeParents.bl_idname, text="Find Node Group Parents")
        
        # Label
        box.label(text="Node Group:")
        
        # Button settings
        box.prop(context.scene.ndpt, "NDPT_OT_FindNodeParents_DefaultNodeGroup")
        
        # Separate
        col.separator()

        # Show results list
        if len(context.scene.ndpt.NDPT_OT_FindNodeParents_Results) > 0:
            box.label(text="Results:")
            box.template_list("NDPT_UL_NodeParentResults", "", context.scene.ndpt, "NDPT_OT_FindNodeParents_Results", context.scene.ndpt, "NDPT_OT_FindNodeParents_Results_Index")
        else:
            box.label(text="No results yet.")
        
        # Button
        prop = box.operator(NDPT_OT_MergeDuplicateNodeGroups.bl_idname, text="Merge duplicate node groups")
        
        # Label
        box.label(text="Priority mode:")
        
        # Button settings
        box.prop(context.scene.ndpt, "NDPT_OT_MergeDuplicateNodeGroups_PriorityMode")
        
        # Separate
        col.separator()
        

# --------------------------------------------------------------------------------
# Initiate addon

# Class for all the button setting properties
class NDPT_SceneProperties(bpy.types.PropertyGroup):
    # Boolean Property
    # Toggle shape keys: toggle all
    NDPT_OT_ToggleShapeKeys_ToggleAll: bpy.props.BoolProperty(
        name='Toggle individually',
        description = "Toggle all shape keys individually instead of turning all on/off",
        default = False
    )
    
    # Boolean Property
    # Join with geometry nodes: Differentiate materials
    NDPT_OT_JoinGeometryNodes_DifferentiateMaterials: bpy.props.BoolProperty(
        name='Differentiate materials',
        description = "Differentiate materials when joining objects, having one object per material. Useful for curves which can only have one material",
        default = True
    )
    
    # Enum property
    # Convert particle system to curves: default preset name
    NDPT_OT_ConvertParticlesToCurves_DefaultNodeGroup: bpy.props.EnumProperty(
        name = '',
        description = "Name of the default node group to apply if there isn't a current curves object with one",
        items = get_geometry_node_groups,
        default = None
    )
    
    # Enum property
    # List of uv maps of current active object
    NDPT_OT_ConvertParticlesToCurves_DefaultUVMap: bpy.props.EnumProperty(
        name = '',
        description = "List of UV maps in the active object",
        items = get_uv_maps,  # Function to get UV maps
        default = None  # First UV map as default (or "None" if no UV maps)
    )
    
    # Boolean Property
    # Convert particle system to curves: attach curves to surface
    NDPT_OT_ConvertParticlesToCurves_AttachCurves: bpy.props.BoolProperty(
        name='Attach curves',
        description = "Automatically attach the curves to the surface so that they get a surface_uv_coordinate",
        default = True
    )
    
    # Boolean Property
    # Convert particle system to curves: attach curves to surface
    NDPT_OT_ConvertParticlesToCurves_OnlyParents: bpy.props.BoolProperty(
        name='Only parent curves',
        description = "Only convert parent curves and skip interpolated child curves",
        default = True
    )
    
    # Boolean Property
    # Apply armature modifiers: restore modifiers
    NDPT_OT_ApplyArmatureModifiers_RestoreModifiers: bpy.props.BoolProperty(
        name='Restore modifiers',
        description = "Add a copy of the armature modifier after applying it",
        default = True
    )
    
    # Boolean Property
    # Apply armature modifiers: apply pose as rest pose
    NDPT_OT_ApplyArmatureModifiers_ApplyPoseAsRestPose: bpy.props.BoolProperty(
        name='Apply pose as rest pose',
        description = "Apply the armature's pose as the rest pose",
        default = False
    )
    
    # Boolean Property
    # Select half: select center vertices
    NDPT_OT_SelectHalf_SelectCenter: bpy.props.BoolProperty(
        name='Select center',
        description = "Select vertices in the central line",
        default = False
    )
    
    # Enum Property
    # Select half: symmetry axis
    NDPT_OT_SelectHalf_SymmetryAxis: bpy.props.EnumProperty(
        name='',
        description = "Select the axis of symmetry",
        items = [("+X", "+X", "+X axis"),("-X", "-X", "-X axis"),("+Y", "+Y", "+Y axis"),("-Y", "-Y", "-Y axis"),("+Z", "+Z", "+Z axis"),("-Z", "-Z", "-Z axis")],
        default = "+X"
    )
    
    # Enum Property
    # Dropdown for finding node parents
    NDPT_OT_FindNodeParents_DefaultNodeGroup: bpy.props.EnumProperty(
        name = '',
        description = "Search which node groups contain this node group",
        items = get_all_node_groups,
        default = None
    )

    # Collection property for node parent search results
    NDPT_OT_FindNodeParents_Results: bpy.props.CollectionProperty(
        type=NDPT_NodeParentResult
    )
    
    NDPT_OT_FindNodeParents_Results_Index: bpy.props.IntProperty(
        default=0
    )

    
    # Enum Property
    # Merge duplicate node groups: Priority mode
    NDPT_OT_MergeDuplicateNodeGroups_PriorityMode: bpy.props.EnumProperty(
        name='',
        description = "Priority mode",
        items = [("Oldest", "Oldest", "Prioritizes the oldest node group with the lowest suffix number"),("Newest", "Newest", "Prioritizes the newest node group with the higest suffix number")],
        default = "Oldest"
    )

# List of enabled classes
classes = [
    NDPT_PT_Sidebar_Object,
    NDPT_PT_Sidebar_Hair,
    NDPT_PT_Sidebar_Armature,
    NDPT_PT_Sidebar_Nodes,
    NDPT_OT_ToggleShapeKeys,
    NDPT_OT_JoinGeometryNodes,
    NDPT_OT_SyncDataNames,
    NDPT_OT_ConvertParticlesToCurves,
    NDPT_OT_ConvertParticlesAll,
    NDPT_OT_ApplyArmatureModifiers,
    NDPT_OT_ConvertScaleToLocation,
    NDPT_OT_SelectHalf,
    NDPT_OT_SelectAsymmetrical,
    NDPT_OT_SelectMergeable,
    NDPT_OT_SelectSimilarNodes,
    NDPT_OT_FindNodeParents,
    NDPT_OT_MergeDuplicateNodeGroups,
    NDPT_NodeParentResult,
    NDPT_UL_NodeParentResults,
    NDPT_SceneProperties,
]

# Run when enabling addon
def register():
    
    # Register all classes
    for cls in classes:
        bpy.utils.register_class(cls)

    # Register scene properties
    if not hasattr(bpy.types.Scene, "ndpt"):
        bpy.types.Scene.ndpt = bpy.props.PointerProperty(type=NDPT_SceneProperties)

    # Log   
    #logging.info("NDP Tools Enabled")

# Run when disabling addon
# Delete all the custom settings buttons
def unregister():

    # Unregister button settings
    if hasattr(bpy.types.Scene, "ndpt"):
        del bpy.types.Scene.ndpt

    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Log   
    #logging.info("NDP Tools Disabled")

# Register
# Commented out as it's unecessary apparently. Maybe only on older versions.
#if __name__ == '__main__':
#    register()