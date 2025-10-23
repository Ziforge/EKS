"""
Setup script for Jupyter-Overleaf Workflow.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jupyter-overleaf-workflow",
    version="1.0.0",
    author="Jupyter-Overleaf Workflow Contributors",
    description="Convert Jupyter notebooks to academic LaTeX papers with Overleaf integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/jupyter-overleaf-workflow",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "License :: Free for non-commercial use",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "jupyter>=1.0.0",
        "nbformat>=5.0.0",
        "nbconvert>=7.0.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "nb2paper=workflow.cli:main",
        ]
    },
    include_package_data=True,
    license="CC BY-NC-SA 4.0",
)
