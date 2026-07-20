import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#game window
window = tkinter.Tk()
window.title("snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))
#format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) #single tile, snake's head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body = [] #multiple snake tiles
velocityX = 0
velocityY = 0
game_over = False
score = 0


def spawn_food():
    """Place food on a random tile that isn't occupied by the snake."""
    global food
    while True:
        fx = random.randint(0, COLS-1) * TILE_SIZE
        fy = random.randint(0, ROWS-1) * TILE_SIZE

        collision = (fx == snake.x and fy == snake.y)
        if not collision:
            for tile in snake_body:
                if fx == tile.x and fy == tile.y:
                    collision = True
                    break

        if not collision:
            food = Tile(fx, fy)
            return


def reset_game():
    global snake, food, snake_body, velocityX, velocityY, game_over, score
    snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0
    spawn_food()


def change_direction(e): #e = event
    global velocityX, velocityY, game_over

    if (game_over):
        if (e.keysym in ("space", "Return")):
            reset_game()
        return

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score
    if (game_over):
        return

    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return

    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return



    #collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        score += 1
        spawn_food()

    #update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

     #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "red")

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "lime green")

    if (game_over):
        canvas.create_rectangle(0, WINDOW_HEIGHT/2 - 40, WINDOW_WIDTH, WINDOW_HEIGHT/2 + 40, fill = "black", outline = "")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 15, font = "Arial 20", text = f"Game Over: {score}", fill = "white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 15, font = "Arial 12", text = "Press SPACE to restart", fill = "white")
    else:
        canvas.create_rectangle(0, 0, WINDOW_WIDTH, 26, fill = "black", outline = "")
        canvas.create_text(45, 15, font = "Arial 12", text = f"Score: {score}", fill = "white")

    window.after(100, draw) #100ms = 1/10 second, 10 frames/second

spawn_food()
draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()
