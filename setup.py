import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ampalibe",                  # This is the name of the package
    version='1.0.7-dev',                      # The release version
    author="iTeam-$",                         # Full name of the author
    description="Ampalibe is a light open source framework for bot messenger.",
    long_description=long_description,  # Long description read from the readme
    long_description_content_type="text/markdown",
    packages=['ampalibe'],  # List of all modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                      # Information to filter the project on PyPi website
    python_requires='>=3.7',
    py_modules=["ampalibe"],                      # Name of the python package
    install_requires=[
        "fastapi", "uvicorn", "retry", "requests",
        "requests_toolbelt", "watchdog"
    ],  # depandance
    include_package_data=True, # Include all data file with the package
    scripts=['bin/ampalibe', 'bin/ampalibe.bat']
)
