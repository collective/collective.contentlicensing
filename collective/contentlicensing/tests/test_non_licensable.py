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
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from collective.contentlicensing.utilities.interfaces import IContentLicensingUtility


class TestContentLicensing(ContentLicensingTestCase):   

    def afterSetUp(self):
        self.props = self.portal.portal_properties.content_licensing_properties
        self.clutil = getUtility(IContentLicensingUtility)
    
    def testNonLicensableTopic(self):
        from collective.contentlicensing.browser import CopyrightBylineView
        self.setRoles(['Manager'])
        
        self.portal.invokeFactory('Folder','folder1')
        folder1 = getattr(self.portal,'folder1')
        folder1.setTitle('Test Folder 01')
        
        folder1.invokeFactory('Document','doc1')
        doc1 = getattr(folder1,'doc1')
        doc1.setTitle('Test Document 01')
        doc1.setCreators('Piotr Tchaikovsky\nWinter Daydreams\nLon Pathetique\nGuido Van Rossum')
        doc1.setText('lorem ipsum blah blah blah')
        
        folder1.invokeFactory('Topic','sf1')
        sf1 = getattr(folder1,'sf1')
        sf1.setTitle('Test Smart Folder 01')
        sf1.setDescription('This is a test Smart Folder')

        view = CopyrightBylineView(doc1, self.app.REQUEST)
        assert(view.getLicenseByline())

        view = CopyrightBylineView(doc1, self.app.REQUEST)
        self.assertRaises(TypeError, view.getLicenseByline())

        
    def testNonLicensableRecurse(self):
        from collective.contentlicensing.browser import CopyrightBylineView
        self.setRoles(['Manager'])

        self.portal.invokeFactory('Folder','folder1')
        folder1 = getattr(self.portal,'folder1')
        folder1.setTitle('Test Folder 01')
        
        folder1.invokeFactory('Document','doc1')
        doc1 = getattr(folder1,'doc1')
        doc1.setTitle('Test Document 01')
        doc1.setCreators('Piotr Tchaikovsky\nWinter Daydreams\nLon Pathetique\nGuido Van Rossum')
        doc1.setText('lorem ipsum blah blah blah')
        
        folder1.invokeFactory('Topic','sf1')
        sf1 = getattr(folder1,'sf1')
        sf1.setTitle('Test Smart Folder 01')
        sf1.setDescription('This is a test Smart Folder')

        gnu_license = self.props.getProperty('license_gnuFree')
        folder1.REQUEST['license'] = gnu_license[0]
        folder1.REQUEST['license_cc_name'] = gnu_license[1]
        folder1.REQUEST['recurse_cc_url'] = gnu_license[2]
        folder1.REQUEST['recurse_cc_button'] = gnu_license[3]
        folder1.REQUEST['recurse_folders'] = True
        notify(ObjectModifiedEvent(folder1))

        self.assertEqual(self.clutil.getLicenseAndHolderFromObject(doc1)[1][0],
                         'GNU Free Documentation License')
        
        
def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestContentLicensing))
    return suite

