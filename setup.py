from setuptools import setup, find_packages

setup(
    name='Apache Flink example',
    version='0.1.0',
    author='Wiley Marques',
    description='Description of your project',
    packages=find_packages(),
    install_requires=[
        'boto3==1.34.122',
    ],
)
