# What every button does

The add-on has no panel of its own: it adds one item to the `Add > Mesh` menu, and all its settings live in the **Adjust Last Operation** box — the one that opens in the bottom-left corner of the viewport after an action, or with ++f9++. Which settings that box shows depends on what the add-on is doing: building a new cylinder, or rebuilding a selected one. Both sets are covered below, along with the rule table in the add-on preferences.

## Where it lives

One item, directly under the built-in Cylinder.

### Add → Mesh → qc Smart Cylinder

![Add → Mesh → qc Smart Cylinder](img/c/menu-item.png){ .control-shot }

The only way in. The item sits **directly under the built-in Cylinder**, so your hand goes where it always went.

**When you need it.** What it does depends on the selection. Nothing selected — a new cylinder appears at the 3D cursor. A mesh with a cylindrical form selected — the add-on rebuilds it. The mode can be switched afterwards in Adjust Last Operation.

!!! warning "Worth knowing"
    When the selection holds no cylindrical form, the add-on does **not** drop a surprise cylinder beside it — it writes the reason into the report.

## New Cylinder

The settings in Adjust Last Operation when the mode is **New Cylinder**. Change the diameter and the segment count is recomputed on the spot.

### Mode

![Mode](img/c/mode.png){ .control-shot }

Switches between **New Cylinder** and **Fix Selected**.

**When you need it.** When the add-on guessed wrong. Say a cylinder is selected but you want a new one beside it rather than that one repaired: switch to New Cylinder right in the box, without clearing the selection.

**Default:** picked from the selection at the moment of the call

### Diameter

![Diameter](img/c/diameter.png){ .control-shot }

The cylinder's diameter — not its radius. The segment count comes from it.

**When you need it.** The main field in New mode. Type any unit you like: enter `40 cm` and Blender converts it. The scene scale (`Scene → Units → Unit Scale`) is honoured — the rule works in real centimetres, not in nominal units.

**Default:** `0.4 m`, i.e. 40 cm — 36 segments by the table.

### Depth

![Depth](img/c/depth.png){ .control-shot }

The height of the cylinder.

**When you need it.** It has no effect on the segment count: the rule only ever looks at the diameter.

**Default:** `1 m`

### Segments and Edge Length

![Segments and Edge Length](img/c/readout.png){ .control-shot }

Two fields you cannot edit: how many segments the rule produced and how long an edge came out.

**When you need it.** This is how you see what the rule actually does. Drag the diameter and the count climbs in steps while the edge length stays roughly put. That is what the table exists for: one edge length across meshes of every size.

!!! warning "Worth knowing"
    The edge length is the real chord between neighbouring vertices, not the arc length.

### Cap Fill Type

![Cap Fill Type](img/c/cap-fill.png){ .control-shot }

How the ends are closed: **N-Gon**, **Triangle Fan** or not at all.

**When you need it.** The same thing as on the built-in Cylinder, and it means the same. N-Gon is the usual low-poly choice: one face, easy to select and cut into.

**Default:** N-Gon

### Generate UVs

![Generate UVs](img/c/uvs.png){ .control-shot }

Make a plain unwrap right away.

**When you need it.** Leave it on: you will need the unwrap anyway, and a mesh with no UV layer is easy to walk past on the way to baking.

**Default:** on

### Align, Location, Rotation

![Align, Location, Rotation](img/c/transform.png){ .control-shot }

Where the new cylinder lands and how it is turned.

**When you need it.** Blender's standard block, the same on every primitive. **Align: View** faces the cylinder at the camera, **3D Cursor** takes the cursor's rotation.

**Default:** `Align: World`, placed at the 3D cursor.

## Fix Selected

The same operator, but instead of a new cylinder it rebuilds forms that already exist. The add-on switches to this mode by itself when something is selected as you call it.

### Segments — Per Section or Whole Form

![Segments — Per Section or Whole Form](img/c/count-mode.png){ .control-shot }

Whether every section of a form gets its own count, or one count covers the whole form.

**When you need it.** **Per Section** is for parts whose diameter changes: lathed shapes, pipes with reductions, rods with thicker ends. The wide part gets more segments, the narrow one fewer, and the add-on bridges between them with triangles. **Whole Form** is for a part that has to stay one even cylinder with no transitions. The count comes from a single ring, chosen below.

**Default:** Per Section

### Section Step

![Section Step](img/c/section-step.png){ .control-shot }

How much the diameter has to change between neighbouring rings for the add-on to call it the start of a new section.

**When you need it.** Only appears in Per Section mode. Too many sections — raise it; the part split more coarsely than you wanted — lower it.

**Default:** 25 %

!!! warning "Worth knowing"
    A flat ledge between two radii always starts a new section, whatever this number says.

### Diameter From

![Diameter From](img/c/diameter-source.png){ .control-shot }

Which ring sets a section's diameter when its rings differ in size: **Largest Ring**, **Average Ring** or **Smallest Ring**.

**When you need it.** By default the widest ring decides, so the silhouette stays smooth where it shows most. Average is worth having on long cones, where the top ring is far narrower than the bottom one and "by the widest" comes out excessive.

**Default:** Largest Ring

### Manual Segments

![Manual Segments](img/c/manual.png){ .control-shot }

Overrule the rule and rebuild with the count typed in by hand.

**When you need it.** For cases the rule has nothing to do with: the neighbouring part is already built on 24 segments and the new one has to match it. Or a form the add-on skipped as ambiguous — the count can be forced on it.

**Default:** off

!!! warning "Worth knowing"
    The number field is greyed out while the tick is off. Nothing is broken: that is how you see the value affects nothing right now.

### The report

![The report](img/c/report.png){ .control-shot }

Line by line: what the add-on found and what it did with it. One line per form.

**When you need it.** Worth reading always, not only when something went wrong. `40 cm, 36 → 82` is the diameter, before and after; `already right` means the form was correct and was left alone; `no cylindrical form` means the add-on recognised nothing and **broke nothing**.

!!! warning "Worth knowing"
    At most twelve lines are shown; the rest collapse into "… and N more". Forms welded to the rest of the geometry, meshes with shape keys and closed rings of sections are the ones that go unrecognised — these are known limits, not a fault.

## Add-on preferences

`Edit → Preferences… → Add-ons → QC Smart Cylinder`. The rule itself lives here: the table the segment count is computed from.

### The anchor table

![The anchor table](img/c/prefs-anchors.png){ .control-shot }

The rule itself: how many segments at which diameter. The rows are anchor points, not ranges.

**When you need it.** Between anchors the count is interpolated, so there are more steps than rows: 15 cm → 24, 30 → 32, 50 → 38. Outside the table the edge length of the nearest anchor is kept — below 10 cm the count falls in proportion to the diameter, above 100 cm it grows the same way.

**What happens.** The buttons on the right: **+** adds an anchor 10 cm above the largest, **–** removes the selected one, the circular arrow restores the studio table. An edit takes effect at once, on new cylinders and on rebuilds alike — the rule is read on every call.

**Default:** the studio table: 10 cm → 20, 20 → 28, 40 → 36, 60 → 40, 80 → 48, 100 → 68.

!!! warning "Worth knowing"
    The table lives in Blender's preferences, not in the scene file: it is shared by every scene on this machine and survives a restart. If you tailor it to one project, remember that the next project on the same machine sees the same numbers.

### Minimum Segments and Even Counts Only

![Minimum Segments and Even Counts Only](img/c/prefs-limits.png){ .control-shot }

The floor under the segment count, and rounding to an even number.

**When you need it.** The minimum keeps very small parts from degenerating: without it the rule would hand a 2 cm diameter a four-sided shape. Even counts keep the cylinder symmetric on both axes, which makes it easier to cut in half and mirror.

**Default:** minimum 6, even counts on

### Preview

![Preview](img/c/prefs-preview.png){ .control-shot }

What the rule gives at eight representative diameters.

**When you need it.** For checking an edit without leaving the preferences: move an anchor and the line recomputes. Quicker than building test cylinders.

---

*Assembled from `content/qc-smart-cylinder.en.yml`. Screenshots taken in **QC Smart Cylinder 1.6.0**.*
