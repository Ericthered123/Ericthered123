import svgwrite
import random
from datetime import datetime

# Parámetros de la tabla
ROWS = 7        # días
COLS = 52       # semanas
CELL_SIZE = 15  # px
FRAME_DELAY = 0.1  # segundos entre frames (para simulación)

# Genera la "matriz de commits" fake (para ejemplo)
grid = [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]

# Función para generar SVG de un frame
def draw_frame(snake_pos):
    dwg = svgwrite.Drawing('snake_contributions.svg', profile='tiny',
                           size=(COLS*CELL_SIZE, ROWS*CELL_SIZE))
    
    for r in range(ROWS):
        for c in range(COLS):
            color = "#ebedf0"  # gris base
            if grid[r][c]:
                color = "#40c463"  # verde commits
            if (r, c) in snake_pos:
                color = "#ff4500"  # color de la serpiente
            dwg.add(dwg.rect(insert=(c*CELL_SIZE, r*CELL_SIZE),
                             size=(CELL_SIZE-1, CELL_SIZE-1),
                             fill=color))
    dwg.save()

# Ejemplo de animación: una serpiente recorriendo diagonal
snake = []
for i in range(min(ROWS, COLS)):
    snake.append((i, i))
draw_frame(snake)
