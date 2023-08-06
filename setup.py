from setuptools import setup, find_packages

with open("README.md", "r") as readme:
     long_description = readme.read()



setup(
    name='hny-mailsort',
    python_requires='>3.12.0',
    version='0.0.1',
    description='simple mailsorte',
    py_modules=['hny-mailsort'],
    package_dir={'hny-mailsort':'src'},
    packages=['hny-mailsort'],
    install_requires=[],
    extras_require={
        "dev":[
            "pytest>=6.2"
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Topic :: Utilities'
    ],
    url='https://github.com/Soldy/mailsort',
    author='Soldy',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
