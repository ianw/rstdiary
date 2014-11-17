from setuptools import setup, find_packages

setup(
    name='rstdiary',
    version='0.1',
    author='Ian Wienand <ian@wienand.org>',
    packages = find_packages(),

    package_data = {
        '': ['templates/*.html'],
    },

    description='',
    long_description='',
    license='MIT License',
    entry_points = {
        'console_scripts': ['rstdiary = rstdiary.rstdiary:main'],
    },
    install_requires=['docutils', 'Jinja2>=2.4']
)
