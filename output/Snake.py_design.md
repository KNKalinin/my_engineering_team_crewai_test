# Snake Game Logic: Design Document

This document outlines the detailed design for the `snake.py` module. It is intended for the backend developer and describes all necessary components, classes, and methods to implement the core logic of a Snake game. The module is designed to be self-contained and framework-agnostic.

## 1. Overview

The `snake.py` module encapsulates the entire state and rules of the Snake game. It manages the game board, the snake's movement, food placement, collision detection, and scoring. The design allows a separate UI layer to easily interact with the game logic by calling update methods and querying the game state for rendering.

## 2. Module: `snake.py`

A single, self-contained Python module.

### Dependencies

-   `enum`: To create enumerations for game states and directions.
-   `random`: To handle random placement of food.
-   `typing`: For type hinting (`List`, `Tuple`, `TypeAlias`).

### Contents

-   **`Direction` (Enum)**: Represents the four possible directions of movement.
-   **`GameState` (Enum)**: Represents the different states of the game.
-   **`Point` (TypeAlias)**: A type alias for a coordinate tuple `(x, y)`.
-   **`Snake` (Class)**: The main class that contains all game logic and state.

---

## 3. Data Structures and Constants

### `Point`

A type alias for representing coordinates on the game grid.

-   **Type**: `TypeAlias = Tuple[int, int]`
-   **Description**: Represents an `(x, y)` coordinate pair on the game field.

### `Direction`

An `Enum` to provide clear, readable, and type-safe direction values.

-   **Enum Name**: `Direction`
-   **Members**:
    -   `UP = (0, -1)`
    -   `DOWN = (0, 1)`
    -   `LEFT = (-1, 0)`
    -   `RIGHT = (1, 0)`
-   **Description**: Each member holds a tuple representing the change in `(x, y)` for that direction. This simplifies movement logic.

### `GameState`

An `Enum` to manage the flow of the game.

-   **Enum Name**: `GameState`
-   **Members**:
    -   `READY`: The initial state before the game starts. The UI can display a "Press Start" message.
    -   `RUNNING`: The game is in progress. The `update()` method will advance the game state.
    -   `GAME_OVER`: The game has ended due to a collision. The UI can display the final score and a "Game Over" message.

---

## 4. Class `Snake`

This is the main class that orchestrates the entire game.

### Description

The `Snake` class holds the complete state of a single game instance. It is responsible for initializing the game, processing player input, updating the game state at each tick, and checking for game-over conditions.

### Attributes

| Attribute Name          | Type                     | Description                                                                                             |
| ----------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------- |
| `width`                 | `int`                    | The width of the game field in grid units.                                                              |
| `height`                | `int`                    | The height of the game field in grid units.                                                             |
| `snake_body`            | `List[Point]`            | A list of `Point` tuples representing the snake's segments. The head is at index `0`.                   |
| `food_position`         | `Point`                  | The `(x, y)` coordinates of the current food item.                                                      |
| `direction`             | `Direction`              | The current direction the snake is moving.                                                              |
| `score`                 | `int`                    | The player's current score.                                                                             |
| `state`                 | `GameState`              | The current state of the game (`READY`, `RUNNING`, `GAME_OVER`).                                        |
| `_initial_snake_length` | `int`                    | A constant defining the snake's starting length (e.g., 3).                                              |
| `_grow_snake`           | `bool`                   | A private flag that is set to `True` when the snake eats food, to signal growth on the next update.      |

### Methods

#### `__init__(self, width: int, height: int)`

-   **Signature**: `def __init__(self, width: int, height: int) -> None:`
-   **Description**: Constructor for the `Snake` class. It initializes the game dimensions and calls `reset()` to set up the initial game state.
-   **Parameters**:
    -   `width`: The width of the game board.
    -   `height`: The height of the game board.

#### `reset(self)`

-   **Signature**: `def reset(self) -> None:`
-   **Description**: Resets the game to its initial state. This method should be called to start a new game. It performs the following actions:
    1.  Sets `self.state` to `GameState.READY`.
    2.  Sets `self.score` to `0`.
    3.  Initializes `self.snake_body` to a starting position and length (e.g., `[(w/2, h/2), (w/2-1, h/2), (w/2-2, h/2)]`).
    4.  Sets the initial `self.direction` to `Direction.RIGHT`.
    5.  Calls `_place_food()` to position the first food item.
    6.  Resets internal flags like `_grow_snake` to `False`.

#### `change_direction(self, new_direction: Direction)`

-   **Signature**: `def change_direction(self, new_direction: Direction) -> None:`
-   **Description**: Updates the snake's direction based on player input. It includes logic to prevent the snake from immediately reversing on itself (e.g., if moving `RIGHT`, an input of `LEFT` is ignored). If the game state is `READY`, the first valid direction change will set the state to `RUNNING`.
-   **Parameters**:
    -   `new_direction`: The desired new `Direction` from player input.

#### `update(self)`

-   **Signature**: `def update(self) -> None:`
-   **Description**: This is the main "tick" function that advances the game forward by one step. It should only execute if `self.state` is `RUNNING`. The update cycle is as follows:
    1.  Calls `_move()` to update the snake's position.
    2.  Checks if the new snake head position is on the food. If so:
        -   Increment `self.score`.
        -   Set the `_grow_snake` flag to `True`.
        -   Call `_place_food()` to generate a new food location.
    3.  Calls `_check_collision()`. If a collision is detected, set `self.state` to `GameState.GAME_OVER`.

---

### Private Helper Methods

These methods are intended for internal use by the `Snake` class and should be prefixed with an underscore (`_`).

#### `_move(self)`

-   **Signature**: `def _move(self) -> None:`
-   **Description**: Calculates the new head position based on the current `self.direction`. A new head segment is inserted at the beginning of the `self.snake_body` list. If `_grow_snake` is `False`, the last segment of the tail is removed. If `_grow_snake` is `True`, the tail is not removed, and the flag is reset to `False`, effectively making the snake grow by one segment.

#### `_place_food(self)`

-   **Signature**: `def _place_food(self) -> None:`
-   **Description**: Finds a random `(x, y)` coordinate for the new food. It must ensure the new food position is not located on any of the snake's body segments. It will repeatedly generate random coordinates until a valid empty spot is found.

#### `_check_collision(self) -> bool`

-   **Signature**: `def _check_collision(self) -> bool:`
-   **Description**: Checks for game-ending collisions. Returns `True` if a collision occurs, otherwise `False`. A collision happens if:
    1.  The snake's head hits one of the four borders of the game field (`x < 0`, `x >= self.width`, `y < 0`, `y >= self.height`).
    2.  The snake's head collides with any part of its own body (i.e., the head's coordinates are present in the rest of `self.snake_body`).