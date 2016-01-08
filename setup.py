from setuptools import setup, find_packages


setup(
    name='cookiepatcher',
    description='A tool to apply updates of cookiecutter templates',
    packages=find_packages('cookiepatcher'),
    install_requires=['cookiecutter'],
    entry_points={
        'console_scripts': [
            'cookiepatcher = cookiepatcher.main:cookiepatch'
        ]
    }
)
