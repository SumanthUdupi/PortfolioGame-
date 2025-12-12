# PortfolioGame

A Python/Pygame game demonstrating various game development concepts.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone [repository_url]
    cd PortfolioGame
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  **Ensure your virtual environment is activated.**
2.  **Run the main game file:**
    ```bash
    python main.py
    ```

## Controls

### Menu Scene:
*   **SPACE**: Start Game
*   **Q**: Quit Game

### Game Scene:
*   **ESC**: Return to Menu
*   **W, A, S, D** or **Arrow Keys**: Move Player (once player movement is implemented)

## Running Tests

1.  **Ensure your virtual environment is activated.**
2.  **Run tests using pytest:**
    ```bash
    pytest
    ```

## Project Structure

```
project/
├── main.py              # Entry point, game initialization, main loop
├── config.py            # Constants, settings, configurations, key bindings
├── game/
│   ├── scenes/          # Different game states/screens (e.g., title_screen.py, game_scene.py)
│   ├── entities/        # Player, enemies, items, projectiles, etc. (with components)
│   ├── systems/         # Collision, rendering, physics, AI, audio
│   ├── managers/        # Asset, audio, input, save/load managers
│   └── utils/           # Helper functions, math utilities, constants
├── assets/
│   ├── sprites/         # Images, spritesheets, animations
│   ├── sounds/          # Audio files (effects, music)
│   └── fonts/           # Font files, UI icons
├── tests/               # Unit tests, integration tests
├── requirements.txt     # Dependencies (pygame, pytest, etc.)
├── setup.py             # Packaging script for distribution
└── README.md           # Setup, play instructions, changelog
```

