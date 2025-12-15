import tkinter as tk
import random
import time
import threading
try:
    import pygame
    pygame.mixer.init()
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False
    print("Pygame not found, sound disabled.")

# Optional: Replace with your own .wav file paths
SHOOT_SOUND = 'shoot.wav'
HIT_SOUND = 'hit.wav'

# Game Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SPEED = 20
BULLET_SPEED = 15
ENEMY_SPEED = 3
GAME_TIME = 60  # seconds

class Bullet:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x+10, y+10, fill='blue')
    
    def move(self):
        self.canvas.move(self.id, 0, -BULLET_SPEED)
        coords = self.canvas.coords(self.id)
        return coords[1] > 0

class Enemy:
    def __init__(self, canvas):
        self.canvas = canvas
        x = random.randint(50, WINDOW_WIDTH - 50)
        self.id = canvas.create_rectangle(x, 0, x+40, 40, fill='red')
    
    def move(self):
        self.canvas.move(self.id, 0, ENEMY_SPEED)
        coords = self.canvas.coords(self.id)
        return coords[3] < WINDOW_HEIGHT

class WaterGunGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Gun Battle Game")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='white')
        self.canvas.pack()

        # Player
        self.player = self.canvas.create_rectangle(WINDOW_WIDTH//2 - 25, WINDOW_HEIGHT - 50,
                                                   WINDOW_WIDTH//2 + 25, WINDOW_HEIGHT - 20, fill='green')
        
        # Game Elements
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.health = 5
        self.running = True
        self.remaining_time = GAME_TIME

        # UI
        self.score_text = self.canvas.create_text(70, 20, text=f"Score: {self.score}", font=('Arial', 14))
        self.health_text = self.canvas.create_text(200, 20, text=f"Health: {self.health}", font=('Arial', 14))
        self.timer_text = self.canvas.create_text(330, 20, text=f"Time: {self.remaining_time}", font=('Arial', 14))
        
        # Controls
        self.root.bind('<Left>', lambda e: self.move_player(-PLAYER_SPEED))
        self.root.bind('<Right>', lambda e: self.move_player(PLAYER_SPEED))
        self.root.bind('<space>', lambda e: self.shoot())

        # Start game loop
        self.spawn_enemy_loop()
        self.update_loop()
        self.timer_loop()

    def move_player(self, dx):
        self.canvas.move(self.player, dx, 0)
        coords = self.canvas.coords(self.player)
        if coords[0] < 0:
            self.canvas.move(self.player, -coords[0], 0)
        elif coords[2] > WINDOW_WIDTH:
            self.canvas.move(self.player, WINDOW_WIDTH - coords[2], 0)

    def shoot(self):
        coords = self.canvas.coords(self.player)
        bullet = Bullet(self.canvas, (coords[0] + coords[2]) / 2 - 5, coords[1] - 10)
        self.bullets.append(bullet)
        if SOUND_ENABLED:
            pygame.mixer.Sound(SHOOT_SOUND).play()

    def spawn_enemy_loop(self):
        if self.running:
            enemy = Enemy(self.canvas)
            self.enemies.append(enemy)
            self.root.after(random.randint(1000, 2000), self.spawn_enemy_loop)

    def update_loop(self):
        if not self.running:
            return

        # Update bullets
        new_bullets = []
        for bullet in self.bullets:
            if bullet.move():
                new_bullets.append(bullet)
        self.bullets = new_bullets

        # Update enemies
        new_enemies = []
        for enemy in self.enemies:
            if enemy.move():
                new_enemies.append(enemy)
            else:
                self.health -= 1
                self.canvas.itemconfig(self.health_text, text=f"Health: {self.health}")
                if SOUND_ENABLED:
                    pygame.mixer.Sound(HIT_SOUND).play()
                if self.health <= 0:
                    self.end_game()
                    return
        self.enemies = new_enemies

        # Check collisions
        self.check_collisions()

        # Refresh the canvas
        self.root.after(30, self.update_loop)

    def check_collisions(self):
        for bullet in list(self.bullets):
            bullet_coords = self.canvas.coords(bullet.id)
            for enemy in list(self.enemies):
                enemy_coords = self.canvas.coords(enemy.id)
                if self.intersect(bullet_coords, enemy_coords):
                    self.canvas.delete(bullet.id)
                    self.canvas.delete(enemy.id)
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                    break

    def intersect(self, a, b):
        return not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3])

    def timer_loop(self):
        if not self.running:
            return
        if self.remaining_time <= 0:
            self.end_game()
            return
        self.remaining_time -= 1
        self.canvas.itemconfig(self.timer_text, text=f"Time: {self.remaining_time}")
        self.root.after(1000, self.timer_loop)

    def end_game(self):
        self.running = False
        self.canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, text=f"Game Over!\nScore: {self.score}",
                                font=('Arial', 24), fill='black')
        restart_button = tk.Button(self.root, text="Restart", command=self.restart)
        self.canvas.create_window(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 80, window=restart_button)

    def restart(self):
        self.canvas.delete("all")
        self.__init__(self.root)

# Start the Game
if __name__ == "__main__":
    root = tk.Tk()
    game = WaterGunGame(root)
    root.mainloop()