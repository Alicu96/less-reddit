from setuptools import setup, find_packages

setup(
    name="less-reddit",
    version="0.1.0",
    description="A terminal-based Reddit browser with a less-like scrollable viewer.",
    author="Alicu96",
    author_email="trihm1996@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "praw",
        "click",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "less-reddit=less_reddit.cli:main"
        ]
    },
    python_requires='>=3.7',
)