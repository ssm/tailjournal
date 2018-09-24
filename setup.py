import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tailjournal",
    version="0.1.0",
    author="Stig Sandbeck Mathisen",
    author_email="ssm@fnord.no",
    description="Tail the systemd journal, keeping track of the location",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.fnord.no/ssm/tailjournal",
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD 3-Clause",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['tailjournal=tailjournal.tailjournal:main'],
    }
)
