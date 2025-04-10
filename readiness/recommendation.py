# Refactored recommendation generator to be aware of business level

from typing import Dict, List
from .constants import EXPECTED_CHECKS, SUGGESTIONS
from datetime import date
from decimal import Decimal

def generate_recommendations(assessment, level: str) -> Dict[str, List[str]]:
    """
    Generate category-specific recommendations based on missing or insufficient fields.

    Recommendations are filtered according to business level and conditionally checked
    for fields like year_started, employee_count, and annual_revenue.

    Args:
        assessment: Object with all relevant business properties
        level: str business classification ('micro', 'small', etc.)

    Returns:
        dict: category → list of improvement suggestions (in Bahasa Indonesia)
    """
    EXPECTED_FIELDS = EXPECTED_CHECKS[level]
    current_year = date.today().year
    suggestions = SUGGESTIONS

    recs: Dict[str, List[str]] = {}

    for category, fields in EXPECTED_FIELDS.items():
        recs[category] = []
        for field in fields:
            if field == 'year_started':
                if current_year - assessment.year_started <= 3:
                    recs[category].append(suggestions[field])
            elif field == 'employee_count':
                if assessment.employee_count <= 5:
                    recs[category].append(suggestions[field])
            elif field == 'annual_revenue':
                if assessment.annual_revenue <= Decimal('1000000000'):
                    recs[category].append(suggestions[field])
            else:
                if not getattr(assessment, field, False):
                    suggestion = suggestions.get(field)
                    if suggestion:
                        recs[category].append(suggestion)

    return recs 