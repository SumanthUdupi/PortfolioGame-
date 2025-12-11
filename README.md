# Pixel Art RPG Portfolio - The System Chronicles

An innovative professional development game that transforms real career achievements into an immersive gaming experience. Navigate "The System" - a digital ecosystem representing the modern professional landscape - where professional skills become game mechanics, career milestones become quests, and portfolio development becomes character progression.

## Features

- **Four Professional Zones**: Enterprise Integration, Data Processing, Analytics Academy, and Engineering Workshop
- **Authentic Professional Mapping**: Real career achievements converted to gameplay mechanics
- **Gherkin Puzzles**: Write user stories meeting quality standards
- **API Validation**: REST API testing and documentation challenges
- **SQL Query Building**: Database interaction challenges
- **Analytics Dashboards**: Data visualization and predictive modeling
- **Blueprint Design**: System architecture and QA challenges
- **Progression System**: Level up through professional skill demonstration
- **Save/Load System**: JSON-based game state persistence
- **Audio System**: Volume controls with placeholder audio feedback

## System Requirements

- **Operating System**: Windows 10 or higher
- **Python Version**: Python 3.8 or higher (for source installation)
- **RAM**: Minimum 2GB
- **Storage**: 100MB free space
- **Display**: 1280x720 resolution or higher

## Installation

### Option 1: Standalone Executable (Recommended for End Users)

1. Download the `Pixel_Art_RPG_Portfolio.exe` file from the releases page
2. Double-click the executable to run the game
3. No installation required - the game runs directly from the executable

### Option 2: From Source Code

#### Prerequisites
- Python 3.8 or higher
- pip package manager

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Alternative Installation
```bash
pip install .
```

## Running the Game

### Direct Execution
```bash
python main.py
```

### Installed Execution
```bash
system-chronicles
```

## Controls

- **WASD**: Move player
- **E**: Interact with objects
- **1-4**: Switch between zones
- **ESC**: Pause/return to menu
- **Mouse**: UI interactions

## Gameplay Instructions

### Getting Started
1. Launch the game using either the executable or by running `python main.py`
2. Navigate through the menu to start a new game or load a saved game
3. Use WASD to move your character around the game world

### Professional Zones
Explore four distinct professional zones, each representing different aspects of a technical career:

- **Zone 1: Enterprise Integration** - Focus on agile practices and API development
- **Zone 2: Data Processing** - Master SQL queries and data analytics
- **Zone 3: Analytics Academy** - Learn statistical modeling and research
- **Zone 4: Engineering Workshop** - Design systems and ensure quality

### Objectives
- Complete challenges in each zone to demonstrate professional skills
- Progress through levels by successfully solving technical problems
- Build your portfolio by mastering various professional competencies
- Save your progress to continue your journey

### Tips
- Read challenge descriptions carefully before attempting solutions
- Use the pause menu (ESC) to review controls or exit to menu
- Your progress is automatically saved when completing challenges

## Game Zones

### Zone 1: Enterprise Integration
- Gherkin user story crafting
- API validation challenges
- Agile ceremony management

### Zone 2: Data Processing
- SQL query building
- Content moderation puzzles
- Analytics dashboard creation

### Zone 3: Analytics Academy
- Statistical model building
- Research paper decryption
- Algorithm implementation

### Zone 4: Engineering Workshop
- System blueprint design
- Process optimization
- Quality assurance testing

## Technical Architecture

- **Game Loop**: Fixed timestep at 60 FPS
- **Scene Management**: State-based scene transitions
- **Entity System**: Component-based architecture
- **Collision Detection**: Bounding box collision system
- **Asset Management**: LRU caching with placeholder assets
- **Save System**: JSON-based persistence

## Testing

Run unit tests:
```bash
python -m unittest tests/test_core.py
```

## Troubleshooting

### Game Won't Start
- **Executable version**: Ensure you have Windows 10 or higher. Try running as administrator.
- **Source version**: Verify Python 3.8+ is installed and all dependencies are installed via `pip install -r requirements.txt`

### Performance Issues
- Close other applications to free up RAM
- Lower display resolution if available
- The game requires at least 2GB RAM

### Audio Problems
- Audio is currently placeholder text-based feedback
- Volume controls are implemented but may not affect actual audio output

### Save File Issues
- Save files are stored as `savegame.json` in the game directory
- Delete the save file to reset progress if corrupted
- Ensure write permissions in the game directory

### Missing Assets
- The game uses placeholder graphics (colored rectangles)
- All required assets are included in the distribution

### Python Import Errors
- Ensure all packages from `requirements.txt` are installed
- Try reinstalling dependencies: `pip uninstall -r requirements.txt && pip install -r requirements.txt`

## Project Structure

```
pixel-art-rpg-portfolio/
├── main.py                 # Game entry point
├── config.py              # Game configuration
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
├── README.md             # This file
├── game/                 # Game modules
│   ├── managers/         # Game managers
│   │   ├── game_manager.py
│   │   ├── scene_manager.py
│   │   ├── asset_manager.py
│   │   ├── input_manager.py
│   │   ├── save_manager.py
│   │   └── audio_manager.py
│   ├── scenes/           # Game scenes
│   │   ├── base_scene.py
│   │   ├── menu_scene.py
│   │   ├── game_scene.py
│   │   └── zones/        # Zone implementations
│   ├── entities/         # Game entities
│   │   ├── entity.py
│   │   └── player.py
│   ├── systems/          # Game systems
│   │   └── collision_system.py
│   └── utils/            # Utility functions
├── assets/               # Game assets
│   ├── sprites/          # Sprite images
│   ├── sounds/           # Audio files
│   └── fonts/            # Font files
└── tests/                # Unit tests
    └── test_core.py
```

## Known Limitations

- **Graphics**: Currently uses placeholder graphics (colored rectangles) instead of actual sprites
- **Audio**: Audio system provides text-based feedback only; no actual sound files are played
- **Platform**: Currently only supports Windows; Linux/Mac support not tested
- **Performance**: May experience slowdowns on systems with less than 2GB RAM
- **Save System**: Basic JSON-based saving; no cloud sync or multiple save slots
- **UI/UX**: Basic GUI implementation; advanced features like fullscreen mode not implemented
- **Multiplayer**: No multiplayer or online features
- **Accessibility**: Limited accessibility features; no screen reader support

## Development

This game uses Pygame for graphics and game logic. All assets are currently placeholders (colored rectangles) with text-based audio feedback. The game is designed to be extensible with real assets and more complex mechanics.

## Credits

**Game Developer**: Senior Technical Leader

**Technologies Used**:
- **Pygame**: Game framework and graphics
- **Pygame GUI**: User interface components
- **PyTMX**: Tiled map support
- **Pillow**: Image processing
- **NumPy**: Numerical computations
- **JSON Schema**: Data validation

**Special Thanks**:
- Open source community for the amazing libraries
- Professional mentors and colleagues for inspiration
- The gaming community for continuous feedback

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please ensure all new code includes appropriate tests and follows the existing code style.

## Support

For support or questions, please open an issue on the project repository.