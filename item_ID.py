import tkinter as tk
from tkinter import ttk, messagebox
import uuid
import json
import os

DATA_FILE = "items.json"

ICONS = [
    "⚔️","🛡️","🪄","👑","💎","⭐","⚡","🔥","❄️","🌿",
    "💀","❤️","🗝️","🔒","👁️","👻","🧿","🤖","🐛","🐟",
    "🪶","💧","🌙","☀️","☁️","🌪️","🌈","⛰️","📦","🎁",
    "💰","🧰","🔨","🪓","✂️","🧪","💊","🗺️","🧭","🔭",
    "🔬","📖","📜","🎵","🏆","🎫","🚀","⚓","🎯","♾️",
]

def load_items():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_items(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Менеджер предметов")
        self.geometry("900x640")
        self.minsize(700, 480)
        self.configure(bg="#1e1e2e")

        self.items = load_items()
        self.selected_icon = tk.StringVar(value="📦")
        self.search_var    = tk.StringVar()
        self.name_var      = tk.StringVar()
        self.id_var        = tk.StringVar()

        self.BG       = "#1e1e2e"
        self.PANEL    = "#2a2a3e"
        self.CARD     = "#313149"
        self.ACCENT   = "#7c6af7"
        self.FG       = "#e0dff5"
        self.FG2      = "#9090b0"
        self.BORDER   = "#3d3d5c"
        self.SUCCESS  = "#3dba7a"
        self.DANGER   = "#e05c6a"
        self.ENTRY_BG = "#252538"

        self._setup_styles()
        self._build_ui()
        self._refresh_list()

    def _setup_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("Treeview",
            background=self.CARD, fieldbackground=self.CARD,
            foreground=self.FG, font=("Segoe UI", 11),
            rowheight=34, borderwidth=0, relief="flat")
        s.configure("Treeview.Heading",
            background=self.PANEL, foreground=self.FG2,
            font=("Segoe UI", 10, "bold"), relief="flat", borderwidth=0)
        s.map("Treeview",
            background=[("selected", self.ACCENT)],
            foreground=[("selected", "#ffffff")])
        s.map("Treeview.Heading",
            background=[("active", self.BORDER)])
        s.configure("Vertical.TScrollbar",
            background=self.PANEL, troughcolor=self.CARD,
            arrowcolor=self.FG2, borderwidth=0, relief="flat")

    # ─────────────────────────── главный макет ───────────────────────────────

    def _build_ui(self):
        # корень: два столбца через grid
        self.columnconfigure(0, weight=0, minsize=310)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        left  = tk.Frame(self, bg=self.BG)
        right = tk.Frame(self, bg=self.BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(14, 7), pady=14)
        right.grid(row=0, column=1, sticky="nsew", padx=(7, 14), pady=14)

        # левая колонка: pack сверху вниз
        left.pack_propagate(True)
        self._build_search(left)
        self._build_add_form(left)

        # правая колонка: pack сверху вниз
        self._build_list(right)

    # ────────────────────────────── поиск ────────────────────────────────────

    def _build_search(self, parent):
        # заголовок секции
        tk.Label(parent, text="🔍  Поиск по ID",
                 font=("Segoe UI", 11, "bold"), fg=self.FG, bg=self.BG
                 ).pack(anchor="w", pady=(0, 4))

        box = tk.Frame(parent, bg=self.PANEL,
                       highlightthickness=1, highlightbackground=self.BORDER)
        box.pack(fill="x", pady=(0, 10))

        # строка ввода
        row = tk.Frame(box, bg=self.PANEL)
        row.pack(fill="x", padx=12, pady=10)

        entry = self._entry(row, self.search_var, "Введите ID...", mono=True)
        entry.pack(side="left", fill="x", expand=True, ipady=5)

        clr = tk.Button(row, text="✕", font=("Segoe UI", 10),
                        bg=self.CARD, fg=self.FG2,
                        activebackground=self.BORDER, activeforeground=self.FG,
                        relief="flat", bd=0, cursor="hand2", padx=8,
                        command=lambda: self.search_var.set(""))
        clr.pack(side="left", padx=(6, 0))

        self.search_var.trace_add("write", lambda *_: self._do_search())

        self.result_box = tk.Frame(box, bg=self.PANEL)
        self.result_box.pack(fill="x", padx=12, pady=(0, 8))

    def _do_search(self):
        for w in self.result_box.winfo_children():
            w.destroy()
        q = self.search_var.get().strip()
        if not q:
            return
        found = self.items.get(q)
        if found:
            card = tk.Frame(self.result_box, bg="#1e3a2f",
                            highlightthickness=1, highlightbackground=self.SUCCESS)
            card.pack(fill="x", pady=2)
            tk.Label(card, text=found["icon"], font=("Segoe UI Emoji", 26),
                     bg="#1e3a2f").pack(side="left", padx=12, pady=8)
            info = tk.Frame(card, bg="#1e3a2f")
            info.pack(side="left", pady=8)
            tk.Label(info, text=found["name"], font=("Segoe UI", 13, "bold"),
                     fg="#7de8b5", bg="#1e3a2f").pack(anchor="w")
            tk.Label(info, text=f"ID: {q}", font=("Courier New", 9),
                     fg="#4dab80", bg="#1e3a2f").pack(anchor="w")
        else:
            tk.Label(self.result_box,
                     text=f"😕  Не найдено: «{q}»",
                     font=("Segoe UI", 10), fg=self.DANGER, bg=self.PANEL
                     ).pack(pady=6)

    # ──────────────────────────── форма ──────────────────────────────────────

    def _build_add_form(self, parent):
        tk.Label(parent, text="➕  Новый предмет",
                 font=("Segoe UI", 11, "bold"), fg=self.FG, bg=self.BG
                 ).pack(anchor="w", pady=(0, 4))

        box = tk.Frame(parent, bg=self.PANEL,
                       highlightthickness=1, highlightbackground=self.BORDER)
        box.pack(fill="both", expand=True)

        # иконка
        icon_row = tk.Frame(box, bg=self.PANEL)
        icon_row.pack(fill="x", padx=14, pady=(12, 8))

        self.icon_btn = tk.Button(
            icon_row, textvariable=self.selected_icon,
            font=("Segoe UI Emoji", 26), width=3, height=1,
            bg=self.CARD, fg=self.FG,
            activebackground=self.BORDER, activeforeground=self.FG,
            relief="flat", bd=0, cursor="hand2",
            command=self._open_icon_picker)
        self.icon_btn.pack(side="left", padx=(0, 10))

        tk.Label(icon_row, text="← нажми чтобы\n   выбрать иконку",
                 font=("Segoe UI", 9), fg=self.FG2, bg=self.PANEL,
                 justify="left").pack(side="left")

        # название
        tk.Label(box, text="НАЗВАНИЕ *", font=("Segoe UI", 9, "bold"),
                 fg=self.FG2, bg=self.PANEL).pack(anchor="w", padx=14)
        self._entry(box, self.name_var, "Например: Меч дракона").pack(
            fill="x", padx=14, ipady=6, pady=(2, 10))

        # ID
        tk.Label(box, text="ID ПРЕДМЕТА", font=("Segoe UI", 9, "bold"),
                 fg=self.FG2, bg=self.PANEL).pack(anchor="w", padx=14)

        id_row = tk.Frame(box, bg=self.PANEL)
        id_row.pack(fill="x", padx=14, pady=(2, 14))

        self._entry(id_row, self.id_var, "Авто-генерация", mono=True).pack(
            side="left", fill="x", expand=True, ipady=6)

        regen = tk.Button(id_row, text="🔄", font=("Segoe UI", 11),
                          bg=self.CARD, fg=self.FG,
                          activebackground=self.BORDER, activeforeground=self.FG,
                          relief="flat", bd=0, cursor="hand2", padx=8,
                          command=self._gen_id)
        regen.pack(side="left", padx=(6, 0))

        # кнопка добавить
        add_btn = tk.Button(
            box, text="  ➕  Добавить предмет  ",
            font=("Segoe UI", 11, "bold"),
            bg=self.ACCENT, fg="#ffffff",
            activebackground="#6357d6", activeforeground="#ffffff",
            relief="flat", bd=0, cursor="hand2", pady=9,
            command=self._add_item)
        add_btn.pack(fill="x", padx=14, pady=(0, 14))
        self._hover(add_btn, self.ACCENT, "#6357d6")

    # ────────────────────────────── список ───────────────────────────────────

    def _build_list(self, parent):
        # заголовок
        hdr = tk.Frame(parent, bg=self.BG)
        hdr.pack(fill="x", pady=(0, 6))
        tk.Label(hdr, text="📋  Все предметы",
                 font=("Segoe UI", 12, "bold"), fg=self.FG, bg=self.BG
                 ).pack(side="left")
        self.count_lbl = tk.Label(hdr, text="0 шт.",
                                   font=("Segoe UI", 10), fg=self.FG2, bg=self.BG)
        self.count_lbl.pack(side="right")

        # таблица
        tree_wrap = tk.Frame(parent, bg=self.CARD,
                              highlightthickness=1, highlightbackground=self.BORDER)
        tree_wrap.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_wrap, columns=("icon", "name", "id"),
                                  show="headings", selectmode="browse")
        self.tree.heading("icon", text="")
        self.tree.heading("name", text="Название")
        self.tree.heading("id",   text="ID")
        self.tree.column("icon", width=44,  minwidth=44,  stretch=False, anchor="center")
        self.tree.column("name", width=200, minwidth=120, stretch=True)
        self.tree.column("id",   width=160, minwidth=100, stretch=True)

        sb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # кнопка удалить
        del_btn = tk.Button(
            parent, text="  🗑  Удалить выбранный  ",
            font=("Segoe UI", 10),
            bg=self.CARD, fg=self.DANGER,
            activebackground=self.DANGER, activeforeground="#fff",
            relief="flat", bd=0, cursor="hand2", pady=8,
            command=self._delete_selected)
        del_btn.pack(fill="x", pady=(8, 0))
        self._hover(del_btn, self.CARD, self.DANGER,
                    fg_normal=self.DANGER, fg_hover="#fff")

    # ──────────────────────────── логика ─────────────────────────────────────

    def _gen_id(self):
        self.id_var.set("ITEM-" + uuid.uuid4().hex[:6].upper())

    def _add_item(self):
        name    = self.name_var.get().strip()
        item_id = self.id_var.get().strip() or ("ITEM-" + uuid.uuid4().hex[:6].upper())
        icon    = self.selected_icon.get()

        if not name:
            messagebox.showwarning("Ошибка", "Введи название предмета!")
            return
        if item_id in self.items:
            messagebox.showwarning("Ошибка", f"ID «{item_id}» уже занят!")
            return

        self.items[item_id] = {"name": name, "icon": icon}
        save_items(self.items)
        self.name_var.set("")
        self.id_var.set("")
        self.selected_icon.set("📦")
        self._refresh_list()
        self._do_search()

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Удаление", "Сначала выбери предмет в списке.")
            return
        values  = self.tree.item(sel[0], "values")
        item_id = values[2]
        name    = values[1]
        if messagebox.askyesno("Удаление", f"Удалить «{name}»?\nID: {item_id}"):
            self.items.pop(item_id, None)
            save_items(self.items)
            self._refresh_list()
            self._do_search()

    def _refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        for iid, data in self.items.items():
            self.tree.insert("", "end", values=(data["icon"], data["name"], iid))
        self.count_lbl.config(text=f"{len(self.items)} шт.")

    # ───────────────────────── выбор иконки ──────────────────────────────────

    def _open_icon_picker(self):
        win = tk.Toplevel(self)
        win.title("Выбери иконку")
        win.configure(bg=self.BG)
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text="Выбери иконку",
                 font=("Segoe UI", 12, "bold"), fg=self.FG, bg=self.BG
                 ).pack(pady=(14, 8))

        grid = tk.Frame(win, bg=self.BG)
        grid.pack(padx=16, pady=(0, 16))

        COLS = 10
        for i, icon in enumerate(ICONS):
            r, c = divmod(i, COLS)
            b = tk.Button(
                grid, text=icon, font=("Segoe UI Emoji", 20),
                width=2, height=1,
                bg=self.CARD, fg=self.FG, relief="flat", bd=0,
                activebackground=self.ACCENT, cursor="hand2",
                command=lambda ic=icon: self._pick_icon(ic, win))
            b.grid(row=r, column=c, padx=3, pady=3)

    def _pick_icon(self, icon, win):
        self.selected_icon.set(icon)
        win.destroy()

    # ──────────────────────────── хелперы ────────────────────────────────────

    def _entry(self, parent, var, placeholder="", mono=False):
        font = ("Courier New", 11) if mono else ("Segoe UI", 11)
        e = tk.Entry(parent, textvariable=var, font=font,
                     bg=self.ENTRY_BG, fg=self.FG,
                     insertbackground=self.FG,
                     relief="flat", bd=0,
                     highlightthickness=1,
                     highlightbackground=self.BORDER,
                     highlightcolor=self.ACCENT)
        if placeholder:
            if not var.get():
                e.insert(0, placeholder)
                e.config(fg=self.FG2)
            def on_in(ev, e=e, var=var, ph=placeholder):
                if e.get() == ph and not var.get():
                    e.delete(0, "end")
                    e.config(fg=self.FG)
            def on_out(ev, e=e, var=var, ph=placeholder):
                if not e.get():
                    e.insert(0, ph)
                    e.config(fg=self.FG2)
            e.bind("<FocusIn>",  on_in)
            e.bind("<FocusOut>", on_out)
        return e

    def _hover(self, btn, bg_n, bg_h, fg_normal=None, fg_hover=None):
        btn.bind("<Enter>", lambda e: (btn.config(bg=bg_h),
                                       fg_hover and btn.config(fg=fg_hover)))
        btn.bind("<Leave>", lambda e: (btn.config(bg=bg_n),
                                       fg_normal and btn.config(fg=fg_normal)))


if __name__ == "__main__":
    app = App()
    app.mainloop()