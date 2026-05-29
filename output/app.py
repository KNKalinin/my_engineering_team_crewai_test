import tkinter as tk
from tkinter import messagebox
import threading
import time
from Snake import Snake, Direction, GameState

class SnakeGameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake Game Demo")
        self.root.resizable(False, False)
        
        # Game configuration
        self.board_width = 20
        self.board_height = 15
        self.cell_size = 20
        self.game_speed = 0.2
        
        # Initialize game backend
        self.game = Snake(self.board_width, self.board_height)
        
        # Game state
        self.running = False
        self.game_thread = None
        
        self._setup_ui()
        self._setup_controls()
        
    def _setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)
        
        # Score display
        self.score_label = tk.Label(main_frame, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(pady=(0, 10))
        
        # Game canvas
        canvas_width = self.board_width * self.cell_size
        canvas_height = self.board_height * self.cell_size
        
        self.canvas = tk.Canvas(
            main_frame,
            width=canvas_width,
            height=canvas_height,
            bg="black",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.canvas.pack()
        
        # Control buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=(10, 0))
        
        # Start/Restart button
        self.start_button = tk.Button(
            button_frame,
            text="Start Game",
            command=self._start_game,
            font=("Arial", 12)
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Reset button
        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            command=self._reset_game,
            font=("Arial", 12)
        )
        self.reset_button.pack(side=tk.LEFT)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Press Start to begin!", font=("Arial", 12))
        self.status_label.pack(pady=(10, 0))
        
        # Initial render
        self._render_game()
        
    def _setup_controls(self):
        # Bind keyboard events
        self.root.bind('<Key>', self._handle_keypress)
        self.root.focus_set()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
    def _handle_keypress(self, event):
        key = event.keysym.lower()
        
        # Direction controls
        direction_map = {
            'up': Direction.UP,
            'down': Direction.DOWN,
            'left': Direction.LEFT,
            'right': Direction.RIGHT,
            'w': Direction.UP,
            's': Direction.DOWN,
            'a': Direction.LEFT,
            'd': Direction.RIGHT
        }
        
        if key in direction_map:
            self.game.change_direction(direction_map[key])
            
    def _start_game(self):
        if not self.running:
            if self.game.get_state() == GameState.GAME_OVER:
                self.game.reset()
                
            self.game.start_game()
            self.running = True
            self.start_button.config(text="Running...", state="disabled")
            self.status_label.config(text="Game running! Use arrow keys or WASD")
            
            # Start game loop in separate thread
            self.game_thread = threading.Thread(target=self._game_loop, daemon=True)
            self.game_thread.start()
            
    def _reset_game(self):
        self.running = False
        if self.game_thread:
            self.game_thread.join(timeout=1.0)
            
        self.game.reset()
        self.start_button.config(text="Start Game", state="normal")
        self.status_label.config(text="Press Start to begin!")
        self._render_game()
        
    def _game_loop(self):
        while self.running and self.game.get_state() == GameState.RUNNING:
            self.game.update()
            
            # Schedule UI update on main thread
            self.root.after_idle(self._render_game)
            
            # Check for game over
            if self.game.get_state() == GameState.GAME_OVER:
                self.root.after_idle(self._handle_game_over)
                break
                
            time.sleep(self.game_speed)
            
    def _handle_game_over(self):
        self.running = False
        score = self.game.get_score()
        self.start_button.config(text="Start Game", state="normal")
        self.status_label.config(text=f"Game Over! Score: {score}")
        
    def _render_game(self):
        # Clear canvas
        self.canvas.delete("all")
        
        # Update score
        self.score_label.config(text=f"Score: {self.game.get_score()}")
        
        # Draw snake
        snake_body = self.game.get_snake_body()
        for i, (x, y) in enumerate(snake_body):
            x1 = x * self.cell_size
            y1 = y * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            # Different color for head
            color = "lightgreen" if i == 0 else "green"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="darkgreen")
            
        # Draw food
        food_x, food_y = self.game.get_food_position()
        fx1 = food_x * self.cell_size
        fy1 = food_y * self.cell_size
        fx2 = fx1 + self.cell_size
        fy2 = fy1 + self.cell_size
        self.canvas.create_rectangle(fx1, fy1, fx2, fy2, fill="red", outline="darkred")
        
        # Draw grid lines (optional, for better visibility)
        for i in range(self.board_width + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.board_height * self.cell_size, fill="gray25")
            
        for i in range(self.board_height + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.board_width * self.cell_size, y, fill="gray25")
            
    def _on_closing(self):
        self.running = False
        if self.game_thread:
            self.game_thread.join(timeout=1.0)
        self.root.destroy()
        
    def run(self):
        self.root.mainloop()

def main():
    app = SnakeGameUI()
    app.run()

if __name__ == "__main__":
    main()