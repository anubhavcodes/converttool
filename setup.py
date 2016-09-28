from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['tests/']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import sys, pytest
        errcode = pytest.main(self.pytest_args)
        sys.exit(errcode)


with open('README.md') as f:
    readme = f.read()


with open('LICENSE') as f:
    license = f.read()


setup(
    name='converttool',
    version='0.0.1',
    description='A tool to convert CSV into other formats',
    long_description=readme,
    author='Anubhav Yadav',
    author_email='anubhav1691@gmail.com',
    url='www.example.com',
    license=license,
    packages=['converttool'],
    install_requires=[
        'dicttoxml==1.7.4',
        'click==6.6',
        'unicodecsv==0.14.1',
    ],
    tests_require='pytest==3.0.2',
    entry_points={
        'console_scripts':[
            'converttool = converttool.app:main',
            ]
        },
    cmdclass={'test': PyTest},
)
