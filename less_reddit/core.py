import os
from dotenv import load_dotenv
import praw
import click

# Load environment variables
def init_reddit():
    load_dotenv()
    try:
        return praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
    except Exception as e:
        print(f"Error initializing Reddit API: {e}")
        exit(1)

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def view_trending_posts(reddit):
    try:
        subreddit = reddit.subreddit("all")
        generator = subreddit.hot(limit=None)
        chunk_size = 10
        all_posts = []
        current_page = 0

        while True:
            # Load initial posts if needed
            while len(all_posts) <= current_page * chunk_size:
                print("Loading more trending posts...")
                new_posts = [post for post in [next(generator, None) for _ in range(chunk_size)] if post is not None]
                if not new_posts:
                    print("[No more trending posts available.]")
                    break
                all_posts.extend(new_posts)

            start_idx = current_page * chunk_size
            end_idx = start_idx + chunk_size
            page_posts = all_posts[start_idx:end_idx]

            if not page_posts:
                print("\n[No more trending posts to show.]")
                input("Press Enter to go back...")
                return

            selected_index = 0
            while True:
                clear_screen()
                print(f"Trending Posts - Page {current_page + 1}\n")
                print("-" * 60)
                for i, post in enumerate(page_posts):
                    if i == selected_index:
                        print(f"> [{i+1}] {post.title} | Upvotes: {post.score}, r/{post.subreddit}")
                    else:
                        print(f"  [{i+1}] {post.title} | Upvotes: {post.score}, r/{post.subreddit}")
                print("-" * 60)
                print("↑ ↓ to navigate | Enter to open | n: Next 10 | p: Prev 10 | q: Back")

                key = get_key().lower()  # Make sure we lowercase the key

                # Handle arrow keys (if supported)
                if os.name != 'nt':
                    if key == '\x1b':  # ESC sequence for arrow keys
                        get_key()  # skip [
                        ch = get_key()
                        if ch == 'A':  # Up
                            selected_index = max(0, selected_index - 1)
                        elif ch == 'B':  # Down
                            selected_index = min(len(page_posts) - 1, selected_index + 1)
                        continue  # Skip rest of loop
                else:
                    if key == '\xe0':  # Windows arrow prefix
                        key = get_key()

                # Handle command keys
                if key == '\r':  # Enter
                    view_post_with_comments(page_posts[selected_index])
                elif key == 'n':
                    if (current_page + 1) * chunk_size < len(all_posts):
                        current_page += 1
                    else:
                        print("Loading next 10 posts...")
                        new_posts = [post for post in [next(generator, None) for _ in range(chunk_size)] if post is not None]
                        if new_posts:
                            all_posts.extend(new_posts)
                            current_page += 1
                        else:
                            print("No more posts available.")
                    selected_index = 0
                    break  # Break inner loop to refresh screen
                elif key == 'p' and current_page > 0:
                    current_page -= 1
                    selected_index = 0
                    break  # Refresh screen
                elif key == 'q':
                    return

    except Exception as e:
        print(f"[Error loading trending posts: {e}]")
        input("\nPress Enter to continue...")

# Get subreddit name
def get_subreddit(reddit):
    while True:
        try:
            subreddit_name = input("Enter subreddit name (e.g., 'technology'): ").strip()
            subreddit = reddit.subreddit(subreddit_name)
            subreddit.hot(limit=1)  # Test fetch
            return subreddit
        except Exception as e:
            print(f"Error fetching subreddit: {e}")
            retry = input("Try again? (y/n): ").lower().startswith('y')
            if not retry:
                return None

# Choose category (hot, new, top)
def choose_category():
    options = ['hot', 'new', 'top']
    selected = 0

    while True:
        clear_screen()
        print("Select post type:\n")
        for i, opt in enumerate(options):
            if i == selected:
                print(f"> {opt}")
            else:
                print(f"  {opt}")
        print("\n↑ ↓ to navigate, Enter to select")
        key = get_key()

        if os.name == 'nt':
            if key == '\xe0':  # Arrow key prefix
                key = get_key()
                if key == 'H':  # Up
                    selected = max(0, selected - 1)
                elif key == 'P':  # Down
                    selected = min(len(options) - 1, selected + 1)
        else:
            if key == '\x1b':  # ESC sequence
                get_key()  # skip [
                ch = get_key()
                if ch == 'A':  # Up
                    selected = max(0, selected - 1)
                elif ch == 'B':  # Down
                    selected = min(len(options) - 1, selected + 1)

        if key == '\r':  # Enter
            return options[selected]

# Fetch posts
def get_posts(subreddit, category, limit=10):
    try:
        if category == 'hot':
            posts = subreddit.hot(limit=limit)
        elif category == 'new':
            posts = subreddit.new(limit=limit)
        elif category == 'top':
            posts = subreddit.top(limit=limit)
        return list(posts)
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []

# Display posts with selection
def display_posts_with_selection(posts):
    selected_index = 0

    while True:
        clear_screen()
        print("Reddit Posts\n")
        print("-" * 60)
        for i, post in enumerate(posts):
            if i == selected_index:
                print(f"> [{i+1}] {post.title} | Upvotes: {post.score}, Comments: {post.num_comments}")
            else:
                print(f"  [{i+1}] {post.title} | Upvotes: {post.score}, Comments: {post.num_comments}")
        print("-" * 60)
        print("↑ ↓ to navigate, Enter to select, q to go back")

        key = get_key()

        if os.name == 'nt':
            if key == '\xe0':  # Arrow key prefix
                key = get_key()
                if key == 'H':  # Up
                    selected_index = max(0, selected_index - 1)
                elif key == 'P':  # Down
                    selected_index = min(len(posts) - 1, selected_index + 1)
        else:
            if key == '\x1b':  # ESC sequence
                get_key()  # skip [
                ch = get_key()
                if ch == 'A':  # Up
                    selected_index = max(0, selected_index - 1)
                elif ch == 'B':  # Down
                    selected_index = min(len(posts) - 1, selected_index + 1)

        if key == '\r':  # Enter
            return posts[selected_index]
        elif key.lower() == 'q':
            return None

# Get a single key press
def get_key():
    if os.name == 'nt':  # Windows
        import msvcrt
        return msvcrt.getch().decode('utf-8')
    else:  # Unix/Linux/Mac
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

# Less-like viewer using plain text and click pager
def view_post_with_comments(post):
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from time import sleep
    import click

    buffer = []

    # Add post title and author
    buffer.append(f"Title: {post.title}")
    buffer.append(f"Posted by u/{post.author}")
    buffer.append("-" * 60)
    buffer.append("")

    # Add post content or link
    if post.is_self:
        if post.selftext.strip():
            buffer.append("Post Content:")
            buffer.append(post.selftext)
        else:
            buffer.append("[This post has no text.]")
    else:
        buffer.append(f"Link: {post.url}")

    buffer.append("")
    buffer.append("Top Comments:")
    buffer.append("-" * 60)

    try:
        # Show loading spinner while fetching comments
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description="Loading comments...", total=None)
            post.comments.replace_more(limit=None)
            comments = post.comments.list()

        # Append loaded comments
        for comment in comments:
            author = comment.author if comment.author else "[deleted]"
            buffer.append(f"\nComment by u/{author}:")
            buffer.append(comment.body)

            # Add replies if available
            if hasattr(comment, "replies") and comment.replies:
                buffer.append("  Replies:")
                for reply in comment.replies:
                    rep_author = reply.author if reply.author else "[deleted]"
                    buffer.append(f"    Reply by u/{rep_author}:")
                    buffer.append(f"    {reply.body}")

    except Exception as e:
        buffer.append(f"[Error loading comments: {e}]")

    # Show everything in pager
    click.echo_via_pager("\n".join(buffer))

# Show detailed post view
def run():
    while True:
        clear_screen()
        print("Reddit Terminal Browser")
        print("=" * 30)
        print("1. Browse subreddit")
        print("2. View trending posts")  # NEW OPTION
        print("Q. Quit")
        print("=" * 30)
        print("Use number keys or ↑ ↓ to navigate")

        key = get_key().lower()

        if key == '1' or (key == '\xe0' and get_key() == 'A'):
            reddit = init_reddit()
            subreddit = get_subreddit(reddit)
            if subreddit:
                category = choose_category()
                posts = get_posts(subreddit, category)
                while posts:
                    selected_post = display_posts_with_selection(posts)
                    if selected_post:
                        view_post_with_comments(selected_post)
                    else:
                        break
        elif key == '2':
            reddit = init_reddit()
            view_trending_posts(reddit)
        elif key == 'q':
            print("Goodbye!")
            break