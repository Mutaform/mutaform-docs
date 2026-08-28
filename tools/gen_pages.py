"""Сборка страниц справочника из написанного текста.

Прежний генератор пересказывал код: выводил идентификаторы операторов, типы
свойств и диапазоны. Для художника это бесполезно — он не видит ни того, ни
другого. Теперь текст пишется руками под каждый элемент интерфейса
(`content/<slug>.<lang>.yml`), а этот скрипт только собирает из него страницу
и следит, чтобы ни один элемент не остался без описания и без снимка.

Проверка полноты по-прежнему опирается на разбор исходников: список того, что
аддон показывает, берётся из кода, а покрытие — из поля `covers`.

    python tools/gen_pages.py --source-root "D:/Mutaform/Mutaform Addons"
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from extract import (  # noqa: E402
    extract_addon,
    extract_maya_addon,
    extract_registry,
    resolve_package_dir,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
CONTENT_DIR = REPO_ROOT / "content"

LABELS = {
    "ru": {
        "when": "Когда пригодится.",
        "result": "Что получится.",
        "default": "По умолчанию:",
        # Формулировка-заголовок, а не начало фразы: текст в содержании пишется
        # обычным предложением с большой буквы, и «Серая, если Выделено…»
        # читалось бы сломанным.
        "disabled": "Когда неактивна.",
        "note": "Обратите внимание",
        "generated": (
            "Страница собрана из файла `content/{slug}.{lang}.yml`. "
            "Снимки сделаны в **{name} {version}**."
        ),
    },
    "en": {
        "when": "When you need it.",
        "result": "What happens.",
        "default": "Default:",
        "disabled": "When it is greyed out.",
        "note": "Worth knowing",
        "generated": (
            "Assembled from `content/{slug}.{lang}.yml`. "
            "Screenshots taken in **{name} {version}**."
        ),
    },
}


def paragraph(text: str) -> str:
    """Свернуть перенос строк из YAML, сохранив разбиение на абзацы."""
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    return "\n\n".join(" ".join(b.split()) for b in blocks)


def render_control(key: str, control: dict, labels: dict) -> list[str]:
    lines = [f"### {control['label']}", ""]

    shot = control.get("shot")
    if shot:
        lines.append(f"![{control['label']}](img/{shot}){{ .control-shot }}")
        lines.append("")

    lines.append(paragraph(control["what"]))
    lines.append("")

    if control.get("when"):
        lines.append(f"**{labels['when']}** {paragraph(control['when'])}")
        lines.append("")
    if control.get("result"):
        lines.append(f"**{labels['result']}** {paragraph(control['result'])}")
        lines.append("")
    # Снимок результата — то, что видно в сцене ПОСЛЕ нажатия. Нарисованное
    # текстом дерево коллекций такого не заменяет: по настоящему аутлайнеру
    # сразу понятно, где что лежит и какого цвета метка.
    if control.get("result_shot"):
        lines.append(
            f"![{control['label']} — результат](img/{control['result_shot']})"
            "{ .screenshot }"
        )
        lines.append("")
    if control.get("default"):
        lines.append(f"**{labels['default']}** {paragraph(control['default'])}")
        lines.append("")
    if control.get("disabled"):
        lines.append(f"**{labels['disabled']}** {paragraph(control['disabled'])}")
        lines.append("")
    if control.get("note"):
        lines.append(f'!!! warning "{labels["note"]}"')
        for block in paragraph(control["note"]).split("\n\n"):
            lines.append(f"    {block}")
            lines.append("")

    return lines


CHECK_LABELS = {
    "ru": {
        "table": "| Проверка | Что ищет | Автофикс |",
        "rule": "| --- | --- | --- |",
        "fix_no": "нет",
        "fix_safe": "да",
        "fix_hard": "да, меняет геометрию",
        "categories": {
            "GEOMETRY": "Геометрия",
            "TRANSFORM": "Трансформации",
            "UV": "UV",
            "NAMING": "Именование",
            "MATERIAL": "Материалы",
            "NANITE": "Nanite",
        },
    },
    "en": {
        "table": "| Check | What it looks for | Auto-fix |",
        "rule": "| --- | --- | --- |",
        "fix_no": "no",
        "fix_safe": "yes",
        "fix_hard": "yes, alters geometry",
        "categories": {
            "GEOMETRY": "Geometry",
            "TRANSFORM": "Transform",
            "UV": "UV",
            "NAMING": "Naming",
            "MATERIAL": "Material",
            "NANITE": "Nanite",
        },
    },
}


def render_checks(content: dict, registry: list[dict], lang: str) -> list[str]:
    """Таблица проверок: подписи и наличие автофикса берутся из кода,
    человеческое описание — из содержания."""
    labels = CHECK_LABELS[lang]
    block = content.get("checks") or {}
    lines = [f"## {block.get('title', 'Проверки')}", ""]
    if block.get("intro"):
        lines.extend([paragraph(block["intro"]), ""])

    by_category: dict[str, list[dict]] = {}
    for check in registry:
        by_category.setdefault(check.get("category", "?"), []).append(check)

    texts = block.get("items") or {}
    # Порядок известных категорий задан, но перебираем не его, а то, что
    # реально есть в реестре: аддон может завести новую категорию, и жёсткий
    # список молча выкинул бы все её проверки со страницы. Так и случилось с
    # NANITE в 1.8.7 — проверка исчезла из таблицы, и никто бы не заметил.
    preferred = ("GEOMETRY", "TRANSFORM", "UV", "NAMING", "MATERIAL")
    ordered = [c for c in preferred if c in by_category]
    ordered += [c for c in by_category if c not in preferred]

    for category in ordered:
        group = by_category.get(category)
        if not group:
            continue
        lines.extend([f"### {labels['categories'].get(category, category)}", ""])
        lines.append(labels["table"])
        lines.append(labels["rule"])
        for check in group:
            entry = texts.get(check["id"]) or {}
            what = paragraph(entry.get("what") or check.get("description") or "")
            fix = check.get("fix")
            if not (check.get("can_fix") and isinstance(fix, dict)):
                fix_text = labels["fix_no"]
            elif check.get("fix_is_destructive"):
                fix_text = labels["fix_hard"]
            else:
                fix_text = labels["fix_safe"]
            lines.append(
                f"| **{check.get('label', check['id'])}** | {what} | {fix_text} |"
            )
        lines.append("")
    return lines


def render_examples(content: dict, labels: dict) -> list[str]:
    block = content.get("examples")
    if not block:
        return []
    lines = [f"## {block['title']}", ""]
    if block.get("intro"):
        lines.extend([paragraph(block["intro"]), ""])
    for item in block["items"]:
        lines.extend([f"### {item['title']}", ""])
        lines.append(f"![{item['title']}](img/{item['shot']}){{ .screenshot }}")
        lines.append("")
        lines.append(paragraph(item["what"]))
        lines.append("")
    return lines


def render_page(content: dict, addon: dict, slug: str, lang: str) -> str:
    labels = LABELS[lang]
    lines = [f"# {content['title']}", ""]
    lines.append(paragraph(content["intro"]))
    lines.append("")

    for section in content["sections"]:
        lines.append(f"## {section['title']}")
        lines.append("")
        if section.get("intro"):
            lines.append(paragraph(section["intro"]))
            lines.append("")
        for key in section["controls"]:
            control = content["controls"][key]
            lines.extend(render_control(key, control, labels))

    registry = (addon.get("registries") or {}).get("checks")
    if registry and content.get("checks"):
        lines.extend(render_checks(content, registry, lang))

    lines.extend(render_examples(content, labels))

    lines.append("---")
    lines.append("")
    lines.append(
        "*"
        + labels["generated"].format(
            slug=slug, lang=lang, name=addon["name"], version=addon["version"]
        )
        + "*"
    )
    return "\n".join(lines).rstrip() + "\n"


def coverage(content: dict, addon: dict) -> list[str]:
    """Что аддон показывает, но в тексте не описано."""
    covered: set[str] = set()
    for control in content["controls"].values():
        covered.update(control.get("covers") or [])

    problems = []

    for op in addon["operators"]:
        idname = op.get("bl_idname")
        options = op.get("bl_options") or []
        if not idname or "INTERNAL" in options:
            continue
        if idname not in covered:
            problems.append(f"оператор без описания: {idname} «{op.get('bl_label')}»")

    shown: set[str] = set()
    for panel in addon["panels"]:
        shown.update(panel.get("settings") or [])
    for identifier in sorted(shown):
        if identifier not in covered:
            problems.append(f"настройка без описания: {identifier}")

    # Проверки живут в реестре, а не в панели, поэтому в `covers` их не
    # перечисляют — полнота сверяется отдельно. Без этого новая проверка
    # молча попадала бы в таблицу с английским описанием из кода.
    registry = (addon.get("registries") or {}).get("checks") or []
    described = (content.get("checks") or {}).get("items") or {}
    for check in registry:
        if check["id"] not in described:
            problems.append(
                f"проверка без описания: {check['id']} «{check.get('label')}»"
            )

    for key, control in content["controls"].items():
        shot = control.get("shot")
        if not shot:
            problems.append(f"без снимка: {key}")
        for field in ("shot", "result_shot"):
            value = control.get(field)
            if value and not (DOCS_DIR / control["_slug"] / "img" / value).is_file():
                problems.append(f"снимок не найден: {key} -> img/{value}")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--only")
    args = parser.parse_args()

    registry = yaml.safe_load((REPO_ROOT / "addons.yml").read_text(encoding="utf-8"))
    source_root = pathlib.Path(args.source_root)

    failures = 0
    manifest: dict = {"addons": {}}
    for entry in sorted(registry["addons"], key=lambda e: e.get("order", 99)):
        slug = entry["slug"]
        if args.only and args.only != slug:
            continue

        package_dir = resolve_package_dir(source_root, entry["source"])
        if not package_dir.is_dir():
            # Пропустить молча нельзя: справочник собрался бы без этого
            # аддона, а слепок api-manifest.json потерял бы его данные —
            # и то и другое выглядело бы как успешная сборка.
            print(f"  ! {slug}: нет исходников, {entry['source']} не найден под {source_root}")
            failures += 1
            continue
        if entry.get("kind") == "maya":
            addon = extract_maya_addon(package_dir, entry)
        else:
            addon = extract_addon(package_dir)

        registries = {}
        for spec in entry.get("registries") or []:
            registries[spec["key"]] = extract_registry(
                package_dir, spec["module"], spec["variable"]
            )
        if registries:
            addon["registries"] = registries
        manifest["addons"][slug] = addon

        for lang, filename in (("ru", "reference.md"), ("en", "reference.en.md")):
            path = CONTENT_DIR / f"{slug}.{lang}.yml"
            if not path.is_file():
                continue
            content = yaml.safe_load(path.read_text(encoding="utf-8"))
            for control in content["controls"].values():
                control["_slug"] = slug

            (DOCS_DIR / slug / filename).write_text(
                render_page(content, addon, slug, lang), encoding="utf-8"
            )

            if lang == "ru":
                count = len(content["controls"])
                # У аддона Maya сверять описание не с чем: слепок пустой, а
                # пустой слепок в coverage() выглядел бы как «всё описано».
                if addon.get("kind") == "maya":
                    print(f"  {slug}: {count} элементов описано (Maya, полнота не сверяется)")
                    problems = []
                else:
                    problems = coverage(content, addon)
                    print(f"  {slug}: {count} элементов описано")
                for problem in problems:
                    print(f"    ! {problem}")
                failures += len(problems)

    # Слепок UI-поверхности: по нему check_drift.py видит, что в аддонах
    # появилось или исчезло с прошлой сборки. Пишется только при полном
    # прогоне — частичный затёр бы данные остальных аддонов.
    if not args.only:
        data_dir = REPO_ROOT / "data"
        data_dir.mkdir(exist_ok=True)
        (data_dir / "api-manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
