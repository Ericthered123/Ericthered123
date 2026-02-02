import os
from github import Github
from PIL import Image, ImageDraw
import datetime

# --- Config ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "Ericthered123"
GIF_PATH = "snake_contributions.gif"
CELL_SIZE = 15
ROWS = 7
COLS = 52
SNAKE_COLOR = (255, 69, 0)
COMMIT_COLOR = (64, 196, 99)
BG_COLOR = (235, 237, 240)

# --- Conectar con GitHub ---
g = Github(GITHUB_TOKEN)
user = g.get_user(USERNAME)

# --- Crear grid de commits reales (simplificado usando últimos eventos) ---
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
start_date = datetime.datetime.now() - datetime.timedelta(weeks=52)

events = list(user.get_events())  # eventos recientes

for week in range(COLS):
    for day in range(ROWS):
        date = start_date + datetime.timedelta(weeks=week, days=day)
        count = sum(1 for e in events if e.created_at.date() == date.date() and e.type=="PushEvent")
        grid[day][week] = 1 if count>0 else 0

# --- Generar frames del GIF ---
frames = []
snake = []
max_len = 10  # longitud de la serpiente

# Recorrido simple: fila por fila
for r in range(ROWS):
    for c in range(COLS):
        snake.append((r, c))
        if len(snake) > max_len:
            snake.pop(0)

        # Crear imagen
        img = Image.new("RGB", (COLS*CELL_SIZE, ROWS*CELL_SIZE), BG_COLOR)
        draw = ImageDraw.Draw(img)

        for i in range(ROWS):
            for j in range(COLS):
                x0, y0 = j*CELL_SIZE, i*CELL_SIZE
                x1, y1 = x0+CELL_SIZE-1, y0+CELL_SIZE-1
                color = COMMIT_COLOR if grid[i][j] else BG_COLOR
                if (i,j) in snake:
                    color = SNAKE_COLOR
                draw.rectangle([x0, y0, x1, y1], fill=color)

        frames.append(img)

# --- Guardar GIF animado ---
frames[0].save(GIF_PATH, save_all=True, append_images=frames[1:], duration=200, loop=0)
print(f"GIF generado: {GIF_PATH}")
