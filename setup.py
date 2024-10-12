from setuptools import setup, find_packages

setup(
    name="screenshot_analyzer",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "PyQt5",
'python-dotenv',
'litellm',
'ollama',
'markdown'    ],
    entry_points={
        "console_scripts": [
            "screenshot_analyzer=main:main",
        ],
    },
)