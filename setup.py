from setuptools import setup, find_packages

setup(
    name="cloud-builder",
    version="0.1.0",
    description="Provider-agnostic Terraform code analysis tool using CrewAI",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",  # CLI framework
        "crewai>=0.12.2",  # AI agent framework
        "python-dotenv>=1.0.0",  # Environment variable management
        "pydantic>=2.6.0",  # Data validation
        "langchain_ollama>=0.1.1",  # Ollama integration
        "langchain_openai>=0.1.0"  # For GPT-4-0-mini support
    ],
    extras_require={
        "dev": [
            "mypy>=1.0.0",  # Type checking
            "black>=23.0.0",  # Code formatting
            "pytest>=7.0.0",  # Testing
        ],
    },
    entry_points={
        'console_scripts': [
            'cloud-build=cloud_builder.cli:cli',
        ],
    },
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
    ],
    keywords="terraform, infrastructure, analysis, ai, cloud-agnostic",
)
