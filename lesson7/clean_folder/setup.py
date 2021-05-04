  
from setuptools import setup, find_packages

setup(
    name = "clean_folder",
    version = "1.0"
    entry_points = {
        'console_scripts': ['clean-folder=clean_folder.clean:main']
    }
    author='MaJluc',
    author_email='ambud@ukr.net',
    zip_safe = False
    packages = find_packages()
    include_package_data = True
    description = "Clean folder script"
    )
