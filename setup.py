from setuptools import setup
from setuptools import find_packages


name = "cloud-functions-test"
version = "0.0.2"


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name=name,
    version=version,
    packages=["cloud_functions_test"],
    package_data={
        'cloud_functions_test': ['test_classes/*'],
    },
    license='apache-2.0',
    description="Test locally GCP Cloud Functions",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=f"https://github.com/RobinPicard/{name}",
    download_url=f"https://github.com/RobinPicard/{name}/releases/download/v0.0.1/{name}-{version}.tar.gz",
    author='Robin Picard',
    author_email='robin.picard@sciencespo.fr',
    install_requires=[
        'functions-framework',
        'python-dotenv',
        'requests',
        'termcolor',
    ],
    entry_points={
        'console_scripts': [
            'cloud-functions-test=cloud_functions_test.cli:main',
        ],
    },
    keywords=[
        "python",
        "testing",
        "tests",
        "gcp",
        "cloud functions",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
    ],
)
