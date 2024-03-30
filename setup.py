from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cotiara',
    version='0.1.3',
    packages=['cotiara'],
    install_requires=[
        "keyboard",
        "pyautogui"
    ],
    entry_points={
        'console_scripts': [
            'cotiara=cotiara.main:main',
        ],
    },
    author='dimabreus',
    author_email='dmitriybreus5@gmail.com',
    description='An interpreter written in Python for the Cotiara language',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
