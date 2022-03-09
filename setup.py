from distutils.core import setup
setup(
  name = 'pypsm',
  packages = ['pypsm'],
  version = 'v1.0',      
  license = 'MIT',
  description = 'This package allows users to construct control groups for their data through propensity score matching with a simple interface.',
  author = 'Hunter Thompson',
  author_email = 'hunteryt@uw.edu',
  url = 'https://github.com/hunteryt17/DATA_511_Projects',
  keywords = ['data science', 'propensity score matching', 'control group'],
  install_requires = [
          'scikit-learn',
          'pandas'
      ],
  classifiers = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)