"""Setup configuration for tasklet-agent package"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tasklet-agent",
    version="0.1.0",
    author="Tasklet Contributors",
    description="An intelligent AI agent framework for task automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/accmoha86-beep/tasklet-agent",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "openai>=1.3.0",
        "anthropic>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.11.0",
            "pylint>=3.0.0",
        ]
    },
)
