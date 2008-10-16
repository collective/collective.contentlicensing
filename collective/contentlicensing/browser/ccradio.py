from Products.Five.browser import BrowserView
from zope.component import getAdapter
from contentlicensingprefs import IContentLicensingPrefsForm

class CCWidgetView(BrowserView):
    """ CC Widget view class """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.prefs = getAdapter(context, IContentLicensingPrefsForm)

    def getJurisdiction(self):
        juris = self.prefs.jurisdiction
        juris_code = juris.split(',')[0]
        if juris_code == 'Unported':
            juris_code = ''
        return juris_code
        
    def getCCLicenseInfo(self):
        return self.prefs.getCCLicense()

    def getFormId(self):
        return '%s.%d' %(self.request['name'], self.request['index'])

    def isChecked(self):
        if self.request.has_key('checked'):
            return True
        return False
