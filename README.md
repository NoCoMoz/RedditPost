# Activism Resource Bot

[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/your-username/activism-resource-bot/blob/main/LICENSE)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A sophisticated Reddit bot built with PRAW (Python Reddit API Wrapper) that monitors activism and social justice subreddits for posts containing specific keywords and automatically responds with relevant resources based on the post content.

## Features

### Core Functionality

- Monitor multiple subreddits simultaneously across different categories
- Intelligent keyword detection to find relevant posts
- Multiple specialized message templates for different topics
- Smart template selection based on post content
- Automatic response with targeted resources
- Rate limit handling and duplicate prevention

### Management Interface

- User-friendly command-line interface for bot management
- View and edit message templates
- Add, remove, and organize subreddits by category
- Enable/disable entire categories of subreddits
- Track and view post history with filtering options
- Test bot functionality without posting to Reddit

### Analytics and Tracking

- Comprehensive post history tracking
- Statistics on bot activity by subreddit and template
- Filter post history by subreddit or template type
- Direct links to all bot responses on Reddit

## Setup Instructions

### 1. Reddit API Credentials

Before running the bot, you need to create a Reddit application to get API credentials:

1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Scroll down and click "create another app..."
3. Fill in the details:
   - Name: MyRedditBot (or any name you prefer)
   - Select "script"
   - Description: A bot that helps users
   - About URL: (can be left blank)
   - Redirect URI: [http://localhost:8080](http://localhost:8080)
4. Click "create app"
5. Note down the following information:
   - Client ID: The string under "personal use script"
   - Client Secret: The string labeled "secret"

### 2. Update Configuration

Edit the `config.py` file and replace the placeholder values with your actual Reddit API credentials:

```python
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
USER_AGENT = 'python:activism-resource-bot:v1.0 (by /u/your_username)'
USERNAME = 'your_reddit_username'
PASSWORD = 'your_reddit_password'
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install praw
```

### 4. Run the Management Interface

The bot comes with a user-friendly management interface. Run it using:

```bash
python main.py
```

From the management interface, you can:

- View and edit message templates
- Manage subreddits (add, remove, enable, disable)
- View post history and statistics
- Run the bot
- Test the bot's template selection logic

### 5. Customize Templates and Subreddits

The bot comes pre-configured with activism-focused templates and subreddits, but you can customize them:

- **Templates**: Edit the `message_templates.py` file to modify existing templates or add new ones
- **Subreddits**: Use the management interface to add or remove subreddits from different categories

### 6. Run the Bot

You can run the bot directly using:

```bash
python reddit_bot.py
```

Or through the management interface by selecting the "Run Bot" option.

The bot will start monitoring the specified subreddits and respond to posts containing the keywords from your templates.

## Important Notes

- **Rate Limiting**: Reddit has rate limits for API requests and new accounts. If you're using a new account, you might face strict rate limits.
- **Bot Behavior**: Make sure your bot follows [Reddit's API rules](https://www.reddit.com/wiki/api) and [bottiquette](https://www.reddit.com/wiki/bottiquette).
- **Security**: Keep your API credentials secure. Never share your `config.py` file or commit it to public repositories.

## GitHub Pages

This project includes a GitHub Pages site to showcase the bot and provide documentation. The site is automatically deployed from the `docs` folder in the main branch.

### Viewing the Site

Once you've pushed this repository to GitHub, you can enable GitHub Pages in your repository settings:

1. Go to your repository on GitHub
2. Click on "Settings"
3. Scroll down to the "GitHub Pages" section
4. Select "main branch /docs folder" as the source
5. Click "Save"

Your site will be available at `https://your-username.github.io/activism-resource-bot/`

### Customizing the Site

The GitHub Pages site is built using HTML, CSS, and JavaScript. You can customize it by editing the files in the `docs` folder:

- `index.html`: The main page of the site
- `css/styles.css`: The stylesheet for the site
- `js/main.js`: JavaScript functionality for the site

## Customization Ideas

- Add more complex keyword matching using regular expressions
- Implement sentiment analysis to detect the tone of posts
- Add functionality to respond to comments as well as posts
- Create a database to track posts and responses
- Add time-based restrictions (e.g., only run during certain hours)

## Troubleshooting

If you encounter issues:

1. Check your API credentials in `config.py`
2. Ensure your Reddit account has enough karma to post frequently
3. Review the log file (`bot_log.log`) for error messages
4. Make sure your account has verified email if required by the subreddits
