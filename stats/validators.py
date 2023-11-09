from datetime import datetime
from django.core.exceptions import ValidationError


def validate_mmdd_date_format(value):
    current_year = datetime.now().year
    try:
        date_obj = datetime.strptime(value, '%m/%d').replace(year=current_year) 
    except ValueError:
        raise ValidationError("Enter a valid date in the 'mm/dd' format.")
