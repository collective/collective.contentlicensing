## Controller Python Script "prefs_content_licensing_set"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=jurisdiction='',site_copyright='', rights_holder='', add_license='', newpub=''
##title=Set Content Licensing Parameters
##

from collective.contentlicensing import ContentLicensingMessageFactory as _

props = context.portal_properties.content_licensing_properties
mdtool = context.portal_metadata

message = ''

#Ignores 'empty' add_license
if add_license != ['', '', '']:
    #duplicates license name
    add_license[1] = add_license[0]
    #rewrites empty image pointer element
    if add_license[3] == '' :
        add_license[3] = 'None'
    license_id = 'license_%s' %add_license[0]
    license_id = string.join(license_id.lower().split(),"")
    props.manage_addProperty(license_id, add_license, 'lines')
    props.manage_changeProperties(SupportedLicenses=list(props.SupportedLicenses)+[license_id])
    props.manage_changeProperties(AvailableLicenses=list(props.AvailableLicenses)+[license_id])


#Redefines licenses that appear in the metadata widget for end users
supported_licenses = []            
for x in list(props.SupportedLicenses):
    supported_license = context.REQUEST.get('supported_'+x)
    if supported_license == 'on':
        supported_licenses.append(x)

props.manage_changeProperties(AvailableLicenses=supported_licenses)

#Sets the default license by grabbing the form node from the request object 
default_site_license = context.REQUEST.license
if default_site_license:
    def_license = context.portal_contentlicensing.getLicense(default_site_license)
    props.manage_changeProperties(DefaultSiteLicense=def_license) 

props.manage_changeProperties(Jurisdiction=jurisdiction,
                              DefaultSiteCopyright=site_copyright,
                              DefaultSiteCopyrightHolder=rights_holder)

mdtool.editProperties(publisher=newpub)

if len(message) == 0:
    message = _(u'Changes saved.')
    context.plone_utils.addPortalMessage(message)

return state
                                                      
