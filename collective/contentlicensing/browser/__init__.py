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

from Products.Five.browser import BrowserView
from zope.component import getUtility
from zope.interface import implements
from collective.contentlicensing.utilities.interfaces import IContentLicensingUtility
from collective.contentlicensing.browser.contentlicensingprefs import IContentLicensingPrefsForm
from Products.CMFPlone.utils import getToolByName, safe_unicode
from urlparse import urlsplit
from xml.dom import minidom
from string import split, find
import urllib
import datetime

from collective.contentlicensing import ContentLicensingMessageFactory as _

class ExtendedCopyrightFieldForm(BrowserView):
    """ Render the additional copyright fields in the metadata form. """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.clutil = getUtility(IContentLicensingUtility)
        self.license = None
        self.holder = None
        results = self.clutil.getLicenseAndHolderFromObject(self.context)
        if results:
            self.holder = results[0]
            self.license = results[1]
            
    def isLicensable(self):
        """ Is the object licensable """
        return self.clutil.isLicensable(self.context)

    def getLicenses(self):
        """ Get list of supported licenses. """
        return self.clutil.getLicenses(self.context)

    def getLicense(self):
        """ Get the copyright license from the object. """
        return self.license

    def getHolder(self):
        """ Get the copyright license holder. """
        return self.holder

    def getJurisdictionCode(self):
        """ Get the Creative Commons jurisdiction code. """
        return self.clutil.getJurisdictionCode(self.context)

    def getSiteDefaultCCLicense(self, item):
        """ Get the Default Site Creative Commons License for prefs panel  """

        pass


    def getDefaultCCLicense(self, item):
        """ If the item already has a creative commons license, return it """
        if self.license and 'Creative Commons License' == self.license[0]:
            return self.license
        else:
            return item

    def getDefaultOtherLicenseName(self):
        """ Get other license name """
        if self.license and 'Other' == self.license[0]:
            return self.license[0]
        else:
            return ''

    def getDefaultOtherLicenseUrl(self):
        """ Get other license URL """
        if self.license and 'Other' == self.license[0]:
            return self.license[0]
        else:
            return ''

    def getDefaultOtherLicenseButton(self):
        """ Get other license URL """
        if self.license and 'Other' == self.license[0]:
            return self.license[0]
        else:
            return 'default_other.gif'

    def getLicenseAndHolderFromObject(self, obj):
        """ Get the license and copyright holder from the object """
        return self.clutil.getLicenseAndHolderFromObject(self.context)        

    def getDefaultSiteLicense(self, request):
        """ Get the default site license  """
        return self.clutil.getDefaultSiteLicense(request)

    def getLicenseTitle(self, request):
        """ Returns the license name. For creative commons licenses, it explicitly appends the CC license type  """
	ts = getToolByName(self.context,'translation_service')
        license = self.clutil.getDefaultSiteLicense(request)
        if license[0] == 'Creative Commons License':
            return ts.translate(license[0]) + ' :: ' + license[1]
        else:
            return ts.translate(license[0])

class FrontpageCopyrightBylineView(BrowserView):
    """ Render the default site copyright byline """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.props = self.context.portal_url.portal_properties.content_licensing_properties
        self.clutil = getUtility(IContentLicensingUtility)

    def getLicenseByline(self):
        """ Get the license byline fields for an object. """

        copyright = self.context.Rights()
        copyright = self.props.DefaultSiteCopyright
        holder = self.props.DefaultSiteCopyrightHolder
        license = self.props.DefaultSiteLicense
        license_name = license[1]
        if not license_name or 'None' == license_name:
            license_name = ''
        if 'Creative Commons License' == license[0]:
            license_name = license[0]
        license_url = license[2]
        if not license_url or 'None' == license_url:
            license_url = ''
        license_button = license[3]
        if not license_button or 'None' == license_button:
            license_button = ''
        return copyright, holder, license_name, license_url, license_button        


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
    
