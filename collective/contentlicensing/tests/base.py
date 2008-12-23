
from zope.testing import doctest
from Products.PloneTestCase.PloneTestCase import setupPloneSite, installProduct
from Products.PloneTestCase.PloneTestCase import PloneTestCase, FunctionalTestCase
from setuptools import find_packages

from Products.Five import fiveconfigure
from Products.Five import zcml
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase.layer import onsetup


packages=find_packages('src')
package_dir={'':'src'},

@onsetup
def setup_contentlicensing_project():
    """
    Load and install packages required for the collective.contentlicensing tests
    """

    fiveconfigure.debug_mode = True
    
    import collective.contentlicensing
    zcml.load_config('configure.zcml',collective.contentlicensing)
    
    fiveconfigure.debug_mode = False

    ztc.installPackage('collective.contentlicensing')


setup_contentlicensing_project()
setupPloneSite(with_default_memberarea=0,extension_profiles=['collective.contentlicensing:default'])

oflags = (doctest.ELLIPSIS |
          doctest.NORMALIZE_WHITESPACE)

prod = "collective.contentlicensing"

class ContentLicensingTestCase(PloneTestCase):
    """ Test Class """

    def _setupHomeFolder(self):
	""" Ugly hack to keep the underlying testing framework from trying to create a user folder."""
	pass


class ContentLicensingFunctionalTestCase(FunctionalTestCase):
    """ Functional test class """
