# mindmapper_ai.py
import subprocess
import sys

# Step 1: Try to import textblob, else install it
try:
    from textblob import TextBlob
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "textblob"])
    from textblob import TextBlob
    import nltk
    nltk.download('punkt')
    nltk.download('brown')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('conll2000')
    nltk.download('movie_reviews')

import tkinter as tk
import random

# Emotion configuration
emotion_settings = {
    'positive': {'color': 'lightgreen', 'speed': 100, 'walls': 5},
    'negative': {'color': 'gray', 'speed': 50, 'walls': 15},
    'neutral': {'color': 'lightblue', 'speed': 75, 'walls': 10}
}

# Emotion classification
def classify_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return 'positive'
    elif polarity < -0.2:
        return 'negative'
    else:
        return 'neutral'

# Maze Game Class
class EmotionMazeGame:
    def __init__(self, master, emotion):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=400, bg=emotion_settings[emotion]['color'])
        self.canvas.pack()
        self.speed = emotion_settings[emotion]['speed']
        self.walls = emotion_settings[emotion]['walls']
        self.player = self.canvas.create_rectangle(20, 20, 40, 40, fill='blue')
        self.create_walls()
        self.master.bind("<KeyPress>", self.move_player)

    def create_walls(self):
        self.wall_rects = []
        for _ in range(self.walls):
            x1 = random.randint(50, 350)
            y1 = random.randint(50, 350)
            x2 = x1 + 40
            y2 = y1 + 40
            wall = self.canvas.create_rectangle(x1, y1, x2, y2, fill='black')
            self.wall_rects.append(wall)
        self.exit = self.canvas.create_rectangle(360, 360, 390, 390, fill='gold')

    def move_player(self, event):
        if event.keysym == 'Up':
            self.canvas.move(self.player, 0, -10)
        elif event.keysym == 'Down':
            self.canvas.move(self.player, 0, 10)
        elif event.keysym == 'Left':
            self.canvas.move(self.player, -10, 0)
        elif event.keysym == 'Right':
            self.canvas.move(self.player, 10, 0)
        self.check_collision()

    def check_collision(self):
        player_coords = self.canvas.bbox(self.player)
        for wall in self.wall_rects:
            if self.canvas.bbox(wall) and self.overlaps(player_coords, self.canvas.bbox(wall)):
                self.canvas.create_text(200, 200, text="Game Over", fill="red", font=("Arial", 20))
                self.master.unbind("<KeyPress>")
        if self.overlaps(player_coords, self.canvas.bbox(self.exit)):
            self.canvas.create_text(200, 200, text="You Win!", fill="green", font=("Arial", 20))
            self.master.unbind("<KeyPress>")

    def overlaps(self, box1, box2):
        return not (
            box1[2] < box2[0] or box1[0] > box2[2] or
            box1[3] < box2[1] or box1[1] > box2[3]
        )

# Start game from emotion input
def start_game():
    user_text = input_field.get("1.0", "end").strip()
    emotion = classify_emotion(user_text)
    emotion_window.destroy()
    game_window = tk.Tk()
    game_window.title("MindMapper AI - Emotion Maze")
    EmotionMazeGame(game_window, emotion)
    game_window.mainloop()

# Initial Input Window
emotion_window = tk.Tk()
emotion_window.title("MindMapper AI")
emotion_window.geometry("400x250")

tk.Label(emotion_window, text="Describe how you're feeling:", font=("Arial", 12)).pack(pady=10)
input_field = tk.Text(emotion_window, height=4, width=40)
input_field.pack()

tk.Button(emotion_window, text="Start Game", command=start_game, bg="purple", fg="white", font=("Arial", 12)).pack(pady=10)
emotion_window.mainloop()
