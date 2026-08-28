# Installation

All studio add-ons are Blender Extensions. You can install them one by one from
a file, but the right way is to add the repository once and let Blender find the
add-ons and offer updates on its own.

## Add the repository

Done once per machine.

1. `Edit → Preferences → Get Extensions`
2. Gear icon, top right → `Repositories`
3. `+` → `Add Remote Repository`
4. Paste the URL of the add-on you need (see the table below)
5. Tick `Check for Updates on Startup`
6. `Create`

A new source appears in the extension list. Find the add-on by name and press
`Install`.

## Repository URLs

| Add-on | URL |
| --- | --- |
| QC Bake | `https://mutaform.github.io/qc-bake/index.json` |
| Scene QC Validator | `https://mutaform.github.io/qc-validator/index.json` |
| QC Maya Viewport | `https://mutaform.github.io/qc-maya-viewport/index.json` |
| QC Bridge Maya ↔ Blender | `https://mutaform.github.io/qc-bridge-blender-maya/index.json` |

!!! note "Studio Render"
    QC Daily Render is file-install only for now — it has no repository.
    Grab the latest `mutaform_studio_render_vX.Y.Z_extension.zip` and use
    `Install from Disk…`.

## Blender version requirements

The minimums differ because the add-ons lean on different parts of the API.

| Add-on | Minimum Blender |
| --- | --- |
| QC Bridge Maya ↔ Blender | 4.2 |
| Scene QC Validator | 4.5 |
| QC Bake | 5.0 |
| QC Maya Viewport | 5.1 |
| QC Daily Render | 5.2 |

Blender refuses to install an extension into a version below its minimum — if an
add-on does not show up in the list, check the Blender version first.

## Updating

With `Check for Updates on Startup` enabled, Blender checks on launch and shows
what is available under `Get Extensions`. Manually: `Get Extensions` → gear →
`Check for Updates`.

## Finding the installed version

The version is printed on the right of the add-on's own panel header:
`ver 2.0.0`. It is read from the installed extension's manifest, so it is always
the real one.

You need that number to pick the matching documentation — the version switcher
sits in the site header.

## Installing from a file

Useful when you need a specific version, or have no network access.

1. `Edit → Preferences → Get Extensions`
2. The `▼` arrow, top right → `Install from Disk…`
3. Pick the add-on's zip

An add-on installed from a file will not update itself.

## The Maya half of the bridge

QC Bridge has a second half that lives in Maya and installs separately — copy an
archive into your `scripts` folder and run the shelf installer. The steps are in
the bridge's own section.
