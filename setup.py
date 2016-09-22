from setuptools import setup

import nullarbor_translate

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='nullarbor_translate',
      version=nullarbor_translate.__version__,
      description=nullarbor_translate.__description__,
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GPLv3',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Intended Audience :: Science/Research',
      ],
      keywords='microbial genomics Nullarbor',
      url=nullarbor_translate.__url__,
      author=nullarbor_translate.__author__,
      author_email=nullarbor_translate.__author_email__,
      license=nullarbor_translate.__license__,
      packages=['nullarbor_translate'],
      install_requires=[
          'click',
          'jinja2',
          'pandas',
          'PyYAML',
      ],
      test_suite='nose.collector',
      tests_require=[],
      entry_points={
          'console_scripts': ['nullarbor_translate=nullarbor_translate.nullarbor_translate:main'],
      },
      include_package_data=True,
      zip_safe=False)
