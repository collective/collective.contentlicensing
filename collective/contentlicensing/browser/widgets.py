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

from zope.app.form.browser import RadioWidget
from zope.app.form.browser.widget import SimpleInputWidget

class LicenseWidget(RadioWidget):
    """ Widget for displaying license options. """

    def __init__(self, field, request):
        """ Initialize the widget. """
        super(LicenseWidget, self).__init__(field, 
                                            field.vocabulary, 
                                            request)
        
    def renderItem(self, index, text, value, name, cssClass):
        if 'Creative Commons License' == value:
            self.request['index'] = index
            self.request['text'] = text
            self.request['value'] = value
            self.request['name'] = name
            self.request['cssClass'] = cssClass
            return self.context.context.context.restrictedTraverse('@@cc_license_widget')()
        else:
            return super(LicenseWidget, self).renderItem(index, text, value, name, cssClass)

    def renderSelectedItem(self, index, text, value, name, cssClass):
        if 'Creative Commons License' == value:
            self.request['index'] = index
            self.request['text'] = text
            self.request['value'] = value
            self.request['name'] = name
            self.request['cssClass'] = cssClass
            self.request['checked'] = True
            return self.context.context.context.restrictedTraverse('@@cc_license_widget')()
        else:
            return super(LicenseWidget, self).renderSelectedItem(index, text, value, name, cssClass)

    
