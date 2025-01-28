from setuptools import setup, find_packages

setup(
    name="package",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Lux King Soft",
    author_email="luxkingsoft@gmail.com",
    description="This package has some utility modules.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/LuxKingSoft/softutils/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)