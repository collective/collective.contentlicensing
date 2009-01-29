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


from zope.component import adapts, getUtility, queryUtility
from zope.interface import implements

from Products.Archetypes import atapi

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

from collective.contentlicensing.DublinCoreExtensions.interfaces import ILicensable, ILicense
from collective.contentlicensing.utilities.interfaces import IContentLicensingUtility
from collective.contentlicensing.widget import LicenseWidget

# custom fields to use the legacy storage via the ILicense adapter rather
# than a simple annotation

class CopyrightHolderField(ExtensionField, atapi.StringField):
    
    def get(self, instance, **kw):
        return ILicense(instance).getRightsHolder()
        
    def set(self, instance, value, **kw):
        ILicense(instance).setRightsHolder(value)

class LicenseField(ExtensionField, atapi.LinesField):
    
    def get(self, instance, **kw):
        return ILicense(instance).getRightsLicense()
    
    def set(self, instance, value, **kw):
        license = ILicense(instance)
        license.setRightsLicense(value)
        
        # recurse
        if instance.REQUEST.has_key('recurse_folders'):
            recursive_license(instance, value)

def recursive_license(obj, license):
    """ Recursively Licenses objects """
    clutil = getUtility(IContentLicensingUtility)
    brains = obj.portal_catalog.searchResults(path={'query':('/'.join(obj.getPhysicalPath())+'/'), })
    for brain in brains:
        object = brain.getObject()
        if clutil.isLicensable(object):
            clutil.setObjLicense(object, license)

class SchemaExtender(object):
    implements(ISchemaExtender)
    adapts(ILicensable)
    
    _fields = [
        CopyrightHolderField('copyright_holder',
            required=False,
            searchable=False,
            languageIndependent=True,
            schemata = 'ownership',
            widget = atapi.StringWidget(
                label = 'Copyright Holder',
                description = """The name of the person or organization owning or managing rights 
                    over the resource.""",
                i18n_domain = 'ContentLicensing',
                visible = {'view':'invisible', 'edit':'visible'},
                ),
            default = '(site default)'
            ),
            
        LicenseField('license',
            required=False,
            searchable=False,
            languageIndependent=True,
            schemata = 'ownership',
            widget = LicenseWidget(
                label = 'Copyright License',
                description = 'The license on this item.',
                i18n_domain = 'ContentLicensing',
                visible = {'view':'invisible', 'edit':'visible'},
                ),
            default = ['Site Default', 'None', 'None', 'None'],
            ),
        ]
        
    def __init__(self, context):
        self.context = context
        
    def getFields(self):
        # only add the fields on sites that have collective.contentlicensing installed
        if queryUtility(IContentLicensingUtility) is not None:
            return self._fields
        else:
            return []
