"""Что изменилось в аддонах с прошлой сборки документации.

Справочник собирается из написанного текста (`content/`), а не из кода,
поэтому сам по себе он про изменения в аддоне не узнает. Эту работу делает
здешняя сверка: свежий разбор исходников сравнивается с закоммиченным
`data/api-manifest.json`.

Что сообщается:

* появившиеся, исчезнувшие и переименованные кнопки и настройки;
* смена версии аддона;
* элементы, не покрытые ни одним разделом содержания.

Запускать надо **до** `gen_pages.py`: тот перезаписывает слепок, и сравнивать
станет не с чем.

    python tools/check_drift.py --source-root "D:/Mutaform/Mutaform Addons"

Код возврата 1 означает «есть что дописать руками». В CI это не роняет сборку
документации, а заводит issue со списком.
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
    extract_registry,
    resolve_package_dir,
)
from gen_pages import coverage  # noqa: E402

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content"
DATA_DIR = REPO_ROOT / "data"


def surface(addon: dict) -> dict[str, str]:
    """Плоский слепок аддона: идентификатор -> подпись.

    Берём только то, что художник видит: неслужебные операторы и свойства,
    которые панель действительно рисует. Внутренние поля — привязки списков,
    индексы активной строки — в сравнении не участвуют, иначе каждый рефакторинг
    выглядел бы как изменение интерфейса.
    """
    items: dict[str, str] = {}
    shown: set[str] = set()

    for panel in addon.get("panels", []):
        key = f"panel:{panel.get('bl_idname') or panel['class_name']}"
        items[key] = panel.get("bl_label") or ""
        shown.update(panel.get("settings") or [])

    for op in addon.get("operators", []):
        if "INTERNAL" in (op.get("bl_options") or []):
            continue
        key = f"operator:{op.get('bl_idname') or op['class_name']}"
        items[key] = op.get("bl_label") or ""

    for group in addon.get("property_groups", []):
        for prop in group.get("properties", []):
            if prop["identifier"] in shown:
                items[f"property:{prop['identifier']}"] = prop.get("label") or ""

    # Проверки валидатора описаны реестром, а не панелью. Без них сверка
    # молчала о новой проверке — ровно тот случай, ради которого она и нужна.
    for check in (addon.get("registries") or {}).get("checks") or []:
        items[f"check:{check['id']}"] = check.get("label") or ""

    return items


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True)
    args = parser.parse_args()

    registry = yaml.safe_load((REPO_ROOT / "addons.yml").read_text(encoding="utf-8"))
    source_root = pathlib.Path(args.source_root)

    manifest_path = DATA_DIR / "api-manifest.json"
    previous = {}
    if manifest_path.is_file():
        previous = json.loads(manifest_path.read_text(encoding="utf-8")).get(
            "addons", {}
        )

    report: list[str] = []
    total = 0

    for entry in sorted(registry["addons"], key=lambda e: e.get("order", 99)):
        slug = entry["slug"]
        package_dir = resolve_package_dir(source_root, entry["source"])
        if not package_dir.is_dir():
            report.append(f"\n### {slug}")
            report.append(
                f"- нет исходников: {entry['source']} не найден под {source_root}"
            )
            total += 1
            continue

        addon = extract_addon(package_dir)

        registries = {}
        for spec in entry.get("registries") or []:
            registries[spec["key"]] = extract_registry(
                package_dir, spec["module"], spec["variable"]
            )
        if registries:
            addon["registries"] = registries

        findings: list[str] = []

        old_addon = previous.get(slug)
        if old_addon:
            current, old = surface(addon), surface(old_addon)
            for key in sorted(set(current) - set(old)):
                findings.append(f"добавлено: {key} «{current[key]}» — опишите в content/")
            for key in sorted(set(old) - set(current)):
                findings.append(f"исчезло: {key} «{old[key]}» — уберите из content/")
            for key in sorted(set(current) & set(old)):
                if current[key] != old[key] and old[key]:
                    findings.append(
                        f"переименовано: {key} «{old[key]}» -> «{current[key]}»"
                    )
            if old_addon.get("version") != addon.get("version"):
                findings.append(
                    f"версия: {old_addon.get('version')} -> {addon.get('version')}"
                )

        content_path = CONTENT_DIR / f"{slug}.ru.yml"
        if content_path.is_file():
            content = yaml.safe_load(content_path.read_text(encoding="utf-8"))
            for control in content["controls"].values():
                control["_slug"] = slug
            findings.extend(coverage(content, addon))
        else:
            findings.append(f"нет файла содержания content/{slug}.ru.yml")

        if findings:
            report.append(f"\n### {addon['name']} ({slug})")
            report.extend(f"- {item}" for item in findings)
            total += len(findings)

    if not total:
        print("Расхождений не найдено.")
        return 0

    print(f"Найдено расхождений: {total}")
    print("\n".join(report))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
