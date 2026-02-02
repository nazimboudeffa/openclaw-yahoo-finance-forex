"""
Skills registry for OpenClaw bot.
"""

from typing import Dict, Any


def get_available_skills() -> Dict[str, Any]:
    """
    Get all available skills for OpenClaw.
    
    Returns:
        Dictionary of skill name to skill instance
    """
    skills = {}
    FOREX_SKILL_AVAILABLE = False
    
    # Try to import and register Yahoo Finance FOREX skill
    try:
        from skills.yahoo_finance_forex_majors import register_skill
        FOREX_SKILL_AVAILABLE = True
        
        # Register the skill
        forex_skill = register_skill()
        skills[forex_skill.name] = forex_skill
        print(f"✅ Loaded skill: {forex_skill.name}")
        
    except ImportError as e:
        print(f"⚠️ Yahoo Finance FOREX skill not available: {e}")
        FOREX_SKILL_AVAILABLE = False
    except Exception as e:
        print(f"❌ Error loading Yahoo Finance FOREX skill: {e}")
        FOREX_SKILL_AVAILABLE = False
    
    if not skills:
        print("⚠️ No skills available")
        return {}
    
    return skills


def get_skill(skill_name: str):
    """
    Get a specific skill by name.
    
    Args:
        skill_name: Name of the skill to retrieve
        
    Returns:
        Skill instance or None if not found
    """
    skills = get_available_skills()
    return skills.get(skill_name)
