"""
Subreddit Manager for Reddit Bot
Manages the list of subreddits the bot monitors
"""
import os
import json
import logging
import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# File to store subreddit configuration
SUBREDDIT_CONFIG_FILE = 'subreddit_config.json'

def initialize_config():
    """Initialize the subreddit configuration file if it doesn't exist."""
    if not os.path.exists(SUBREDDIT_CONFIG_FILE):
        # Create initial config from the current config.py values
        config_data = {
            'categories': config.SUBREDDIT_CATEGORIES,
            'enabled_categories': list(config.SUBREDDIT_CATEGORIES.keys())
        }
        
        with open(SUBREDDIT_CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        logger.info(f"Created new subreddit configuration file: {SUBREDDIT_CONFIG_FILE}")

def get_config():
    """Get the current subreddit configuration."""
    try:
        with open(SUBREDDIT_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is invalid, initialize it
        initialize_config()
        with open(SUBREDDIT_CONFIG_FILE, 'r') as f:
            return json.load(f)

def save_config(config_data):
    """Save the subreddit configuration."""
    with open(SUBREDDIT_CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=2)
    logger.info("Subreddit configuration saved")

def get_all_subreddits():
    """Get a list of all subreddits from all categories."""
    config_data = get_config()
    all_subreddits = []
    
    for category, subreddits in config_data['categories'].items():
        all_subreddits.extend(subreddits)
    
    return all_subreddits

def get_active_subreddits():
    """Get a list of all active subreddits."""
    config_data = get_config()
    active_subreddits = []
    
    for category, subreddits in config_data['categories'].items():
        if category in config_data['enabled_categories']:
            active_subreddits.extend(subreddits)
    
    return active_subreddits

def get_categories():
    """Get a list of all categories and their subreddits."""
    return get_config()['categories']

def get_enabled_categories():
    """Get a list of enabled categories."""
    return get_config()['enabled_categories']

def add_subreddit(category, subreddit):
    """Add a subreddit to a category."""
    config_data = get_config()
    
    # Check if category exists
    if category not in config_data['categories']:
        logger.error(f"Category '{category}' does not exist")
        return False
    
    # Check if subreddit already exists in this category
    if subreddit in config_data['categories'][category]:
        logger.warning(f"Subreddit '{subreddit}' already exists in category '{category}'")
        return False
    
    # Add subreddit
    config_data['categories'][category].append(subreddit)
    save_config(config_data)
    logger.info(f"Added subreddit '{subreddit}' to category '{category}'")
    return True

def remove_subreddit(category, subreddit):
    """Remove a subreddit from a category."""
    config_data = get_config()
    
    # Check if category exists
    if category not in config_data['categories']:
        logger.error(f"Category '{category}' does not exist")
        return False
    
    # Check if subreddit exists in this category
    if subreddit not in config_data['categories'][category]:
        logger.warning(f"Subreddit '{subreddit}' does not exist in category '{category}'")
        return False
    
    # Remove subreddit
    config_data['categories'][category].remove(subreddit)
    save_config(config_data)
    logger.info(f"Removed subreddit '{subreddit}' from category '{category}'")
    return True

def enable_category(category):
    """Enable a category."""
    config_data = get_config()
    
    # Check if category exists
    if category not in config_data['categories']:
        logger.error(f"Category '{category}' does not exist")
        return False
    
    # Check if category is already enabled
    if category in config_data['enabled_categories']:
        logger.warning(f"Category '{category}' is already enabled")
        return False
    
    # Enable category
    config_data['enabled_categories'].append(category)
    save_config(config_data)
    logger.info(f"Enabled category '{category}'")
    return True

def disable_category(category):
    """Disable a category."""
    config_data = get_config()
    
    # Check if category exists
    if category not in config_data['categories']:
        logger.error(f"Category '{category}' does not exist")
        return False
    
    # Check if category is already disabled
    if category not in config_data['enabled_categories']:
        logger.warning(f"Category '{category}' is already disabled")
        return False
    
    # Disable category
    config_data['enabled_categories'].remove(category)
    save_config(config_data)
    logger.info(f"Disabled category '{category}'")
    return True

def add_category(category_name):
    """Add a new category."""
    config_data = get_config()
    
    # Check if category already exists
    if category_name in config_data['categories']:
        logger.warning(f"Category '{category_name}' already exists")
        return False
    
    # Add category
    config_data['categories'][category_name] = []
    save_config(config_data)
    logger.info(f"Added category '{category_name}'")
    return True

def remove_category(category_name):
    """Remove a category."""
    config_data = get_config()
    
    # Check if category exists
    if category_name not in config_data['categories']:
        logger.error(f"Category '{category_name}' does not exist")
        return False
    
    # Remove from enabled categories if present
    if category_name in config_data['enabled_categories']:
        config_data['enabled_categories'].remove(category_name)
    
    # Remove category
    del config_data['categories'][category_name]
    save_config(config_data)
    logger.info(f"Removed category '{category_name}'")
    return True

# Initialize configuration file when module is imported
initialize_config()
