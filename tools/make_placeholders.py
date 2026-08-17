"""Заглушки под скриншоты, которых ещё нет.

Гайды ссылаются на картинки с самого начала, чтобы вёрстка страницы была
настоящей, а замена заглушки на живой скриншот сводилась к перезаписи файла с
тем же именем. Скрипт создаёт недостающие PNG и никогда не трогает уже
существующие — реальный скриншот затереть он не может.

Список нужных картинок берётся из ``shots.yml``: там для каждой записано, что
на ней должно быть, так что файл заодно работает как чек-лист на съёмку.

    python tools/make_placeholders.py          # создать недостающие
    python tools/make_placeholders.py --list   # показать, чего не хватает
"""

from __future__ import annotations

import argparse
import pathlib

import yaml
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
SHOTS_FILE = REPO_ROOT / "shots.yml"

BG = (32, 34, 38)
FRAME = (72, 76, 84)
TEXT = (150, 156, 166)
ACCENT = (196, 142, 74)


def _font(size: int):
    for name in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap(draw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        if draw.textlength(trial, font=font) <= max_width or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def make_placeholder(path: pathlib.Path, caption: str, size: tuple[int, int]) -> None:
    width, height = size
    image = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(image)

    draw.rectangle([1, 1, width - 2, height - 2], outline=FRAME, width=2)

    title_font = _font(15)
    body_font = _font(13)

    draw.text((16, 14), "СКРИНШОТ", font=title_font, fill=ACCENT)

    lines = _wrap(draw, caption, body_font, width - 32)
    y = 44
    for line in lines:
        draw.text((16, y), line, font=body_font, fill=TEXT)
        y += 20

    hint = f"{path.name} · {width}×{height}"
    draw.text((16, height - 26), hint, font=body_font, fill=FRAME)

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="только показать список")
    args = parser.parse_args()

    if not SHOTS_FILE.is_file():
        print(f"нет {SHOTS_FILE}")
        return 1

    shots = yaml.safe_load(SHOTS_FILE.read_text(encoding="utf-8")) or {}
    created = 0
    pending = 0

    for entry in shots.get("shots", []):
        path = DOCS_DIR / entry["path"]
        size = tuple(entry.get("size", [420, 300]))
        manual = entry.get("done") == "manual"

        # На месте кадра, который ещё предстоит снять руками, всегда должна
        # быть заглушка — даже если файл лежит: иначе старая заглушка выдаёт
        # себя за готовую картинку, и о ней забывают.
        if path.is_file() and not manual:
            continue

        pending += 1
        if args.list:
            print(f"  {'РУКАМИ' if manual else 'нет'}: {entry['path']}")
            print(f"      {' '.join(entry['caption'].split())}")
            continue

        make_placeholder(path, entry["caption"], size)
        created += 1

    if args.list:
        print(f"\nосталось снять: {pending}")
    else:
        print(f"заглушек нарисовано: {created}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
