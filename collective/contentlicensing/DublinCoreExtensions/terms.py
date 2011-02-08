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

__author__  = '''Brent Lambert, David Ray, Jon Thomas'''
__docformat__ = 'plaintext'
__version__   = '$ Revision 0.0 $'[11:-2]

from zope.interface import implements
from collective.contentlicensing.DublinCoreExtensions.interfaces import ILicense
from zope.annotation.interfaces import IAnnotations


RIGHTSLICENSE_KEY = 'DublinCoreExtensions.Rights.License'
RIGHTSHOLDER_KEY = 'DublinCoreExtensions.RightsHolder'

class License(object):
    """
        This class adds two Dublin Core Fields to content for storing the copyright
        license, and the holder of the copyright
    """
    implements(ILicense)

    def __init__(self, context):
        self.context = context
        self.annotations = IAnnotations(context)
        rightsLicense = self.annotations.get(RIGHTSLICENSE_KEY, None)
        if rightsLicense is None:
            self.annotations[RIGHTSLICENSE_KEY] = ['Site Default', 'None', 'None', 'None']
        rightsHolder = self.annotations.get(RIGHTSHOLDER_KEY, None)
        if rightsHolder is None:
            self.annotations[RIGHTSHOLDER_KEY] = '(site default)'

    def getRightsLicense(self):
        """ Get the contents of the DC.rights.license field. """
        return self.annotations[RIGHTSLICENSE_KEY]

    def setRightsLicense(self, ldata):
        """ Set the DC.rights.license field. """
        self.annotations[RIGHTSLICENSE_KEY] = ldata

    def getRightsHolder(self):
        """ Get the contents of the DC.rightsHolder field. """
        return self.annotations[RIGHTSHOLDER_KEY]

    def setRightsHolder(self, rhdata):
        """ Set the DC.rightsHolder field. """
        self.annotations[RIGHTSHOLDER_KEY] = rhdata

    license = property(getRightsLicense, setRightsLicense)
    holder = property(getRightsHolder, setRightsHolder)
