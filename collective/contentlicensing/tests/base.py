##################################################################################
#    Copyright (c) 2004-2009 Utah State University, All rights reserved.
#    Portions copyright 2009 Massachusetts Institute of Technology, All rights reserved.
#                                                                                 
#    This program is free software; you can redistribute it and/or modify         
#    it under the terms of the GNU General Public License as published by         
#    the Free Software Foundation, version 2.                                      
#                                                                                 
#    This program is distributed in the hope that it will be useful,              
#    but WITHOUT ANY WARRANTY; without even the implied warranty of               
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                
#    GNU General Public License for more details.                                 
#                                                                                 
#    You should have received a copy of the GNU General Public License            
#    along with this program; if not, write to the Free Software                  
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA    
#                                                                                 
##################################################################################
from zope.testing import doctest
from Products.PloneTestCase.PloneTestCase import setupPloneSite, installProduct
from Products.PloneTestCase.PloneTestCase import PloneTestCase, FunctionalTestCase
from setuptools import find_packages

from Products.Five import fiveconfigure
from Products.Five import zcml
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase.layer import onsetup
from plone.app.blob.tests.layer import BlobReplacementLayer

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

class BlobContentLicensingTestCase(PloneTestCase):
    """ Test Class with blob support """
    layer = BlobReplacementLayer


class ContentLicensingFunctionalTestCase(FunctionalTestCase):
    """ Functional test class """
