from setuptools import setup, find_packages

setup(
    name="cloud-builder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        'console_scripts': [
            'cloud-build=cloud_builder.cli:cli',
        ],
    },
    python_requires=">=3.12",
)
