from setuptools import setup, find_packages
import os

version = '2.2.6'
tests_require = ['plone.app.blob [test]']

setup(name='collective.contentlicensing',
      version=version,
      description="This tool is used to manage copyright licenses within plone.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Printing",
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
