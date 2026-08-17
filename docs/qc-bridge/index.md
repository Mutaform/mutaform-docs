# QC Bridge Maya ↔ Blender

Передача сцен между Blender и Maya через FBX без ручного проставления путей и
настроек экспорта. Обе стороны смотрят в одну папку обмена: одна пишет —
другая читает.

Мост состоит из двух половин, и ставить нужно обе: расширение в Blender и
скрипты в Maya.

![Панель моста](img/panel.png){ .screenshot }

## Установка в Blender

1. `Edit → Preferences → Get Extensions`
2. Шестерёнка → `Repositories` → `+` → `Add Remote Repository`
3. Ссылка:

    ```text
    https://mutaform.github.io/qc-bridge-blender-maya/index.json
    ```

4. Установить `QC Bridge Maya-Blender by Mutaform`

Панель: ++n++ во вьюпорте → вкладка **QC Maya Bridge**. Нужен Blender 4.2 или новее.

## Установка в Maya

1. Закрыть Maya.
2. Скачать [mutaform_bridge_maya_v1.zip](https://mutaform.github.io/qc-bridge-blender-maya/mutaform_bridge_maya_v1.zip)
   и распаковать.
3. Папку `mutaform_bridge` из архива положить сюда:

    ```text
    C:\Users\ИМЯ_ПОЛЬЗОВАТЕЛЯ\Documents\maya\2025\scripts\
    ```

    Должно получиться `...\scripts\mutaform_bridge\`.

4. Запустить Maya, открыть `Windows → General Editors → Script Editor`,
   перейти на вкладку **Python**.
5. Вставить и выполнить, заменив имя пользователя на своё:

    ```python
    import sys

    path = r"C:\Users\ИМЯ_ПОЛЬЗОВАТЕЛЯ\Documents\maya\2025\scripts\mutaform_bridge"
    if path not in sys.path:
        sys.path.append(path)

    import install_shelf_button
    install_shelf_button.install()
    ```

На полке появится кнопка моста. Делается один раз.

## Папка обмена

Свиток **Settings** в панели Blender:

- **Exchange Folder** — папка обмена, по умолчанию `Documents\MutaformBridge`;
- **FBX Name** — имя файла, по умолчанию `mutaform_bridge.fbx`.

Главное условие: **в Blender и в Maya указана одна и та же папка**. Если
передача не срабатывает, проверьте это в первую очередь.

Расширение `.fbx` дописывается само, если его не указать.

## Передача

Из Blender в Maya:

- **Export Selected** — выделенные объекты;
- **Export Selected Coll…** — выделенная коллекция целиком, со структурой.

Из Maya в Blender — **Import From Maya**, после того как Maya выложила файл
кнопкой на полке.

Строка с иконкой ⓘ наверху панели показывает результат последней операции —
в исходном состоянии там написано `Ready.`. Туда же попадают сообщения об
ошибках, и смотреть надо первым делом именно туда, если кажется, что ничего
не произошло.

## Группы и коллекции

В Maya иерархия строится трансформ-нодами, в Blender — коллекциями. При
передаче через FBX группы Maya приезжают пустышками, и работать с ними
неудобно.

Оба преобразования лежат под свитком **Convert Scene** — он свёрнут по
умолчанию.

- **Convert Maya Empties to Collections** — превращает пришедшую иерархию
  пустышек в нормальные коллекции Blender.
- **Convert Collections to Maya Empties** — обратное преобразование перед
  отправкой.

У обоих есть выбор области: вся сцена, выделенное или активный объект. Опция
**Bake Transforms** применяет накопленные трансформации, чтобы объекты встали в
те же мировые координаты.

!!! note "Единицы измерения"
    Maya работает в сантиметрах, Blender — в метрах. Мост пересчитывает
    масштаб и оси при передаче, так что модель приезжает нужного размера и в
    правильной ориентации.

## Что дальше

[Справочник интерфейса](reference.md).
