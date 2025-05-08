#!/usr/bin/env python3
"""
Reddit Bot Manager
A simple interface to manage your multi-template Reddit bot
"""
import os
import sys
import time
import json
import logging
import importlib
import message_templates
import subreddit_manager
import post_history
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the bot manager header."""
    print("\n" + "="*70)
    print("                  ACTIVISM RESOURCE BOT MANAGER")
    print("="*70)
    print(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*70 + "\n")

def list_templates():
    """Display all available message templates."""
    print_header()
    print(f"AVAILABLE MESSAGE TEMPLATES ({len(message_templates.TEMPLATES)})\n")
    
    for i, (name, info) in enumerate(message_templates.TEMPLATES.items(), 1):
        print(f"{i}. {name.upper()} - {info['description']}")
        print(f"   Keywords: {', '.join(info['keywords'][:3])}{'...' if len(info['keywords']) > 3 else ''}")
        print(f"   Response: {info['template'].strip().split(chr(10))[0][:60]}...")
        print()
    
    input("\nPress Enter to return to the main menu...")

def view_template():
    """View a specific template in detail."""
    while True:
        print_header()
        print("VIEW TEMPLATE\n")
        
        # List templates with numbers
        templates = list(message_templates.TEMPLATES.items())
        for i, (name, info) in enumerate(templates, 1):
            print(f"{i}. {name} - {info['description']}")
        
        print("\n0. Back to main menu")
        
        # Get user choice
        try:
            choice = int(input("\nEnter template number to view: "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(templates):
                name, info = templates[choice-1]
                
                print_header()
                print(f"TEMPLATE: {name.upper()}\n")
                print(f"Description: {info['description']}")
                print("\nKEYWORDS:")
                
                # Print keywords in columns
                keywords = info['keywords']
                for i in range(0, len(keywords), 3):
                    row = keywords[i:i+3]
                    print("  " + "  |  ".join(row))
                
                print("\nRESPONSE TEMPLATE:")
                print("-" * 70)
                print(info['template'])
                print("-" * 70)
                
                input("\nPress Enter to continue...")
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1)
        
        except ValueError:
            print("\nPlease enter a number.")
            time.sleep(1)

def edit_template():
    """Edit an existing template."""
    while True:
        print_header()
        print("EDIT TEMPLATE\n")
        
        # List templates with numbers
        templates = list(message_templates.TEMPLATES.items())
        for i, (name, info) in enumerate(templates, 1):
            print(f"{i}. {name} - {info['description']}")
        
        print("\n0. Back to main menu")
        
        # Get user choice
        try:
            choice = int(input("\nEnter template number to edit: "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(templates):
                name, info = templates[choice-1]
                
                print_header()
                print(f"EDITING TEMPLATE: {name.upper()}\n")
                
                # Edit template properties
                print("1. Edit description")
                print("2. Edit keywords")
                print("3. Edit response template")
                print("0. Back to template selection")
                
                sub_choice = int(input("\nWhat would you like to edit? "))
                
                if sub_choice == 0:
                    continue
                elif sub_choice == 1:
                    # Edit description
                    current = info['description']
                    print(f"\nCurrent description: {current}")
                    new = input("Enter new description (or press Enter to keep current): ")
                    if new:
                        # This would modify the template in memory
                        # In a real implementation, this would save to a file
                        print("\nDescription updated! (Note: Changes are not permanent in this demo)")
                elif sub_choice == 2:
                    # Edit keywords
                    print("\nCurrent keywords:")
                    for i, keyword in enumerate(info['keywords'], 1):
                        print(f"{i}. {keyword}")
                    
                    print("\nOptions:")
                    print("1. Add a keyword")
                    print("2. Remove a keyword")
                    print("0. Back")
                    
                    kw_choice = int(input("\nEnter choice: "))
                    if kw_choice == 1:
                        new_keyword = input("Enter new keyword: ")
                        if new_keyword:
                            print(f"\nKeyword '{new_keyword}' would be added. (Note: Changes are not permanent in this demo)")
                    elif kw_choice == 2:
                        kw_index = int(input("Enter keyword number to remove: ")) - 1
                        if 0 <= kw_index < len(info['keywords']):
                            print(f"\nKeyword '{info['keywords'][kw_index]}' would be removed. (Note: Changes are not permanent in this demo)")
                elif sub_choice == 3:
                    # Edit template text
                    print("\nCurrent template:")
                    print("-" * 70)
                    print(info['template'])
                    print("-" * 70)
                    print("\nTo edit the template, you would normally open it in a text editor.")
                    print("In this demo, changes are not saved permanently.")
                
                input("\nPress Enter to continue...")
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1)
        
        except ValueError:
            print("\nPlease enter a number.")
            time.sleep(1)

def create_template():
    """Create a new message template."""
    print_header()
    print("CREATE NEW TEMPLATE\n")
    
    print("In a full implementation, this would allow you to create a new template.")
    print("You would enter:")
    print("1. Template name")
    print("2. Description")
    print("3. Keywords that trigger this template")
    print("4. The response message template")
    
    print("\nTo actually create a new template, edit the message_templates.py file")
    print("and add a new entry to the TEMPLATES dictionary.")
    
    input("\nPress Enter to return to the main menu...")

def run_bot():
    """Run the Reddit bot."""
    print_header()
    print("RUNNING BOT\n")
    
    print("Starting the Reddit bot with multiple message templates...")
    print("The bot will monitor the configured subreddits and respond with")
    print("the appropriate template based on the post content.")
    print("\nPress Ctrl+C in the terminal to stop the bot.")
    
    input("\nPress Enter to start the bot...")
    
    # Import and run the bot
    try:
        import reddit_bot
        reddit_bot.main()
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
        input("\nPress Enter to return to the main menu...")
    except Exception as e:
        print(f"\nError running bot: {e}")
        input("\nPress Enter to return to the main menu...")

def test_bot():
    """Run the bot test script."""
    print_header()
    print("TESTING BOT\n")
    
    print("Running the test script to verify bot functionality...")
    print("This will test Reddit connection and template matching without posting.")
    
    input("\nPress Enter to start the test...")
    
    # Import and run the test script
    try:
        import test_bot
        test_bot.main()
    except Exception as e:
        print(f"\nError running test: {e}")
    
    input("\nPress Enter to return to the main menu...")

def manage_subreddits():
    """Manage the subreddits the bot monitors."""
    while True:
        print_header()
        print("MANAGE SUBREDDITS\n")
        
        # Get current subreddit configuration
        categories = subreddit_manager.get_categories()
        enabled_categories = subreddit_manager.get_enabled_categories()
        
        # Display categories and their status
        print("CATEGORIES:\n")
        for i, (category, subreddits) in enumerate(categories.items(), 1):
            status = "ENABLED" if category in enabled_categories else "DISABLED"
            print(f"{i}. {category} [{status}] - {len(subreddits)} subreddits")
        
        print("\nACTIONS:")
        print("a. View/Edit Category")
        print("b. Add New Category")
        print("c. Enable/Disable Category")
        print("d. Delete Category")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == '0':
            return
        elif choice == 'a':
            # View/Edit Category
            try:
                cat_num = int(input("Enter category number to view/edit: "))
                if 1 <= cat_num <= len(categories):
                    category_name = list(categories.keys())[cat_num-1]
                    edit_category_subreddits(category_name)
                else:
                    print("Invalid category number.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a valid number.")
                time.sleep(1)
        elif choice == 'b':
            # Add New Category
            new_cat = input("Enter new category name: ").strip()
            if new_cat:
                if subreddit_manager.add_category(new_cat):
                    print(f"Category '{new_cat}' added successfully.")
                else:
                    print(f"Failed to add category '{new_cat}'.")
                time.sleep(1)
        elif choice == 'c':
            # Enable/Disable Category
            try:
                cat_num = int(input("Enter category number to toggle: "))
                if 1 <= cat_num <= len(categories):
                    category_name = list(categories.keys())[cat_num-1]
                    if category_name in enabled_categories:
                        subreddit_manager.disable_category(category_name)
                        print(f"Category '{category_name}' disabled.")
                    else:
                        subreddit_manager.enable_category(category_name)
                        print(f"Category '{category_name}' enabled.")
                    time.sleep(1)
                else:
                    print("Invalid category number.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a valid number.")
                time.sleep(1)
        elif choice == 'd':
            # Delete Category
            try:
                cat_num = int(input("Enter category number to delete: "))
                if 1 <= cat_num <= len(categories):
                    category_name = list(categories.keys())[cat_num-1]
                    confirm = input(f"Are you sure you want to delete '{category_name}'? (y/n): ").lower()
                    if confirm == 'y':
                        subreddit_manager.remove_category(category_name)
                        print(f"Category '{category_name}' deleted.")
                        time.sleep(1)
                else:
                    print("Invalid category number.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a valid number.")
                time.sleep(1)
        else:
            print("Invalid choice.")
            time.sleep(1)

def edit_category_subreddits(category_name):
    """Edit the subreddits in a category."""
    while True:
        print_header()
        print(f"EDIT CATEGORY: {category_name}\n")
        
        # Get subreddits in this category
        categories = subreddit_manager.get_categories()
        subreddits = categories[category_name]
        
        # Display subreddits
        print("SUBREDDITS:\n")
        if subreddits:
            for i, subreddit in enumerate(subreddits, 1):
                print(f"{i}. r/{subreddit}")
        else:
            print("No subreddits in this category.")
        
        print("\nACTIONS:")
        print("a. Add Subreddit")
        print("b. Remove Subreddit")
        print("0. Back to Categories")
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == '0':
            return
        elif choice == 'a':
            # Add Subreddit
            new_sub = input("Enter subreddit name (without r/): ").strip()
            if new_sub:
                if subreddit_manager.add_subreddit(category_name, new_sub):
                    print(f"Subreddit 'r/{new_sub}' added to {category_name}.")
                else:
                    print(f"Failed to add subreddit 'r/{new_sub}'.")
                time.sleep(1)
        elif choice == 'b':
            # Remove Subreddit
            try:
                if not subreddits:
                    print("No subreddits to remove.")
                    time.sleep(1)
                    continue
                    
                sub_num = int(input("Enter subreddit number to remove: "))
                if 1 <= sub_num <= len(subreddits):
                    subreddit = subreddits[sub_num-1]
                    confirm = input(f"Are you sure you want to remove 'r/{subreddit}'? (y/n): ").lower()
                    if confirm == 'y':
                        subreddit_manager.remove_subreddit(category_name, subreddit)
                        print(f"Subreddit 'r/{subreddit}' removed.")
                        time.sleep(1)
                else:
                    print("Invalid subreddit number.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a valid number.")
                time.sleep(1)
        else:
            print("Invalid choice.")
            time.sleep(1)

def view_post_history():
    """View the bot's post history."""
    while True:
        print_header()
        print("POST HISTORY\n")
        
        # Get post statistics
        stats = post_history.get_stats()
        
        # Display statistics
        print(f"Total Posts: {stats['total_posts']}")
        if stats['total_posts'] > 0:
            print(f"First Post: {stats.get('first_post', 'Unknown')}")
            print(f"Latest Post: {stats.get('last_post', 'Unknown')}")
            
            # Display posts by subreddit
            print("\nPOSTS BY SUBREDDIT:")
            for subreddit, count in sorted(stats['subreddits'].items(), key=lambda x: x[1], reverse=True):
                print(f"  r/{subreddit}: {count} posts")
            
            # Display posts by template
            print("\nPOSTS BY TEMPLATE:")
            for template, count in sorted(stats['templates'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {template}: {count} posts")
        
        print("\nACTIONS:")
        print("1. View Recent Posts")
        print("2. Filter by Subreddit")
        print("3. Filter by Template")
        print("4. Clear History")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '0':
            return
        elif choice == '1':
            # View Recent Posts
            view_recent_posts()
        elif choice == '2':
            # Filter by Subreddit
            subreddit = input("Enter subreddit name (without r/): ").strip()
            if subreddit:
                view_filtered_posts(subreddit=subreddit)
        elif choice == '3':
            # Filter by Template
            templates = list(message_templates.TEMPLATES.keys())
            print("\nAvailable Templates:")
            for i, template in enumerate(templates, 1):
                print(f"{i}. {template}")
            
            try:
                template_num = int(input("\nEnter template number: "))
                if 1 <= template_num <= len(templates):
                    template = templates[template_num-1]
                    view_filtered_posts(template=template)
                else:
                    print("Invalid template number.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a valid number.")
                time.sleep(1)
        elif choice == '4':
            # Clear History
            confirm = input("Are you sure you want to clear all post history? (y/n): ").lower()
            if confirm == 'y':
                post_history.clear_history()
                print("Post history cleared.")
                time.sleep(1)
        else:
            print("Invalid choice.")
            time.sleep(1)

def view_recent_posts(limit=20):
    """View recent posts the bot has responded to."""
    print_header()
    print(f"RECENT POSTS (Last {limit})\n")
    
    # Get recent posts
    posts = post_history.get_history(limit=limit)
    
    if not posts:
        print("No post history found.")
    else:
        # Display posts
        for i, post in enumerate(posts, 1):
            print(f"{i}. [{post['timestamp']}] r/{post['subreddit']}")
            print(f"   Title: {post['title'][:60]}{'...' if len(post['title']) > 60 else ''}")
            print(f"   Template: {post['template_used']}")
            print(f"   URL: {post['url']}")
            print()
    
    input("Press Enter to continue...")

def view_filtered_posts(subreddit=None, template=None):
    """View posts filtered by subreddit or template."""
    filter_type = f"Subreddit: r/{subreddit}" if subreddit else f"Template: {template}"
    
    print_header()
    print(f"FILTERED POSTS ({filter_type})\n")
    
    # Get filtered posts
    posts = post_history.get_history(subreddit=subreddit, template=template)
    
    if not posts:
        print(f"No posts found for {filter_type}.")
    else:
        # Display posts
        for i, post in enumerate(posts, 1):
            print(f"{i}. [{post['timestamp']}] r/{post['subreddit']}")
            print(f"   Title: {post['title'][:60]}{'...' if len(post['title']) > 60 else ''}")
            print(f"   Template: {post['template_used']}")
            print(f"   URL: {post['url']}")
            print()
    
    input("Press Enter to continue...")

def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print_header()
        print("MAIN MENU\n")
        print("1. List All Templates")
        print("2. View Template Details")
        print("3. Edit Template")
        print("4. Create New Template")
        print("5. Manage Subreddits")
        print("6. View Post History")
        print("7. Run Bot")
        print("8. Test Bot")
        print("0. Exit")
        
        try:
            choice = int(input("\nEnter your choice: "))
            
            if choice == 0:
                print("\nExiting Bot Manager. Goodbye!")
                sys.exit(0)
            elif choice == 1:
                list_templates()
            elif choice == 2:
                view_template()
            elif choice == 3:
                edit_template()
            elif choice == 4:
                create_template()
            elif choice == 5:
                manage_subreddits()
            elif choice == 6:
                view_post_history()
            elif choice == 7:
                run_bot()
            elif choice == 8:
                test_bot()
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1)
        
        except ValueError:
            print("\nPlease enter a number.")
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nExiting Bot Manager. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
