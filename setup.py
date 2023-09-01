from setuptools import setup, find_packages


name = "cloud-function-test"
version = "0.0.1"

setup(
    name=name,
    version=version,
    packages=["cloud_function_test"],
    description="Test locally GCP Cloud Functions",
    url=f"https://github.com/RobinPicard/{name}",
    author='Robin Picard',
    author_email='robin.picard@sciencespo.fr'
    install_requires=[
        'requests',
        'termcolor'
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
