from setuptools import setup

# Use README for the PyPI page
with open('README.md') as f:
    long_description = f.read()

# https://setuptools.readthedocs.io/en/latest/setuptools.html
setup(name='pypresence',
      author='qwertyquerty',
      url='https://github.com/qwertyquerty/pypresence',
      version='4.1.2',
      packages=['pypresence'],
      python_requires='>=3.5',
      platforms=['Windows', 'Linux', 'OSX'],
      zip_safe=True,
      license='MIT',
      description='Discord RPC client written in Python',
      long_description=long_description,
      # PEP 566, PyPI Warehouse, setuptools>=38.6.0 make markdown possible
      long_description_content_type='text/markdown',
      keywords='discord rich presence pypresence rpc api wrapper gamers chat irc',

      # Used by PyPI to classify the project and make it searchable
      # Full list: https://pypi.org/pypi?%3Aaction=list_classifiers
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: MIT License',

            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS :: MacOS X',

            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: Implementation :: CPython',

            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Libraries',
            'Topic :: Communications :: Chat',
            'Framework :: AsyncIO',
      ]
)

print("""
___  _   _ ___  ____ ____ ____ ____ _  _ ____ ____
|__]  \_/  |__] |__/ |___ [__  |___ |\ | |    |___
|      |   |    |  \ |___ ___] |___ | \| |___ |___
""")
