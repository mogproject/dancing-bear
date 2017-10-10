from setuptools import setup, find_packages

SRC_DIR = 'src'


def get_version():
    import sys

    sys.path[:0] = [SRC_DIR]
    return __import__('dancing_bear').__version__


setup(
    name='dancing-bear',
    version=get_version(),
    description='Dancing Bear',
    author='mogproject',
    author_email='mogproj@gmail.com',
    license='Apache 2.0 License',
    url='https://github.com/mogproject/dancing-bear',
    install_requires=[
        'six',
        'python-dateutil',
        'pytz',
        'tzlocal',
        'argparse',
        'pyserial',
        'mog-commons >= 0.1.3',
    ],
    tests_require=[
        'unittest2',
    ],
    package_dir={'': SRC_DIR},
    packages=find_packages(SRC_DIR),
    include_package_data=True,
    test_suite='tests',
    entry_points="""
    [console_scripts]
    dancing-bear = dancing_bear.dancing_bear:main
    """,
)
