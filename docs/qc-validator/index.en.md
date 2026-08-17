# Scene QC Validator

A checklist of scene checks to run before handing work off. The add-on puts a
model through a set of rules — topology, transforms, UVs, materials, naming —
and hands back a list of what needs fixing. Some of it is fixed with one button.

The core idea: there is no single set of checks for every situation. Each stage
of the work gets its own. Demanding clean UVs during blockout is pointless;
demanding them before texturing is mandatory.

![The validator panel](img/panel-main.png){ .screenshot }

## Installation

1. `Edit → Preferences → Get Extensions`
2. Gear icon → `Repositories` → `+` → `Add Remote Repository`
3. The URL:

    ```text
    https://mutaform.github.io/qc-validator/index.json
    ```

4. Find `Scene QC Validator` and install it

Panel: press ++n++ in the 3D viewport → **QC Validator** tab. Requires Blender
4.5 or newer.

## First run

A fresh file has no checklist — the panel offers only **Initialize Checklist**.
Press it once and the checks appear, populated from the default project.

After that the order is:

1. Pick a **Scope** — what to check.
2. Apply the stage matching where you are in the work.
3. Press **Validate**.
4. Work through the results.

## Scope

| Scope | What gets checked |
| --- | --- |
| Selection | selected meshes only |
| Visible Scene | every visible mesh in the active scene |
| Entire Scene | every mesh, hidden ones included |

Selection is the default. It is noticeably faster on a heavy scene, and you are
usually working on one asset anyway.

## Stages

A stage is a saved set: which checks are on, at what severity, with which
parameters. Stages are grouped into a project. The add-on ships with the
`Mutaform_Default` project and five stages, getting stricter as you go:

| Stage | Checks enabled | What it adds |
| --- | --- | --- |
| Blockout | 9 | degenerate geometry, transforms, basic UV and naming requirements |
| HighPoly | 11 | topology: non-manifold, non-planar and concave faces, duplicates, animation |
| LP_UVs | 16 | UVs: maps present, hard edges on seams, random sharps |
| Bake | 22 | UV overlaps, pivot centring, materials and their names |
| Textures | 23 | plus the fully-hard-edged geometry check |

The stages are the row of buttons under the Project line. Pressing one applies
it: checks toggle, parameters fill in.

## Where the checklist actually is

!!! warning "The check list is collapsed by default"
    Below the stage buttons there is a **Check Settings** row with an arrow.
    While it is collapsed the checks themselves are not visible at all — only
    the project and stage pickers. This is the first thing people trip over: it
    looks as though there is no checklist.

Expand it and you get the **Mesh / Objects / Mapping / Material** tabs, a count
of enabled checks on the current tab, Select All and Deselect All, the list
itself with a checkbox and severity per check, and below the list a description
of the selected check plus its parameters.

![The checklist with Check Settings expanded](img/checklist.png){ .screenshot }

!!! tip "Your own set"
    Tuned the checklist for a specific job? Save it as a stage (**Save Stage**)
    or as a whole project (**Save Project**). User projects live in the
    extension's folder and never clash with the bundled ones — a bundled
    project cannot be overwritten.

    To hand a set to someone else use **Export Project**, which produces a JSON
    file. On their machine, **Import Project**.

## Reading the results

After **Validate** the status bar at the top gives the verdict: either "all
checks passed" or the number of blocking problems.

Every check carries a severity:

- **Fail** — blocks until fixed;
- **Info** — reports without spoiling the verdict.

Severity is per-check and set in the checklist. If a check is desirable but not
mandatory in your pipeline, move it to Info rather than switching it off — that
way it stays visible.

![The results list](img/results.png){ .screenshot }

Clicking a result row selects the object and drops into edit mode with the
offending vertices, edges or faces selected — when the check recorded where the
problem was.

### Silencing a problem

The **Ignore** button on the row. A silenced problem stops affecting the verdict
and survives re-running `Validate` — the ignore list is stored in the scene,
separately from the results.

An ignore is bound to the pair "object + check". Rename the object and the
ignore no longer applies.

## Auto-fixing

**Fix Me** handles one row, **Fix All** every row that has a fix.

!!! warning "Some fixes change geometry"
    The [reference](reference.en.md) marks, per check, whether its fix is
    destructive. Triangulating n-gons, deleting degenerate faces, applying
    transforms — those modify the model, they do not merely flag it.

    Fix All walks the list in order and takes a while on a heavy scene, which is
    why it shows progress. **Run Validate again afterwards**: some fixes surface
    new findings.

Checks without a fix are the ones where the right answer depends on the job.
`Pivot Not Centered`, for instance: where the pivot belongs depends on how the
asset is placed in the level, and the add-on does not guess.

## Inspecting UVs

Separate from the checklist there are interactive tools. They report nothing
into the results; they show you the state directly in the editor.

**Show Overlaps** highlights UVs sitting on top of each other, on the UV set
number you pick.

**Show Padding** shows what the gaps between islands become at a given texture
size. Change the texture size and the padding value is rescaled proportionally
so the ratio holds.

**Show Texel Density** colours objects by texel density, making the ones out of
scale obvious at a glance.

![The padding preview](img/padding-preview.png){ .screenshot }

!!! tip "Check All Material Users"
    All three tools have this checkbox and it matters more than it looks.
    Without it only the active object is inspected. With it, every visible mesh
    sharing the same material — that is, everything headed for the same atlas.

    Two objects can each be clean on their own and still overlap in the shared
    layout. Without this checkbox that never shows up.

**Toggle UV Checker** puts a checker texture on every material. The original
materials are not harmed — pressing it again puts everything back. Checker
density is adjustable live.

**Select Material Users** selects every visible mesh using the active object's
material.

## Next

The full list of 26 checks, with parameters and the destructive-fix flag, is in
the [interface reference](reference.en.md).
