#!/usr/bin/env python3
"""
Reddit Bot using PRAW
This bot monitors specified subreddits for posts containing certain keywords
and automatically responds with helpful information based on the post content.
"""
import praw
import time
import logging
from datetime import datetime
import config
import message_templates
import post_history
import subreddit_manager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_log.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_reddit_instance():
    """Create and return a Reddit instance using credentials from config."""
    try:
        reddit = praw.Reddit(
            client_id=config.CLIENT_ID,
            client_secret=config.CLIENT_SECRET,
            user_agent=config.USER_AGENT,
            username=config.USERNAME,
            password=config.PASSWORD
        )
        logger.info(f"Logged in as {reddit.user.me()}")
        return reddit
    except Exception as e:
        logger.error(f"Failed to create Reddit instance: {e}")
        return None

def contains_keywords(text, keywords):
    """Check if any of the keywords are in the text."""
    text = text.lower()
    return any(keyword.lower() in text for keyword in keywords)

def get_best_template(text):
    """Find the best message template for the given text based on keyword matches."""
    return message_templates.get_template_for_text(text)

def already_replied(post, reddit_user):
    """Check if the bot has already replied to this post."""
    post.comments.replace_more(limit=0)
    for comment in post.comments.list():
        if comment.author and comment.author.name == reddit_user:
            logger.info(f"Already replied to post {post.id}")
            return True
    return False

def monitor_subreddits(reddit):
    """Monitor subreddits for new posts containing keywords and reply with the appropriate template."""
    try:
        # Get subreddits from the subreddit manager
        subreddits = subreddit_manager.get_all_subreddits()
        
        if not subreddits:
            logger.error("No subreddits configured or enabled. Please add subreddits in the manager.")
            return
        
        # Create a multi-subreddit instance
        multi_subreddit = reddit.subreddit('+'.join(subreddits))
        
        # Get the bot's username
        bot_username = reddit.user.me().name
        
        # Track posts we've seen to avoid duplicates
        processed_posts = set()
        
        # Get all keywords from all templates
        all_keywords = message_templates.get_all_keywords()
        
        logger.info(f"Starting to monitor {len(subreddits)} subreddits: {', '.join(subreddits)}")
        logger.info(f"Loaded {len(message_templates.TEMPLATES)} different message templates")
        
        # Monitor new submissions
        for post in multi_subreddit.stream.submissions(skip_existing=True):
            # Skip if we've already processed this post
            if post.id in processed_posts:
                continue
            
            processed_posts.add(post.id)
            
            # Combine title and selftext for keyword matching
            post_text = post.title + ' ' + post.selftext
            
            # Check if post contains any keywords from any template
            if contains_keywords(post_text, all_keywords):
                logger.info(f"Found post with keywords in r/{post.subreddit.display_name}: {post.title}")
                
                # Get the best template for this post
                template = get_best_template(post_text)
                template_name = "unknown"
                
                # Determine which template was matched
                for name, info in message_templates.TEMPLATES.items():
                    if template == info['template']:
                        template_name = name
                        break
                
                if not template:
                    logger.warning(f"No suitable template found for post {post.id} despite keyword match")
                    continue
                
                # Check if we've already replied
                if not already_replied(post, bot_username):
                    try:
                        # Reply to the post with the selected template
                        reply = post.reply(template)
                        
                        # Log the reply in post history
                        post_history.add_post(
                            post_id=post.id,
                            subreddit=post.subreddit.display_name,
                            title=post.title,
                            template_name=template_name
                        )
                        
                        logger.info(f"Replied to post: {post.id} - {post.title} with {template_name} template")
                        
                        # Wait to avoid rate limiting
                        time.sleep(10)
                    except Exception as e:
                        logger.error(f"Error replying to post {post.id}: {e}")
                        
                        # If we're being rate limited, wait longer
                        if "RATELIMIT" in str(e):
                            logger.warning("Rate limited. Waiting 10 minutes...")
                            time.sleep(600)
    
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error in monitor_subreddits: {e}")

def main():
    """Main function to run the bot."""
    logger.info("Starting Reddit Bot")
    
    # Create Reddit instance
    reddit = create_reddit_instance()
    if not reddit:
        logger.error("Failed to initialize Reddit instance. Exiting.")
        return
    
    # Monitor subreddits and reply to posts with appropriate templates
    monitor_subreddits(reddit=reddit)

if __name__ == "__main__":
    main()
