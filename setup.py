import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jkcli",
    version="0.0.1",
    author="Luan Tran",
    author_email="minhluantran017@gmail.com",
    description="Small tool to interactive with Jenkins through commandline interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minhluantran017/jkcli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)