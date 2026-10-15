# Laboratorio No. 8 - Análisis de algoritmos

## video: https://youtu.be/yEErX_fD04I 
## Requisitos

Python 3.10 o superior y las bibliotecas `matplotlib`.

```bash
python -m pip install matplotlib
```

## Ejecución

Desde esta carpeta:

```bash
python laboratorio8.py --todos
```

También se puede ejecutar un solo ejercicio:

```bash
python laboratorio8.py --ejercicio 1 --timeout 5
```

El programa genera en `resultados/` un CSV y una gráfica PNG por ejercicio.
La gráfica usa escala logarítmica porque los valores de `n` crecen por
potencias de diez. `tiempo_microsegundos` queda vacío cuando el tamaño excede
el límite de tiempo; `operaciones_teoricas` siempre se calcula. Esto evita que
los tamaños 100000 y 1000000 bloqueen la computadora durante horas.

