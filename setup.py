"""Setup file for pr-agent package."""

from setuptools import find_packages, setup

setup(
    name="pr_agent",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.13",
    install_requires=[
        "python-dotenv",
        "PyGithub",
        "openai",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
            "flake8-docstrings",
            "flake8-quotes",
            "flake8-comprehensions",
            "mypy",
            "pre-commit",
        ]
    },
)
