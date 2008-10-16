## Controller Python Script "validate_license"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=license_url='', license_name='', license_button=''
##title=validates URL and Name for a content object's license

from collective.contentlicensing import ContentLicensingMessageFactory as _

def missing(field):
    state.setError(field, _(u'This field is required, please provide some information.'), 'input_required')

if not license_url:
    missing('license_url')
if not license_name:
    missing('license_name')

if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    return state
