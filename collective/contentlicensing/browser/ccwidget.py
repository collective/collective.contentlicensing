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

from Products.Five.browser import BrowserView
from zope.component import getAdapter
from contentlicensingprefs import IContentLicensingPrefsForm


class CCWidgetView(BrowserView):
    """ CC Widget view class """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.prefs = getAdapter(context, IContentLicensingPrefsForm)

    def getJurisdiction(self):
        juris = self.prefs.jurisdiction
        juris_code = juris.split(',')[0]
        if juris_code == 'Unported':
            juris_code = ''
        return juris_code
        
    def getCCLicenseInfo(self):
        return self.prefs.getCCLicense()

    def getFormId(self):
        return '%s.%d' %(self.request['name'], self.request['index'])

    def isChecked(self):
        if self.request.has_key('checked'):
            return True
        return False
