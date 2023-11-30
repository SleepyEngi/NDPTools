# Addon information, displays on addons list.
bl_info = {
    "name" : "NDP Tools Addon",
    "description" : "Utility scripts by NDP",
    "author" : "NDP",
    "version" : (0, 0, 1),
    "blender" : (3, 6, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "https://github.com/SleepyEngi/NDPTools",
    "tracker_url": "https://github.com/SleepyEngi/NDPTools/issues/new",
    "category" : "3D View"
}

# For everything
import bpy

# For addon operators and panels
from bpy.types import Operator
from bpy.types import Panel

# For operators
import logging

# import the functions


# --------------------------------------------------------------------------------
# Operators
# Adds the operations to the F3 menu. Later we assign them to a button on the panel.


# Toggle shake keys operator
class NDPT_OT_ToggleShapeKeys(bpy.types.Operator):
    """ Toggle the mute state of all shape keys """
    bl_idname = "object.toggleshapekeys"
    bl_label = "Toggle all shape keys"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Toggling shape keys")
        logging.info(f"toggling shape keys")
        logging.info(f"settings:")
        logging.info(f"toggle individually: {context.scene.NDPT_OT_ToggleShapeKeys_ToggleAll}")

        return {'FINISHED'}


# Synchronize data block names operator
class NDPT_OT_SyncDataNames(bpy.types.Operator):
    """ Rename object data blocks to be the same as the object name """
    bl_idname = "object.syncdatanames"
    bl_label = "Rename data blocks to match object name"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Synchronizing data block names")
        logging.info(f"synchronizing data block names")

        return {'FINISHED'}


# Merge duplicate node groups operator
class NDPT_OT_MergeDuplicateNodeGroups(bpy.types.Operator):
    """ Rename object data blocks to be the same as the object name """
    bl_idname = "object.mergeduplicatenodegroups"
    bl_label = "Rename data blocks to match object name"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Merging duplicate node groups")
        logging.info(f"merging duplicate node groups")

        return {'FINISHED'}


# Convert particles to curves
class NDPT_OT_ConvertParticlesToCurves(bpy.types.Operator):
    """ Convert active particle system into a curves object """
    bl_idname = "object.convertparticlestocurves"
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
        logging.info(f"converting particle system to curves")
        logging.info(f"settings:")
        logging.info(f"node group name: {context.scene.NDPT_OT_ConvertParticlesToCurves_DefaultNodeGroup}")
        logging.info(f"attachment uv map: {context.scene.NDPT_OT_ConvertParticlesToCurves_DefaultUVMap}")
        logging.info(f"attach curves: {context.scene.NDPT_OT_ConvertParticlesToCurves_AttachCurves}")

        return {'FINISHED'}


# Convert curves to particles 
class NDPT_OT_ConvertCurvesToParticles(bpy.types.Operator):
    """ Convert active curves object into a particle system """
    bl_idname = "object.convertcurvestoparticles"
    bl_label = "Converts a curves object into a particle system"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    # Button is pressed
    def execute(self, context):
        self.report({'INFO'},f"Converting curves object into a particle system")
        logging.info(f"converting curves to particle system")

        return {'FINISHED'}


# Apply armature modifiers operator
class NDPT_OT_ApplyArmatureModifiers(bpy.types.Operator):
    """ Applies the armature modifiers of all children of an armature """
    bl_idname = "object.applyarmaturemodifiers"
    bl_label = "Apply armature modifiers of all children objects of an armature"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Applying armature modifiers")
        logging.info(f"applying armature modifiers")
        logging.info(f"settings:")
        logging.info(f"restore modifiers: {context.scene.NDPT_OT_ApplyArmatureModifiers_RestoreModifiers}")
        logging.info(f"apply rest pose: {context.scene.NDPT_OT_ApplyArmatureModifiers_ApplyPoseAsRestPose}")

        return {'FINISHED'}


# Convert scale to location operator
class NDPT_OT_ConvertScaleToLocation(bpy.types.Operator):
    """ Converts scale bone pose transforms into location transforms in the same visual location """
    bl_idname = "pose.convertscaletopose"
    bl_label = "Convert bone scale transforms into location transforms"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Converting scale to location")
        logging.info(f"converting scale to location")

        return {'FINISHED'}


# Select half operator
class NDPT_OT_SelectHalf(bpy.types.Operator):
    """ Selects all the vertices on one half of the model """
    bl_idname = "edit.selecthalf"
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
        logging.info(f"selecting half")
        logging.info(f"settings:")
        logging.info(f"select center: {context.scene.NDPT_OT_SelectHalf_SelectCenter}")
        logging.info(f"symmetry axis: {context.scene.NDPT_OT_SelectHalf_SymmetryAxis}")

        return {'FINISHED'}


# Select asymmetrical operator
class  NDPT_OT_SelectAsymmetrical(bpy.types.Operator):
    """ Selects vertices that aren't symmetric with the other half of the model """
    bl_idname = "edit.selectasymmetrical"
    bl_label = "Selects vertices that do not have symmetry with the other half of the model"
    bl_options = {"REGISTER", "UNDO"}
    
    # Only enable in object mode
    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"
    
    # Button is pressed
    def execute(self, context):
        # Log settings
        self.report({'INFO'},f"Selecting assymetrical vertices")
        logging.info(f"selecting assymetrical vertices")
        logging.info(f"settings:")
        logging.info(f"symmetry axis: {context.scene.NDPT_OT_SelectHalf_SymmetryAxis}")

        return {'FINISHED'}


# Select mergeable operator
class  NDPT_OT_SelectMergeable(bpy.types.Operator):
    """ Selects vertices that are in the same location as another vertex """
    bl_idname = "edit.selectamergeable"
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
        logging.info(f"selecting mergeable vertices")

        return {'FINISHED'}


# --------------------------------------------------------------------------------
# Panels
# Adds panels and buttons in the siderbar that when pressed, run operators and their settings


# Sidebar panel definition
class NDPT_PT_Sidebar(bpy.types.Panel):
    """Creates a new tab in the sidebar"""
    bl_label = "NDP Tools Menu"
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
        box.prop(context.scene, "NDPT_OT_ToggleShapeKeys_ToggleAll")
        
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
        
        # Button
        prop = box.operator(NDPT_OT_MergeDuplicateNodeGroups.bl_idname, text="Merge duplicate node groups")
        
        # Separate
        col.separator()
        
        #--------------------------------------------------------------------------------------
        # Convert Hair
        
        # Create a box for separation
        box = col.box()
        box.label(text="Convert Hair")
        
        # Button
        prop = box.operator(NDPT_OT_ConvertParticlesToCurves.bl_idname, text="Convert particles to curves")
        
        # Label
        box.label(text="Default node group:")
        
        # Button settings
        box.prop(context.scene, "NDPT_OT_ConvertParticlesToCurves_DefaultNodeGroup")
        
        # Label
        box.label(text="Attachment UV map:")
        
        # Button settings
        box.prop(context.scene, "NDPT_OT_ConvertParticlesToCurves_DefaultUVMap")
        
        # Button settings
        box.prop(context.scene, "NDPT_OT_ConvertParticlesToCurves_AttachCurves")
        
        # Separate
        col.separator()
        
        # Button
        prop = box.operator(NDPT_OT_ConvertCurvesToParticles.bl_idname, text="Convert curves to particles")
        
        # Separate
        col.separator()
        
        #--------------------------------------------------------------------------------------
        # Armature
        
        # Create a box for separation
        box = col.box()
        box.label(text="Armature")
        
        # Button
        prop = box.operator(NDPT_OT_ApplyArmatureModifiers.bl_idname, text="Apply armature modifiers")
        
        # Button settings
        box.prop(context.scene, "NDPT_OT_ApplyArmatureModifiers_RestoreModifiers")
        
        # Button settings
        box.prop(context.scene, "NDPT_OT_ApplyArmatureModifiers_ApplyPoseAsRestPose")
        
        # Separate
        col.separator()
        
        # Button
        prop = box.operator(NDPT_OT_ConvertScaleToLocation.bl_idname, text="Convert scale to location")
        
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
        box.prop(context.scene, "NDPT_OT_SelectHalf_SelectCenter")
        
        # Label
        box.label(text="Symmetry axis:")
        
        # Button settings
        box.prop(context.scene, "NDPT_OT_SelectHalf_SymmetryAxis")
        
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
        


# --------------------------------------------------------------------------------
# Initiate addon


# List of enabled classes
classes = [
    NDPT_OT_ToggleShapeKeys,
    NDPT_OT_SyncDataNames,
    NDPT_OT_MergeDuplicateNodeGroups,
    NDPT_OT_ConvertParticlesToCurves,
    NDPT_OT_ConvertCurvesToParticles,
    NDPT_OT_ApplyArmatureModifiers,
    NDPT_OT_ConvertScaleToLocation,
    NDPT_OT_SelectHalf,
    NDPT_OT_SelectAsymmetrical,
    NDPT_OT_SelectMergeable,
    NDPT_PT_Sidebar,
]

# Run when enabling addon
def register():
    
    # Register all classes
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Boolean Property
    # Toggle shape keys: toggle all
    bpy.types.Scene.NDPT_OT_ToggleShapeKeys_ToggleAll = bpy.props.BoolProperty(
        name='Toggle individually',
        description = "Toggle all shape keys individually insteaf of turning all on/off",
        default = True
    )
    
    # String Property
    # Convert particle system to curves: default preset name
    bpy.types.Scene.NDPT_OT_ConvertParticlesToCurves_DefaultNodeGroup = bpy.props.StringProperty(
        name = '',
        description = "Name of the default node group to apply if there isn't a current curves object with one",
        default = "Hair Preset"
    )
    
    # String Property
    # Convert particle system to curves: default UV map name
    bpy.types.Scene.NDPT_OT_ConvertParticlesToCurves_DefaultUVMap = bpy.props.StringProperty(
        name = '',
        description = "Name of the UV map to attach the curves to",
        default = "UVMap"
    )
    
    # Boolean Property
    # Convert particle system to curves: attach curves to surface
    bpy.types.Scene.NDPT_OT_ConvertParticlesToCurves_AttachCurves = bpy.props.BoolProperty(
        name='Attach curves',
        description = "Automatically attach the curves to the surface so that they get a surface_uv_coordinate",
        default = True
    )
    
    # Boolean Property
    # Apply armature modifiers: restore modifiers
    bpy.types.Scene.NDPT_OT_ApplyArmatureModifiers_RestoreModifiers = bpy.props.BoolProperty(
        name='Restore modifiers',
        description = "Add a copy of the armature modifier after applying it",
        default = True
    )
    
    # Boolean Property
    # Apply armature modifiers: apply pose as rest pose
    bpy.types.Scene.NDPT_OT_ApplyArmatureModifiers_ApplyPoseAsRestPose = bpy.props.BoolProperty(
        name='Apply pose as rest pose',
        description = "Apply the armature's pose as the rest pose",
        default = False
    )
    
    # Boolean Property
    # Select half: select center vertices
    bpy.types.Scene.NDPT_OT_SelectHalf_SelectCenter = bpy.props.BoolProperty(
        name='Select center',
        description = "Select vertices in the central line",
        default = False
    )
    
    # Enum Property
    # Select half: symmetry axis
    bpy.types.Scene.NDPT_OT_SelectHalf_SymmetryAxis = bpy.props.EnumProperty(
        name='',
        description = "Select the axis of symmetry",
        items = [("+X", "+X", "+X axis"),("-X", "-X", "-X axis"),("+Y", "+Y", "+Y axis"),("-Y", "-Y", "-Y axis"),("+Z", "+Z", "+Z axis"),("-Z", "-Z", "-Z axis")],
        default = "+X"
    )
    
    # Log
    #logging.info("NDP Tools Enabled")
    
# Run when disabling addon
def unregister():
    # Unregister button settings
    del bpy.types.Scene.NDPT_OT_ToggleShapeKeys_ToggleAll
    del bpy.types.Scene.NDPT_OT_ConvertParticlesToCurves_DefaultNodeGroup
    del bpy.types.Scene.NDPT_OT_ConvertParticlesToCurves_DefaultUVMap
    del bpy.types.Scene.NDPT_OT_ConvertParticlesToCurves_AttachCurves
    del bpy.types.Scene.NDPT_OT_ApplyArmatureModifiers_RestoreModifiers
    del bpy.types.Scene.NDPT_OT_ApplyArmatureModifiers_ApplyPoseAsRestPose
    del bpy.types.Scene.NDPT_OT_SelectHalf_SelectCenter
    del bpy.types.Scene.NDPT_OT_SelectHalf_SymmetryAxis
    
    # Unregister classes
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    # Log   
    logging.info("NDP Tools Disabled")

if __name__ == '__main__':
    register()