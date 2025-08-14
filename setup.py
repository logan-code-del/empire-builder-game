"""
Minimal setup.py for Read the Docs compatibility.
This file is only used for documentation building.
"""

from setuptools import setup, find_packages

setup(
    name="empire-builder",
    version="1.0.0",
    description="Empire Builder - Real-time multiplayer strategy game",
    author="Doom",
    author_email="development.doom.endnote612@passfwd.com",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.2.5",
        "supabase>=1.0.4",
        "flask-socketio>=5.3.4",
        "python-dotenv>=1.0.0",
        "Jinja2>=3.1.0",
    ],
    extras_require={
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
            "sphinx-autodoc-typehints>=1.19.0",
        ]
    },
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment :: Real Time Strategy",
    ],
)