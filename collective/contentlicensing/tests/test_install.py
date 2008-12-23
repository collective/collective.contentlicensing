from Products.CMFPlone.tests import PloneTestCase
from unittest import TestSuite, makeSuite
from Testing import ZopeTestCase
from Testing.ZopeTestCase import user_name
from AccessControl import Unauthorized
from collective.contentlicensing.DublinCoreExtensions.interfaces import ILicensable, ILicense
from base import ContentLicensingTestCase
from zope.component import getUtility
from collective.contentlicensing.utilities.interfaces import IContentLicensingUtility

class TestContentLicensing(ContentLicensingTestCase):

    def afterSetUp(self):
        self.clutil = getUtility(IContentLicensingUtility)
        self.props = self.portal.portal_properties.content_licensing_properties

    def testContentLicensingInstall(self):
        # Test that there are 5 default licenses
        self.assertEqual(len(self.clutil.getLicenses(self.portal)), 5)

    def testFrontPage(self):
        frontpage = self.portal.restrictedTraverse('front-page')
        # Test that the front page is licensable
        self.failUnless(self.clutil.isLicensable(frontpage))
        # Test the default ByLine
        byline = self.clutil.getSiteDefaultLicenseByLine(frontpage)
        self.assertEqual(len(byline), 5)
        # Test that the front page has CC RDF when set to CC License
        
        # Test this with a functional test instead
        #temp_license = self.props.getProperty('license_cc')
        #self.clutil.manage_changeProperties(DefaultSiteLicense=temp_license)
        #self.failUnless('<license' in frontpage.view())
    
    def testGettingAndSettingLicenses(self):
        # Create a default document object
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Folder','test-folder')
        self.folder = getattr(self.portal,'test-folder')
        self.folder.invokeFactory('Document', 'testDoc')
        test_doc = self.folder.testDoc

        # Check that the default license for the document is 'Site Default'
        self.assertEqual(self.clutil.getLicenseAndHolderFromObject(test_doc)[1][0],
                         'Site Default')
        # Test setting the license to other
        other_license = ['Other', 'MyLicense', 'None', 'None']
        self.clutil.setRightsLicense(test_doc, other_license)
        self.assertEqual(self.clutil.getLicenseAndHolderFromObject(test_doc)[1][0],
                         'Other')
        # Test setting the rights holder
        self.clutil.setRightsHolder(test_doc, 'David Ray')
        self.assertEqual(self.clutil.getLicenseAndHolderFromObject(test_doc)[0],
                         'David Ray')

def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestContentLicensing))
    return suite

