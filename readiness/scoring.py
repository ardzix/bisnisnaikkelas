from decimal import Decimal
from typing import Dict, List, Tuple
from datetime import date
from .constants import EXPECTED_CHECKS, SUGGESTIONS


def determine_business_level(assessment) -> str:
    """
    Determine the business level based on revenue and employee count.

    Business levels:
    - Micro: revenue <= 300M IDR or <= 4 employees
    - Small: revenue <= 2.5B IDR or <= 19 employees
    - Medium: revenue <= 50B IDR or <= 99 employees
    - Large: revenue > 50B IDR or > 99 employees

    Args:
        assessment: An object containing fields like annual_revenue and employee_count

    Returns:
        str: One of 'micro', 'small', 'medium', or 'large'
    """
    if assessment.annual_revenue <= Decimal('300000000') or assessment.employee_count <= 4:
        return 'micro'
    elif assessment.annual_revenue <= Decimal('2500000000') or assessment.employee_count <= 19:
        return 'small'
    elif assessment.annual_revenue <= Decimal('50000000000') or assessment.employee_count <= 99:
        return 'medium'
    else:
        return 'large'


def calculate_assessment(assessment) -> Tuple[Dict[str, int], str, Dict[str, List[str]]]:
    """
    Calculate readiness scores, business level, and tailored recommendations
    based on the assessment inputs and business classification.

    Args:
        assessment: An object with business attributes (e.g., has_website, has_npwp)

    Returns:
        Tuple:
            - scores: dict of readiness scores per category and total (0–100)
            - level: str business classification ('micro', 'small', etc.)
            - recommendations: dict of improvement tips grouped by category
    """
    level = determine_business_level(assessment)
    expected = EXPECTED_CHECKS.get(level, {})

    scores: Dict[str, int] = {}
    for category, fields in expected.items():
        scores[category] = calculate_weighted_score(assessment, fields)

    scores['total'] = sum(scores.values()) // len(expected)

    recommendations = generate_recommendations(assessment, level)

    return scores, level, recommendations


def calculate_weighted_score(assessment, fields: Dict[str, int]) -> int:
    """
    Compute weighted readiness score for a given category using the relevant fields.

    If a field is fulfilled (True or meets a threshold), the corresponding weight is counted.

    Args:
        assessment: Object with business assessment attributes
        fields: dict mapping field names to weights (out of 100)

    Returns:
        int: Readiness score (0–100) for that category
    """
    if not fields:
        return 100

    score = 0
    current_year = date.today().year

    for field, weight in fields.items():
        if field == 'year_started':
            if current_year - assessment.year_started > 3:
                score += weight
        elif field == 'employee_count':
            if assessment.employee_count > 5:
                score += weight
        elif field == 'annual_revenue':
            if assessment.annual_revenue > Decimal('1000000000'):
                score += weight
        elif getattr(assessment, field, False):
            score += weight

    return round(score)


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
