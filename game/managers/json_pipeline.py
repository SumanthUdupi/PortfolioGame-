from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import json
import jsonschema
from pathlib import Path

# Data Classes to represent the structured portfolio data
@dataclass
class SkillCategory:
    """Represents a category of professional skills."""
    name: str
    skills: List[str]
    game_stat_mapping: Dict[str, int]

@dataclass
class ProfessionalExperience:
    """Represents professional work experience."""
    role: str
    company: str
    achievements: List[str]
    level_requirement: int

class JSONPipeline:
    """Handles loading, validating, and processing of the portfolio JSON data."""

    def __init__(self, schema_path: str = "schemas/portfolio_schema.json"):
        """Initializes the pipeline by loading the validation schema."""
        self.schema = self._load_schema(schema_path)
        self.cache = {}
        if self.schema:
            self.validator = jsonschema.Draft7Validator(self.schema)
        else:
            self.validator = None

        # Defines the mapping from professional skills to in-game character stats.
        self.STAT_MAPPINGS = {
            "python": {"intelligence": 10, "programming": 15},
            "javascript": {"intelligence": 8, "programming": 12},
            "java": {"intelligence": 9, "programming": 13},
            "sql": {"intelligence": 12, "analysis": 15},
            "excel": {"intelligence": 8, "analysis": 10},
            "power bi": {"intelligence": 10, "analysis": 12},
            "tableau": {"intelligence": 11, "analysis": 13},
            "rest api integration": {"technical": 12, "integration": 15},
            "postman": {"technical": 10, "integration": 12},
            "swagger/openapi": {"technical": 11, "integration": 13},
            "project management": {"leadership": 12, "management": 15},
            "team leadership": {"leadership": 14, "charisma": 10},
            "agile": {"leadership": 10, "management": 10},
            "gherkin": {"analysis": 10, "communication": 5},
        }

    def _load_schema(self, schema_path: str) -> Optional[Dict[str, Any]]:
        """Loads the JSON schema from the specified path."""
        try:
            schema_file = Path(schema_path)
            if not schema_file.is_file():
                print(f"Warning: Schema file not found at {schema_path}")
                return None
            with open(schema_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading schema {schema_path}: {e}")
            return None

    def load_portfolio_data(self, json_path: str) -> Optional[Dict[str, Any]]:
        """
        Loads, validates, and transforms the portfolio JSON data from the given path.
        """
        try:
            portfolio_file = Path(json_path)
            if not portfolio_file.is_file():
                raise FileNotFoundError(f"Portfolio file not found: {json_path}")

            with open(portfolio_file, 'r', encoding='utf-8') as file:
                raw_data = json.load(file)

            if self.validator:
                errors = list(self.validator.iter_errors(raw_data))
                if errors:
                    error_messages = [f"Validation error at {'/'.join(map(str, e.path))}: {e.message}" for e in errors]
                    raise jsonschema.ValidationError("\n".join(error_messages))

            processed_data = self._transform_portfolio_data(raw_data)
            self.cache[json_path] = processed_data
            return processed_data

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {json_path}: {e.msg} at line {e.lineno}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error loading portfolio data: {str(e)}")

    def _transform_portfolio_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transforms the raw JSON data into a game-ready structured format."""
        return {
            "player_profile": self._create_player_profile(raw_data),
            "skill_categories": self._process_skill_categories(raw_data.get("skills", {})),
            "experience_entries": self._process_experience(raw_data.get("professional_experience", [])),
            "game_stats": self._calculate_game_stats(raw_data),
            "achievement_definitions": self._generate_achievements(raw_data)
        }

    def _create_player_profile(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates the player's main profile from the contact info and calculated level."""
        level = self._calculate_character_level(data)
        return {
            "name": data.get("contact_info", {}).get("name", "Professional Hero"),
            "title": data.get("contact_info", {}).get("title", "Analyst"),
            "current_level": level,
            "experience_points": self._calculate_total_experience(data),
            "available_skill_points": (level - 1) * 3, # 3 points per level above 1
            "avatar_sprite": self._determine_avatar_sprite(data)
        }

    def _process_skill_categories(self, skills_data: Dict[str, List[str]]) -> List[SkillCategory]:
        """Converts skill data into structured SkillCategory objects with stat mappings."""
        categories = []
        for category_name, skills in skills_data.items():
            category_stats = {}
            for skill in skills:
                # Find matching stat mappings for each skill
                for map_key, stats in self.STAT_MAPPINGS.items():
                    if map_key in skill.lower():
                        for stat, value in stats.items():
                            category_stats[stat] = category_stats.get(stat, 0) + value
            
            category = SkillCategory(
                name=category_name.replace("_", " ").title(),
                skills=skills,
                game_stat_mapping=category_stats
            )
            categories.append(category)
        return categories

    def _calculate_character_level(self, data: Dict[str, Any]) -> int:
        """Calculates the character's level based on total experience points."""
        experience_points = self._calculate_total_experience(data)
        level = 1
        xp_for_next_level = 100
        while experience_points >= xp_for_next_level:
            level += 1
            experience_points -= xp_for_next_level
            xp_for_next_level = int(xp_for_next_level * 1.5) # Exponential growth
        return min(level, 100)  # Level cap

    def _calculate_total_experience(self, data: Dict[str, Any]) -> int:
        """Calculates total experience points from experience, skills, and certifications."""
        total_xp = 0
        for exp in data.get("professional_experience", []):
            total_xp += 500  # Base XP per role
            total_xp += len(exp.get("key_achievements", [])) * 150
        
        for category, skill_list in data.get("skills", {}).items():
            total_xp += len(skill_list) * 25
            
        total_xp += len(data.get("certifications", [])) * 300
        return total_xp

    def _determine_avatar_sprite(self, data: Dict[str, Any]) -> str:
        """Determines the player's avatar based on their primary skills."""
        skills_str = str(data.get("skills", {})).lower()
        if "business_analysis" in skills_str:
            return "sprites/player/analyst.png"
        if any(s in skills_str for s in ["api", "python", "sql"]):
            return "sprites/player/developer.png"
        if "management" in skills_str:
            return "sprites/player/manager.png"
        return "sprites/player/professional.png"

    def _process_experience(self, experience_data: List[Dict[str, Any]]) -> List[ProfessionalExperience]:
        """Converts professional experience entries into structured game data."""
        processed = []
        for exp in experience_data:
            role = exp.get("role", "").lower()
            level_req = 10  # Default mid-level
            if any(s in role for s in ["lead", "senior", "manager"]): level_req = 15
            elif any(s in role for s in ["junior", "associate", "intern"]): level_req = 5
            
            processed.append(ProfessionalExperience(
                role=exp.get("role", "Unknown Role"),
                company=exp.get("company", "Unknown Company"),
                achievements=exp.get("key_achievements", []),
                level_requirement=level_req
            ))
        return processed

    def _calculate_game_stats(self, data: Dict[str, Any]) -> Dict[str, int]:
        """Calculates the player's base game stats from their skills."""
        base_stats = {
            "intelligence": 10, "programming": 5, "analysis": 5, "technical": 5,
            "integration": 5, "leadership": 5, "management": 5, "charisma": 8
        }
        for category, skill_list in data.get("skills", {}).items():
            for skill in skill_list:
                # Find matching stat mappings for each skill
                for map_key, stats in self.STAT_MAPPINGS.items():
                    if map_key in skill.lower():
                        for stat, bonus in stats.items():
                            base_stats[stat] = base_stats.get(stat, 0) + bonus
        return base_stats

    def _generate_achievements(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates in-game achievements based on real-world accomplishments."""
        achievements = []
        for exp in data.get("professional_experience", []):
            for achievement_text in exp.get("key_achievements", []):
                if "200+" in achievement_text and "gherkin" in achievement_text.lower():
                    achievements.append({
                        "name": "Story Master",
                        "description": "Authored 200+ Gherkin user stories.",
                        "icon": "achievements/story_master.png",
                    })
                if "7-member" in achievement_text and "squad" in achievement_text.lower():
                    achievements.append({
                        "name": "Squad Leader",
                        "description": "Led a 7-member cross-functional squad.",
                        "icon": "achievements/squad_leader.png",
                    })
        return achievements
