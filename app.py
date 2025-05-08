import os
import json
import time
import threading
from flask import Flask, render_template, request, redirect, url_for, jsonify
import logging
from datetime import datetime

# Import bot modules
import reddit_bot
import message_templates
import subreddit_manager
import post_history

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("web_interface.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Custom Jinja2 filters
@app.template_filter('timestamp_to_date')
def timestamp_to_date(timestamp):
    """Convert a Unix timestamp to a formatted date string."""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

@app.template_filter('timestamp_to_time')
def timestamp_to_time(timestamp):
    """Convert a Unix timestamp to a formatted time string."""
    return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

# Global variables
bot_thread = None
bot_running = False
bot_status = "Stopped"
bot_last_action = "N/A"
bot_start_time = None

def run_bot_thread():
    global bot_running, bot_status, bot_last_action
    
    bot_status = "Running"
    bot_last_action = "Starting bot..."
    
    try:
        reddit_bot.run_bot(status_callback=update_bot_status)
    except Exception as e:
        bot_status = f"Error: {str(e)}"
        logger.error(f"Bot error: {str(e)}")
    
    bot_running = False
    bot_status = "Stopped"
    bot_last_action = "Bot stopped"

def update_bot_status(action):
    global bot_last_action
    bot_last_action = action
    logger.info(action)

@app.route('/')
def home():
    # Get bot runtime if running
    runtime = None
    if bot_start_time:
        runtime = int(time.time() - bot_start_time)
        hours, remainder = divmod(runtime, 3600)
        minutes, seconds = divmod(remainder, 60)
        runtime = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    # Get statistics
    stats = {
        "total_posts": len(post_history.get_all_posts()),
        "subreddits": len(subreddit_manager.get_all_subreddits()),
        "templates": len(message_templates.get_all_templates()),
        "active_subreddits": len(subreddit_manager.get_active_subreddits())
    }
    
    # Get recent posts
    recent_posts = post_history.get_all_posts()[-5:] if post_history.get_all_posts() else []
    
    return render_template('index.html', 
                          bot_status=bot_status,
                          bot_running=bot_running,
                          bot_last_action=bot_last_action,
                          runtime=runtime,
                          stats=stats,
                          recent_posts=recent_posts)

@app.route('/start_bot', methods=['POST'])
def start_bot():
    global bot_thread, bot_running, bot_start_time
    
    if not bot_running:
        bot_running = True
        bot_start_time = time.time()
        bot_thread = threading.Thread(target=run_bot_thread)
        bot_thread.daemon = True
        bot_thread.start()
        
    return redirect(url_for('home'))

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    global bot_running, bot_start_time
    
    if bot_running:
        bot_running = False
        bot_start_time = None
        
    return redirect(url_for('home'))

@app.route('/templates')
def templates():
    all_templates = message_templates.get_all_templates()
    return render_template('templates.html', templates=all_templates)

@app.route('/template/<template_name>')
def view_template(template_name):
    template = message_templates.get_template(template_name)
    if not template:
        return redirect(url_for('templates'))
    
    return render_template('template_detail.html', template=template)

@app.route('/edit_template/<template_name>', methods=['GET', 'POST'])
def edit_template(template_name):
    template = message_templates.get_template(template_name)
    
    if request.method == 'POST':
        # Update template
        new_keywords = request.form.get('keywords').split(',')
        new_keywords = [k.strip() for k in new_keywords if k.strip()]
        
        new_message = request.form.get('message')
        
        # Update the template (you'll need to implement this in message_templates.py)
        message_templates.update_template(template_name, new_keywords, new_message)
        
        return redirect(url_for('view_template', template_name=template_name))
    
    return render_template('edit_template.html', template=template)

@app.route('/add_template', methods=['GET', 'POST'])
def add_template():
    if request.method == 'POST':
        template_name = request.form.get('name')
        keywords = request.form.get('keywords').split(',')
        keywords = [k.strip() for k in keywords if k.strip()]
        message = request.form.get('message')
        
        # Add the template (you'll need to implement this in message_templates.py)
        message_templates.add_template(template_name, keywords, message)
        
        return redirect(url_for('templates'))
    
    return render_template('add_template.html')

@app.route('/subreddits')
def subreddits():
    categories = subreddit_manager.get_subreddit_categories()
    return render_template('subreddits.html', categories=categories)

@app.route('/add_subreddit', methods=['GET', 'POST'])
def add_subreddit():
    categories = subreddit_manager.get_subreddit_categories()
    
    if request.method == 'POST':
        subreddit_name = request.form.get('name')
        category = request.form.get('category')
        
        # Add the subreddit
        subreddit_manager.add_subreddit(category, subreddit_name)
        
        return redirect(url_for('subreddits'))
    
    return render_template('add_subreddit.html', categories=categories)

@app.route('/toggle_subreddit/<subreddit_name>', methods=['POST'])
def toggle_subreddit(subreddit_name):
    # Toggle the subreddit's enabled status
    subreddit_manager.toggle_subreddit(subreddit_name)
    
    return redirect(url_for('subreddits'))

@app.route('/history')
def history():
    posts = post_history.get_all_posts()
    
    # Group by date
    posts_by_date = {}
    for post in posts:
        date = datetime.fromtimestamp(post['timestamp']).strftime('%Y-%m-%d')
        if date not in posts_by_date:
            posts_by_date[date] = []
        posts_by_date[date].append(post)
    
    return render_template('history.html', posts_by_date=posts_by_date)

@app.route('/api/status')
def api_status():
    # Get bot runtime if running
    runtime = None
    if bot_start_time:
        runtime = int(time.time() - bot_start_time)
    
    return jsonify({
        'status': bot_status,
        'running': bot_running,
        'last_action': bot_last_action,
        'runtime': runtime,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True, port=5000)
