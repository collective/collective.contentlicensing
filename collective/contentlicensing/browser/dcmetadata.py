from zope.publisher.browser import BrowserView
from zope.component import getUtility
from collective.contentlicensing.utilities.interfaces import IContentLicensingUtility
from Products.CMFPlone.utils import getToolByName


class DCMetadataEditFields(BrowserView):
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

    def getCurrentOtherLicense(self):
        """ Get other license """
        if self.license and 'Other' == self.license[0]:
            return self.license
        else:
            return ['Other', '', '', '']

    def getLicenseAndHolderFromObject(self, obj):
        """ Get the license and copyright holder from the object """
        return self.clutil.getLicenseAndHolderFromObject(self.context)        

    def getDefaultSiteLicense(self, request):
        """ Get the default site license  """
        return self.clutil.getDefaultSiteLicense(request)

    def getLicenseTitle(self, request):
        """ Returns the license name. For creative commons licenses, it explicitly appends the 
        CC license type  """
	ts = getToolByName(self.context,'translation_service')
        license = self.clutil.getDefaultSiteLicense(request)
        if license[0] == 'Creative Commons License':
            return ts.translate(license[0]) + ' :: ' + license[1]
        else:
            return ts.translate(license[0])

