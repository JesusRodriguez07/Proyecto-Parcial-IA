# Proyecto-parcial-IA

## jesus rodriguez

## 12-sisn-2-043

## Proyecto

# Robotron IA – Examen Final

### Autor: Jesús Rodríguez  
### Matrícula: 12-sisn-2-043

---

## 🎮 Descripción del juego

Este es un clon inspirado en *Robotron 2084*, desarrollado completamente desde cero con Python y Pygame.  
El jugador debe sobrevivir en un entorno hostil lleno de enemigos, mientras rescata humanos y evita ser destruido.

- Enemigos persiguen y disparan.
- Humanos pueden ser convertidos en enemigos.
- Niveles progresivos y dificultad creciente.

---

## 🧪 Inteligencia Artificial implementada

### ✔️ Árbol de comportamiento (Behavior Tree)

Implementado en `arbol_comportamiento.py`, y utilizado por enemigos como:
- `Enemigo`: elige si atacar al jugador, perseguir un humano o buscar con A*.
- `EnemigoConversor`: puede convertir humanos en enemigos.

### ✔️ Algoritmo A*

Implementado en `a_estrella.py`.  
Usado por los enemigos para planificar rutas óptimas hacia el jugador en una grilla.

---

## 🕹️ Controles

### Teclado:
- Flechas: mover al jugador
- ESC: pausar juego
- ENTER: confirmar en menú

### Gamepad (obligatorio y soportado):
- Stick izquierdo: moverse
- Stick derecho: disparar
- Botón Gatillo izquierdo: pausa 
- Botón A / X: confirmar

---

## 🔊 Recursos

- Sonido y música descargados de uso libre o generados.
- Sprites editados y adaptados, algunos de juegos clásicos.

---

## 📁 Estructura del proyecto

```
proyecto/
│── main.py
├── scripts/
│   ├── jugador.py
│   ├── enemigo.py
│   ├── ...
├── assets/
│   ├── images/
│   ├── sounds/
│   ├── music/
├── requirements.txt
├── README.md
└── info.txt
```

---

## 📆 Requisitos

### Librerías necesarias:
```
pygame>=2.5.2
```

Instalar con:

```bash
pip install -r requirements.txt
```

---

## 📹 Video explicativo

El video explicativo (en formato MP4, resolución 720p) está incluido en el ZIP.  
En él se muestra el funcionamiento del juego, su estructura, la IA implementada y un gameplay completo.

---

## 🥺 Evaluación

- ✅ Árbol de Comportamiento
- ✅ A* desde cero
- ✅ Gamepad funcional
- ✅ Sonido y sprites integrados
- ✅ Menú de inicio y pausa
- ✅ Estructura, commits y README

---

## 🔗 GitHub

Repositorio del proyecto:  
[https://github.com/JesusRodriguez07/Proyecto-Parcial-IA](https://github.com/JesusRodriguez07/Proyecto-Parcial-IA)
