# less-reddit – A Terminal-Based Reddit Browser

A simple, keyboard-navigable Reddit browser that runs in your terminal. It lets you browse subreddits, view posts, and read comments using a scrollable "less"-like interface.


---

## 📦 Features

- Browse any subreddit from your terminal
- View hot, new, or top posts
- Navigate with arrow keys (`↑ ↓`) or `j/k`
- Read full post content and comments in a scrollable viewer
- Works on Windows, macOS, and Linux

---

## 🧰 Requirements

Make sure you have these installed before proceeding:

- Python 3.7+
- `pip` (Python package installer)

---

## 🧩 Installation

### Option 1: Install from PyPI (Coming Soon)

Once published to PyPI, you'll install it like this:

```bash
pip install less-reddit
```

### Option 2: Install from Source

1. Clone the repository:
```bash
git clone https://github.com/Alicu96/less-reddit.git
cd less-reddit
```

2. Install the package:
```bash
pip install -e .
```

## 🔧 Configuration

Before using less-reddit, you need to set up your Reddit API credentials:

1. Create a Reddit application at https://www.reddit.com/prefs/apps
2. Create a `.env` file in your home directory with the following content:
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=less-reddit/0.1.0 (by /u/your_username)
```

## 🚀 Usage

Start the application by running:
```bash
less-reddit
```

### Basic Commands

- Use arrow keys to navigate posts
- Press `Enter` to view a post and its comments
- Press `q` to quit

