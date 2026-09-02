# Installation — Modular Environment Tools

Installs from a file: this add-on has no extension repository.

## What you need

Blender **4.2** or newer.

## Step 1. Get the archive

There is no public download link yet — the
`modular_environment_tools_vX.Y.Z.zip` archive comes from the studio.

!!! info ""
    A third-party add-on: the author is **Kirill Kharichev**, licensed
    GPL-3.0-or-later. The studio keeps its own branch of improvements, and this
    documentation describes that branch. Sources:
    [original](https://github.com/HarichevK/Modular-environment-tools),
    [studio branch](https://github.com/Mutaform/Modular-environment-tools/tree/studio/rework).

## Step 2. Install from file

1. `Edit → Preferences…`
2. Pick **Get Extensions** on the left
3. Click the `▼` icon in the top right corner → **Install from Disk…**
4. Choose the archive you downloaded

## Step 3. Check that it worked

Press **++ctrl+shift+m++** in the viewport — the panel pops up under the cursor.

That is the intended way to work: the add-on is built so as not to occupy screen
space permanently.

!!! tip "If you prefer a tab"
    The add-on preferences (`Edit → Preferences → Add-ons`, find **Modular
    Environment Tools**) carry a **Show in the sidebar** tick. With it, a
    **Modular** tab appears in the viewport sidebar with the same contents.

    The shortcut itself is changed there too.

## Updates

An add-on installed from a file does not update itself. A new version is
installed the same way: take the newer archive and repeat step 2 — Blender
replaces the installed one.

## If it did not work

| What you see | What is wrong |
| --- | --- |
| Cannot find `Install from Disk…` | The `▼` icon is in the top right corner of **Get Extensions**, next to the gear |
| Installed, but ++ctrl+shift+m++ opens nothing | The shortcut may be taken by another add-on. Check which one is set in the add-on preferences and change it if needed |
| Blender complains during installation | The Blender version is older than 4.2 |

## Next

What the add-on does is in the [overview](index.en.md). Every button is broken
down in the [reference](reference.en.md).
