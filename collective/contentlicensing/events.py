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

from zope.component import getUtility
from collective.contentlicensing.utilities.interfaces import IContentLicensingUtility


def recursive_license(obj, evt):
    if not getattr(obj, 'REQUEST', None) or not obj.REQUEST.has_key('recurse_folders'):
        return
    #Recursively Licenses objects
    clutil = getUtility(IContentLicensingUtility)
    brains = obj.portal_catalog.searchResults(path={'query':('/'.join(obj.getPhysicalPath())+'/'), })
    for brain in brains:
        object = brain.getObject()
        if clutil.isLicensable(object):
            clutil.setObjLicense(object)
    
