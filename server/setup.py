from setuptools import find_packages
from setuptools import setup
from pip.req import parse_requirements

requirements = parse_requirements('requirements/dev.txt', session='null')

setup(
    name="server",
    version="1.0.0",
    url="http://dkozlov.com",
    license="MIT",
    maintainer="Dmitry Kozlov",
    maintainer_email="dmitry.f.kozlov@gmail.com",
    description="Home Task - SRE/DevOps Engineer",
    long_description="",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[str(requirement.req) for requirement in requirements],
    extras_require={"test": ["pytest", "coverage"]},
)
