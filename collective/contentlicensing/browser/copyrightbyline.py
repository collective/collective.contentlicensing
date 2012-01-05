from zope.publisher.browser import BrowserView
from zope.component import getUtility
from collective.contentlicensing.utilities.interfaces import IContentLicensingUtility
from Products.CMFPlone.utils import getToolByName
from collective.contentlicensing.browser import unicode_sanitize
from collective.contentlicensing import ContentLicensingMessageFactory as _
import datetime


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
        ts = getToolByName(self.context, 'translation_service')
        return copyright, ts.translate(holder.decode('utf-8','ignore')), license_name, license_url, license_button

    def getAlertMsg(self):
        """Use this domain for translation"""
        ts = getToolByName(self.context, 'translation_service') 
        msg = _(
            _(u'The citation for this resource is presented in APA format. '
            'Copy the citation to your clipboard for reuse.')
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
         
        id = self.context.getId()
        portal_url = getToolByName(self.context, 'portal_url')
        portal_name = portal_url.getPortalObject().title
	# TODO: Adds support at format date on every languages at this string
        create_date = self.context.creation_date.strftime('%Y, %B %d')
        url = self.context.absolute_url()
        date = datetime.date.today().strftime('%B %d, %Y')
        
        ts = getToolByName(self.context, 'translation_service') 
        if creator:
            prompt_text = ts.translate(
                _(u"%s (%s). %s. Retrieved %s, from %s Web site: %s.")
            ) % (
                unicode_sanitize(creator),
                create_date,unicode_sanitize(title),
                date,unicode_sanitize(portal_name),url
            )
        else:
            prompt_text = ts.translate(
                _(u"%s. (%s). Retrieved %s, from %s Web site: %s.")
            ) % (
                unicode_sanitize(title),
                create_date,date,unicode_sanitize(portal_name),
                url
            )

        return prompt_text.replace('\'','\\\'').replace('\"','\\\'')

