"""Fórmulas y conversiones para las calculadoras eléctricas."""

from __future__ import annotations

from collections.abc import Iterable

# Factores SI, expresados como unidades base por unidad seleccionada.
PREFIXES: dict[str, float] = {
    "p": 1e-12,
    "n": 1e-9,
    "µ": 1e-6,
    "m": 1e-3,
    "(base)": 1.0,
    "k": 1e3,
    "M": 1e6,
}

COULOMB_CONSTANT = 8.9875517862e9  # N·m²/C², calculado con permitividad CODATA 2022


def to_base(value: float, prefix: str) -> float:
    """Convierte un valor con prefijo SI a su unidad base."""
    try:
        return value * PREFIXES[prefix]
    except KeyError as exc:
        raise ValueError(f"Prefijo SI desconocido: {prefix}") from exc


def from_base(value: float, prefix: str) -> float:
    """Convierte una magnitud SI base al prefijo seleccionado."""
    try:
        return value / PREFIXES[prefix]
    except KeyError as exc:
        raise ValueError(f"Prefijo SI desconocido: {prefix}") from exc


def ohms_law(*, voltage: float | None = None, current: float | None = None,
             resistance: float | None = None) -> tuple[str, float]:
    """Calcula la incógnita de V=I·R. Los argumentos deben estar en SI."""
    values = {"voltaje": voltage, "corriente": current, "resistencia": resistance}
    known = [name for name, value in values.items() if value is not None]
    if len(known) != 2:
        raise ValueError("Ingresa exactamente dos valores para calcular el tercero.")

    if voltage is None:
        assert current is not None and resistance is not None
        return "voltaje", current * resistance
    if current is None:
        assert resistance is not None
        if resistance == 0:
            raise ValueError("La resistencia debe ser distinta de cero para calcular la corriente.")
        return "corriente", voltage / resistance
    assert current is not None
    if current == 0:
        raise ValueError("La corriente debe ser distinta de cero para calcular la resistencia.")
    return "resistencia", voltage / current


def series_parallel(values: Iterable[float], *, component: str, connection: str) -> float:
    """Calcula el equivalente de resistencias o capacitores en SI."""
    items = list(values)
    if not items:
        raise ValueError("Ingresa al menos un componente.")
    if any(value <= 0 for value in items):
        raise ValueError("Todos los componentes deben ser mayores que cero.")
    if component == "resistencia":
        if connection == "serie":
            return sum(items)
        if connection == "paralelo":
            return 1.0 / sum(1.0 / value for value in items)
    elif component == "capacitor":
        if connection == "paralelo":
            return sum(items)
        if connection == "serie":
            return 1.0 / sum(1.0 / value for value in items)
    raise ValueError("Selecciona un componente y una conexión válidos.")


def coulomb_force(q1: float, q2: float, distance: float) -> float:
    """Magnitud de la fuerza de Coulomb en newtons (cargas en C, distancia en m)."""
    if distance <= 0:
        raise ValueError("La distancia debe ser mayor que cero.")
    return COULOMB_CONSTANT * abs(q1 * q2) / (distance**2)
