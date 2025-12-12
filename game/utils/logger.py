import logging
import sys

def setup_logging():
    # REQ-TECH-07: Logging System
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("game.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
