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

from utilities.interfaces import IContentLicensingUtility
from utilities.utils import ContentLicensingUtility


def setupUtilities(context):
    site = context.getSite()
    sm = site.getSiteManager()
    if not sm.queryUtility(IContentLicensingUtility):
        sm.registerUtility(ContentLicensingUtility('contentlicensing'), 
                           IContentLicensingUtility)

def importFinalSteps(context):
    site = context.getSite()
    reindexIndexes(site)


def reindexIndexes(site):
    """ Reindex dublin core copyright fields. """
    
