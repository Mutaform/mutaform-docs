"""Извлечение UI-поверхности Blender-аддона из исходников.

Разбор идёт через ``ast``, без импорта модулей и без ``bpy``: генератор должен
работать в CI, где Blender не установлен. Из пакета аддона достаётся:

* метаданные из ``blender_manifest.toml`` (id, версия, минимальный Blender);
* панели (``bpy.types.Panel``) с их иерархией через ``bl_parent_id``;
* операторы (``bpy.types.Operator``) с тултипом из docstring;
* свойства ``PropertyGroup`` и свойства самих операторов, с типом, дефолтом,
  диапазоном и вариантами Enum;
* привязка «какая панель показывает какие свойства и кнопки».

Последний пункт намеренно сделан по грубой, но устойчивой эвристике: внутри
тела класса панели собираются все строковые литералы, и те из них, что
совпадают с известным ``bl_idname`` оператора или именем свойства, считаются
частью этой панели. Это переживает любые обёртки вроде ``self._toggle(col,
settings, "detect_cage", ...)``, на которых сломался бы разбор конкретно
``layout.prop(...)``.
"""

from __future__ import annotations

import ast
import dataclasses
import pathlib
import re
import tomllib
from typing import Any

# Классы Blender, которые нас интересуют, по имени базового класса.
BASE_PANEL = "Panel"
BASE_OPERATOR = "Operator"
BASE_PROPERTY_GROUP = "PropertyGroup"
BASE_UI_LIST = "UIList"
BASE_MENU = "Menu"

# Фабрики свойств из bpy.props.
PROP_FACTORIES = {
    "BoolProperty": "bool",
    "BoolVectorProperty": "bool[]",
    "IntProperty": "int",
    "IntVectorProperty": "int[]",
    "FloatProperty": "float",
    "FloatVectorProperty": "float[]",
    "StringProperty": "string",
    "EnumProperty": "enum",
    "PointerProperty": "pointer",
    "CollectionProperty": "collection",
}

# Метаданные класса, которые вытаскиваем как есть.
BL_ATTRS = (
    "bl_idname",
    "bl_label",
    "bl_description",
    "bl_category",
    "bl_parent_id",
    "bl_space_type",
    "bl_region_type",
    "bl_order",
    "bl_options",
)


@dataclasses.dataclass
class PropertyInfo:
    identifier: str
    kind: str
    label: str | None = None
    description: str | None = None
    default: Any = None
    minimum: Any = None
    maximum: Any = None
    soft_minimum: Any = None
    soft_maximum: Any = None
    unit: str | None = None
    subtype: str | None = None
    items: list[dict[str, str]] = dataclasses.field(default_factory=list)
    owner: str = ""
    source: str = ""

    def to_dict(self) -> dict:
        data = dataclasses.asdict(self)
        return {k: v for k, v in data.items() if v not in (None, [], "")}


@dataclasses.dataclass
class ClassInfo:
    class_name: str
    base: str
    module: str
    bl: dict[str, Any] = dataclasses.field(default_factory=dict)
    docstring: str | None = None
    properties: list[PropertyInfo] = dataclasses.field(default_factory=list)
    literals: list[str] = dataclasses.field(default_factory=list)
    has_poll: bool = False
    poll_source: str | None = None

    def to_dict(self) -> dict:
        return {
            "class_name": self.class_name,
            "base": self.base,
            "module": self.module,
            **self.bl,
            "docstring": self.docstring,
            "properties": [p.to_dict() for p in self.properties],
            "has_poll": self.has_poll,
        }


# --------------------------------------------------------------------------
# Разбор литералов
# --------------------------------------------------------------------------
def _literal(node: ast.AST, constants: dict[str, Any]) -> Any:
    """Свести узел AST к Python-значению, насколько это возможно.

    Возвращает ``None`` для всего, что не сводится: вызовов, лямбд, ссылок на
    неизвестные имена. Ссылки на модульные константы (в том числе через точку,
    ``core.PRESET_ITEMS``) резолвятся по общей таблице ``constants``.
    """
    try:
        return ast.literal_eval(node)
    except (ValueError, SyntaxError, TypeError):
        pass

    if isinstance(node, ast.Name):
        return constants.get(node.id)
    if isinstance(node, ast.Attribute):
        return constants.get(node.attr)
    if isinstance(node, (ast.List, ast.Tuple)):
        return [_literal(el, constants) for el in node.elts]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _literal(node.left, constants)
        right = _literal(node.right, constants)
        if isinstance(left, str) and isinstance(right, str):
            return left + right
    return None


def _collect_constants(tree: ast.Module) -> dict[str, Any]:
    """Собрать модульные константы верхнего уровня, сводимые к литералам."""
    found: dict[str, Any] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            try:
                found[target.id] = ast.literal_eval(node.value)
            except (ValueError, SyntaxError, TypeError):
                continue
    return found


def _enum_items(raw: Any) -> list[dict[str, str]]:
    """Нормализовать items EnumProperty в список словарей.

    Blender принимает кортежи из 2-5 элементов; нам нужны первые три —
    идентификатор, подпись и описание.
    """
    items: list[dict[str, str]] = []
    if not isinstance(raw, (list, tuple)):
        return items
    for entry in raw:
        if not isinstance(entry, (list, tuple)) or len(entry) < 2:
            continue
        item = {"value": str(entry[0]), "label": str(entry[1])}
        if len(entry) >= 3 and entry[2]:
            item["description"] = str(entry[2])
        items.append(item)
    return items


def _parse_property(
    identifier: str,
    call: ast.Call,
    constants: dict[str, Any],
    owner: str,
    module: str,
) -> PropertyInfo | None:
    func = call.func
    name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
    if name not in PROP_FACTORIES:
        return None

    info = PropertyInfo(
        identifier=identifier,
        kind=PROP_FACTORIES[name],
        owner=owner,
        source=module,
    )

    for keyword in call.keywords:
        value = _literal(keyword.value, constants)
        if keyword.arg == "name":
            info.label = value
        elif keyword.arg == "description":
            info.description = value
        elif keyword.arg == "default":
            info.default = value
        elif keyword.arg == "min":
            info.minimum = value
        elif keyword.arg == "max":
            info.maximum = value
        elif keyword.arg == "soft_min":
            info.soft_minimum = value
        elif keyword.arg == "soft_max":
            info.soft_maximum = value
        elif keyword.arg == "unit":
            info.unit = value
        elif keyword.arg == "subtype":
            info.subtype = value
        elif keyword.arg == "items":
            info.items = _enum_items(value)
        elif keyword.arg == "type" and isinstance(keyword.value, ast.Attribute):
            info.default = keyword.value.attr

    # Для Enum без явного default Blender берёт первый вариант.
    if info.kind == "enum" and info.default is None and info.items:
        info.default = info.items[0]["value"]

    return info


def _base_names(node: ast.ClassDef) -> list[str]:
    names = []
    for base in node.bases:
        if isinstance(base, ast.Name):
            names.append(base.id)
        elif isinstance(base, ast.Attribute):
            names.append(base.attr)
    return names


def _string_literals(node: ast.AST) -> list[str]:
    out = []
    for child in ast.walk(node):
        if isinstance(child, ast.Constant) and isinstance(child.value, str):
            out.append(child.value)
    return out


def _parse_class(
    node: ast.ClassDef,
    constants: dict[str, Any],
    module: str,
) -> ClassInfo | None:
    bases = _base_names(node)
    for candidate in (
        BASE_PANEL,
        BASE_OPERATOR,
        BASE_PROPERTY_GROUP,
        BASE_UI_LIST,
        BASE_MENU,
    ):
        if candidate in bases:
            base = candidate
            break
    else:
        return None

    info = ClassInfo(
        class_name=node.name,
        base=base,
        module=module,
        docstring=ast.get_docstring(node),
    )

    for stmt in node.body:
        # bl_* метаданные
        if isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name) and target.id in BL_ATTRS:
                    value = _literal(stmt.value, constants)
                    if isinstance(value, (set, list, tuple)):
                        value = sorted(str(v) for v in value)
                    info.bl[target.id] = value
        # Аннотированные свойства: `foo: BoolProperty(...)`
        elif isinstance(stmt, ast.AnnAssign):
            if not isinstance(stmt.target, ast.Name):
                continue
            if isinstance(stmt.annotation, ast.Call):
                prop = _parse_property(
                    stmt.target.id, stmt.annotation, constants, node.name, module
                )
                if prop is not None:
                    info.properties.append(prop)
        elif isinstance(stmt, ast.FunctionDef) and stmt.name == "poll":
            info.has_poll = True
            info.poll_source = ast.unparse(stmt)

    info.literals = _string_literals(node)
    return info


# --------------------------------------------------------------------------
# Разбор пакета аддона
# --------------------------------------------------------------------------
def read_manifest(package_dir: pathlib.Path) -> dict:
    manifest_path = package_dir / "blender_manifest.toml"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"нет blender_manifest.toml в {package_dir}")
    with manifest_path.open("rb") as handle:
        return tomllib.load(handle)


def extract_addon(package_dir: pathlib.Path) -> dict:
    """Собрать полное описание UI-поверхности одного аддона."""
    package_dir = package_dir.resolve()
    manifest = read_manifest(package_dir)

    py_files = sorted(package_dir.rglob("*.py"))

    # Первый проход: модульные константы со всего пакета, чтобы ссылки вида
    # `core.PRESET_ITEMS` из соседнего модуля резолвились.
    constants: dict[str, Any] = {}
    trees: list[tuple[str, ast.Module]] = []
    for path in py_files:
        try:
            # utf-8-sig, а не utf-8: часть файлов сохранена с BOM, и хотя сам
            # Python при импорте его снимает, ast.parse на строке с BOM падает.
            tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except SyntaxError as exc:
            raise SyntaxError(f"{path}: {exc}") from exc
        module = path.relative_to(package_dir).as_posix()
        trees.append((module, tree))
        constants.update(_collect_constants(tree))

    # Второй проход: классы.
    classes: list[ClassInfo] = []
    for module, tree in trees:
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                parsed = _parse_class(node, constants, module)
                if parsed is not None:
                    classes.append(parsed)

    panels = [c for c in classes if c.base == BASE_PANEL]
    operators = [c for c in classes if c.base == BASE_OPERATOR]
    groups = [c for c in classes if c.base == BASE_PROPERTY_GROUP]

    # Индексы для привязки панель → содержимое.
    operator_by_idname = {
        c.bl.get("bl_idname"): c for c in operators if c.bl.get("bl_idname")
    }
    props_by_identifier: dict[str, list[PropertyInfo]] = {}
    for group in groups:
        for prop in group.properties:
            props_by_identifier.setdefault(prop.identifier, []).append(prop)

    panel_entries = []
    for panel in panels:
        seen_ops: list[str] = []
        seen_props: list[str] = []
        for literal in panel.literals:
            if literal in operator_by_idname and literal not in seen_ops:
                seen_ops.append(literal)
            elif literal in props_by_identifier and literal not in seen_props:
                seen_props.append(literal)
        entry = panel.to_dict()
        entry["operators"] = seen_ops
        entry["settings"] = seen_props
        panel_entries.append(entry)

    # Простые модульные константы отдаются наружу целиком: генератору иногда
    # нужен именно такой флаг (например, список скрытых из чек-листа проверок),
    # и заводить под каждый отдельный механизм извлечения не стоит.
    simple_constants = {
        name: (sorted(value) if isinstance(value, (set, frozenset)) else value)
        for name, value in constants.items()
        if isinstance(value, (str, int, float, bool, set, frozenset))
        or (isinstance(value, (list, tuple)) and len(value) < 64)
    }

    return {
        "constants": simple_constants,
        "id": manifest.get("id"),
        "name": manifest.get("name"),
        "tagline": manifest.get("tagline"),
        "version": manifest.get("version"),
        "blender_version_min": manifest.get("blender_version_min"),
        "website": manifest.get("website"),
        "tags": manifest.get("tags", []),
        "license": manifest.get("license", []),
        "panels": panel_entries,
        "operators": [c.to_dict() for c in operators],
        "property_groups": [c.to_dict() for c in groups],
        "menus": [c.to_dict() for c in classes if c.base == BASE_MENU],
        "ui_lists": [c.to_dict() for c in classes if c.base == BASE_UI_LIST],
    }


def extract_registry(
    package_dir: pathlib.Path, module: str, variable: str
) -> list[dict]:
    """Разобрать реестр вида ``NAME = [dict(...), dict(...)]``.

    Часть аддонов описывает свою функциональность не панелями, а таблицей
    данных: Scene QC Validator, например, держит все проверки в
    ``CHECK_DEFINITIONS``. Для художника это и есть главное содержимое
    справочника, а обычным обходом классов оно не находится.

    ``ast.literal_eval`` тут не годится: среди аргументов есть ссылки на
    функции (``run=check_ngons``). Литеральные аргументы забираются как есть,
    ссылки сохраняются строкой имени — по ним видно, например, есть у проверки
    автофикс или стоит ``fix=None``.
    """
    path = package_dir / module
    if not path.is_file():
        raise FileNotFoundError(f"нет модуля {path}")

    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    constants = _collect_constants(tree)

    target = None
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for name in node.targets:
            if isinstance(name, ast.Name) and name.id == variable:
                target = node.value
    if target is None:
        raise ValueError(f"{module}: не найдена переменная {variable}")
    if not isinstance(target, (ast.List, ast.Tuple)):
        raise ValueError(f"{module}: {variable} — не список")

    entries: list[dict] = []
    for element in target.elts:
        if not isinstance(element, ast.Call):
            continue
        entry: dict[str, Any] = {}
        for keyword in element.keywords:
            if keyword.arg is None:
                continue
            value = _literal(keyword.value, constants)
            if value is None and not isinstance(keyword.value, ast.Constant):
                # Ссылка на функцию или другое невычислимое выражение.
                node_value = keyword.value
                if isinstance(node_value, ast.Name):
                    entry[keyword.arg] = {"ref": node_value.id}
                elif isinstance(node_value, ast.Attribute):
                    entry[keyword.arg] = {"ref": node_value.attr}
                else:
                    entry[keyword.arg] = {"ref": "<выражение>"}
            else:
                entry[keyword.arg] = value
        if entry:
            entries.append(entry)
    return entries


def panel_tree(panels: list[dict]) -> list[dict]:
    """Разложить плоский список панелей в дерево по bl_parent_id."""
    by_id = {p.get("bl_idname"): p for p in panels if p.get("bl_idname")}
    roots: list[dict] = []
    for panel in panels:
        panel.setdefault("children", [])
    for panel in panels:
        parent_id = panel.get("bl_parent_id")
        parent = by_id.get(parent_id) if parent_id else None
        if parent is not None and parent is not panel:
            parent.setdefault("children", []).append(panel)
        else:
            roots.append(panel)

    def sort_key(item: dict) -> tuple:
        order = item.get("bl_order")
        return (order if isinstance(order, int) else 999, item.get("bl_label") or "")

    def sort_recursive(nodes: list[dict]) -> None:
        nodes.sort(key=sort_key)
        for node in nodes:
            sort_recursive(node.get("children", []))

    sort_recursive(roots)
    return roots


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
