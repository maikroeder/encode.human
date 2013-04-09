from setuptools import setup
from setuptools import find_packages


install_requires = [
    'setuptools',
    # -*- Extra requirements: -*-
]

entry_points = """
    # -*- Entry points: -*-
    """

classifiers = [
    'Programming Language :: Python',
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
]

with open("README.txt") as f:
    README = f.read()

with open("CHANGES.txt") as f:
    CHANGES = f.read()

setup(name='encode.human',
      version='1.0',
      packages=find_packages(),
      description=(""),
      long_description=README + '\n' + CHANGES,
      author='',
      author_email='',
      include_package_data=True,
      zip_safe=False,
      classifiers=classifiers,
      install_requires=install_requires,
      keywords='',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      namespace_packages=['encode'],
      entry_points=entry_points,
      )
