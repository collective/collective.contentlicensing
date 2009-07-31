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

__author__ = 'Brent Lambert, David Ray, Jon Thomas'
__docformat__ = 'restructuredtext'
__version__ = "$Revision: 1 $"[11:-2]


from zope.interface import Interface

class IContentLicensingUtility(Interface):
    """ Content Licensing Utility """

    def getLicenses(request):
        """ Return titles and ids for the supported licenses. """

    def getAvailableLicenses(request):
        """ Get available licenses. """

    def getLicenseByTitle(request, title):
        """ Return a license based on its title. """

    def getLicenseFromObject(self, obj):
        """ Get the copyright license for an object. """

    def getHolderFromObject(self, obj):
        """ Get the copyright holder for an object. """

    def getLicenseAndHolderFromObject(obj):
        """ Get the copyright holder and license from an object. """

    def setLicense(obj, license):
        """ Set a license using the Dublin Core Annotations interface. """

    def getDefaultSiteLicense(self, request):
        """ Get the default site license """

    def getSiteDefaultLicenseByLine(request):
        """ Get the site default for a copyright byline. """

    def isLicensable(obj):
        """ Is an object licensable? """

    def setRightsLicense(obj, newLicense):
        """ Set the Dublin Core Extension field. """

    def setRightsHolder(obj, holder):
        """ Set the Dublin Core Extension RighsHolder field. """

    def listSupportedJurisdictions(request):
        """ Return a list of supported jurisdiction codes. """

    def getJurisdictionCode(request):
        """ Return the current jurisdiction code. """
