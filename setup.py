from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in accounting/__init__.py
from accounting import __version__ as version

setup(
	name="accounting",
	version=version,
	description="Accounting app for dev",
	author="ruthra",
	author_email="ruthra@sample.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
