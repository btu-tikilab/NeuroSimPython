from setuptools import setup, find_packages

setup(
    name="neurosim-engine",
    version="1.0.0",
    description="NeuroSim Genetic Algorithm Engine",
    author="Unit A (BitGA)",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "pytest>=7.4.3",
        "neurosim-problems>=0.1.0",
    ],
)