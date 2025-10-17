NDPTools: Scene clean up tools
Author: NDP
Version: 1.0.2
Blender 4.2+
YYYY-MM-DD: 2025-10-14
=========================================================================================================
Manual Download instructions
1. You can find the latest version of this addon at https://github.com/SleepyEngi/NDPTools
2. Go to the green "<> Code" button
3. Click "Download ZIP"
=========================================================================================================
Manual Installation instructions
1. On blender, go to Edit -> Preferences -> Add-ons.
2. Click the down arrow on the top right corner and select "Install from disk".
3. Select the .zip file "ndptools-master.zip" that contains the addon.
4. Make sure the addon is enabled with the checkmark on the left side of the title.
=========================================================================================================
**Features**

Toggle shape keys:
-Toggles all shape keys in an object.
-Settings:
-Toggle individually: Toggles the status of each key individually instead of turning all key shapes on/off.

Join with geometry nodes:
-Joins objects using an automatically generated geometry nodes node group, useful for joining curves objects which don't have a join feature.
-Settings:
-Differentiate materials: Create a different object for each material. Useful for curves objects which can only have one material.

Sync data block names: 
-Renames all object's data blocks to match the name of the object.

Find node group parents:
-Finds all the node groups that contain the selected node group and lists them in the console. Useful for cleaning up duplicates or finding where something is used.

Merge duplicate node groups: 
-Cleans up all duplicate node groups ending in .001 and replaces them with their original if found.
-Settings:
-Priority mode: Oldest to make the original take priority, and newest to make the highest .### number take priority

Synchronize data block names
-Synchronizes all data block names to be the same as their object names. Useful for cleaning up incorrect old names in the data dropdown.

Convert particles to curves:
-Converts a particle system to curves and automatically sets up its surface object, uv map, and adds a geometry nodes modifier.
-If a pre-existing curves object exists, it copies all data and modifiers from that object and restores it to the new curves object.
-Useful for using the old particle system combing and then quickly converting it back to the new hair curves
-Settings:
-Default node group: The geometry nodes group that will be added by default if there was no pre-existing curves object. Can be none.
-Attachment UV map: The uv map that the curves will be attached to.
-Attach curves: Automatically go into sculpt mode and run an attach curves to nearest surface operation.
-Only parents: Only uses parent particles and disables interpolated child particles. 

Convert all particle systems to curves:
-Runs the convert particles to curves operation on every particle system of the selected object instead of just the active one.

Apply armature modifiers:
-Applies the armature modifiers of all the children of a selected armature.
-Settings: 
-Restore modifiers: After applying the modifiers, adds a copy back in.
-Apply pose as rest pose: After applying modifiers, applies the current armature's pose as the rest pose.

Convert scale to location:
-Converts a pose bone's scale transforms into visually identical location transforms.

Select half:
-Selects one half of the model on edit mode
-Settings:
-Select center: Selects the central line
-Symmetry axis: Tells it which side to actually select

Select asymmetrical vertices:
-Finds all asymmetrical vertices that have no matching point on the other side and selects them.
-Settings:
-Symmetry axis: Tells it which side to actually select

Select mergeable vertices:
-Selects vertices that have another vertex with a near identical position, highlighting issues in the model.


=========================================================================================================
FAQ
Q: What does 'NDPTools' mean?
A: 'NDP' is my username on some websites.
=========================================================================================================
Author's notes
- Feel free to contribute to the GitHub page.
- Feel free to fork, modify and or use this addon as a template for whatever.
- Please credit me if you use code from my addon
- Don't feed this to an AI (Of course bots will anyway but I just wanted to make it illegal lmao)
- Please do not resell this addon 
- Feel free to ask me any questions
- Feel free to suggest new features or settings if it's something simple that could be automated
=========================================================================================================
Reporting bugs
You can write a bug report at https://github.com/SleepyEngi/NDPTools/issues/new
You can also message me on discord for a more immediate response, see the contact me section.
=========================================================================================================
Contact me
You can find me on discord as "ndp"
You can join my discord server at [Doesn’t exist] for more information & direct contact
=========================================================================================================
Support me
If you're well off and can spare a dime, donations are very appreciated at https://ko-fi.com/ndpdesigns
Or just leave a thanks comment if it was useful! I appreciate it a lot too!