from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gewechat-client",
    version="0.1.0",
    author="Gewechat",
    author_email="contact@gewechat.com",
    description="A package for interacting with the Gewechat API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gewechat-python-github",
    license='MIT',
    packages=find_packages(exclude=["reference-code"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests"
    ],
    keywords='gewechat api client',
    include_package_data=True,
)