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

from zope.component import getUtility
from collective.contentlicensing.utilities.interfaces import IContentLicensingUtility

class RSSView:
    """ Implements base view functionality. """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.cclicenses = {}
        self.props = context.portal_url.portal_properties.content_licensing_properties
        self.clutil = getUtility(IContentLicensingUtility)

    def getRSSObjects(self):
        """ Get objects for RSS. """
        syn = self.context.portal_syndication
        return list(syn.getSyndicatableContent(self.context))

    def getCCLicense(self, obj):
        """ Get License information """
        holder = self.props.DefaultSiteCopyrightHolder
        license = self.props.DefaultSiteLicense
        if obj != self.context.portal_url.getPortalObject():
            result = self.clutil.getLicenseAndHolderFromObject(obj)
            if result:
                if result[0] != '(site default)':
                    holder = license[0]
                if result[1][0] != 'Site Default':
                    license = result[1]
        if license and 'Creative Commons License' == license[0]:
            if not self.cclicenses.has_key(license[2]):
                self.cclicenses[license[2]] = license[1].split(' ')[0]
            return license[2], holder
        else:
            return None

    def getCCLicenseTags(self):
        """ Get the list of CC Licenses listed in the RSS Feed. """
        return [(self.cclicenses[x],x) for x in self.cclicenses]

    def getCCLicenseTag(self, cclicense, tag):
        """ Get appropriate cc license entries for the license tag. """
        if self.clutil.hasCCLicenseInfo(cclicense):
            license = self.clutil.getCCLicenseInfo(cclicense)
            if license.has_key(tag):
                return license[tag]
        return []
        
    def getRightsAndHolder(self, obj):
        """ Get the rights and rights holder for the object. """
        copyright = obj.Rights()
        if not copyright:
            copyright = self.props.DefaultSiteCopyright
        holder = self.props.DefaultSiteCopyrightHolder
        if obj != self.context.portal_url.getPortalObject():
            result = self.clutil.getLicenseAndHolderFromObject(obj)
            if result:
                if result[0] != '(site default)':
                    holder = result[0]
        return copyright, holder
    
