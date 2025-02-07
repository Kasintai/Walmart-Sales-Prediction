from setuptools import find_packages, setup
from typing import List

# setuptools: Provides utilities for packaging Python projects.
# find_packages(): Automatically finds and includes all Python packages in the project.
# typing.List: Used for type hinting (ensuring that get_requirements() returns a list of strings).
    
HYPHEN_E_DOT = '-e .'
def get_requirements(filepath:str)->List[str]:
    '''
    This function will return the list of requirements
    '''

    requirements=[]
    with open(filepath) as file_obj:
        requirements= file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements] #replace /n
        # requirements = [req.strip() for req in requirements]

        # Removes -e . if present (Recall -e . was used to automatically trigger/link to setup.py file)
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements

setup(
    name= 'mlproject',
    version= '0.0.1',
    author= 'Kasin',
    author_email= 'Kasintai45@gmail.com',
    packages= find_packages(),
    install_requires= get_requirements('requirements.txt') #['pandas', 'numpy', 'seaborn']
)