"""
Setup script for the keylogger_project package.

This script uses setuptools to package and distribute the keylogger_project.
It defines the package metadata, dependencies, entry points, and other configuration
needed for installation and distribution.

For more information, visit: https://github.com/Deepanshuthappa/keyloggerpython.git
"""

from setuptools import setup, find_packages

setup(
    name='keylogger_project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pynput>=1.7.6',  # Specify a version of pynput if needed
    ],
    entry_points={
        'console_scripts': [
            'keylogger=keylogger.keylogger:main',  # Entry point for the keylogger command
        ],
    },
    author='Deepanshu Thappa',
    author_email='deepanshuthappa01@gmail.com',
    description='A keylogger package using python',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/keylogger_project',  # Replace with your actual GitHub repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
