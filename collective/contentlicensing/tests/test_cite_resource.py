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
from Products.CMFPlone.tests import PloneTestCase
from unittest import TestSuite, makeSuite
from Testing import ZopeTestCase
from Testing.ZopeTestCase import user_name
from AccessControl import Unauthorized
from base import ContentLicensingTestCase


class testContentLicensing(ContentLicensingTestCase):
    
    def testThreeAuthorCitation(self):
        from collective.contentlicensing.browser import CopyrightBylineView
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document','doc1')
        doc1 = getattr(self.portal,'doc1')
        doc1.setTitle('Test Course 04')
        doc1.setCreators('Piotr Tchaikovsky\nWinter Daydreams\nLon Pathetique\nGuido Van Rossum')
        view = CopyrightBylineView(doc1,self.app.REQUEST)
        info = view.getCitationInfo()
        assert (info.find('Tchaikovsky, P., Daydreams, W., Pathetique, L., Rossum, G. V. (') == 0)
        assert (info.find('Test Course 04') > -1)
        assert (info.find('http://nohost/plone/doc1') > -1)
        
    def testNoAuthorCitation(self):
        from collective.contentlicensing.browser import CopyrightBylineView
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document','doc1')
        doc1 = getattr(self.portal,'doc1')
        doc1.setTitle('Test Course 04')
        doc1.setCreators('')
        view = CopyrightBylineView(doc1,self.app.REQUEST)
        info = view.getCitationInfo()
        assert (info.find('Test Course 04. (') == 0)
        assert (info.find('http://nohost/plone/doc1') > -1)
        assert (info.find('). Retrieved') > -1)
        
    def testOneAuthorCitation(self):
        from collective.contentlicensing.browser import CopyrightBylineView
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document','doc1')
        doc1 = getattr(self.portal,'doc1')
        doc1.setTitle('Test Course 04')
        doc1.setCreators('Guido Van Rossum')
        view = CopyrightBylineView(doc1,self.app.REQUEST)
        info = view.getCitationInfo()
        assert (info.find('Rossum, G. V. (') == 0)
        assert (info.find('Test Course 04') > -1)
        assert (info.find('http://nohost/plone/doc1') > -1)
        
    def testOneNameAuthorCitation(self):
        from collective.contentlicensing.browser import CopyrightBylineView
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Document','doc1')
        doc1 = getattr(self.portal,'doc1')
        doc1.setTitle('Test Course 04')
        doc1.setCreators('Rossum')
        view = CopyrightBylineView(doc1,self.app.REQUEST)
        info = view.getCitationInfo()
        assert (info.find('Rossum. (') == 0)
        assert (info.find('Test Course 04') > -1)
        assert (info.find('http://nohost/plone/doc1') > -1)
        

def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(testContentLicensing))
    return suite

