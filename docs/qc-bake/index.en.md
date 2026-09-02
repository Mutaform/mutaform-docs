# QC Bake

The add-on renames objects into the pairs a baker expects — `asset_low`,
`asset_high`, `asset_cage` — then helps you hide half of each pair, sort the
scene into collections, and merge far-apart assets into shared bake groups.

Everything it does is renaming and re-linking collections. It never touches
geometry.

![The QC Bake panel](img/panel-main.png){ .screenshot }

How to install it is on its own page:
**[Installation](install.en.md)**.

## Quick start

You have a high-poly sculpt and a low-poly mesh for it.

1. Select both. Order does not matter.
2. Press **Create Namepair**.

Done — the objects are now `<name>_low` and `<name>_high`. The base name comes
from whichever object the add-on decided was the low poly, with any old suffix
stripped off.

![Creating a namepair and organising collections](img/create-namepair.gif){ .screenshot }

The recording goes past the quick start: after the renaming it presses **Flat**
and then **Per Asset** — the collection layouts covered further down. Only the
panel and the outliner are in frame, so that the names stay readable.

## Which one is the high poly

With **two** objects selected, the add-on compares their triangle counts and
calls the heavier one the high poly. The count is taken from the evaluated
mesh — modifiers included — so a Subdivision Surface on the low poly can flip
the result.

Change the metric under **Naming → Detect By**: triangles (default), faces or
vertices.

With **three or more** objects selected the add-on stops guessing. The low poly
is the active object — the one selected last, outlined in a lighter colour.
Everything else becomes a high poly and gets numbered:

```text
asset_low
asset_high_01
asset_high_02
asset_high_03
```

!!! tip "If the roles came out backwards"
    Select both objects and press **Swap High / Low**. Faster than renaming by
    hand.

## Cages

A cage is recognised by name: if one of the selected objects **already** ends in
`_cage`, it is kept out of the high/low comparison and simply renamed to
`<base>_cage`.

So the cage has to be named beforehand — `anything_cage` will do. The add-on
never tries to guess a cage from geometry.

Turn it off with **Options → Detect Cage**.

## Naming conventions

Under **Naming → Convention**:

| Preset | Suffixes |
| --- | --- |
| Substance | `_low` `_high` `_cage` |
| Marmoset | identical |
| xNormal | `_lo` `_hi` `_cage` |
| Custom | your own, set in the three fields below |

Substance and Marmoset produce the same result — two names for one preset, kept
for clarity.

![The Naming sub-panel](img/naming.png){ .screenshot }

The choice affects more than renaming. The Visibility panel and both utilities
find their objects by these same suffixes, so after switching presets the older
objects stop existing as far as the add-on is concerned.

## Hiding half the scene

**Visibility** shows and hides objects by role, across the whole scene,
regardless of what is selected.

![The Visibility sub-panel](img/visibility.png){ .screenshot }

Read the buttons like this:

- depressed, with an eye icon — the whole group is in that state;
- neither depressed — some objects are hidden, some are not;
- row greyed out — no objects with that suffix exist in the scene.

## Collection layouts

**Utilities → Collection Layout**. Both buttons work on the entire scene and
pick objects by suffix, so props and helper meshes are left alone.

**Flat** groups by role:

```text
Bake Group
├── High
├── Low
└── Cage
```

**Per Asset** groups by pair:

```text
Bake Group
├── Bake_barrel
├── Bake_crate
└── Bake_pillar
```

In Per Asset mode the collections are colour-tagged: green means the pair has
both a low and a high and is ready to bake; red means something is missing.
Incomplete pairs are visible in the Outliner without expanding anything.

![The Outliner after Per Asset](img/outliner-per-asset.png){ .screenshot }

Switch between layouts as often as you like — each button rebuilds the tree from
scratch and removes collections left empty.

## Many assets in one scene

When a scene holds a dozen small pairs, baking each in its own pass is wasteful.
Assets far enough apart in space cannot project into one another, so they can
share a single bake pass.

That is what **Utilities → Reduce Bake Groups** does. It takes every complete
pair, looks at their bounding boxes, and merges into one group those that sit
further apart than **Minimum Gap**. Members of a merged group share a name:

```text
BakeGroup_01_low
BakeGroup_01_high_01
BakeGroup_01_high_02
BakeGroup_02_low
...
```

![Before and after Reduce](img/reduce-before-after.png){ .screenshot }

Worth knowing:

- Incomplete pairs (only a low, or only a high) are skipped. The status bar
  reports how many.
- The larger **Minimum Gap** is, the more conservative the merge and the more
  groups survive. The default of 0.05 assumes a scene in metres.
- If no safe merge exists, nothing is renamed.

!!! warning "Undoing it"
    The arrow button next to it — **Restore Bake Groups** — puts back the names
    from before the last Reduce pass. The old names are stored on the objects
    themselves, so the undo survives saving and reloading the file and does not
    depend on Blender's undo stack.

    Only the **most recent** pass can be restored. Run Reduce twice and the
    first set of names is gone.

    After restoring, rebuild the collection layout.

## When the add-on complains

| Message | What happened |
| --- | --- |
| `Select at least two mesh objects` | Fewer than two meshes selected. Curves, empties and lights do not count. |
| `Both meshes have the same tris count` | The two objects are indistinguishable by the chosen metric. Change Detect By, or rename by hand. |
| `Need at least two non-cage meshes` | One of the two selected objects was read as a cage, leaving fewer than two candidates. |
| `Name '...' already taken` | The target name belongs to an unrelated object. Rename it — or enable **Allow Name Collisions** and let Blender append `.001`. |
| `Low and high suffixes must differ` | The Custom preset has the same suffix twice. |
| `Need at least two complete bake namepairs` | Reduce found fewer than two complete pairs in the scene. |
| `No safe group reduction found` | Every asset sits too close to the others. Lower Minimum Gap — or there is genuinely nothing to merge. |
| `No named bake objects found` | Nothing in the scene carries the current suffixes. Check which preset is selected. |

!!! danger "About Allow Name Collisions"
    The checkbox lifts the block, but it is also exactly how `asset_low.001`
    ends up in a scene. To a baker that is a different name, and the pair falls
    apart. Only enable it when you know why the name was taken.

## Next

The full list of buttons and settings, with operator identifiers, is in the
[interface reference](reference.en.md).
