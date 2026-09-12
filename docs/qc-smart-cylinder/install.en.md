# Installation — QC Smart Cylinder

Installed once; after that Blender offers the updates itself.

## What you need

Blender **4.2** or newer. The version is in the Blender window title, and in
`Help → About Blender`.

## Step 1. Add the repository

This is done **once per machine**. If you have already added a repository for
another Mutaform add-on, add this one too — every add-on has its own.

1. `Edit → Preferences…` — Blender's settings open
2. Pick **Get Extensions** on the left
3. Click the gear icon in the top-right corner → **Repositories**
4. In the window that opens click **+** → **Add Remote Repository**
5. Paste this link into the **URL** field:

    ```text
    https://mutaform.github.io/qc-smart-cylinder/index.json
    ```

6. Tick **Check for Updates on Startup**
7. Press **Create**

The repositories window can be closed.

![Adding the repository](../img/install-extension.gif){ .screenshot }

The recording shows one of the other add-ons — the buttons are the same for all
of them, only the link differs. Yours is the one in step 5 above.

## Step 2. Install the add-on

1. Still in **Get Extensions**, type this into the search box at the top:

    ```text
    QC Smart Cylinder
    ```

2. The add-on appears in the list — press **Install** to the right of its name

That is it. Blender's settings can be closed.

## Step 3. Check that it worked

This add-on adds no panel and no tab. It adds **one menu item**: in the
viewport press ++shift+a++ → **Mesh** and look down the list.

**qc Smart Cylinder** should sit directly under the ordinary **Cylinder**.

![The item in the Add → Mesh menu](img/menu.png){ .screenshot }

If it is there, the installation went through.

## Updates

Blender checks for them at startup because **Check for Updates on Startup** was
ticked in step 1. When a new version comes out it shows up in `Get Extensions`
with an **Update** button.

To check by hand: `Get Extensions` → gear icon → **Check for Updates**.

The installed version is in `Edit → Preferences… → Add-ons → QC Smart
Cylinder`, the **Version** row. You also need it to tell whether you are
reading the right documentation — the version switch is in this site's header.

## If it did not work

| What you see | What is wrong |
| --- | --- |
| The search finds nothing | The repository was not added, or the link has a typo. Go back to step 1 and check the whole address |
| The add-on is listed but `Install` does nothing | Your Blender is older than **4.2**. Update Blender |
| It installed but there is no menu item | Look in `Add → Mesh`, not in the top-level `Add`: the item sits among the primitives, under Cylinder. If it is not there, check in `Get Extensions` that the add-on is ticked — installing and enabling are two different things |
| The item is there but at the end of the menu | That happens when another add-on replaced the whole `Add → Mesh` menu. It still works exactly the same; only its place in the list moved |
| The repository list is empty | No network access, or a proxy is blocking it. Ask the studio for the archive and install from the file: `Get Extensions` → the `▼` icon in the top right → **Install from Disk…** |

## Next

What the add-on does is in the [overview](index.en.md). Every setting is
covered in the [reference](reference.en.md).
