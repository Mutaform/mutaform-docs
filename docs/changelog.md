# Что нового

Версии, из которых собрана эта документация. Номер в заголовке панели аддона должен совпадать с номером здесь — если он ниже, переключите версию документации в шапке сайта.

| Аддон | Версия | Blender |
| --- | --- | --- |
| QC Bake | `2.0.0` | 5.0.0+ |
| Scene QC Validator by Mutaform Studio | `1.8.6` | 4.5.0+ |
| Mutaform Studio Render | `1.5.10` | 5.2.0+ |
| QC Maya Viewport | `0.22.8` | 5.1.0+ |
| QC Bridge Maya-Blender by Mutaform | `1.1.8` | 4.2.0+ |

История изменений каждого аддона ведётся в его собственном репозитории и подтягивается сюда при сборке.

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

## Mutaform Studio Render

_История изменений в репозитории аддона пока не ведётся._

## QC Maya Viewport

_История изменений в репозитории аддона пока не ведётся._

## QC Bridge Maya-Blender by Mutaform

_История изменений в репозитории аддона пока не ведётся._
