from typing import Dict, Tuple
import re

class PasswordPolicy:
    """Enterprise password policy validation"""
    
    @staticmethod
    def validate(password: str) -> Tuple[bool, Dict]:
        """
        Validate password against structural security requirements
        
        Returns:
            Tuple[bool, Dict]: (is_valid, error_details)
        """
        errors = {}

        if len(password) < 8:
            errors['min_length'] = "Password must be at least 8 characters"
        
        if not re.search(r'[A-Z]', password):
            errors['uppercase'] = "Must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            errors['lowercase'] = "Must contain at least one lowercase letter"
        
        if not re.search(r'[0-9]', password):
            errors['number'] = "Must contain at least one number"
        
        return len(errors) == 0, errors
    
    @staticmethod
    def get_requirements() -> Dict:
        """Get password requirements for API documentation"""
        return {
            "min_length": 8,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_numbers": True,
            "description": "HENNGE Security Enterprise Password Policy"
        }