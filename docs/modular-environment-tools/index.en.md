# Modular Environment Tools

A tool for building modular environments for a game engine. It keeps a library
of unique modules, makes draft collisions in the Unreal convention, puts names
in order and checks the scene before export.

!!! info ""
    The author is **Kirill Kharichev**, licensed GPL-3.0-or-later. The studio
    keeps its own branch of improvements and sends them back to him; this
    documentation describes that branch. The original lives
    [here](https://github.com/HarichevK/Modular-environment-tools), the studio
    branch [here](https://github.com/Mutaform/Modular-environment-tools/tree/studio/rework).

![The Modular Environment Tools panel](img/popup.png){ .screenshot }

How to install it is on its own page:
**[Installation](install.en.md)**.

## Opening the panel

**++ctrl+shift+m++** in the viewport — the panel pops up under the cursor.

That is the intended way: the tool is built so as not to occupy screen space
permanently. The shortcut is changed in the add-on preferences.

!!! tip "If the popup does not suit you"
    The preferences carry a **Show in the sidebar** tick. With it, a **Modular**
    tab appears in the sidebar of the 3D viewport with the same contents.
    Switching the tab off breaks nothing: the shortcut keeps working.

## The idea: a library of modules

The add-on assumes a modular kit is arranged like this: the scene holds a
collection of unique meshes — the **library** — and everything else is placed as
instances, objects sharing the same data.

Hence most of the **Modules** section:

- **Select unprocessed modules** — what in the scene is not filed in the library;
- **Select unused modules** — which modules sit in the library for nothing;
- **Select instances** — where this particular module stands across the scene;
- **Count unique modules** — how many different modules a piece of level uses.

The library is named in the **Library** field. Only **Add selected to library**
may create it — the other tools say plainly when they cannot find it rather than
making one behind your back.

## Collisions

**Make collision draft** turns the selected meshes into draft hulls: the copy is
parented to the original, gets the collision material and a modifier stack —
convex hulls per island, a simplification pass and a pull inwards.

The stack stays live until **Apply modifiers** is switched on, and that is the
working mode: edit a module, then **Rebuild collisions** with nothing selected
regenerates every outdated collision in the scene at once.

Three selections then answer "what to rebuild" and "what to throw away":

| Button | What it selects |
| --- | --- |
| **Generated** | everything the add-on generated |
| **Outdated** | collisions whose module was edited afterwards |
| **Orphans** | collisions whose module is gone from the file |

!!! warning "Names matter more than they look"
    The engine ties a collision to its mesh by name. Rename modules and run
    **Sync collision names**, or the link breaks silently.

Shape is checked with **Select incorrect collision** (non-manifold and flattened
islands) and **Select box shaped collision** (hulls that are really plain boxes —
cheaper for the engine as `UBX`).

## Sizes in names

The **Naming** section appends dimensions to a name: `Wall_200_300`. Axes are
picked with toggles, the order with a field of its own.

Two things worth knowing up front:

- the default order is **XZY**, not XYZ: in a modular kit width and height
  matter more than depth;
- **Round to** is a rounding step, not a number of digits. At a step of 10 the
  sizes land on tens of centimetres, which is what a modular grid wants.

The panel shows the outcome in advance — under the settings it says what the
active object's name would become. Running it again replaces the sizes instead
of appending them, so the geometry can be edited and the tool run once more.

## Checking before handover

**Validate scene** walks the modules and collisions and fills the report.
Counters beside the header show errors and warnings.

The report can be walked through: clicking a row selects the object, and **All
alike** selects every object with the same finding. That is the way to fix
things in batches — the same mistake usually repeats across a kit.

## Export

**Export selected modules** writes the modules with their collisions to FBX, one
file per module. Live collision stacks are exported evaluated; otherwise the
engine would receive the source mesh instead of the hull.

## Project presets

Settings live in the scene, and a preset carries them between files and artists.
Presets are plain JSON files in a folder named in the preferences: point it at a
share and the whole project sees the same prefixes, units and export folder.

With no shared folder, a preset can be handed over as a file — **Send to file**
and **Import from file** at the bottom of the menu.

## Next

Every button and every setting is broken down in the
[interface reference](reference.en.md).
