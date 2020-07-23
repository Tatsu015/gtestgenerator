from setuptools import setup,find_packages

setup(
    name="gtestgenerator",
    version='1.0.0',
    description='C++ google test skeleton generator',
    author='s_tatsu',
    author_email='',
    url='https://bitbucket.org/s_tatsu/gtestgenerator.git',
    packages=find_packages(),
    entry_points={'console_scripts': ['gtestgenerator = gtestgenerator.gtestgenerator:main']},
)