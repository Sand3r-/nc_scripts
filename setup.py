import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nctexconv", # Replace with your own username
    version="1.0.0",
    author="Michal Gallus",
    author_email="michal.gallus@gmail.com",
    description="Nightmare Creatures Texture Converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sand3r-/nc_scripts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft",
    ],
    python_requires='>=3.6',
    py_modules=['image_loading'],
    package_data={
        "": ["*.json"]
    }
)