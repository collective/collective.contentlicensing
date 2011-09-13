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
from Products.CMFPlone.utils import getToolByName
from urlparse import urlsplit
from xml.dom import minidom
from string import split, find
import urllib
import datetime

from collective.contentlicensing import ContentLicensingMessageFactory as _

def unicode_sanitize(text):
    """
    Intended to be used to correct the inconsistency of plone when you call
    methods such as Title or Publisher which should ALLWAYS return a unicode
    object if the output is text.
    """
    if isinstance(text,list):
        sanit_list = []
        for item in text:
            if isinstance(item, str):
                sanit_list += item.decode('utf-8')
            else:
                sanit_list += item
        text = sanit_list          
    elif isinstance(text, str):
        text = text.decode('utf-8')
    return text


class CopyrightBylineView(BrowserView):
    """ Render the copyright byline """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.props = self.context.portal_url.portal_properties.content_licensing_properties
        self.clutil = getUtility(IContentLicensingUtility)

    def getLicenseByline(self):
        """ Get the license byline fields for an object. """
        copyright = self.context.Rights()
        if not copyright:
            copyright = self.props.DefaultSiteCopyright
        holder, license = self.clutil.getLicenseAndHolderFromObject(self.context)
        if '(site default)' == holder:
            holder = self.props.DefaultSiteCopyrightHolder
        if 'Site Default' == license[0]:
            license = self.props.DefaultSiteLicense
        license_name = license[0]
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
        ts = getToolByName(self.context, 'translation_service')
        return copyright, ts.translate(holder), license_name, license_url, license_button



    def getAlertMsg(self):
        """Use this domain for translation"""
        ts = getToolByName(self.context, 'translation_service') 
        msg = _(
            u'The citation for this resource is presented in APA format. '
            'Copy the citation to your clipboard for reuse.'
        )
        return ts.translate(msg)

    def getCitationInfo(self):
        """ Gets the citation information """

        # Title
        title = self.context.title

        # Creators
        creator = ''
        index = 1
        
        names = [name.strip() for name in self.context.Creators()]
        
        for cr in names:
            inits = ''
            crs = []

            crs = cr.split(' ')
            
            for part in crs[:-1]:
                inits += ' ' + part[0] + '.'   
                
            creator += crs[-1]
            if inits:
                creator += "," + inits
            creator += ', '
            index += 1
            
        if creator:
            creator = creator[:-2]
            if creator:
                if creator[-1] != '.':
                    creator += '.'
         
        id = self.context.getId()
        portal_url = getToolByName(self.context, 'portal_url')
        portal_name = portal_url.getPortalObject().title
        create_date = self.context.creation_date.strftime('%Y, %B %d')
        url = self.context.absolute_url()
        date = datetime.date.today().strftime('%B %d, %Y')
        
        ts = getToolByName(self.context, 'translation_service') 
        if creator:
            prompt_text = ts.translate(
                _(u"%s (%s). %s. Retrieved %s, from %s Web site: %s.")
            ) % (
                unicode_sanitize(creator),
                unicode_sanitize(create_date),unicode_sanitize(title),
                unicode_sanitize(date),unicode_sanitize(portal_name),unicode_sanitize(url)
            )
        else:
            prompt_text = ts.translate(
                _(u"%s. (%s). Retrieved %s, from %s Web site: %s.")
            ) % (
                unicode_sanitize(title),
                unicode_sanitize(create_date),unicode_sanitize(date),unicode_sanitize(portal_name),
                unicode_sanitize(url)
            )

        return prompt_text.replace('\'','\\\'').replace('\"','\\\'')



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

class RDFMetadataView(BrowserView):
    """ Express Dublin Core As Rdf  """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.document = minidom.Document()
        self.props = self.context.portal_url.portal_properties.content_licensing_properties
        self.clutil = getUtility(IContentLicensingUtility)
        self.holder, self.license = self.clutil.getLicenseAndHolderFromObject(context)        

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/rdf+xml')
        return self.writeRDF()

    def writeRDF(self):
        """ Write RDF metadata """
        if 'Creative Commons License' == self.license[0] or ('Creative Commons License' == self.props.DefaultSiteLicense[0] and 'Site Default' == self.license[0]):
            if self.license[0] == 'Site Default':
                self.license = self.props.DefaultSiteLicense
            data = self.getCCLicenseRDF()
        else:
            data = self.getRDFMetadata()
        # Remove the XML header
        index = find(data, '\n')
        if (index > -1):
            data = data[index + 1:]
        return data

    def getRDFMetadata(self):
        """ Write metadata fields as RDF. """
        rdf_node = self._createNode(self.document, 'rdf:RDF',
                       attrs=[('xmlns:rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
                              ('xmlns:dc', 'http://purl.org/dc/elements/1.1/'),
                              ('xmlns:dcterms', 'http://purl.org/dc/terms')])
        desc_node = self._createNode(rdf_node, 'rdf:Description',
                        attrs=[('rdf:about', self.context.renderBase())])
        self._writeDCMetadata(desc_node)
        return self.document.toprettyxml()        
                                

    def getCCLicenseRDF(self):
        """ Write into RDF CC License elements. """

        holder, license = self.clutil.getLicenseAndHolderFromObject(self.context)
        licenseId = ''
        if len(self.license) >= 3:
            lid = urlsplit(self.license[2])
            if len(lid) >= 3:
                lid = lid[2].split('/')
                if len(lid) >= 3:
                    licenseId = lid[2]

        if licenseId and self.clutil.hasCCLicenseInfo(licenseId):
            cc_rdf = self.clutil.getCCLicenseInfo(licenseId)
        
            rdf_node = self._createNode(self.document, 'rdf:RDF',
                           attrs=[('xmlns', 'http://creativecommons.org/ns#'),
                                  ('xmlns:dc', 'http://purl.org.dc/elements/1.1/'),
                                  ('xmlns:rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')])
            work_node = self._createNode(rdf_node, 'Work', attrs=[('rdf:about',
                                                                   self.context.renderBase())])
            self._writeDCMetadata(work_node)
            self._createNode(work_node, 'license', attrs=[('rdf:resource', self.license[2])])
            return self.document.toprettyxml()
        else:
            return ''

    def _writeDCMetadata(self, node):
        """ Write the dublin core metadata in RDF. """

        # Identifier
        self._createNode(node, 'dc:identifier', self.context.renderBase())

        # Title
        self._createNode(node, 'dc:title', self.context.title )

        # Description
        desc = self.context.Description()
        if desc:
            self._createNode(node, 'dc:description', self.context.Description() )

        # Subject
        self._renderList(node, 'dc:subject', [sub for sub in self.context.Subject() ] )

        # Publisher
        self._createNode(node, 'dc:publisher', self.context.portal_url.getPortalObject().Publisher() )
        
        # Creators
        self._renderList(node, 'dc:creator', [creat for creat in self.context.Creators() ] )

        # Contributors
        self._renderList(node, 'dc:contributor', [contrib for contrib in self.context.Contributors() ] )

        # Rights
        rights = self.context.Rights()
        if not rights:
            rights = self.props.DefaultSiteCopyright
        holder = self.props.DefaultSiteCopyrightHolder
        if self.context != self.context.portal_url.getPortalObject():
            result = self.clutil.getLicenseAndHolderFromObject(self.context)
            if result:
                if result[0] != '(site default)':
                    holder = license[0]            
        self._createNode(node, 'dc:rights', '%s, %s' % (rights, holder))

        # Language
        lang = self.context.Language()
        if not lang:
            po = self.context.portal_url.getPortalObject()
            lang = po.portal_properties.site_properties.getProperty('default_language')
        self._createNode(node, 'dc:language', lang )

        # Type
        self._createNode(node, 'dc:type', self.context.Type())

        # Format
        self._createNode(node, 'dc:format', self.context.Format())


    def _renderList(self, node, element, value):
        """ Render a list of items in RDF. """
        if value:
            if len(value) > 1:
                value_node = self._createNode(node, element)
                bag_node = self._createNode(value_node, 'rdf:Bag')
                for x in value:
                    self._createNode(bag_node, 'rdf:li', x )
            else:
                self._createNode(node, element, value[0] )
        

    def _createNode(self, parent, ename, value=None, attrs=None):
        """ Create a node in the document. """
        newNode = self.document.createElement(ename)
        parent.appendChild(newNode)
        if value:
            newNode.appendChild(self.document.createTextNode(unicode_sanitize(value) ) )
        if attrs:
            for x in attrs:
                newNode.setAttribute(x[0], x[1] )
        return newNode


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
    
