from setuptools import setup, find_packages

long_description = """

A program to create a simple "daily-diary" from a flat RST file input.
The output is chunked into months and lightly styled with bootstrap.

"""

setup(
    name='rstdiary',
    version='0.9',
    author='Ian Wienand',
    author_email='ian@wienand.org',
    packages=find_packages(),
    package_data={
        '': ['templates/*.html', 'templates/*.xml'],
    },
    description='Create static HTML diary from single RST input',
    long_description=long_description,
    license='MIT License',
    entry_points={
        'console_scripts': ['rstdiary = rstdiary.rstdiary:main'],
    },
    install_requires=['docutils', 'Jinja2>=2.4'],
    url='https://github.com/ianw/rstdiary',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Topic :: Office/Business :: News/Diary',
    ]

)
