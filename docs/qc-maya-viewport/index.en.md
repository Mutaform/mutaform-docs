# QC Maya Viewport

Diagnostic viewport shading: look at the model the way the engine sees it, and
catch problems in baked maps before they travel any further.

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
| **Default Material** | one flat grey material | clean silhouette and topology, no maps at all |

Modes are buttons in the menu; the active one is depressed.

![Normal Only mode](img/mode-normal.png){ .screenshot }

## Normal map convention

At the bottom of the menu is an **OpenGL / DirectX** toggle. This is the
direction of the normal map's green channel:

- **OpenGL** — Y up. Blender, Marmoset and Unreal work this way.
- **DirectX** — Y down. Unity's default, and some in-house engines.

Pick the wrong one and bumps read as dents. That is the first thing to check
when relief looks inside-out.

!!! warning "Match the engine, not your gut"
    The toggle only changes how Blender displays the map. If the map was baked
    in one convention and the engine expects the other, the fix belongs in the
    bake, not on this button.

## After a re-bake

**Reimport Textures** re-reads the maps from disk. Blender caches textures and
does not pick up changes on its own, so after re-baking in an external tool the
viewport keeps showing the old image until you press this.

## Next

The [interface reference](reference.en.md).
