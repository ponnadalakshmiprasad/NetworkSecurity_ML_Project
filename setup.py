import os
import sys
from setuptools import setup,find_packages
hypen_dot_e="-e ." 
def get_requirements(file_path):
    """
    This function will return the list of requirements
    """
    try:
        with open(file_path,"r") as file:
            requirements=file.readlines()
            requirements=[req.replace("\n","") for req in requirements] #removing the new line character
            if hypen_dot_e in requirements:
                requirements.remove(hypen_dot_e)
            return requirements
    except FileNotFoundError:
        print("my requirements.txt is not found")



"""
definition 1 of setup.py file:

The setup.py file is used to define the project’s package metadata (such as name, version, and author), 
manage dependencies by linking to requirements.txt, 
and install the entire project as a Python package so it can be imported and used anywhere in the environment.


"""

"""
definition 2 of setup.py file:

setup.py enables packaging the ML project as a reusable Python module.
It allows consistent dependency installation, supports modular imports across the project,
and ensures compatibility with tools like MLflow, pipelines, and deployment frameworks.


"""



setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Prasad",
    author_email="ponnadaapparao6@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)