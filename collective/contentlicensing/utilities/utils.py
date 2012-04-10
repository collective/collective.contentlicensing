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


from OFS.SimpleItem import SimpleItem
from zope.interface import implements
from interfaces import IContentLicensingUtility
from collective.contentlicensing.DublinCoreExtensions.interfaces import ILicensable, ILicense


cc_license_rdf = {'by':
                      {
                          'requires':['http://web.resource.org/cc/Attribution',
                                      'http://web.resource.org/cc/Notice'],
                          'permits':['http://web.resource.org/cc/Reproduction',
                                     'http://web.resource.org/cc/Distribution',
                                     'http://web.resource.org/cc/DerivativeWorks'],
                          'prohibits':[],
                      },
                  'by-nd':
                      {
                          'requires':['http://web.resource.org/cc/Attribution',
                                      'http://web.resource.org/cc/Notice'],
                          'permits':['http://web.resource.org/cc/Reproduction',
                                     'http://web.resource.org/cc/Distribution'],
                          'prohibits':[],
                      },
                  'by-nc-nd':
                      {
                          'requires':['http://web.resource.org/cc/Attribution',
                                      'http://web.resource.org/cc/Notice'],
                          'permits':['http://web.resource.org/cc/Reproduction',
                                     'http://web.resource.org/cc/Distribution'],
                          'prohibits':['http://web.resource.org/cc/CommercialUse'],
                      },
                  'by-nc':
                      {
                          'requires':['http://web.resource.org/cc/Attribution',
                                      'http://web.resource.org/cc/Notice'],
                          'permits':['http://web.resource.org/cc/Reproduction',
                                     'http://web.resource.org/cc/Distribution',
                                     'http://web.resource.org/cc/DerivativeWorks'],
                          'prohibits':['http://web.resource.org/cc/CommercialUse'],
                      },
                  'by-nc-sa':
                      {
                          'requires':['http://web.resource.org/cc/Attribution',
                                      'http://web.resource.org/cc/ShareAlike',
                                      'http://web.resource.org/cc/Notice'],
                          'permits':['http://web.resource.org/cc/Reproduction',
                                     'http://web.resource.org/cc/Distribution',
                                     'http://web.resource.org/cc/DerivativeWorks'],
                          'prohibits':['http://web.resource.org/cc/CommercialUse'],
                      },
                  'by-sa':
                      {
                          'requires':['http://web.resource.org/cc/Attribution',
                                      'http://web.resource.org/cc/ShareAlike',
                                      'http://web.resource.org/cc/Notice'],
                          'permits':['http://web.resource.org/cc/Reproduction',
                                     'http://web.resource.org/cc/Distribution',
                                     'http://web.resource.org/cc/DerivativeWorks'],
                          'prohibits':[],
                      },
                  'publicdomain':
                      {
                          'requires':[],
                          'permits':['http://web.resource.org/cc/Reproduction',
                                     'http://web.resource.org/cc/Distribution',
                                     'http://web.resource.org/cc/DerivativeWorks'],
                          'prohibits':[],
                      },
                  }


class ContentLicensingUtility(SimpleItem):
    """ Content Licensing Utility """

    implements(IContentLicensingUtility)

    def getLicenses(self, request):
        """ return titles and ids for the supported licenses. """
        props = request.portal_url.portal_properties.content_licensing_properties
        licenses = [props.license_siteDefault]
        for x in props.AvailableLicenses:
            licenses.append(getattr(props, x))
        licenses.append(props.license_other)
        return licenses


    def getSupportedLicenses(self, request):
        """ Return titles and ids fo the supported licenses for the configlet. """
        props = request.portal_url.portal_properties.content_licensing_properties
        return [[x, getattr(props, x)[0], getattr(props, x)[1]] for x in props.SupportedLicenses]
            

    def getAvailableLicenses(self, request):
        """ return titles and ids for the supported licenses """
        props = request.portal_url.portal_properties.content_licensing_properties
        return [x for x in props.AvailableLicenses]


    def getLicenseByTitle(self, request, title):
        """ Return a license based on its title. """
        props = request.portal_url.portal_properties.content_licensing_properties

        if 'Site Default' == title:
            return props.license_siteDefault
        elif 'Other' == title:
            return props.license_other
        else:
            for x in props.SupportedLicenses:
                sl = getattr(props, x)
                if sl and sl[0] == title:
                    return sl
            return None


    def getLicenseFromObject(self, obj):
        """ Get the copyright license for an object. """
        if ILicensable.providedBy(obj):
            lic = ILicense(obj)
            return lic.license
        else:
            return None


    def getHolderFromObject(self, obj):
        """ Get the copyright holder for an object. """
        if ILicensable.providedBy(obj):
            lic = ILicense(obj)
            return lic.holder
        else:
            return None

    def getLicenseAndHolderFromObject(self, obj):
        """ Get the copyright holder and license from an object. """
        if ILicensable.providedBy(obj):
            lic = ILicense(obj)
            return lic.holder, lic.license
        else:
            return None


    def setLicense(self, obj, lic):
        """ Set a license using the Dublin Core Annotations interface. """
        if getattr(obj.REQUEST, 'copyright_holder', None):
            lic.holder = obj.REQUEST['copyright_holder']
        if getattr(obj.REQUEST, 'license', None):
            newLicense = obj.REQUEST['license']
            if 'Creative Commons License' == newLicense:
                lic.license = (['Creative Commons License',
                                obj.REQUEST['license_cc_name'],
                                obj.REQUEST['license_cc_url'],
                                obj.REQUEST['license_cc_button']])
            elif 'Other' == newLicense:
                lic.license = (['Other',
                                obj.REQUEST['license_other_name'],
                                obj.REQUEST['license_other_url'],
                                obj.REQUEST['license_other_button']])
            else:
                nl = self.getLicenseByTitle(obj, newLicense)
                lic.license = nl


    def getDefaultSiteLicense(self, request):
        """ Get the default site license """
        props = request.portal_url.portal_properties.content_licensing_properties
        return props.DefaultSiteLicense


    def getSiteDefaultLicenseByLine(self, request):
        """ Get the site default for a copyright byline. """
        props = request.portal_url.portal_properties.content_licensing_properties
        copyright = props.DefaultSiteCopyright
        holder = props.DefaultSiteCopyrightHolder
        license = props.DefaultSiteLicense
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


    def isLicensable(self, obj):
        """ Is an object licensable? """
        return ILicensable.providedBy(obj)


    def setRightsLicense(self, obj, newLicense):
        """ Set the Dublin Core Extension field. """
        if ILicensable.providedBy(obj):
            lic = ILicense(obj)
            lic.license = newLicense


    def setRightsHolder(self, obj, holder):
        """ Set the Dublin Core Extension RightsHolder field. """
        if ILicensable.providedBy(obj):
            lic = ILicense(obj)
            lic.holder = holder


    def listSupportedJurisdictions(self, request):
        """ Return a list of supported jurisdiction codes. """
        props = request.portal_url.portal_properties.content_licensing_properties
        return [(x, allowedJurisdictions[x]) for x in props.jurisdiction_options]
               

    def getJurisdictionCode(self, request):
        """ Return the current jurisdiction code. """
        props = request.portal_url.portal_properties.content_licensing_properties
        juris_code = props.Jurisdiction.split(',')[0]
        if juris_code == 'Unported':
            juris_code = ''
        return juris_code


    def hasCCLicenseInfo(self, licenseId):
        """ Check to see if we have a particular CC license. """
        return cc_license_rdf.has_key(licenseId)


    def getCCLicenseInfo(self, licenseId):
        """ Return the CC license info for a CC license. """
        return cc_license_rdf[licenseId]

    def setObjLicense(self, obj):
        """ Set a license using the object """
        license = ILicense(obj)
        self.setLicense(obj, license)
        
