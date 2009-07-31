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
from Products.CMFPlone import MigrationTool
try:
    from Products.contentmigration.migrator import InlineFieldActionMigrator, BaseInlineMigrator
    from Products.contentmigration.walker import CustomQueryWalker
    haveContentMigrations = True
except ImportError:
    haveContentMigrations = False

import types

from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Archetypes import transaction
from Products.Archetypes.BaseUnit import BaseUnit
from Products.CMFPlone.utils import safe_hasattr

from collective.contentlicensing.tool import ContentLicensingTool
from Acquisition import aq_base
from collective.contentlicensing.Extensions import Install


def GenericToUnported (self, out):
    """ Change Jurisdiction to valid attribute
    """
    print >> out, "Changing Jurisdiction from Generic to Unported"
    if self.portal_contentlicensing.Jurisdiction == 'Generic':
        self.portal_contentlicensing._updateProperty('Jurisdiction','Unported')

def migrate(self):
    """Run migrations
    """
    out = StringIO()
    print >> out, "Starting Content Licensing Migration"
    GenericToUnported(self, out)
    print >> out, "Content Licensing Migration Completed"
    return out.getvalue()


