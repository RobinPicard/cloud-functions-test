from setuptools import setup
from setuptools import find_packages


name = "cloud-function-test"
version = "0.0.5"

setup(
    name=name,
    version=version,
    packages=["cloud_function_test"],
    package_data={
        'cloud_function_test': ['test_classes/*'],
    },
    license='apache-2.0',
    description="Test locally GCP Cloud Functions",
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
            'cloud-function-test=cloud_function_test.cli:main',
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
