import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime

# check if the date is in the mm/dd/yy format
def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%m/%d/%y')
        return True
    except ValueError:
        return False

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"