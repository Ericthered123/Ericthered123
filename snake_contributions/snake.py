import svgwrite
from github import Github
import os
import datetime

# --- Config ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "Ericthered123"
SVG_PATH = "snake_contributions.svg"
CELL_SIZE = 15
ROWS = 7
COLS = 52

# --- Conectar con GitHub ---
g = Github(GITHUB_TOKEN)
user = g.get_user(USERNAME)

# --- Crear grid de contribuciones ---
# 7 filas (días) x 52 semanas
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Fecha de hace 1 año
start_date = datetime.datetime.now() - datetime.timedelta(weeks=52)

for week in range(COLS):
    for day in range(ROWS):
        date = start_date + datetime.timedelta(weeks=week, days=day)
        # Obtener commits en esta fecha
        commits = user.get_events()  # get_events devuelve eventos recientes
        # Contamos solo los commits que caen en esa fecha
        count = sum(
            1 for c in commits 
            if c.created_at.date() == date.date() and c.type == "PushEvent"
        )
        grid[day][week] = 1 if count > 0 else 0

# --- Dibujo del SVG ---
dwg = svgwrite.Drawing(SVG_PATH, profile='tiny',
                       size=(COLS*CELL_SIZE, ROWS*CELL_SIZE))

# Generamos una serpiente simple recorriendo diagonal
snake = []
for i in range(min(ROWS, COLS)):
    snake.append((i, i))

for r in range(ROWS):
    for c in range(COLS):
        color = "#ebedf0"  # gris base
        if grid[r][c]:
            color = "#40c463"  # verde commits
        if (r, c) in snake:
            color = "#ff4500"  # serpiente
        dwg.add(dwg.rect(insert=(c*CELL_SIZE, r*CELL_SIZE),
                         size=(CELL_SIZE-1, CELL_SIZE-1),
                         fill=color))
dwg.save()
print(f"SVG generado: {SVG_PATH}")
