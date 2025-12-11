# Neon Space Shooter

A fast-paced, neon-styled vertical scrolling space shooter built with Python and Pygame.

## Features

*   **Beautiful Neon Visuals**: Procedurally generated glowing sprites and particle effects.
*   **Classic Gameplay**: Dodge enemies, shoot them down, and aim for the high score.
*   **Audio**: Synthesized sound effects.
*   **Save System**: High scores are persisted.

## Requirements

*   Python 3.8+
*   Pygame 2.0+

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Game

1.  **Generate Assets**:
    Before running the game for the first time, generate the assets:
    ```bash
    python3 tools/asset_generator.py
    ```
    This will create the necessary sprites and sounds in the `assets/` directory.

2.  **Start the Game**:
    ```bash
    python3 main.py
    ```

## Packaging (Optional)

To create a standalone executable:

1.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2.  Build the executable:
    ```bash
    pyinstaller --onefile --noconsole --name "NeonSpaceShooter" --add-data "assets:assets" main.py
    ```
    *Note: On Windows, use `;` instead of `:` for `--add-data`.*

3.  The executable will be in the `dist/` folder.

## Controls

*   **Arrow Keys / WASD**: Move the ship
*   **Space / Left Click**: Shoot
*   **ESC**: Quit (Menu) / Return to Menu (Game Over)

## Structure

*   `game/`: Source code
    *   `entities/`: Game objects (Player, Enemy, etc.)
    *   `managers/`: Systems (Input, Assets, Scenes)
    *   `scenes/`: Game states (Title, Game, GameOver)
*   `assets/`: Generated images and sounds
*   `tools/`: Helper scripts

## Credits

Created by Jules (AI Assistant).
