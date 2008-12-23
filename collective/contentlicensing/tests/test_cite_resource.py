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

