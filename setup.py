from setuptools import setup, find_packages

setup(
    name="neon_space_shooter",
    version="1.0.0",
    description="A neon-styled vertical scrolling space shooter",
    author="Jules",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "neon-shooter=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
