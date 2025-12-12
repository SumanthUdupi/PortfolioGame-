import json
from pathlib import Path
from typing import Dict, Any, Optional
import time
from datetime import datetime

class SaveManager:
    """
    Manages saving and loading game data to and from the filesystem.
    Handles save file versioning and naming.
    """

    def __init__(self, saves_directory: str = "saves"):
        """
        Initializes the SaveManager, creating the save directory if it doesn't exist.

        Args:
            saves_directory (str): The name of the directory to store save files in.
        """
        self.saves_directory = Path(saves_directory)
        self.saves_directory.mkdir(exist_ok=True)
        self.max_save_files = 10
        self.current_save_version = "1.0"

    def save_game(self, game_data: Dict[str, Any], filename: Optional[str] = None) -> bool:
        """
        Saves the provided game data to a JSON file.

        Args:
            game_data (Dict[str, Any]): The game state data to save.
            filename (Optional[str]): The name of the save file. If not provided, a timestamped
                                     filename is generated.

        Returns:
            bool: True if saving was successful, False otherwise.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"save_{timestamp}"

        save_path = self.saves_directory / f"{filename}.json"

        try:
            save_package = {
                "version": self.current_save_version,
                "timestamp": time.time(),
                "data": game_data
            }

            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_package, f, indent=2)
            
            print(f"Game saved successfully to {save_path}")
            return True

        except Exception as e:
            print(f"Failed to save game: {e}")
            return False

    def load_game(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Loads game data from a specified JSON file.

        Args:
            filename (str): The name of the save file to load.

        Returns:
            Optional[Dict[str, Any]]: The loaded game state data, or None if loading fails.
        """
        save_path = self.saves_directory / f"{filename}.json"

        if not save_path.is_file():
            print(f"Error: Save file not found at {save_path}")
            return None

        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                save_package = json.load(f)

            save_version = save_package.get("version")
            if save_version != self.current_save_version:
                print(f"Warning: Save file version '{save_version}' does not match "
                      f"current game version '{self.current_save_version}'. "
                      "Data might not load correctly.")
                # In a real game, data migration logic would be needed here.

            return save_package.get("data")

        except Exception as e:
            print(f"Failed to load game from {save_path}: {e}")
            return None
            
    def list_saves(self) -> List[Path]:
        """Lists all available save files."""
        return sorted(self.saves_directory.glob('*.json'), key=os.path.getmtime, reverse=True)
