# Installation — QC Bake for Maya

This is a tool for **Maya**, not Blender. It installs by dragging one file.

## What you need

Maya **2025**.

## Step 1. Download and unpack

1. Download [`qc_bake_maya.zip`](https://mutaform.github.io/qc-bake-maya/qc_bake_maya.zip)
2. Unpack it **somewhere it will stay for good**: a tools folder, a network
   share, any permanent place

!!! warning "Where you unpack it is where it lives"
    The unpacked folder **is** the installation. Nothing is copied into Maya's
    internal directories: Maya only gets a pointer to that folder.

    Two consequences. Updating is a matter of replacing one folder. But delete
    or move the folder and the tool falls off — unpack it again and repeat
    step 2.

## Step 2. Drag the installer into Maya

1. Start Maya
2. Open the unpacked folder in the file manager
3. Drag `install/install.py` **into Maya's viewport with the mouse**

The installer registers the module, adds a **QC Bake** button to the *Mutaform*
shelf and opens the panel straight away.

## Step 3. Check that it worked

A **QC Bake** button has appeared on the *Mutaform* shelf; it opens the panel.
Maya picks the tool up on every launch, nothing has to be repeated.

## Updates

The add-on checks for them whenever the panel opens and, if a newer version
exists, shows a bar with an **Install** button at the top. Pressing it downloads
the archive, verifies the checksum, replaces the folder and reloads — **without
restarting Maya**.

The previous version is kept until the new one has loaded, so a broken release
rolls itself back.

To switch the check off or run one by hand: **Options → Updates** in the panel.

## If it did not work

| What you see | What is wrong |
| --- | --- |
| Dragged the file, nothing happened | It has to go into the viewport (the window with the 3D scene), not onto a shelf and not into the Script Editor |
| There is no button on the shelf | Check that the *Mutaform* shelf is the active one: there are many shelves and yours may not be selected |
| The panel opened, but it is gone after restarting Maya | The add-on folder was moved or deleted. Unpack it again and repeat step 2 |

To remove it: run `install.uninstall()` in the Script Editor. The folder itself
is left alone.

## Next

What the add-on does is in the [overview](index.en.md). Every button is broken
down in the [reference](reference.en.md).
