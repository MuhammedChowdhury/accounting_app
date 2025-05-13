<<<<<<< HEAD
import logging
from sqlalchemy import func
from app.models import AssetLiability
from app import db

def get_total_data(category, company_id):
    """
    Get the total sum for a specific category (asset/liability).
    Handles errors gracefully and validates inputs.
    """
    try:
        if not category or not isinstance(company_id, int):
            raise ValueError("Invalid category or company_id.")

        total = db.session.query(func.sum(AssetLiability.amount)).filter_by(
            company_id=company_id, category=category
        ).scalar() or 0.0
        
        return total
    except Exception as e:
        logging.error(f"Error fetching total data for category '{category}': {e}", exc_info=True)
        return 0.0  # Return a fallback value to avoid breaking execution

def get_grouped_data(category, company_id, **filters):
    """
    Group assets or liabilities by subcategory and return totals.
    Supports additional filtering options via keyword arguments.
    """
    try:
        if not category or not isinstance(company_id, int):
            raise ValueError("Invalid category or company_id.")

        query = db.session.query(
            AssetLiability.subcategory,
            func.sum(AssetLiability.amount).label('total')
        ).filter_by(company_id=company_id, category=category)
        
        # Apply additional filters
        for key, value in filters.items():
            query = query.filter(getattr(AssetLiability, key) == value)

        grouped = query.group_by(AssetLiability.subcategory).all()
        return [{'subcategory': item.subcategory, 'total': item.total} for item in grouped]
    except Exception as e:
        logging.error(f"Error grouping data for category '{category}': {e}", exc_info=True)
        return []  # Return an empty list in case of failure
=======
import logging
from sqlalchemy import func
from app.models import AssetLiability
from app import db

def get_total_data(category, company_id):
    """
    Get the total sum for a specific category (asset/liability).
    Handles errors gracefully and validates inputs.
    """
    try:
        if not category or not isinstance(company_id, int):
            raise ValueError("Invalid category or company_id.")

        total = db.session.query(func.sum(AssetLiability.amount)).filter_by(
            company_id=company_id, category=category
        ).scalar() or 0.0
        
        return total
    except Exception as e:
        logging.error(f"Error fetching total data for category '{category}': {e}", exc_info=True)
        return 0.0  # Return a fallback value to avoid breaking execution

def get_grouped_data(category, company_id, **filters):
    """
    Group assets or liabilities by subcategory and return totals.
    Supports additional filtering options via keyword arguments.
    """
    try:
        if not category or not isinstance(company_id, int):
            raise ValueError("Invalid category or company_id.")

        query = db.session.query(
            AssetLiability.subcategory,
            func.sum(AssetLiability.amount).label('total')
        ).filter_by(company_id=company_id, category=category)
        
        # Apply additional filters
        for key, value in filters.items():
            query = query.filter(getattr(AssetLiability, key) == value)

        grouped = query.group_by(AssetLiability.subcategory).all()
        return [{'subcategory': item.subcategory, 'total': item.total} for item in grouped]
    except Exception as e:
        logging.error(f"Error grouping data for category '{category}': {e}", exc_info=True)
        return []  # Return an empty list in case of failure
>>>>>>> dc8cfbe92444c4d49f3be126b10a798f1295dd81
