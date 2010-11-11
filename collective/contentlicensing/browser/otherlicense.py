from zope.interface import Interface
from plone.app.form.base import AddForm
from zope.formlib.form import FormFields, action
from zope.schema import TextLine
from collective.contentlicensing import ContentLicensingMessageFactory as _

from Products.Five.formlib.formbase import PageForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class OtherLicensePageForm(PageForm):
    """ Override default page form. """

    template = ViewPageTemplateFile('otherlicenseformlayout.pt')


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
                             description=_(u''),
                             required=False)

class OtherLicenseForm(OtherLicensePageForm):
    """ Other License Form """

    form_fields = FormFields(IOtherLicenseForm)
    label = _(u'Create License')
    description = _(u'Create a new license for use with your content types.')

    @action(u'Submit',
            name=u'Submit')
    def action_submit(self, action, data):
        """ Submit new fields for a license """


    
