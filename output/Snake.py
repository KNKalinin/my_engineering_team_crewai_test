from enum import Enum
import random
from typing import List, Tuple, TypeAlias

# Type alias for coordinates
Point: TypeAlias = Tuple[int, int]

class Direction(Enum):
    """Direction enumeration with coordinate changes"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class GameState(Enum):
    """Game state enumeration"""
    READY = "ready"
    RUNNING = "running"
    GAME_OVER = "game_over"

class Snake:
    """Main Snake game logic class"""
    
    def __init__(self, width: int, height: int) -> None:
        """Initialize the Snake game with given dimensions"""
        self.width = width
        self.height = height
        self._initial_snake_length = 3
        self._grow_snake = False
        self.reset()
    
    def reset(self) -> None:
        """Reset the game to initial state"""
        self.state = GameState.READY
        self.score = 0
        self.direction = Direction.RIGHT
        self._grow_snake = False
        
        # Initialize snake in center, moving right
        center_x = self.width // 2
        center_y = self.height // 2
        
        self.snake_body = []
        for i in range(self._initial_snake_length):
            self.snake_body.append((center_x - i, center_y))
        
        self._place_food()
    
    def change_direction(self, new_direction: Direction) -> None:
        """Change snake direction with reverse prevention"""
        if self.state == GameState.GAME_OVER:
            return
        
        # Get current direction vector
        current_dx, current_dy = self.direction.value
        new_dx, new_dy = new_direction.value
        
        # Prevent immediate reversal
        if (current_dx + new_dx == 0) and (current_dy + new_dy == 0):
            return
        
        self.direction = new_direction
        
        # Start game on first valid direction change
        if self.state == GameState.READY:
            self.state = GameState.RUNNING
    
    def update(self) -> None:
        """Update game state by one tick"""
        if self.state != GameState.RUNNING:
            return
        
        # Calculate next head position
        head_x, head_y = self.snake_body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Check if new position will eat food
        will_eat_food = (new_head == self.food_position)
        
        # Move the snake
        self.snake_body.insert(0, new_head)
        
        # Handle food consumption and growth
        if will_eat_food:
            self.score += 1
            self._place_food()
            # Don't remove tail (grow by 1 segment)
        else:
            # Remove tail (maintain same length)
            self.snake_body.pop()
        
        # Check for collisions
        if self._check_collision():
            self.state = GameState.GAME_OVER
    
    def _place_food(self) -> None:
        """Place food at random empty position"""
        attempts = 0
        max_attempts = self.width * self.height
        
        while attempts < max_attempts:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            food_pos = (x, y)
            
            # Ensure food is not on snake body
            if food_pos not in self.snake_body:
                self.food_position = food_pos
                return
            
            attempts += 1
        
        # Fallback if board is nearly full
        for y in range(self.height):
            for x in range(self.width):
                pos = (x, y)
                if pos not in self.snake_body:
                    self.food_position = pos
                    return
    
    def _check_collision(self) -> bool:
        """Check for boundary or self-collision"""
        head_x, head_y = self.snake_body[0]
        
        # Check boundary collision
        if (head_x < 0 or head_x >= self.width or 
            head_y < 0 or head_y >= self.height):
            return True
        
        # Check self-collision (head with body)
        if self.snake_body[0] in self.snake_body[1:]:
            return True
        
        return False
    
    # Getter methods for UI access
    def get_snake_body(self) -> List[Point]:
        """Get snake body segments"""
        return self.snake_body.copy()
    
    def get_food_position(self) -> Point:
        """Get food position"""
        return self.food_position
    
    def get_score(self) -> int:
        """Get current score"""
        return self.score
    
    def get_state(self) -> GameState:
        """Get current game state"""
        return self.state
    
    def start_game(self) -> None:
        """Start the game from ready state"""
        if self.state == GameState.READY:
            self.state = GameState.RUNNING