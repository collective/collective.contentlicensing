from zope.publisher.browser import BrowserView
from zope.component import getUtility, getMultiAdapter
from zope.i18n import translate
from collective.contentlicensing.utilities.interfaces import IContentLicensingUtility
from Products.CMFPlone.utils import getToolByName, safe_unicode
from collective.contentlicensing import ContentLicensingMessageFactory as _
from DateTime import DateTime

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

        return copyright, translate(holder.decode('utf-8','ignore'), domain="ContentLicensing", target_language=self.request.LANGUAGE), license_name, license_url, license_button

    def getAlertMsg(self):
        """Use this domain for translation"""
        msg = _(
            _(u'The citation for this resource is presented in APA format. '
            'Copy the citation to your clipboard for reuse.')
        )
        return translate(msg, domain="ContentLicensing", target_language=self.request.LANGUAGE)

    def getCitationInfo(self):
        """ Gets the citation information """

        # Title
        title = self.context.title

        # Creators
        creator = ''
        index = 1
        
        try:
            names = [name.strip() for name in self.context.Creators()]
        except AttributeError:
            names = []

        for cr in names:
            if cr and '@' == cr[0]:
                creator += '%s, ' %cr[1:]
            else:
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
         
        portal_url = getToolByName(self.context, 'portal_url')
        portal_name = portal_url.getPortalObject().title
        plone_view = getMultiAdapter((self.context, self.request), name='plone')
        create_date = plone_view.toLocalizedTime(self.context.creation_date)
        url = self.context.absolute_url()
        date = plone_view.toLocalizedTime(DateTime())
        
        if creator:
            prompt_text = translate(
                _(u"%s (%s). %s. Retrieved %s, from %s Web site: %s."),
                domain="ContentLicensing",
                target_language=self.request.LANGUAGE,
            ) % (
                safe_unicode(creator),
                safe_unicode(create_date),
                safe_unicode(title),
                safe_unicode(date),
                safe_unicode(portal_name),
                safe_unicode(url)
            )
        else:
            prompt_text = translate(
                _(u"%s. (%s). Retrieved %s, from %s Web site: %s."),
                domain="ContentLicensing",
                target_language=self.request.LANGUAGE,
            ) % (
                safe_unicode(title),
                safe_unicode(create_date),
                safe_unicode(date),
                safe_unicode(portal_name),
                safe_unicode(url)
            )

        return prompt_text.replace('\'','\\\'').replace('\"','\\\'')

