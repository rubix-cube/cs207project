from setuptools import setup
import distutils.cmd

class print_docs(distutils.cmd.Command):
    description = 'print documentation'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        readme = open('README.md', 'r')
        print(readme.read())


setup(
	name='cs207rbtree',

	version='1.0.3',

	description='A red-black tree implemented key-value database',

	url='https://github.com/rubix-cube/cs207project',

	author='rubix-cube',

	classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.5'
    ],

    packages=['cs207rbtree'],

    install_requires=['portalocker'],

    setup_requires=['pytest-runner'],

    test_suite='tests',

    tests_require=['pytest'],

    cmdclass={
        'docs': print_docs
    },
)