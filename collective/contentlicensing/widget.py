##################################################################################
#
#    Copyright (C) 2006 Utah State University, All rights reserved.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
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


from zope.component import getUtility
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget
from AccessControl import ClassSecurityInfo
from collective.contentlicensing.utilities.interfaces import IContentLicensingUtility

class LicenseWidget(TypesWidget):
    """ Customized selection widget allowing better configuration of licenses.
    """

    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : 'license_widget',
        'blurrable' : True,
        })

    security = ClassSecurityInfo()
    
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        """ Provide custom logic for determing the license based on several form fields """

        value, kw = TypesWidget.process_form(self, instance, field, form,
            empty_marker, emptyReturnsMarker, validating)
        
        if 'Creative Commons License' == value:
            newLicense = ['Creative Commons License',
                          instance.REQUEST['license_cc_name'],
                          instance.REQUEST['license_cc_url'],
                          instance.REQUEST['license_cc_button']]
        elif 'Other' == value:
            newLicense = ['Other',
                          instance.REQUEST['license_other_name'],
                          instance.REQUEST['license_other_url'],
                          'None']
        elif 'Site Default' == value:
            props = instance.portal_url.portal_properties.content_licensing_properties
            newLicense = props.license_siteDefault
        else:
            clutil = getUtility(IContentLicensingUtility)
            newLicense = clutil.getLicenseByTitle(instance, value)
        
        return newLicense, kw

# Register the widget with Archetypes
registerWidget(LicenseWidget,
               title = 'License widget',
               description= ('Allows configuring which license applies to the content.',),
               used_for = ('collective.contentlicensing.fields.LicenseField',)
               )
