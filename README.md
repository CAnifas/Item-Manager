# 📦 Item Manager

A simple Python desktop app for storing items with icons and searching by ID.

---

## Features

- Add items with a custom name and icon
- Auto-generate an ID or enter your own
- Search for any item by ID in real time
- Delete items from the list
- All data is saved to `items.json` and persists between sessions

---

## Getting Started

### Requirements

- Python 3.8 or newer
- `tkinter` (included with Python by default)

### Run from source

```bash
python item_manager.py
```

### Run the .exe (Windows)

Just double-click `item_manager.exe` — no installation required.

---

## Build the .exe yourself

Install PyInstaller:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile --windowed --icon=icon.ico item_manager.py
```

The finished executable will appear in the `dist/` folder.

---

## Interface

```
┌─────────────────────┬──────────────────────────────┐
│  🔍 Search by ID    │  📋 All items                │
│  ─────────────────  │  ──────────────────────────  │
│  ➕ New item        │  [icon] [name]        [ID]   │
│                     │  [icon] [name]        [ID]   │
│  🖼 icon picker     │  ...                         │
│  Name *             │                              │
│  Item ID            │  🗑 Delete selected          │
└─────────────────────┴──────────────────────────────┘
```

**Left panel** — search bar and the add-item form.  
**Right panel** — scrollable table of all items, resizes with the window.

---

## Data format

Items are stored in `items.json` next to the executable:

```json
{
  "ITEM-3F9A1C": {
    "name": "Dragon Sword",
    "icon": "⚔️"
  },
  "ITEM-AA72B0": {
    "name": "Healing Potion",
    "icon": "🧪"
  }
}
```

The file can be edited manually or consumed by other tools.

---

## Project structure

```
item_manager/
├── item_manager.py   # source code
├── icon.ico          # application icon
├── items.json        # database (created automatically on first run)
└── README.md         # this file
```

---

## License

Do whatever you want with it — it's yours.
