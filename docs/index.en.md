---
hide:
  - navigation
---

# Mutaform Add-ons

Studio add-ons for Blender and Maya: bake preparation, pre-export scene
validation, studio rendering, a diagnostic viewport, Maya interchange, modular
environment building and modelling to the studio rules.

These docs are generated from the add-on sources, so the list of buttons and
settings in each reference always matches the released version. Pick a docs
version in the header — if you are running an older add-on, switch to its
version.

<div class="addon-grid" markdown>

<div class="addon-card" markdown>
### [QC Bake](qc-bake/index.en.md)
Names and collections for baking: high/low pairs, cages, group reduction.
</div>

<div class="addon-card" markdown>
### [Scene QC Validator](qc-validator/index.en.md)
A checklist of scene and mesh checks before export.
</div>

<div class="addon-card" markdown>
### [QC Daily Render](qc-daily-render/index.en.md)
One-click Marmoset-style studio render.
</div>

<div class="addon-card" markdown>
### [QC Maya Viewport](qc-maya-viewport/index.en.md)
Maya-style diagnostic viewport shading.
</div>

<div class="addon-card" markdown>
### [QC Bridge Maya ↔ Blender](qc-bridge/index.en.md)
Scene interchange between Blender and Maya over FBX.
</div>

<div class="addon-card" markdown>
### [QC Bake for Maya](qc-bake-maya/index.en.md)
The same QC Bake, inside Maya.
</div>

<div class="addon-card" markdown>
### [Modular Environment Tools](modular-environment-tools/index.en.md)
Modular environments for an engine: a module library and collisions.
</div>

<div class="addon-card" markdown>
### [QC Smart Cylinder](qc-smart-cylinder/index.en.md)
Cylinders with the segment count their diameter calls for, and repairs for
existing ones.
</div>

</div>

## Start here

New to the studio? Start with the [installation page](install.en.md): pick the
add-on you need and follow the steps written out for it.

Most Blender add-ons install the same way: add the repository once, and the
add-on installs and updates from inside Blender. Three are different —
**QC Bake for Maya** (it lives in Maya), **QC Bridge** (two halves, one in
Blender and one in Maya) and **Modular Environment Tools** (installs from a
file).

## How the docs are organised

Each add-on has three pages.

**Installation** — what to download, where to click and how to check that it
worked. Needed once, but worth returning to on a new machine.

**Overview** — how to use it: where to start, the common scenarios, and what to
do when the add-on complains. Read once.

**Reference** — what every button and setting does, with exact defaults and
ranges. Come back to it for details.

## Found a mismatch

If an add-on behaves differently from what is written here, that is a
documentation bug worth reporting. Check the version first — it is shown on the
right of the add-on's panel header and in the reference heading. If the versions
match but the behaviour does not, say so in the studio chat.
