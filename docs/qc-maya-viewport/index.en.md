# QC Maya Viewport

Diagnostic viewport shading: look at the model the way the engine sees it, and
catch problems in baked maps before they travel any further. It also assembles a
material out of a folder of maps, so that there is something to look at.

The add-on does not live in the sidebar. It adds a sphere icon to the 3D
viewport header — that toggles the mode, and the arrow next to it opens the
menu with the settings.

![The menu in the viewport header](img/header-menu.png){ .screenshot }

## Installation

1. `Edit → Preferences → Get Extensions`
2. Gear icon → `Repositories` → `+` → `Add Remote Repository`
3. The URL:

    ```text
    https://mutaform.github.io/qc-maya-viewport/index.json
    ```

Requires Blender 5.1 or newer.

## Modes

| Mode | What it shows | What it is for |
| --- | --- | --- |
| **Normal Only** | the normal map alone, unlit | seams, gradients along UV borders, cage artefacts |
| **Normal + AO** | normals together with occlusion | closest to how the engine will look |
| **AO Only** | occlusion alone | form and volume read clearly, texture does not distract |
| **Roughness Only** | the roughness map, flat | shows where an unexpected highlight or a dead matte patch comes from |
| **Default Material** | one flat grey material | clean silhouette and topology, no maps at all |

Modes are buttons in the menu; the active one is depressed.

On the left, **Normal Only** in Blender; on the right, the same model in Maya's
viewport. That match is the whole point of the add-on: review can happen in
Blender without opening Maya for a second opinion.

![Normal Only in Blender and the same model in Maya](img/mode-normal.png){ .screenshot }

## Assembling a material from a folder

**Find Textures** is the add-on's other half. Select the object, pick a material
slot, press the button: a file browser opens, and the maps in the chosen folder
wire themselves into the Principled BSDF, sorted by the suffixes in their names.

The browser opens on that asset's own folder. Blender does not keep the path an
object was imported from, so the add-on solves it from both ends: anything
imported from now on gets stamped with its path, and whatever is already in the
scene is found by name under the **Project Roots** set in Settings.

What happens to the maps:

- data maps (roughness, metallic, AO) get Non-Color;
- the normal goes through a Normal Map node, height through a Bump node;
- packed maps such as `_ORM`, `_MRO`, `_spec` and `_NRM` are split into channels;
- textures already wired up are repointed, not duplicated.

Utility maps are deliberately left alone: the `_cc` tint mask, the `_curve`,
`_cavity`, `_thickness`, `_objid`, `_matid`, `_position` and `_id` bakes, and
object-space normals.

!!! tip "If some maps were not picked up"
    Naming is the usual reason. Turn off **Match Material Name** and everything
    in the folder is taken, whether or not it resembles the material's name. If
    the project uses a suffix of its own, add a rule in **Settings**.

## Your own suffixes

**Settings**, at the bottom of the menu, opens the suffix table: which tail in a
filename counts as which map. It holds 104 built-in rules with a reset button
beside them. A row can be edited, added, or deleted — a deleted rule really does
stop matching.

The table lives in the Blender preferences rather than the scene file, so it
survives a restart and applies to every scene on the machine. Project Roots are
set there too.

!!! warning "Check that the preferences are being saved"
    The dialog says whether the table is being saved. With Auto-Save Preferences
    off it offers a **Save Preferences** button; without it the edit is dropped
    when Blender exits.

## Normal map convention

At the bottom of the menu is an **OpenGL / DirectX** toggle. This is the
direction of the normal map's green channel:

- **OpenGL** — Y up. Blender, Marmoset and Unreal work this way.
- **DirectX** — Y down. Unity's default, and some in-house engines.

Pick the wrong one and bumps read as dents. That is the first thing to check
when relief looks inside-out.

The toggle switches more than the diagnostic mode: every Normal Map node in the
scene's materials moves with it, node groups included. So an ordinary EEVEE or
Cycles render agrees with the QC viewport instead of disagreeing with it. The
change is a normal edit and undoes with ++ctrl+z++.

Turning the viewer on does the reverse: the convention is read off the scene's
nodes, so viewport and materials never start out disagreeing.

!!! warning "Match the engine, not your gut"
    This is a way to look at the map the way the engine will, not a way to
    repair one baked wrong. If the map was baked in one convention and the
    engine expects the other, the fix belongs in the bake.

## After a re-bake

**Reimport Textures** re-reads the maps from disk. Blender caches textures and
does not pick up changes on its own, so after re-baking in an external tool the
viewport keeps showing the old image until you press this.

## Next

The [interface reference](reference.en.md).
