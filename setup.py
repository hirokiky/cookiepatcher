from setuptools import setup, find_packages


setup(
    name='cookiepatcher',
    version='0.1.1',
    description='A tool to apply updates of cookiecutter templates',
    packages=find_packages(),
    install_requires=['cookiecutter>=1.5.0'],
    entry_points={
        'console_scripts': [
            'cookiepatcher = cookiepatcher.main:cookiepatch'
        ]
    }
)
