from setuptools import find_packages
from distutils.core import setup

if __name__ == "__main__":
    with open("README.md", "r") as fh:
        long_description = fh.read()
    setup(
        name="pyisotopomer",
        version="0.0.2",
        author="Colette L. Kelly",
        author_email="clkelly@stanford.edu",
        description="Nitrous oxide isotopocule data corrections in Python",
        url="https://github.com/ckelly314/pyisotopomer",
        project_urls={
            "Bug Tracker": "https://github.com/ckelly314/pyisotopomer/issues",
        },
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Natural Language :: English",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Chemistry",
        ],
        include_package_data=True,
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        setup_requires=[],
        install_requires=[
            "numpy",
            "pandas",
            "scipy",
            "datetime",
            "openpyxl",
            "jupyter"
        ],
    )
