from setuptools import setup, find_packages


setup(
    name='cookiepatcher',
    version='0.1',
    description='A tool to apply updates of cookiecutter templates',
    packages=find_packages(),
    install_requires=['cookiecutter'],
    entry_points={
        'console_scripts': [
            'cookiepatcher = cookiepatcher.main:cookiepatch'
        ]
    }
)
