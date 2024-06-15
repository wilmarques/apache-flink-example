from setuptools import setup, find_packages

setup(
    name='Apache Flink example',
    version='0.1.0',
    author='Wiley Marques',
    description='Example of using Apache Flink. Following AWS guides and it\'s managed service (<https://aws.amazon.com/managed-service-apache-flink>).',
    packages=find_packages(),
    install_requires=[
        'boto3==1.34.122',
    ],
)
