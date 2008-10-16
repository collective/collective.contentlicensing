## Script (Python) "content_edit_recurse"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id='',recurse_folders=''
##

if context.isPrincipiaFolderish and recurse_folders:
        brains = context.portal_catalog.searchResults(path={'query':('/'.join(context.getPhysicalPath())+'/'), })
        for brain in brains:
            obj = brain.getObject()
	    if context.portal_contentlicensing.isLicensable(obj):
                context.portal_contentlicensing.setObjLicense(brain.getObject())
            
return state.set(context=context,status='success')
