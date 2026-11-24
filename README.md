# ElectroCalc

Aplicación de escritorio en español para cálculos eléctricos, creada con Python y Tkinter. Incluye una pantalla de bienvenida con navegación entre calculadoras, controles de unidades SI de pico a mega y validaciones claras.

La interfaz usa un tema oscuro. La bienvenida muestra las tres calculadoras como tarjetas clicables en una sola fila. En cada calculadora, el resultado aparece en el recuadro destacado debajo de los campos, después de pulsar el botón **Calcular** correspondiente.

## Requisitos

- Python 3.10 o posterior.
- Tkinter, incluido normalmente con Python.

## Ejecución

```bash
python main.py
```

## Calculadoras

- **Ley de Ohm:** ingresa exactamente dos de los valores de voltaje (V), corriente (A) y resistencia (Ω); el tercero se calcula. El resultado usa el prefijo elegido para esa magnitud.
- **Serie y paralelo:** selecciona resistencia o capacitor, conexión, prefijo para cada componente y prefijo de salida. Admite hasta 10 campos; los vacíos se ignoran. Se requiere al menos un valor positivo.
- **Ley de Coulomb:** calcula la magnitud `F = k · |q₁ q₂| / r²`. Las cargas pueden ser positivas o negativas; la distancia debe ser positiva. La constante utilizada es `k = 8.9875517862 × 10⁹ N·m²/C²`, derivada de la permitividad del vacío CODATA 2022 publicada por [NIST](https://physics.nist.gov/cuu/Constants/Value?ep0%7Csearch_for=electron-neutron).

Los prefijos disponibles son pico (`p`), nano (`n`), micro (`µ`), mili (`m`), unidad base, kilo (`k`) y mega (`M`). En las calculadoras que lo permiten, se usan campos vacíos para indicar los valores que se desean calcular.

## Estructura

```text
electrocalc/
├── electrocalc/
│   ├── calculations.py   # fórmulas, validaciones y conversiones SI
│   └── ui/app.py         # interfaz gráfica y navegación Tkinter
├── main.py               # punto de entrada
└── README.md
```
