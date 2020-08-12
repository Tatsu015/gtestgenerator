from setuptools import setup, find_packages

setup(
    name="gtestgenerator",
    version="1.0.0",
    description="C++ google test skeleton generator",
    author="s_tatsu",
    install_requires=["lizard"],
    url="https://bitbucket.org/s_tatsu/gtestgenerator.git",
    packages=["."],
    entry_points={"console_scripts": ["gtestgenerator = gtestgenerator:main"]},
    data_files=[("etc/gtestgenerator", ["etc/gtestgenerator/testcode.template"])],
)
