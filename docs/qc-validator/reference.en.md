# What every button does

Every control in the QC Validator panel, then a table of all the checks, and at the end what those checks look like on a real model.

## The top of the panel

Always visible: the scope, the run button and the status bar above them.

### Scope

![Scope](img/c/scope.png){ .control-shot }

Which objects the run covers.

**When you need it.** Keep it on Selection while working on one asset: it is noticeably faster on a heavy scene. Visible Scene and Entire Scene are for the hand-off, when you need to be sure nothing forgotten is left in the file. The difference between them is one thing: Entire Scene looks at hidden objects too.

**Default:** Selection — selected meshes only.

### Validate

![Validate](img/c/validate.png){ .control-shot }

Runs every enabled check and fills the results list.

**When you need it.** After each meaningful step, not once before the hand-off: the earlier a problem is caught, the cheaper it is to fix.

**What happens.** The status bar above the button turns green ("All checks passed") or red with the number of blocking problems. The list appears below, in the Results fold.

!!! warning "Worth knowing"
    A fresh file has no checklist, and instead of Validate the panel shows **Initialize Checklist**. Press it once — the checks are created from the active project — and the button never comes back.

## Results — working through what was found

The list of problems after a run. Until Validate has been pressed the fold is empty and says so.

### The list filter and Fix All

![The list filter and Fix All](img/c/filter.png){ .control-shot }

On the left, what to narrow the list to; on the right, the "fix everything fixable" button.

**When you need it.** The filter helps on a long list: **Fixable Only** leaves what will close automatically, so you can see how much hand work remains. It affects the display only — the verdict does not change.

**What happens.** Fix All walks the list and fixes everything it can, showing progress. On a heavy scene it is not instant.

**Default:** All Results — every row is shown.

!!! warning "Worth knowing"
    Always run Validate again afterwards. Some fixes alter geometry, and new findings can appear on the changed model — triangulating n-gons, for instance, can produce degenerate faces.

### The list of problems

![The list of problems](img/c/results-list.png){ .control-shot }

Each row is one problem on one object: the object name, the check name and a severity icon.

**When you need it.** Click through the rows. A click does more than highlight the row: the add-on selects the offending object and enters edit mode with the exact vertices, edges or faces that triggered the check already selected.

!!! warning "Worth knowing"
    A red icon is Fail and blocks the hand-off. A crossed-out grey eye is a silenced row that no longer affects the verdict. Severity is set per check in the checklist.

### Ignore / Select / Fix Me

![Ignore / Select / Fix Me](img/c/result-actions.png){ .control-shot }

Actions on the selected row, with a plain-text explanation of what the check found above them.

**When you need it.** **Select** puts the selection back on the offending elements if you have selected something else since. **Fix Me** fixes this row alone and only appears on checks that have a fix. **Ignore** silences the problem.

**What happens.** A silenced row stops affecting the verdict and survives re-running Validate: the ignore list is stored in the scene, separately from the results. The button changes to Restore.

!!! warning "Worth knowing"
    An ignore is bound to the pair "object + check". Rename the object and it detaches, and the problem comes back.

## Checklist — what gets checked

The set of checks lives in a project and is split into stages of the work. The UV inspection tools live here too, but they do not always appear — see below.

### The Project row

![The Project row](img/c/project.png){ .control-shot }

The project picker and three buttons: save the current set as a project, load one from a file, write one out to a file.

**When you need it.** A project is a set of stages. You make your own when the rules differ from the studio's: different naming, different tolerances. To hand a set to someone else, export to JSON and let them import it.

!!! warning "Worth knowing"
    A bundled project cannot be overwritten — saving always creates a user copy in the extension's folder, so the studio set is safe from accidents.

### The stage buttons

![The stage buttons](img/c/stages.png){ .control-shot }

The row of buttons under the project line. Each is a saved set: which checks are on, at what severity, with which parameters.

**When you need it.** Switch as the work progresses. Strictness grows left to right: Blockout enables 9 checks, Textures 23. Demanding clean UVs during blockout is pointless; before texturing it is mandatory.

**What happens.** Pressing one applies it immediately: checkboxes move, parameters fill in. The active stage stays depressed.

!!! warning "Worth knowing"
    LP_UVs is a special case: only on that stage do the three UV inspection tools appear in the panel. On every other stage they simply are not there.

### The small buttons beside the stages

![The small buttons beside the stages](img/c/stage-tools.png){ .control-shot }

A small row of icons: write the current checklist into a stage, save the whole project as a copy, delete a stage.

**When you need it.** When you have tuned the checklist for a particular job and want it back tomorrow.

!!! warning "Worth knowing"
    The delete button only exists for user projects; a bundled one cannot lose a stage.

### Check Settings

![Check Settings](img/c/check-settings.png){ .control-shot }

Opens the checklist itself.

**When you need it.** When you need to switch individual checks on or off, change a severity or adjust a parameter.

**Default:** collapsed

!!! warning "Worth knowing"
    This is the first thing newcomers trip over: while the row is collapsed no checks are visible at all — only the project and stage pickers. It looks as though there is no checklist.

### The Mesh / Objects / Mapping / Material tabs

![The Mesh / Objects / Mapping / Material tabs](img/c/tabs.png){ .control-shot }

Split the checks by kind: geometry, objects and transforms, UVs, materials.

**When you need it.** Simply to avoid scrolling 26 rows. Below the tabs is a count of how many checks are enabled on the current one.

!!! warning "Worth knowing"
    A tab only changes what you see. Validate always runs every enabled check, not just the ones on screen.

### Select All / Deselect All

![Select All / Deselect All](img/c/select-all.png){ .control-shot }

Turns every check on the current tab on or off at once.

**When you need it.** The quick way to build your own set: clear everything, then tick what you need, rather than switching two dozen checkboxes one by one.

### The check list

![The check list](img/c/check-list.png){ .control-shot }

A checkbox enables the check; the dropdown on the right sets its severity.

**When you need it.** Severity is worth changing more often than the checkbox. **Fail** blocks the hand-off, **Info** only reports. If a check is desirable but not mandatory in your pipeline, move it to Info — it stays visible without spoiling the verdict.

!!! warning "Worth knowing"
    Changes apply to the current scene. To carry them across files, save a stage.

### The check description and parameters

![The check description and parameters](img/c/check-params.png){ .control-shot }

The box under the list: a description of the selected check and its settings, where it has any.

**When you need it.** You come here when a check complains about something that is normal in your project. Object Name Pattern, for instance, is a regular expression — this is where you match it to your own naming.

!!! warning "Worth knowing"
    Most checks have no settings and the box shows only the description. What each parameter means differs per check; it is spelled out in the table below.

## UV inspection tools

Three interactive tools. They report nothing into the results; they show the state directly in the UV editor.

### Show Overlaps

![Show Overlaps](img/c/show-overlaps.png){ .control-shot }

Highlights UV islands sitting on top of each other in the UV editor.

**When you need it.** When the Overlapped UV check has reported an overlap and your eyes cannot find it. The results list only says an overlap exists — this shows where.

![Show Overlaps — результат](img/g/uv-overlaps-pair.png){ .screenshot }

!!! warning "Worth knowing"
    The checkbox on the left matters more than it looks. Without it only the active object is inspected; with it, every visible mesh sharing the same material — that is, everything headed for the same atlas. Two objects can each be clean and still overlap each other, and without this checkbox that never surfaces. The UV set field on the right is the set number, counting from one.

### Show Padding

![Show Padding](img/c/show-padding.png){ .control-shot }

Shows what the gaps between islands become at a given texture size.

**When you need it.** Before baking, to see whether neighbouring islands will bleed into each other. The arrows change two numbers: texture size on the left, padding in pixels on the right.

![Show Padding — результат](img/g/uv-padding-pair.png){ .screenshot }

!!! warning "Worth knowing"
    Changing the texture size rescales the padding proportionally — the ratio holds and there is no arithmetic to do in your head.

### Show Texel Density

![Show Texel Density](img/c/show-texel.png){ .control-shot }

Colours objects by texel density.

**When you need it.** With several assets in a scene, to confirm they share a UV scale. An object that is out of line shows up immediately by colour — on the texture it would appear as a difference in detail sharpness.

## Review Scene — materials and the checker

Collapsed by default. Inside: a breakdown of the materials in the scene, and a checker texture for judging UVs.

### The material list

![The material list](img/c/materials.png){ .control-shot }

Every material in the current scope: how many objects and slots use it, with a selection button on the right.

**When you need it.** Before baking, to see what will end up in one atlas. The button selects every visible mesh using that material.

!!! warning "Worth knowing"
    The list follows the chosen Scope. With Selection it shows only the materials of the selected objects.

### Checker Tiling

![Checker Tiling](img/c/checker-tiling.png){ .control-shot }

Checker texture density.

**When you need it.** Adjusts live while the checker is on. A fine checker shows stretching more precisely; a coarse one makes the overall scale clearer.

**Default:** 0.25

### Square Checker / Line Checker

![Square Checker / Line Checker](img/c/checker-buttons.png){ .control-shot }

Put a test texture on every material: a checker or stripes.

**When you need it.** The checker shows stretching and scale, the stripes show UV direction and skew. Pressing again removes the texture.

!!! warning "Worth knowing"
    The original materials are not harmed — the add-on remembers them and puts them back. Still, do not save a file with the test texture on: it is easy to forget and hand the asset over in that state.

## Every check

Labels and the auto-fix flag come straight from the add-on, so the table cannot drift from what you see in the panel. "Alters geometry" means the fix edits the model rather than merely flagging the problem.

### Geometry

| Check | What it looks for | Auto-fix |
| --- | --- | --- |
| **Too Much Hard Edge** | Catches a mesh where every edge is marked hard. Usually a leftover from an import or from Shade Flat applied to the whole model. | yes |
| **N-Gons** | Faces with more than four vertices. The fix triangulates them. | yes, alters geometry |
| **Non-Manifold Geometry** | Invalid topology: edges shared by three or more faces, inverted fans, holes in a solid. The fix splits fans and welds vertices only within each separate piece, so neighbouring parts do not fuse. | yes |
| **Zero Area Faces** | Degenerate faces — area below the tolerance. | yes, alters geometry |
| **Zero Length Edges** | Edges shorter than the tolerance, usually doubled vertices. | yes, alters geometry |
| **Non-Planar Faces** | Quads whose vertices do not lie in one plane. In an engine such a face splits into triangles unpredictably. | yes, alters geometry |
| **Concave Faces** | Faces with a concave corner. | yes, alters geometry |
| **Duplicate Faces** | Two faces on the same set of vertices. | yes, alters geometry |
| **Loose Geometry** | Vertices and edges not part of any face. They are lost on export, or arrive as junk. | yes, alters geometry |
| **Animation Keys** | Animation left on the object, the mesh or its shape keys — dead weight in the FBX of a static asset. | yes |

### Transform

| Check | What it looks for | Auto-fix |
| --- | --- | --- |
| **Unapplied Transform** | Location, rotation or scale differ from the defaults. The fix applies the transform, which moves vertex coordinates. | yes, alters geometry |
| **Pivot Not At World Origin** | The object's origin is not at the world origin. | yes |
| **Pivot Not Centered** | The origin is not centred on the geometry. There is deliberately no fix: where the pivot belongs depends on how the asset is placed in a level. | no |

### UV

| Check | What it looks for | Auto-fix |
| --- | --- | --- |
| **Missing UV Map** | The mesh has no UV set at all. | no |
| **UV Sets Count** | More UV sets than the parameter allows. | no |
| **Shells Outside 0-1 Square** | Islands have left the first 0-1 tile. An error for an ordinary asset; for a UDIM pipeline the check is switched off. | no |
| **UV Set Names** | Blender's `UVMap` names become `map1`, `map2` — what Maya and some engines expect. | yes |
| **Overlapped UV** | UVs sitting on top of each other. Hits are expanded to whole islands so the selection means something. | yes |
| **Padding** | Not a check but an interactive padding preview. It reports nothing and does not appear in the checklist. | no |
| **No Hard Edge On UV Borders** | Every edge on an island border must be hard. Otherwise a gradient runs along the seam on the baked normal. | yes |
| **Random Sharp** | The reverse check: hard edges with no UV border under them. Such an edge creates a needless seam in the normals. | yes |
| **Unaligned UV Edges** | Island borders off-axis by fractions of a degree, on layouts that are otherwise rectilinear. Invisible to the eye, but the texture comes out ragged along that edge. | yes |

### Naming

| Check | What it looks for | Auto-fix |
| --- | --- | --- |
| **Object Name Pattern** | The object name must match a regular expression. | yes |

### Material

| Check | What it looks for | Auto-fix |
| --- | --- | --- |
| **Missing Material** | No material assigned to the object or to some of its faces. | no |
| **Material Count** | More materials on one mesh than allowed. | no |
| **Material Name** | Material names must match the pattern. | yes |

## What it looks like on a model

On the left, what gets highlighted when you click a result row. On the right, what remains after Fix Me. Every frame comes from a real validator run on deliberately broken geometry.

### N-Gons

![N-Gons](img/g/ngons.png){ .screenshot }

The cylinder caps are ten-vertex faces. The fix triangulates them and leaves the side quads alone.

### Loose Geometry

![Loose Geometry](img/g/loose.png){ .screenshot }

A vertex and an edge belonging to no face. You cannot see them in the scene until you turn on the wireframe or click the result row.

### Non-Manifold Geometry

![Non-Manifold Geometry](img/g/non-manifold.png){ .screenshot }

Three faces meeting on one edge. The edge itself is highlighted, which points straight at where the piece was built wrong.

### Concave Faces

![Concave Faces](img/g/concave.png){ .screenshot }

A face with a concave corner. The fix splits it into convex ones.

### Non-Planar Faces

![Non-Planar Faces](img/g/non-planar.png){ .screenshot }

A quad with one vertex lifted out of the plane of the others. The fix splits the face so the engine has nothing left to guess.

### Zero Area Faces

![Zero Area Faces](img/g/zero-area.png){ .screenshot }

A face with no area: two of its vertices sit in the same spot. It is invisible on the model and turns into junk on export.

### Zero Length Edges

![Zero Length Edges](img/g/zero-length.png){ .screenshot }

An edge between two coincident vertices. The fix welds them.

### Duplicate Faces

![Duplicate Faces](img/g/duplicate-faces.png){ .screenshot }

Two faces on the same set of vertices. The model looks fine, but at bake time those faces fight over the same texels.

### Too Much Hard Edge

![Too Much Hard Edge](img/g/hard-edges.png){ .screenshot }

A sphere with every single edge marked hard. The fix clears the marks and the smoothing comes back.

### Pivot Not Centered

![Pivot Not Centered](img/g/pivot-center.png){ .screenshot }

The object's origin sits away from its geometry. There is deliberately no fix: where the pivot belongs depends on how the asset is placed in a level, and the add-on will not guess for you.

### Show Overlaps

![Show Overlaps](img/g/uv-overlaps-pair.png){ .screenshot }

On the left the ordinary UV view: the overlap is there but the eye will not catch it. On the right Show Overlaps is on and the intersection is filled with colour.

### Show Padding

![Show Padding](img/g/uv-padding-pair.png){ .screenshot }

On the right, the islands that lack clearance from their neighbours at the chosen texture size. Baked as-is, those islands bleed into one another.

---

*Assembled from `content/qc-validator.en.yml`. Screenshots taken in **Scene QC Validator by Mutaform Studio 1.8.6**.*
