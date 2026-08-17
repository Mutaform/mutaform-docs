# Установка

Все студийные аддоны — это Blender Extensions. Их можно ставить по одному из
файла, но правильный способ один: добавить репозиторий, после чего Blender сам
находит аддоны и предлагает обновления.

## Добавить репозиторий

Делается один раз на машину.

1. `Edit → Preferences → Get Extensions`
2. Шестерёнка в правом верхнем углу → `Repositories`
3. `+` → `Add Remote Repository`
4. Вставить ссылку нужного аддона (см. таблицу ниже)
5. Поставить галочку `Check for Updates on Startup`
6. `Create`

После этого в списке расширений появится новый источник. Найдите аддон по имени
и нажмите `Install`.

## Ссылки на репозитории

| Аддон | Ссылка |
| --- | --- |
| QC Bake | `https://mutaform.github.io/qc-bake/index.json` |
| Scene QC Validator | `https://mutaform.github.io/qc-validator/index.json` |
| QC Maya Viewport | `https://mutaform.github.io/qc-maya-viewport/index.json` |
| QC Bridge Maya ↔ Blender | `https://mutaform.github.io/qc-bridge-blender-maya/index.json` |

!!! note "Studio Render"
    Mutaform Studio Render пока ставится из файла — репозитория у него нет.
    Возьмите свежий `mutaform_studio_render_vX.Y.Z_extension.zip` и поставьте
    через `Install from Disk…`.

## Требования к версии Blender

У аддонов разный минимум, потому что они опираются на разные части API.

| Аддон | Минимальная версия Blender |
| --- | --- |
| QC Bridge Maya ↔ Blender | 4.2 |
| Scene QC Validator | 4.5 |
| QC Bake | 5.0 |
| QC Maya Viewport | 5.1 |
| Mutaform Studio Render | 5.2 |

Blender не даст установить расширение в версию ниже минимальной — если аддон не
находится в списке, начните с проверки версии самого Blender.

## Обновление

Когда галочка `Check for Updates on Startup` включена, Blender сам проверяет
обновления при запуске и показывает их в `Get Extensions`. Вручную:
`Get Extensions` → шестерёнка → `Check for Updates`.

## Как узнать установленную версию

Версия написана в заголовке панели самого аддона, справа: `ver 2.0.0`. Она
читается из манифеста установленного расширения, то есть всегда настоящая.

Эта же версия нужна, чтобы выбрать правильную документацию — переключатель
версий находится в шапке сайта.

## Установка из файла

Годится, когда нужна конкретная версия или нет доступа в сеть.

1. `Edit → Preferences → Get Extensions`
2. Стрелка `▼` в правом верхнем углу → `Install from Disk…`
3. Выбрать zip-архив аддона

Аддон, поставленный из файла, обновляться сам не будет.

## Maya-часть моста

У QC Bridge есть вторая половина, которая живёт в Maya и ставится отдельно —
скачиванием архива в папку `scripts` и запуском установщика полки. Порядок
описан в разделе самого моста.
