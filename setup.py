from setuptools import setup, find_packages

setup(
    name="gtestgenerator",
    version="1.0.0",
    description="C++ google test skeleton generator",
    packages=find_packages(),
    install_requires=["lizard"],
    entry_points={"console_scripts": ["gtestgenerator = gtestgenerator.main:execute"]},
#    data_files=[("etc/gtestgenerator", ["etc/gtestgenerator/testcode.template"])],
)
