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

from zope.interface import Interface, implements 
from zope.component import adapts, getMultiAdapter, getUtility
from zope.formlib import form
from zope.schema import TextLine, Choice, Tuple, Field
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName
from collective.contentlicensing import ContentLicensingMessageFactory as _
from Products.CMFCore.interfaces import IPropertiesTool, IMetadataTool
from plone.app.controlpanel.form import ControlPanelForm
try:
    from plone.fieldsets import FormFieldsets
except ImportError:
    from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.form.validators import null_validator
from widgets import LicenseWidget
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget 


def jurisdictionvocab(context):
    props = getToolByName(context, 'portal_properties')
    juris = props.content_licensing_properties.jurisdiction_options
    return SimpleVocabulary.fromItems([x.split(',') for x in juris])


def supportedvocab(context):
    props = getToolByName(context, 'portal_properties')
    supp = props.content_licensing_properties.AvailableLicenses
    ts = getToolByName(context.context,'translation_service')
    licenses = []
    for x in supp:
        value = getattr(props.content_licensing_properties, x)[0], x
        if 'Creative Commons License' == value[0]:
            value = (_(u'Creative Commons License Picker'), x)
	value = ts.translate(value[0]), value[1]
        licenses.append(value)
    return SimpleVocabulary.fromItems(licenses)


def defaultlicensevocab(context):
    props = getToolByName(context, 'portal_properties')
    supp = props.content_licensing_properties.SupportedLicenses
    ts = getToolByName(context.context,'translation_service')
    licenses = []
    for x in supp:
        value = getattr(props.content_licensing_properties, x)[0]
        licenses.append((ts.translate(value), value))
    return SimpleVocabulary.fromItems(licenses)

        
class IContentLicensingSettingsForm(Interface):    
    """ The view for content licensing prefs form. """

    jurisdiction = Choice(title=_(u'Jurisdiction'),
                          description=_(u'Specify the jurisdiction in which the content license '
                                        'is valid. (Any Jurisdiction changes must be saved before '
                                        'choosing a new Creative Commons license.)'),
                          required=True,
                          default='unported',
                          vocabulary='contentlicensing.jurisdictionvocab')

    publisher = TextLine(title=_(u'Publisher'),
                         description=_(u'The institution or individual responsible for publishing '
                                       'content in this portal.'),
                         required=False)
    default_copyright = TextLine(title=_(u'Default Copyright'),
                                 description=_(u'The default copyright to be used with content '
                                               'in this portal.'),
                                 required=False)

    default_copyright_holder = TextLine(title=_(u'Default Copyright Holder'),
                                        description=_(u'The default copyright owner for content in '
                                                      'this portal.'),
                                        required=False,)

    default_license = Choice(title=_(u'Default License'),
                             description=_(u'Default License'),
                             required=True,
                             vocabulary='contentlicensing.defaultlicensevocab')

    supported_licenses = Tuple(title=_(u'Supported Licenses'),
                               description=_(u'Choose the licenses which can be selected for individual '
                                             'objects. The Creative Commons License Picker provides an '
                                             'interactive form to choose an appropriate Creative '
                                             'Commons license.'),
                               required=True,
                               missing_value=tuple(),
                               value_type=Choice(vocabulary='contentlicensing.supportedvocab'))


class IContentLicensingNewLicenseForm(Interface):
    """ The view for the add new license form """
    new_license_name = TextLine(title=_(u'License Name'),
                                description=_(u'The name of the license.'),
                                required=False)

    new_license_url = TextLine(title=_(u'License Location'),
                               description=_(u'The URL pointer to information about the license.'),
                               required=False)

    new_license_icon = TextLine(title=_(u'License Icon'),
                                description=_(u'The URL pointer to an image associated with the license.'),
                                required=False)
                                           

class IContentLicensingPrefsForm(IContentLicensingSettingsForm, IContentLicensingNewLicenseForm):
    """ Combined settings and new license form. """


class ContentLicensingControlPanelAdapter(SchemaAdapterBase):
    """ Control Panel adapter """

    adapts(IPloneSiteRoot)
    implements(IContentLicensingPrefsForm)
    
    temp_license = ['', '', '', '']

    def __init__(self, context):
        super(ContentLicensingControlPanelAdapter, self).__init__(context)
        pprop = getUtility(IPropertiesTool)
        self.clprops = pprop.content_licensing_properties
        self.mdtool = getUtility(IMetadataTool)

    def get_jurisdiction(self):
        return self.clprops.Jurisdiction

    def set_jurisdiction(self, juris):
        self.clprops.Jurisdiction = juris

    def get_publisher(self):
        return self.mdtool.Publisher()

    def set_publisher(self, publisher):
        self.mdtool.editProperties(publisher=publisher)
    
    def get_default_copyright(self):
        return self.clprops.getProperty('DefaultSiteCopyright')

    def set_default_copyright(self, copyright):
        self.clprops.DefaultSiteCopyright = copyright

    def get_default_copyright_holder(self):
        return self.clprops.getProperty('DefaultSiteCopyrightHolder')
    
    def set_default_copyright_holder(self, holder):
        self.clprops.DefaultSiteCopyrightHolder = holder

    def get_default_license(self):
        return self.clprops.getProperty('DefaultSiteLicense')[0]

    def set_default_license(self, license_name):
        licenses = self.clprops.getProperty('AvailableLicenses')
        for x in licenses:
            license = getattr(self.clprops, x, None)
            if license and license[0] == license_name:
                self.clprops.DefaultSiteLicense = license
                break

    def get_supported_licenses(self):
        return self.clprops.SupportedLicenses

    def set_supported_licenses(self, licenses):
        self.clprops.SupportedLicenses = licenses

    def getCCLicense(self):
        return self.clprops.license_cc
    
    def setCCLicense(self, subname, url, icon):
        self.clprops.license_cc = ('Creative Commons License',
                                   subname,                                  
                                   url,
                                   icon)
        self.clprops.DefaultSiteLicense = ('Creative Commons License',
                                           subname,                                  
                                           url,
                                           icon) 

    
    jurisdiction = property(get_jurisdiction, set_jurisdiction)
    publisher = property(get_publisher, set_publisher)
    default_copyright = property(get_default_copyright, 
                                 set_default_copyright)
    default_copyright_holder = property(get_default_copyright_holder,
                                        set_default_copyright_holder)
    default_license = property(get_default_license,
                               set_default_license)
    supported_licenses = property(get_supported_licenses, 
                                  set_supported_licenses)


    # Use the new license fields to generate a new license, not set individual properties

    def get_nothing(self):
        return ''

    def set_nothing(self, param):
        pass

    new_license_name = property(get_nothing, set_nothing)
    new_license_url = property(get_nothing, set_nothing)
    new_license_icon = property(get_nothing, set_nothing)

    def setNewLicense(self, name, url, icon):
        """ Set a new license """
        new_license = [name, name, '', '']
        if url:
            new_license[2] = url
        if icon:
            new_license[3] = icon
        license_id = 'license_%s' %(''.join(name.lower().split()))
        self.clprops.manage_addProperty(license_id, new_license, 'lines')
        self.clprops.manage_changeProperties(SupportedLicenses=list(self.clprops.getProperty('SupportedLicenses')) + [license_id])
        self.clprops.manage_changeProperties(AvailableLicenses=list(self.clprops.getProperty('AvailableLicenses')) + [license_id])


settingsset = FormFieldsets(IContentLicensingSettingsForm)
settingsset.id = 'contentlicensingsettings'
settingsset.label = _(u'Content License Settings')

newlicenseset = FormFieldsets(IContentLicensingNewLicenseForm)
newlicenseset.id = 'contentlicensenewlicense'
newlicenseset.label = _(u'New License')


class ContentLicensingPrefsForm(ControlPanelForm):
    """ The view class for the content licensing preferences form. """

    implements(IContentLicensingPrefsForm)
    form_fields = FormFieldsets(settingsset, newlicenseset)
    form_fields['default_license'].custom_widget = LicenseWidget
    form_fields['supported_licenses'].custom_widget = MultiCheckBoxVocabularyWidget

    label = _(u'Content Licensing Settings')
    description = _(u'Configure site wide settings for copyright licensing '
                    'of content within this portal.')
    form_name = _(u'Content Licensing Settings')


    @form.action(_(u'Save'), name=u'save')
    def handle_edit_action(self, action, data):
        # If the CC license option has been chosen, copy the new fields
        # into the license
        if 'Creative Commons License' == data['default_license']:
            ad = self.adapters[IContentLicensingSettingsForm]
            # Get the hidden field data from the view in the form
            ad.setCCLicense(self.request['license_cc_name'],
                            self.request['license_cc_url'],
                            self.request['license_cc_button'])

        # Apply form changes        
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):

            # If there is a new license in the form, add it to the properties page
            if data.has_key('new_license_name') and data['new_license_name']:
                ad = self.adapters[IContentLicensingNewLicenseForm]
                ad.setNewLicense(data['new_license_name'], 
                                 data['new_license_url'], 
                                 data['new_license_icon'])

            self.status = _("Changes saved.")
            self._on_save(data)
            self.request['fieldset.current'] = u'fieldsetlegend-contentlicensingsettings'
        else:
            self.status = _("No changes made.")
            
        
