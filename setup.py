from setuptools import setup, find_packages

setup(
    name="map_generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.26.0",
        "tensorflow>=2.15.0",
        "keras>=2.15.0",
        "matplotlib>=3.8.0",
        "scikit-learn>=1.3.0",
        "pillow>=10.0.0",
        "pygame>=2.5.0",
        "scipy>=1.11.1",
        "h5py>=3.9.0"
    ],
) 