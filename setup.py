import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reflector-kgolsen",
    version="0.0.1",
    author="Kyle Olsen",
    author_email="kyle.g.olsen@gmail.com",
    description="A package to auto generate OpenAPI specs from SQLAlchemy reflection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kgolsen/reflector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'reflect=reflector.cli:reflect',
        ]
    },
)
