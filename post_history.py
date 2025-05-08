"""
Post History Tracker for Reddit Bot
Tracks where the bot has posted and stores the history in a JSON file
"""
import os
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# File to store post history
HISTORY_FILE = 'post_history.json'

def initialize_history():
    """Initialize the post history file if it doesn't exist."""
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f)
        logger.info(f"Created new post history file: {HISTORY_FILE}")

def add_post(post_id, subreddit, title, template_name, timestamp=None):
    """Add a post to the history."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    # Load existing history
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    # Add new post
    post_data = {
        'post_id': post_id,
        'subreddit': subreddit,
        'title': title,
        'template_used': template_name,
        'timestamp': timestamp,
        'url': f"https://www.reddit.com/comments/{post_id}"
    }
    
    history.append(post_data)
    
    # Save updated history
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)
    
    logger.info(f"Added post to history: {post_id} in r/{subreddit}")
    return post_data

def get_history(limit=None, subreddit=None, template=None):
    """Get post history, optionally filtered by subreddit or template."""
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    # Apply filters
    if subreddit:
        history = [post for post in history if post['subreddit'].lower() == subreddit.lower()]
    
    if template:
        history = [post for post in history if post['template_used'].lower() == template.lower()]
    
    # Sort by timestamp (newest first)
    history.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Apply limit
    if limit and limit > 0:
        history = history[:limit]
    
    return history

def get_stats():
    """Get statistics about bot activity."""
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    if not history:
        return {
            'total_posts': 0,
            'subreddits': {},
            'templates': {}
        }
    
    # Count posts by subreddit
    subreddits = {}
    for post in history:
        subreddit = post['subreddit']
        if subreddit in subreddits:
            subreddits[subreddit] += 1
        else:
            subreddits[subreddit] = 1
    
    # Count posts by template
    templates = {}
    for post in history:
        template = post['template_used']
        if template in templates:
            templates[template] += 1
        else:
            templates[template] = 1
    
    # Get first and last post timestamps
    timestamps = [datetime.fromisoformat(post['timestamp']) for post in history]
    first_post = min(timestamps).isoformat()
    last_post = max(timestamps).isoformat()
    
    return {
        'total_posts': len(history),
        'subreddits': subreddits,
        'templates': templates,
        'first_post': first_post,
        'last_post': last_post
    }

def clear_history():
    """Clear the post history."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump([], f)
    logger.info("Post history cleared")

# Initialize history file when module is imported
initialize_history()
