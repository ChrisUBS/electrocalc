"""Interfaz Tkinter de ElectroCalc."""

from __future__ import annotations

import math
import re
import tkinter as tk
from tkinter import ttk

from electrocalc.calculations import (
    COULOMB_CONSTANT,
    PREFIXES,
    coulomb_force,
    from_base,
    ohms_law,
    series_parallel,
    to_base,
)

BG = "#0B1020"
CARD = "#151D30"
INK = "#F1F5F9"
MUTED = "#9AA8BD"
ACCENT = "#7C9CFF"
ACCENT_DARK = "#5B7DEB"
LINE = "#2B3850"
FIELD = "#0F1728"
RESULT_BG = "#101A2B"
FONT = "Helvetica"
PREFIX_OPTIONS = tuple(PREFIXES)


class ElectroCalcApp(tk.Tk):
    """Aplicación de calculadoras eléctricas con navegación por pantallas."""

    def __init__(self) -> None:
        super().__init__()
        self.title("ElectroCalc | Calculadoras eléctricas")
        self.geometry("1000x820")
        self.minsize(800, 650)
        self.configure(bg=BG)
        self.option_add("*Font", (FONT, 10))
        self.option_add("*TCombobox*Listbox.font", (FONT, 10))

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox", padding=7, fieldbackground=FIELD,
                        background=CARD, foreground=INK, arrowcolor=ACCENT,
                        bordercolor=LINE, lightcolor=LINE, darkcolor=LINE)
        style.map("TCombobox", fieldbackground=[("readonly", FIELD)],
                  foreground=[("readonly", INK)], selectbackground=[("readonly", FIELD)],
                  selectforeground=[("readonly", INK)])
        style.configure("TEntry", padding=5, fieldbackground=FIELD,
                        foreground=INK, insertcolor=ACCENT, bordercolor=LINE,
                        lightcolor=LINE, darkcolor=LINE)

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)
        self._numeric_validator = (self.register(self._valid_numeric_edit), "%P")
        self.show_home()

    @staticmethod
    def _valid_numeric_edit(candidate: str) -> bool:
        """Permite escribir números decimales con signo y notación científica."""
        return bool(re.fullmatch(r"[+-]?(?:\d*(?:[.,]\d*)?)(?:[eE][+-]?\d*)?", candidate))

    def _numeric_entry(self, parent: tk.Misc, *, width: int = 24) -> ttk.Entry:
        return ttk.Entry(parent, width=width, validate="key",
                         validatecommand=self._numeric_validator)

    def clear(self) -> None:
        for child in self.container.winfo_children():
            child.destroy()

    def show_home(self) -> None:
        self.clear()
        page = tk.Frame(self.container, bg=BG)
        page.pack(fill="both", expand=True, padx=54, pady=42)

        tk.Label(page, text="ELECTROCALC", bg=BG, fg=ACCENT,
                 font=(FONT, 10, "bold")).pack(anchor="w")
        tk.Label(page, text="Calculadoras eléctricas", bg=BG, fg=INK,
                 font=(FONT, 31, "bold")).pack(anchor="w", pady=(10, 7))
        tk.Label(page, text="Herramientas sencillas para resolver circuitos y fuerzas eléctricas.",
                 bg=BG, fg=MUTED, font=(FONT, 12)).pack(anchor="w", pady=(0, 34))

        cards = tk.Frame(page, bg=BG)
        cards.pack(fill="x", expand=False)
        cards.columnconfigure((0, 1, 2), weight=1, uniform="card")
        options = [
            ("01", "Ley de Ohm", "Calcula voltaje, corriente o resistencia.", "Ω", self.show_ohm),
            ("02", "Serie y paralelo", "Combina resistencias o capacitores.", "▤", self.show_network),
            ("03", "Ley de Coulomb", "Calcula la magnitud de la fuerza eléctrica.", "±", self.show_coulomb),
        ]
        for index, (number, title, description, icon, callback) in enumerate(options):
            col = index
            card = tk.Frame(cards, bg=CARD, highlightbackground=LINE, highlightthickness=1)
            card.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 8, 8 if col < 2 else 0),
                      pady=(0, 12), ipadx=5, ipady=8)
            card.grid_columnconfigure(0, weight=1)
            tk.Label(card, text=icon, bg="#202D49", fg=ACCENT, width=3, height=1,
                     font=(FONT, 18, "bold")).grid(row=0, column=0, sticky="w", padx=18, pady=(18, 12))
            tk.Label(card, text=number, bg=CARD, fg=MUTED, font=(FONT, 9, "bold")).grid(
                row=0, column=1, sticky="e", padx=18, pady=(18, 12))
            tk.Label(card, text=title, bg=CARD, fg=INK, font=(FONT, 16, "bold")).grid(
                row=1, column=0, columnspan=2, sticky="w", padx=18)
            tk.Label(card, text=description, bg=CARD, fg=MUTED, font=(FONT, 10),
                     wraplength=275, justify="left").grid(row=2, column=0, columnspan=2,
                                                            sticky="w", padx=18, pady=(7, 19))
            open_button = self._button(card, "Abrir  →", callback)
            open_button.grid(row=3, column=0, columnspan=2, sticky="ew", padx=14, pady=(0, 16))
            # La tarjeta completa funciona como acceso, y mantiene el botón visible.
            for widget in (card, *card.winfo_children()):
                widget.bind("<Button-1>", lambda _event, fn=callback: fn())
        tk.Label(page, text="Unidades SI  ·  Resultados instantáneos  ·  Sin conexión", bg=BG,
                 fg=MUTED, font=(FONT, 9)).pack(anchor="w", pady=(12, 0))

    def _button(self, parent: tk.Misc, text: str, command, *, secondary: bool = False) -> tk.Label:
        # Tk usa botones nativos de macOS que pueden ignorar sus colores bg/fg.
        # Una etiqueta estilizada mantiene contraste y se comporta como botón.
        normal = "#263653" if secondary else "#4368E8"
        hover = "#33486B" if secondary else "#3157D5"
        button = tk.Label(parent, text=text, relief="flat", cursor="hand2",
                          bg=normal, fg="#DCE6FF" if secondary else "#FFFFFF",
                          font=(FONT, 10, "bold"), padx=16, pady=11)
        button.bind("<Button-1>", lambda _event: command())
        button.bind("<Enter>", lambda _event: button.configure(bg=hover))
        button.bind("<Leave>", lambda _event: button.configure(bg=normal))
        return button

    def _header(self, title: str, subtitle: str) -> tk.Frame:
        self.clear()
        page = tk.Frame(self.container, bg=BG)
        page.pack(fill="both", expand=True, padx=54, pady=34)
        self._button(page, "←  Inicio", self.show_home, secondary=True).pack(anchor="w", pady=(0, 23))
        tk.Label(page, text=title, bg=BG, fg=INK, font=(FONT, 25, "bold")).pack(anchor="w")
        tk.Label(page, text=subtitle, bg=BG, fg=MUTED, font=(FONT, 11)).pack(anchor="w", pady=(6, 23))
        return page

    def _panel(self, parent: tk.Misc) -> tk.Frame:
        frame = tk.Frame(parent, bg=CARD, highlightbackground=LINE, highlightthickness=1)
        # El panel conserva su altura natural: evita el enorme espacio vacío
        # que empujaba las acciones y el resultado fuera de la ventana.
        frame.pack(fill="x", expand=False)
        return frame

    def _label(self, parent: tk.Misc, text: str, *, color: str = INK,
               size: int = 10, weight: str = "normal") -> tk.Label:
        return tk.Label(parent, text=text, bg=CARD, fg=color, font=(FONT, size, weight))

    def _field(self, parent: tk.Misc, row: int, label: str, unit: str,
               *, prefix: str = "(base)") -> tuple[tk.Entry, tk.StringVar]:
        self._label(parent, label, weight="bold").grid(row=row, column=0, sticky="w", padx=(24, 8), pady=12)
        entry = self._numeric_entry(parent, width=24)
        entry.grid(row=row, column=1, sticky="ew", padx=8, pady=12)
        var = tk.StringVar(value=prefix)
        selector = ttk.Combobox(parent, textvariable=var, values=PREFIX_OPTIONS, state="readonly", width=9)
        selector.grid(row=row, column=2, sticky="w", padx=(8, 24), pady=12)
        self._label(parent, unit, color=MUTED, size=9).grid(row=row, column=3, sticky="w", padx=(0, 20), pady=12)
        return entry, var

    def _result_box(self, parent: tk.Misc, row: int, *, pady: tuple[int, int] = (14, 12)) -> tk.Label:
        result = tk.Label(parent, text="Completa los datos y calcula el resultado.",
                          bg=RESULT_BG, fg=MUTED, font=(FONT, 11, "bold"), padx=18, pady=16,
                          anchor="w", justify="left", wraplength=670)
        result.grid(row=row, column=0, columnspan=4, sticky="ew", padx=24, pady=pady)
        return result

    @staticmethod
    def _read(entry: tk.Entry, label: str, prefix: str) -> float:
        raw = entry.get().strip()
        if not raw:
            raise ValueError(f"El campo {label} es obligatorio.")
        try:
            number = float(raw.replace(",", "."))
        except ValueError as exc:
            raise ValueError(f"Escribe un número válido en {label}.") from exc
        if not math.isfinite(number):
            raise ValueError(f"El valor de {label} debe ser finito.")
        return to_base(number, prefix)

    @staticmethod
    def _format(value: float, unit: str) -> str:
        if value == 0:
            return f"0 {unit}"
        if abs(value) >= 1e7 or abs(value) < 1e-4:
            return f"{value:.6g} {unit}"
        return f"{value:.6f}".rstrip("0").rstrip(".") + f" {unit}"

    def show_ohm(self) -> None:
        page = self._header("Ley de Ohm", "V = I × R  ·  Ingresa dos valores y selecciona sus prefijos SI.")
        panel = self._panel(page)
        panel.grid_columnconfigure(1, weight=1)
        v, vu = self._field(panel, 0, "Voltaje", "V")
        i, iu = self._field(panel, 1, "Corriente", "A")
        r, ru = self._field(panel, 2, "Resistencia", "Ω")
        self._label(panel, "Deja vacío el valor que quieres calcular.", color=MUTED, size=9).grid(
            row=3, column=0, columnspan=4, sticky="w", padx=24, pady=(4, 10))
        result = self._result_box(panel, 4)

        def calculate() -> None:
            try:
                rows = [("Voltaje", v, vu, "V"), ("Corriente", i, iu, "A"),
                        ("Resistencia", r, ru, "Ω")]
                present = [(name, entry, prefix, unit) for name, entry, prefix, unit in rows
                           if entry.get().strip()]
                if len(present) != 2:
                    raise ValueError("Ingresa exactamente dos valores y deja uno vacío.")
                parsed = {name: self._read(entry, name.lower(), prefix.get())
                          for name, entry, prefix, _unit in present}
                key_map = {"Voltaje": "voltage", "Corriente": "current", "Resistencia": "resistance"}
                args = {key_map[name]: value for name, value in parsed.items()}
                name, value = ohms_law(**args)
                output = {"voltaje": ("Voltaje", "V", "V"),
                          "corriente": ("Corriente", "A", "A"),
                          "resistencia": ("Resistencia", "Ω", "Ω")}[name]
                target_prefix = {"voltaje": vu, "corriente": iu, "resistencia": ru}[name].get()
                converted = from_base(value, target_prefix)
                result_unit = ("" if target_prefix == "(base)" else target_prefix) + output[1]
                result.config(text=f"{output[0]} calculado:  {self._format(converted, result_unit)}",
                              fg=ACCENT)
            except ValueError as exc:
                result.config(text=str(exc), fg="#B42318")

        self._button(panel, "Calcular", calculate).grid(
            row=5, column=0, columnspan=4, sticky="e", padx=24, pady=(0, 20))
        v.focus_set()

    def show_network(self) -> None:
        page = self._header("Serie y paralelo", "Combina hasta 10 componentes y elige sus unidades de forma independiente.")
        panel = self._panel(page)
        panel.grid_columnconfigure(1, weight=1)
        top = tk.Frame(panel, bg=CARD)
        top.grid(row=0, column=0, columnspan=5, sticky="ew", padx=24, pady=(18, 5))
        self._label(top, "Componente", weight="bold").pack(side="left")
        component = tk.StringVar(value="Resistencia")
        ttk.Combobox(top, textvariable=component, values=("Resistencia", "Capacitor"),
                     state="readonly", width=16).pack(side="left", padx=(8, 24))
        self._label(top, "Conexión", weight="bold").pack(side="left")
        connection = tk.StringVar(value="Serie")
        ttk.Combobox(top, textvariable=connection, values=("Serie", "Paralelo"),
                     state="readonly", width=14).pack(side="left", padx=8)

        column_titles = ("#", "Valor", "Prefijo", "Unidad")
        for col, title in enumerate(column_titles):
            self._label(panel, title, color=MUTED, size=9, weight="bold").grid(
                row=1, column=col, sticky="w", padx=(24 if col == 0 else 8, 8), pady=(7, 2))
        entries: list[tuple[tk.Entry, tk.StringVar]] = []
        unit_labels: list[tk.Label] = []
        for idx in range(10):
            row = idx + 2
            self._label(panel, f"{idx + 1:02}", color=MUTED).grid(row=row, column=0, sticky="w", padx=24, pady=3)
            entry = self._numeric_entry(panel)
            entry.grid(row=row, column=1, sticky="ew", padx=8, pady=1)
            prefix = tk.StringVar(value="(base)")
            ttk.Combobox(panel, textvariable=prefix, values=PREFIX_OPTIONS, state="readonly", width=9).grid(
                row=row, column=2, sticky="w", padx=8, pady=1)
            unit = self._label(panel, "Ω", color=MUTED, size=9)
            unit.grid(row=row, column=3, sticky="w", padx=(0, 20), pady=1)
            unit_labels.append(unit)
            entries.append((entry, prefix))

        def sync_unit(*_args) -> None:
            symbol = "Ω" if component.get() == "Resistencia" else "F"
            for label in unit_labels:
                label.configure(text=symbol)
            output_unit.configure(text=symbol)

        component.trace_add("write", sync_unit)
        output_frame = tk.Frame(panel, bg=CARD)
        output_frame.grid(row=12, column=0, columnspan=4, sticky="w", padx=24, pady=(14, 2))
        self._label(output_frame, "Prefijo del resultado", weight="bold").pack(side="left")
        output_prefix = tk.StringVar(value="(base)")
        ttk.Combobox(output_frame, textvariable=output_prefix, values=PREFIX_OPTIONS,
                     state="readonly", width=9).pack(side="left", padx=10)
        output_unit = self._label(output_frame, "Ω", color=MUTED)
        output_unit.pack(side="left")
        result = self._result_box(panel, 13, pady=(10, 10))

        def calculate() -> None:
            try:
                parsed = []
                for index, (entry, prefix) in enumerate(entries, start=1):
                    if not entry.get().strip():
                        continue
                    parsed.append(self._read(entry, f"componente {index}", prefix.get()))
                component_key = "resistencia" if component.get() == "Resistencia" else "capacitor"
                connection_key = connection.get().lower()
                value = series_parallel(parsed, component=component_key, connection=connection_key)
                converted = from_base(value, output_prefix.get())
                unit = "Ω" if component_key == "resistencia" else "F"
                symbol = "" if output_prefix.get() == "(base)" else output_prefix.get()
                result.config(text=f"Equivalente:  {self._format(converted, symbol + unit)}", fg=ACCENT)
            except ValueError as exc:
                result.config(text=str(exc), fg="#B42318")

        self._button(panel, "Calcular equivalente", calculate).grid(
            row=14, column=0, columnspan=4, sticky="e", padx=24, pady=(0, 15))
        entries[0][0].focus_set()

    def show_coulomb(self) -> None:
        page = self._header("Ley de Coulomb", "F = k · |q₁ × q₂| / r²  ·  Calcula la magnitud de la fuerza eléctrica.")
        panel = self._panel(page)
        panel.grid_columnconfigure(1, weight=1)
        self._label(panel, "Constante de Coulomb (k)", weight="bold").grid(
            row=0, column=0, sticky="w", padx=(24, 8), pady=(22, 13))
        self._label(panel, f"{COULOMB_CONSTANT:.7g} N·m²/C²", color=ACCENT, weight="bold").grid(
            row=0, column=1, columnspan=3, sticky="w", padx=8, pady=(22, 13))
        q1, q1u = self._field(panel, 1, "Carga q₁", "C")
        q2, q2u = self._field(panel, 2, "Carga q₂", "C")
        distance, du = self._field(panel, 3, "Distancia r", "m")
        result = self._result_box(panel, 4, pady=(15, 10))

        def calculate() -> None:
            try:
                charge1 = self._read(q1, "q₁", q1u.get())
                charge2 = self._read(q2, "q₂", q2u.get())
                radius = self._read(distance, "distancia r", du.get())
                force = coulomb_force(charge1, charge2, radius)
                result.config(text=f"Fuerza eléctrica:  {self._format(force, 'N')}\n"
                                    "La magnitud es positiva; el signo de las cargas determina si se atraen o se repelen.",
                              fg=ACCENT)
            except ValueError as exc:
                result.config(text=str(exc), fg="#B42318")

        self._button(panel, "Calcular fuerza", calculate).grid(
            row=5, column=0, columnspan=4, sticky="e", padx=24, pady=(5, 22))
        q1.focus_set()


def main() -> None:
    """Arranca la ventana principal."""
    ElectroCalcApp().mainloop()
