from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="pixel-art-rpg-portfolio",
    version="1.0.0",
    description="Pixel Art RPG Portfolio - The System Chronicles",
    author="Senior Technical Leader",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'game': ['**/*'],
        '': ['assets/**/*', 'tests/**/*', 'config.py', 'savegame.json'],
    },
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'system-chronicles=main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)