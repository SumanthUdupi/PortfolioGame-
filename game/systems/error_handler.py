import pygame
import traceback
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import json

class ErrorSeverity(Enum):
    """Defines the severity level of an error for prioritization."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Categorizes errors for specific handling strategies."""
    USER_INPUT = "user_input"
    SYSTEM_RESOURCE = "system_resource"
    GAME_LOGIC = "game_logic"
    ACCESSIBILITY = "accessibility"
    PROFESSIONAL_CONTENT = "professional_content"
    NETWORK = "network"
    DATA_VALIDATION = "data_validation"
    ASSET_LOADING = "asset_loading"

@dataclass
class UserGuidanceContext:
    """Holds context about the user to provide tailored guidance."""
    user_experience_level: str  # "beginner", "intermediate", "advanced"
    accessibility_mode: bool
    professional_context: bool
    current_task: str
    previous_errors: List[str]
    user_preferences: Dict[str, Any]

class ErrorHandler:
    """A comprehensive system for handling errors and providing user guidance."""

    def __init__(self):
        """Initializes the error handler with history and resolution strategies."""
        self.error_history = []
        self.user_guidance_context = UserGuidanceContext(
            user_experience_level="intermediate",
            accessibility_mode=False,
            professional_context=True,
            current_task="",
            previous_errors=[],
            user_preferences={}
        )
        # In a full implementation, templates would be loaded from external files.
        self.guidance_templates = self._load_guidance_templates()
        self.professional_guidance = self._load_professional_guidance()

    def _load_guidance_templates(self) -> Dict[str, Dict]:
        """Loads predefined templates for user guidance messages."""
        return {
            "beginner": {
                ErrorCategory.USER_INPUT: {
                    "template": "It looks like there was an issue with '{action}'. Please try the following steps.",
                    "steps": [
                        "Ensure the correct keys are being used.",
                        "Check if the intended UI element is selected.",
                        "Press F1 for a detailed help menu."
                    ]
                }
            }
        }

    def _load_professional_guidance(self) -> Dict[str, Dict]:
        """Loads guidance specific to professional context errors."""
        return {
            "portfolio_export": {
                "common_issues": ["File format compatibility", "Content privacy settings"],
                "solutions": ["Choose an appropriate export format (e.g., PDF for documents).", "Review privacy settings before sharing."]
            }
        }

    def handle_error(self, error_category: ErrorCategory, severity: ErrorSeverity,
                    error_message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Logs an error, and in a full system, would provide UI guidance and attempt recovery.
        """
        error_record = {
            'category': error_category,
            'severity': severity,
            'message': error_message,
            'timestamp': pygame.time.get_ticks() if pygame.get_init() else 0,
            'context': context or {},
        }
        self.error_history.append(error_record)
        if len(self.error_history) > 100: # Limit history size
            self.error_history.pop(0)

        # For this implementation, we will print to the console.
        # A full implementation would trigger a UI element to display guidance.
        print(f"ERROR: [{severity.value.upper()}] in {category.value}: {error_message}")
        if context:
            print(f"  CONTEXT: {context}")

        return {'error_handled': True}

    def set_user_context(self, experience_level: str, accessibility_mode: bool,
                        professional_context: bool):
        """Sets the user context to allow for more personalized guidance."""
        self.user_guidance_context.user_experience_level = experience_level
        self.user_guidance_context.accessibility_mode = accessibility_mode
        self.user_guidance_context.professional_context = professional_context
