"""setup.py

Used for creation and DESTRUCTION of SAAS environments

Author:
    Alex Potter-Dixon <apotter-dixon@glasswallsolutions.com>
"""
from setuptools import setup, find_packages


def repo_file_as_string(file_path: str) -> str:
    with open(file_path, "r") as repo_file:
        return repo_file.read()


setup(
    dependency_links=[],
    install_requires=[
        "click", "marshmallow", "pyyaml", "requests", "azure-devops"
    ],
    name="destroyer",
    version="0.2.0",
    description="Allows the creation and DESTRUCTION of SAAS on the cloud.",
    long_description=repo_file_as_string("README.md"),
    long_description_content_type="text/markdown",
    author="Alex Potter-Dixon",
    author_email="apotter-dixon@glasswallsolutions.com",
    packages=find_packages(),
)