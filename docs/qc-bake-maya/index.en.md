# QC Bake for Maya

The same QC Bake as the Blender one, inside Maya. It brings objects to the names
a baker understands — `asset_low`, `asset_high`, `asset_cage` — and from there
hides half of a pair, organises the outliner and merges widely separated assets
into shared bake groups.

Everything it does is renaming and regrouping. It never touches geometry.

![The QC Bake for Maya panel](img/panel-main.png){ .screenshot }

How to install it is on its own page:
**[Installation](install.en.md)**.

## Quick start

You have a high-poly sculpt and a low-poly model for it.

1. Select both. Order does not matter.
2. Press **Create Namepair**.

Done: the objects are now `<name>_low` and `<name>_high`. The name comes from
whichever object was taken for the low, with any old suffix cut off.

The line under the buttons reads before you press: it says how many meshes are
selected and which one is taken for the high.

## Which one is the high

With **two** objects selected, mesh density is compared and the one with more
triangles becomes the high. The measure is switched in **Naming → Detect By**:
triangles, faces or vertices.

With **three or more**, one object is the low and the rest are numbered:

```text
asset_low
asset_high_01
asset_high_02
```

Which one becomes the low depends on the **Track Selection Order** option.

!!! tip "Different from Blender"
    Blender has an active object — the one selected last, outlined in white.
    Maya has no such notion, and by default does not record selection order at
    all. The **Options → Track Selection Order** tick switches that recording
    on: then the low is whatever was selected last. While it is off, the low is
    chosen by mesh weight.

If the roles come out wrong, **Swap High / Low** exchanges them.

## The smoothed mesh

One tick has no counterpart in the Blender version: **Naming → Count Smooth
Preview**.

Maya shows a smoothed model on the ++3++ key, but `polyEvaluate` does not see
that smoothing and counts the base mesh. A high you are viewing smoothed looks
light to the add-on and easily loses to the low on triangles. The tick makes it
count what is on screen.

## Hiding half the scene

The **Visibility** section shows and hides objects by role, across the whole
scene at once and regardless of the selection. A role with nothing in the scene
is greyed out: until Create Namepair has run, every row is inactive.

!!! note "Why display layers"
    The add-on does not set visibility on objects directly; it creates layers.
    That is why it **does not overwrite what you hid by hand**: turning a role
    back on restores the previous state rather than what the tool thought was
    right.

    **Clear QC Bake Layers** removes those housekeeping layers before the scene
    is handed off. Names and objects are unaffected.

## Organising the outliner

**Utilities → Collection Layout**. Both buttons work on the whole scene and pick
objects by suffix, so props and helper geometry are left alone. Grouping moves no
geometry.

**Flat** sorts everything by role:

```text
Bake_Group
├── High
├── Low
└── Cage
```

**Per Asset** sorts by pair:

```text
Bake_Group
├── Bake_barrel
├── Bake_crate
└── Bake_pillar
```

In Per Asset mode groups are colour-tagged: green when the pair is complete and
ready to bake, red when a member is missing or a stranger sits inside.

## Many assets in one scene

When a scene holds a dozen small pairs, baking each in its own pass is wasteful.
Assets far enough apart in space do not project into one another, which means
they can share a bake pass.

That is **Utilities → Reduce Bake Groups**. It takes every complete pair, looks
at the bounding boxes and merges those standing further apart than **Minimum
Gap**.

```text
BakeGroup_01_low
BakeGroup_01_high_01
BakeGroup_01_high_02
BakeGroup_02_low
...
```

!!! warning "The undo survives a restart"
    The arrow beside the button restores the names as they were before the last
    run. The old names are stored in the scene itself, so the restore works
    tomorrow too, long after Maya's undo stack is empty.

    Only the **last** run is restored. Run Reduce twice and the first set of
    names is gone.

## Updates

Maya has no add-on repository, so the update check lives in the panel. Every
time it opens, the tool asks a manifest on GitHub Pages whether a newer version
exists. The check runs in the background and stays quiet if it fails.

When there is a new version, a bar with an **Install** button appears at the top.
Pressing it downloads the archive, verifies it against the checksum, unpacks it
and swaps the folder — **without restarting Maya**. The previous version is kept
until the new one has loaded, so a broken release rolls itself back.

To switch the automatic check off or run one by hand: **Options → Updates**.

## How it differs from the Blender version

Functionally it is the same tool. Three things work differently, and all three
are deliberate:

| | Blender | Maya |
| --- | --- | --- |
| Settings | in the scene | in `optionVars`, so they follow the artist rather than the file |
| Grouping | collections | groups, with display layers doing show and hide |
| Mesh density | counted as-is | a **Count Smooth Preview** tick, because `polyEvaluate` does not see smooth preview |

## Next

Every button and every tick is broken down in the
[interface reference](reference.en.md).
