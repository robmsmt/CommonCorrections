import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def read_file(fname):
    with open(fname, "r") as f:
        return f.read()



setuptools.setup(
    name="commoncorrections",
    version="1.0.12",
    author="Rob Smith",
    author_email="robmsmt@gmail.com",
    description="A small python implementation of common ASR corrections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robmsmt/CommonCorrections",
    # package_dir={"": "commoncorrections"},
    # packages=setuptools.find_packages(where="commoncorrections"),
    packages=setuptools.find_packages(exclude=['tests']),
    python_requires=">=3.6",
    package_data={
        'commoncorrections': ['corrections.csv'],
    },
    install_requires=[
        elem.strip() for elem in read_file("requirements.txt").splitlines()
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)


#sudo apt install twine -y
#python3 -m pip install --upgrade setuptools wheel
#python3 setup.py sdist bdist_wheel
#twine upload dist/*

#one liner
#rm -rf ./build ./dist ./commoncorrections.egg-info && python3 setup.py sdist bdist_wheel && twine upload dist/*
