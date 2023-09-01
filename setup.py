from setuptools import setup, find_packages


name = "cloud-function-test"
version = "0.0.1"

setup(
    name=name,
    version=name,
    packages=[name],
    description="Test locally GCP Cloud Functions",
    url=f"https://github.com/RobinPicard/{name}",
    install_requires=[
        'requests',
        'termcolor'
    ],
    entry_points={
        'console_scripts': [
            'cloud-function-test=cloud_function_test.cli:main',
        ],
    },
)
