from zope.interface import Interface
from zope.component import getMultiAdapter, getUtility
from plone.app.form.base import AddForm
from plone.app.form.validators import null_validator
from zope.formlib.form import FormFields, action
from zope.schema import TextLine
from Acquisition import aq_inner
from Products.statusmessages.interfaces import IStatusMessage
from collective.contentlicensing import ContentLicensingMessageFactory as _
from collective.contentlicensing.utilities.interfaces import IContentLicensingUtility
try:
    # Zope2 < 2.13
    from Products.Five.formlib.formbase import PageForm, AddForm
except:
    # Zope2 >= 2.13
    from five.formlib.formbase import PageForm, AddForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IOtherLicenseForm(Interface):
    """ Marker interface for other license form """

    license_name = TextLine(title=_(u'License Name'),
                            description=_(u'The title of the license that will '
                                          'appear on the licensed object.'),
                            required=True)

    license_url = TextLine(title=_(u'License URL'),
                           description=_(u'The external URL of the license, '
                                         'this usually contains the actual '
                                         'content of the license.'),
                           required=True)

    license_image = TextLine(title=_(u'License Image'),
                             description=_(u'An external URL link to an image that '
                                           'represents the license.'),
                             required=False)

class OtherLicenseForm(AddForm):
    """ Other License Form """

    form_fields = FormFields(IOtherLicenseForm)
    label = _(u'Create License')
    description = _(u'Create a new license for use with your content types.')

    @action(_(u'Submit'), name=u'Submit') 
    def action_submit(self, action, data):
        """ Submit new fields for a license """
#        context = aq_inner(self.context)
#        nl = (data['license_name'], data['license_name'], data['license_url'], data['license_image'])
#        clutils = getUtility(IContentLicensingUtility)
#        clutils.setRightsLicense(context, nl)
#        IStatusMessage(self.request).addStatusMessage(_(u'Copyright License Changed.'), type='info')
#        self.request.response.redirect('%s/insert_license' %self.context.absolute_url())
        return ''

    @action(_(u'Cancel'), validator=null_validator, name=u'Cancel')
    def action_cancel(self, action, data):
        """ Cancel create other license. """
#        context = aq_inner(self.context)
#        IStatusMessage(self.request).addStatusMessage(_(u'Copyright License change cancelled.'), type='info')
#        self.request.response.redirect(context.absolute_url())
        return ''
    
