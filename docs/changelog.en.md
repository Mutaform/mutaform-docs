# Changelog

The versions these docs were built from. The number in the add-on's panel header should match the one here — if it is lower, switch the docs version in the site header.

| Add-on | Version | Requires |
| --- | --- | --- |
| QC Bake | `2.0.0` | Blender 5.0+ |
| Scene QC Validator by Mutaform Studio | `1.9.2` | Blender 4.5+ |
| QC Daily Render | `1.6.0` | Blender 5.2+ |
| QC Maya Viewport | `0.34.1` | Blender 5.1+ |
| QC Bridge Maya-Blender by Mutaform | `1.1.8` | Blender 4.2+ |
| QC Bake for Maya | `1.2.4` | Maya 2025 |
| Modular Environment Tools | `2.15.0` | Blender 4.2+ |

Each add-on's change history lives in its own repository; it is copied here by hand when the docs are updated.

## QC Bake


### 2.0.0

Major update - accumulated a batch of workflow fixes since 1.1.0, most
notably making Reduce Bake Groups non-destructive.

#### Added
- **Restore Bake Groups**: a new button next to *Reduce Bake Groups* that
  undoes the most recent reduce pass, restoring every renamed object (and
  mesh datablock) to its prior name. The backup is stored on the objects
  themselves, so it survives file save/reload and outlives Blender's native
  undo stack - not just a Ctrl+Z.
- **Per-Asset health colors**: in the *Per Asset* collection layout, each
  `Bake_<name>` collection is now color-tagged in the Outliner - green when
  it holds a complete low/high namepair, red when only a low or only a high
  is present (a member is missing or was accidentally deleted).
- **Version display**: the add-on's version now shows right-aligned in the
  N-panel header ("ver X.Y.Z"), read live from `blender_manifest.toml`.

#### Changed
- **Collection Layout (Flat & Per Asset)**: newly built collections are now
  automatically collapsed in the Outliner after organizing, instead of being
  left fully expanded.

### 1.1.0

- Initial tracked release: namepair creation, swap, visibility toggles,
  reduce bake groups, and Flat / Per Asset collection organizing.

## Scene QC Validator by Mutaform Studio


### 1.9.2

Every UV review is now scoped to one material, because one material is one
texture set. Covers the changes since 1.8.7.

#### Added

- Review Scene: clicking a material name selects every object in the scene that
  uses it and makes it their active material slot.
- Review Scene: the UV button next to a material isolates its faces in Edit
  Mode, so the UV Editor holds that material's UVs alone. Clicking it again
  restores the selection, mode, UV sync setting and edit-mode selection that
  were there before.
- The material list keeps describing the objects that were in scope when a
  review started, so an artist can hop from material to material without a
  'Selection' scope collapsing onto the one under review.
- Show Overlaps, Show Padding and Show Texel Density follow the active material
  slot: picking another slot in the Properties editor (or another material in
  the Review Scene list) re-aims the running review at it, without leaving Edit
  Mode when the same meshes carry that material.
- A line under the three overlay toggles names the material being reviewed, and
  the operator reports name it too.
- The bundled Mutaform_Default project ships the studio checklist for all five
  stages, instead of a stale copy that was missing four checks entirely.

#### Fixed

- Overlaps between two materials on one mesh are no longer reported or drawn as
  overlapping: a second material is a second texture set, free to sit anywhere
  in UV space.
- The padding band follows the reviewed material's footprint. The edge where its
  faces meet another material's counts as an island border, and other
  materials' islands are no longer wrapped in a band of their own.
- Texel density is measured against the average of the reviewed material's faces
  only, so a second material at another scale no longer shifts every colour.
- The UV Editor no longer shows every material's UVs during a review, which is
  what made a multi-material mesh unreadable there.
- Reviews opened from a validation result still cover the whole mesh, matching
  what the checker reported.
- `tools/build_release.ps1` produced an archive with "\" path separators and no
  top-level folder, which only Windows could unpack. It now writes a normal
  `scene_qc_validator/` archive plus a version-stamped copy beside it.

### 1.1.1

- Fixed repeated UV checker restore on objects that originally had no materials.
- Rebuilt the line checker texture as a 1024x1024 asset.
- Added the add-on version label to the main panel header.

### 1.1.0

- Packaged as a Blender Extension.
- Added scene and mesh validation checklist workflow.
- Added preset import/export support.
- Added UV checker assets and controls.
- Added FBX export workflow with Mutaform preset.

## QC Daily Render

_No change history in the add-on repository yet._

## Modular Environment Tools

A third-party add-on by Kirill Kharichev. Below is the studio branch the
documentation is built from; the author's `master` stays at 1.0.0.

### 2.15.0

- **Import from file** and **Send to file** at the bottom of the preset menu. A
  shared folder is the tidy way to pass a preset around; a file is the way that
  always works.

### 2.14.0

- Presets are shareable: plain JSON in a folder named in the preferences. Point
  it at a share or at the project and everyone sees the same presets. Before
  this they went through Blender's own preset system, as Python inside the
  artist's profile, where nobody else could reach them.
- The scene remembers which preset it was set from, and the menu button says so.
- A preset written by another version is used as far as it is understood instead
  of being refused whole.

### 2.13.0 — 2.12.0

- The panel shows in advance what the active object's name will become: reading
  two controls and guessing is work, showing the outcome is not.
- Collisions are skipped when sizes are written: their name follows the module.

### 2.9.0 — 2.11.0

- FBX export: folder, one file per module, axes and scale.
- The validation report filters by severity, a row selects its object, and
  **All alike** selects every object with the same finding.

### 2.0.0

A rework of the whole add-on around three things it did not have: one place for
names, marks on what it generates, and checks that produce a report.

- Sidebar tab **Modular** in the 3D view. The panel had no category before, so
  no tab ever appeared and the README asked the artist to bind it by hand.
- Add-on preferences with an editable **Ctrl + Shift + M** shortcut.
- **Add selected to library**: the one tool allowed to create the library
  collection.
- **Rebuild collisions**, the **Generated / Outdated / Orphans** selections,
  **Show / hide**, **Delete orphans** — all of it possible because generated
  objects are now marked with their source and a fingerprint of it.
- **Validate scene**: a report with severities, a list in the panel, selection
  from a line.
- Settings for what used to be constants: library collection, both prefixes,
  collision material and its colour, dissolve angle, shrink.
- Collisions are numbered: `UCX_Wall_01`, `UCX_Wall_02`.
- A test suite run by Blender itself.

### 1.0.0

The author's first version: a module library, draft collisions, `UCX`/`UBX`
renaming, sizes in names, batch transform apply and unwrapping.

## QC Bake for Maya

### 1.2.4

The shelf icon is built from a real vector, `icons_src/qc_bake.svg`, so every
size is drawn from the source rather than resampled from a bitmap.

It still ships as PNG, and here is why. Maya does accept an `.svg` for a shelf
button, but draws it through Qt, which implements SVG Tiny — no `<mask>`. The
element is ignored and the mask's own contents are painted as artwork, which on
this file floods green across the lettering and leaves a white rectangle behind
it. Measured on a real shelf button: 29% green, 11% white. So the PNGs are
rendered by a browser, which implements the whole spec.

### 1.2.2

**Opening the panel now always checks for updates.** No timestamp, no interval —
only the "Check on Open" switch itself.

1.2.1 tried to be clever: remember when the last check happened and skip recent
ones. Twice on a real install it produced the only outcome that matters — a tool
that knew it was out of date and said nothing. Opening the panel from the shelf
is a deliberate act and the best moment to hear about an update.

### 1.2.0

Its own icon on the *Mutaform* shelf, in place of the default one.

### 1.1.0 — 1.1.4

Self-updating: the panel asks a manifest on GitHub Pages, downloads the archive,
verifies the checksum and swaps the folder without restarting Maya. The previous
version is kept until the new one has loaded.

### 1.0.0

First release: full parity with the QC Bake extension for Blender 2.0.0 —
namepair creation, Swap High / Low, visibility by role, Reduce Bake Groups with a
reversible restore, and both outliner layouts.

Beyond the Blender version, what Maya demanded: **Count Smooth Preview**
(`polyEvaluate` does not see smooth mesh preview), **Track Selection Order**
(Maya has no active object), recognition of Maya's own auto-numbering, and
namespaces preserved through renaming.

## QC Maya Viewport

### 0.34.1

- Put the key light's upward tilt back. 0.34.0 aimed it straight down the view
  axis on the strength of a flat-plane reading, but a plane cannot show where a
  light is. A shaded sphere can: Maya's puts its brightest point 15% of the
  radius above centre, so the light is tilted. Flattening it made the shading
  read as if lit from the wrong side.
- Specular back to 0.30, which is what the tilt needs to reach Maya's peak.

Known difference: Maya's blinn highlight is tighter and peaks about 12/255 above
its surrounding surface, this shader's Blinn-Phong lobe about 5. The lobe shape
differs, not the level.

### 0.34.0

- **Maya's view transform is reproduced, so the whole grey ramp matches, not
  just one point.** 0.33.0 matched the mid grey by lowering the diffuse level,
  but Maya runs its viewport through a tone curve (ACES 1.0 SDR-video by
  default) and no single multiplier can follow that. The curve was measured out
  of Maya — a surfaceShader stepped through 16 known values, read back off a
  playblast — and fitted into the shader. Worst error is under 1/255 above black.
- With the curve in place the levels are Maya's own again: diffuse 0.4 (blinn
  colour 0.5 x diffuse 0.8) and a 0.22 highlight.
- `Settings` gained a **Maya Tone Curve** switch beside the two levels, for a
  Maya set to plain sRGB rather than ACES.

### 0.33.0

- **The viewport greys now match Maya.** The shading levels were guesses; they
  are measured now. A flat plane facing the camera, shaded by a default blinn
  (colour 0.5, diffuse 0.8) under the default headlight, reads 146/255 in Maya
  2025 and 179/255 with the highlight. The QC viewport was painting 183 and 187
  — visibly lighter.
- Both levels are exposed in `Settings` under **Maya Match**.

### 0.32.0

- **Checkbox next to `Find Textures`, on by default.** One press now fills every
  material on every selected object, so a set that arrives as twenty
  one-material meshes takes one press instead of one per material. Untick it to
  go back to filling only the active slot. The state is remembered.
- Fixed: files named per UDIM tile (`bake_1001_ao`, `bake_1002_ao`) were merged
  into a single tiled image, so every material got tile 1001. When the material
  name carries the tile number (`vzor_1002`), the files are treated as separate
  sets and each material takes its own.

### 0.31.0

- **Fixed: Find Textures did not open on the imported mesh's folder.** Two
  things were wrong. The import tracker read the path off the operator history,
  but Blender never puts importers there; it now asks the window manager for the
  properties each importer was last called with, which does hold the path. And
  the handler was not marked persistent, so Blender threw it away the moment a
  .blend was opened.
- When an object carries no recorded path and the name search finds nothing, the
  browser falls back to the folder of the last import rather than opening
  nowhere. That covers everything imported before this version.

### 0.30.4

- **Fixed the viewport going black on part of the scene.** `Roughness Only`
  added five push constants to the shader, which shifted the `MAT3` normalMatrix
  inside the constant block and fed the vertex stage garbage object normals —
  whole objects rendered black in every mode, `Default Material` included.
  normalMatrix is a `MAT4` now, where the padding is unambiguous.
- Every texture is built before any sampler is assigned. Creating one in between
  disturbed the slots already bound.
- An image whose file is missing falls back to flat shading instead of being
  handed to the GPU as a black texture.

### 0.30.1

- Reverted 0.30.0. The header dropdown is a panel popover again: turning it into
  a menu did left-align the labels, but it looked and behaved worse. Blender
  centres button labels in a popover and there is no setting for it.

### 0.29.1

- Turning the viewer on now reads the green-channel convention off the scene's
  Normal Map nodes. The viewport setting is a module global, so it used to reset
  to OpenGL whenever the add-on reloaded while the nodes stayed on DirectX, and
  the two silently disagreed.

### 0.29.0

- **`OpenGL` / `DirectX` now switch the Normal Map nodes as well**, so the
  regular EEVEE and Cycles render agrees with the QC viewport instead of only
  the viewport changing. Every Normal Map node behind the scene's materials
  moves together, node groups included, and the change is undoable.

### 0.28.1

- Fixed a crash in `Find Textures` on any material without a packed map: the
  packed-map builder returned one value where two were expected, so a set of
  plain `_ao` + `_normal` files raised
  `TypeError: cannot unpack non-iterable NoneType object`. The material was left
  half wired; running `Find Textures` again finishes it.

### 0.28.0

- **Find Textures now opens on the object's own asset folder**, not a generic
  browser. Blender throws the import path away, so this works two ways: the path
  of anything imported from now on is recorded on the object, and for everything
  already in the scene the asset is found by name under the project roots you
  set in `Settings`. A hit inside a `Meshes` subfolder climbs out to the folder
  that really holds the maps.
- Object-space bakes (`_normalobj`, `_objnormal`, `_normalworld`,
  `_worldposition`) are ignored like the other utility maps.

### 0.27.0

- **New viewport mode `Roughness Only`**, in the popover right after `AO Only`.
  Shows the roughness map flat, pulling the right channel out of a packed
  `_ORM`/`_MRO`/`_spec` map or out of the blue of an `_NRM` map. A material with
  no roughness reads as mid grey rather than white.

### 0.26.1

- Every edit to the suffix table now flags the preferences as changed. Without
  it, rows added or removed with the `+`/`-` buttons could be dropped on exit by
  Auto-Save Preferences.
- The settings dialog says whether the table is being saved, and offers a
  `Save Preferences` button when auto-save is off.

### 0.26.0

- **New `Settings` entry at the bottom of the popover**: the whole suffix table
  is now editable. Change what a suffix maps to, add your own, or delete one to
  stop it being recognised. Seeded with 104 built-in rules, with a reset button.
- Also reachable as `Suffixes` in the Find Textures sidebar and from the add-on's
  own preferences. Rules are stored in the Blender preferences, so they survive a
  restart and apply to every scene on the machine.

### 0.25.1

- **Fixed: the viewport could get stuck on permanently.** The GPU draw handle
  lived only in a module variable, so reloading or disabling the add-on while the
  viewer ran orphaned the handler — it kept drawing with nothing left able to
  switch it off. The handle is now kept where a reload cannot lose it, stale
  handlers are swept on register, and disabling the add-on shuts the viewer down.

### 0.25.0

- `_spec` is read as a packed **Metalness / Roughness / AO** map, matching the
  studio's own deliveries, instead of a specular level.
- `_cc` (tint-mapping mask) and the bake maps `_curve`, `_cavity`, `_thickness`,
  `_objid`, `_matid`, `_position`, `_id` are never wired up.
- Fixed: a folder picked in the file browser arrives with a trailing separator,
  which stopped the "file with no suffix is the base color" rule from firing.

### 0.24.0

- **`_NRM` support** — the delivery format where R and G hold the normal and B
  holds roughness. Unpacked through a `MVM Unpack NRM` node group that rebuilds
  Z as `sqrt(1 - x² - y²)`; the QC viewport rebuilds the same Z on the GPU. A
  plain `_Normal` plus `_Roughness` in the same folder still win.
- Recognises `_COL` and `_NM`.
- A file with **no suffix at all** is taken as the base color when a suffixed
  sibling with the same name sits next to it.
- When a set has an `_AO` map but nothing for the diffuse, AO goes to Base Color.
- A file in the chosen folder beats the same file in a subfolder, so full-size
  maps win over a `1k/` copy.
- A filename that spells out OpenGL or DirectX now also sets the Normal Map
  node's convention, not just the viewport's.

### 0.23.0

- **New: `Find Textures`.** Select an object and a material slot, pick the folder
  holding the maps, and the textures are linked into the Principled BSDF by their
  filename suffix. Data maps get `Non-Color`, normals go through a Normal Map
  node, height through a Bump node, and packed `_ORM`-style maps are split into
  their channels.
- When several texture sets share one folder, the set whose name matches the
  material is used; with no match, whatever the folder holds is assigned.
- Existing textures in a material are repointed rather than duplicated, and
  `.psd` files only win when nothing else carries the same map.
- Options: search subfolders, match material name, fill every material slot, read
  the normal convention off the filename.

### 0.22.8 and earlier

Diagnostic GPU viewport: `Normal Only`, `Normal + AO`, `AO Only`,
`Default Material`, OpenGL/DirectX normal convention, `Reimport Textures`.

## QC Bridge Maya-Blender by Mutaform

_No change history in the add-on repository yet._
