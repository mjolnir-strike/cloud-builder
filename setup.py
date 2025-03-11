from setuptools import setup, find_packages

setup(
    name="cloud-builder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "crewai>=0.1.0",
        "python-dotenv>=1.0.0",  # For environment variable management
        "pydantic>=2.0.0",  # Required by CrewAI
    ],
    extras_require={
        "langchain": ["langchain>=0.1.0"],  # Optional LangChain support
    },
    entry_points={
        'console_scripts': [
            'cloud-build=cloud_builder.cli:cli',
        ],
    },
    python_requires=">=3.12",
)
