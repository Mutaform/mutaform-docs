# Installation

Every add-on has its own installation page, with the link to paste and a
recording of where to click. Pick the one you need:

| Add-on | What it does | Installation |
| --- | --- | --- |
| **QC Bake** | high/low pairs and bake groups | [Blender 5.0+](qc-bake/install.en.md) |
| **Scene QC Validator** | checking a scene before handover | [Blender 4.5+](qc-validator/install.en.md) |
| **QC Daily Render** | a studio render of a model in one press | [Blender 5.1.2+](qc-daily-render/install.en.md) |
| **QC Maya Viewport** | a Maya-like viewport for reviewing maps | [Blender 5.1+](qc-maya-viewport/install.en.md) |
| **QC Bridge Maya ↔ Blender** | moving scenes between the two | [Blender 4.2+ and Maya](qc-bridge/install.en.md) |
| **QC Bake for Maya** | the same QC Bake, inside Maya | [Maya 2025](qc-bake-maya/install.en.md) |
| **Modular Environment Tools** | modular environments for an engine | [Blender 4.2+](modular-environment-tools/install.en.md) |

## How it works

Most of the studio's add-ons are **Blender extensions**, and they install the
same way: add the repository once, and Blender finds the add-on and offers
updates from then on. Each add-on has its own repository; the link is on its
installation page.

Three are different:

- **QC Bake for Maya** lives in Maya and installs by dragging the installer into
  the viewport;
- **QC Bridge** has two halves — an extension in Blender and scripts in Maya,
  and both are needed;
- **Modular Environment Tools** installs from a file: it has no repository.

## Finding the installed version

The version is written on the right of the add-on's panel header: `ver 2.0.0`.
It is read from the installed extension itself, so it is always the real one.

You need it to read the right documentation: if the number in the panel is lower
than the one in the table on the [Changelog](changelog.en.md) page, switch the
documentation version in the site header.

## If nothing installs

The first thing to check is the Blender version itself: `Help → About Blender`.
Blender refuses to install an extension into a version below its minimum, and
the add-on simply never shows up in the list.

The second is network access. If the repository will not load, ask the studio
for the archive and install from file: `Get Extensions` → the `▼` icon in the
top right corner → **Install from Disk…**
