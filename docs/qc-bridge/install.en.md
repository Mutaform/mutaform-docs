# Installation — QC Bridge Maya ↔ Blender

Set it up once; after that Blender offers updates on its own.

## What you need

Blender **4.2** or newer. The version is in the window title, and in
`Help → About Blender`.

## Step 1. Add the repository

This is done **once per machine**. Even if you have added a repository for
another Mutaform add-on, add this one too — each add-on has its own.

1. `Edit → Preferences…` opens Blender's preferences
2. Pick **Get Extensions** on the left
3. Click the gear icon in the top right corner → **Repositories**
4. In the window that opens click **+** → **Add Remote Repository**
5. Paste this into the **URL** field:

    ```text
    https://mutaform.github.io/qc-bridge-blender-maya/index.json
    ```

6. Tick **Check for Updates on Startup**
7. Press **Create**

The repositories window can be closed.

![Adding the repository](../img/install-extension.gif){ .screenshot }

The recording uses one of the add-ons as an example — the sequence of clicks is
the same for all of them, only the URL differs. Yours is the one in step 5 above.

## Step 2. Install the add-on

1. Still in **Get Extensions**, type into the search box at the top:

    ```text
    QC Bridge
    ```

2. The add-on appears in the list — press **Install** beside its name

That is it. Preferences can be closed.

## Step 3. Check that it worked

A blue Maya icon appears in the **3D viewport header**, right after the
Proportional Editing buttons. Clicking it opens the bridge menu.

![The bridge button in the viewport header](../qc-bridge/img/header-button.png){ .screenshot }

!!! note "There is no sidebar tab any more"
    Before 1.2.0 the bridge lived in a **QC Maya Bridge** tab in the
    sidebar. If you updated from an older version and are looking for it —
    it was removed on purpose, everything moved into this menu.

If the panel is there, the installation is done.

## Updates

Blender checks for them at startup, because step 1 ticked **Check for Updates on
Startup**. A new version shows up in `Get Extensions` with an **Update** button.

To check by hand: `Get Extensions` → gear → **Check for Updates**.

The installed version is written on the right of the panel header, like
`ver 1.0.0`. It also tells you whether you are reading the right documentation —
the version switcher is in the header of this site.

## If it did not work

| What you see | What is wrong |
| --- | --- |
| The search finds nothing | The repository was not added, or the URL has a typo. Go back to step 1 and check the whole address |
| The add-on is listed but `Install` does nothing | Your Blender is older than **4.2**. Update Blender |
| It installed but there is no button | The bridge lives in the **3D viewport header**, not in the sidebar: a blue Maya icon right after the Proportional Editing buttons. If the header is narrow, some buttons in it are hidden — scroll it with the mouse wheel |
| The repository list is empty | No network access, or a proxy blocks it. Ask the studio for the archive and install from file: `Get Extensions` → the `▼` icon top right → **Install from Disk…** |

## The other half — in Maya

The bridge has two halves and **both are needed**. The steps above installed the
Blender half; now Maya. It installs by dragging one file.

1. Download [`mutaform_bridge_maya.zip`](https://mutaform.github.io/qc-bridge-blender-maya/mutaform_bridge_maya.zip)
2. Unpack it **somewhere it will stay for good**: a tools folder, a network
   share — anywhere permanent
3. Start Maya and drag `install/install.py` from the unpacked folder **into the
   viewport with the mouse**

The installer registers the Maya module and adds a **QC Bridge** button to the
*Mutaform* shelf. This is done once; Maya picks the bridge up on every launch
after that.

!!! warning "Where you unpack it is where it lives"
    The unpacked folder **is** the installation: Maya only gets a pointer to it.
    Move or delete the folder and the bridge falls off — unpack it again and
    drag `install.py` once more.

!!! danger "If the bridge was already installed — versions 1.1.x"
    The Maya half used to install differently: the folder was copied into
    `scripts\` and the button was created by running code in the Script Editor.
    The 1.2.0 installer clears that away itself — it removes the old buttons
    from the shelves, deletes the old copy from `scripts\` and unloads it from
    Maya's memory.

    Nothing extra to do, but worth knowing: **the button moved**. It used to sit
    on the *Polygons* shelf; now it is on *Mutaform*, next to QC Bake and the
    validator.

## Updating the Maya half

The bridge checks for updates every time its panel opens. When a newer version
exists, a bar with **Install** and **Skip** appears at the top. **Install**
downloads the archive, verifies the checksum and swaps the folder — without
restarting Maya. The previous version is kept until the new one has loaded.

To switch the check off or run one by hand: **Settings → Updates** in the bridge
panel.

!!! warning "Both sides must point at the same folder"
    The one condition for the bridge to work: **the exchange folder is the same
    in Blender and in Maya**. If a transfer does nothing, check that first.

## Next

What the add-on does is in the [overview](index.en.md). Every button is broken
down in the [reference](reference.en.md).
