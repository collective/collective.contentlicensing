from setuptools import setup, find_packages
import os

version = '2.2.6'
tests_require = ['plone.app.blob [test]']

setup(name='collective.contentlicensing',
      version=version,
      description="This tool is used to manage copyright licenses within plone.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Licensing License Creative-Commons GPL All-Rights-Reserved Copyright Rights',
      author='enPraxis',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://plone.org/products/contentlicensing',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      extras_require={'tests' : tests_require},
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
