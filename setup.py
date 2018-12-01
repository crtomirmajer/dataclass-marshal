from setuptools import find_packages, setup

setup(
    name='dataclass-marshal',
    author='Črtomir Majer',
    version='0.1.0',
    long_description='Easy (Un)Marshal Dataclasses',
    python_requires='>3.6',
    packages=find_packages(
        include=[
            'dataclass_marshal',
        ],
        exclude=[
            'tests',
        ],
    ),
    install_requires=[
        'dataclasses'
    ],
    extras_require={
        'unit-tests': [
            'pytest',
        ]
    },
    include_package_data=True,
    dependency_links=[],
)
