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

    def testRecursive(self):
        self.setRoles(['Manager'])
        # Create a folder
        self.portal.invokeFactory('Folder','folder1')
        folder1 = getattr(self.portal,'folder1')
        folder1.setTitle('Test Folder 01')
        # Create a document
        folder1.invokeFactory('Document','doc1')
        doc1 = getattr(folder1,'doc1')
        doc1.setTitle('Test Document 01')
        doc1.setCreators('Piotr Tchaikovsky\nWinter Daydreams\nLon Pathetique\nGuido Van Rossum')
        doc1.setText('lorem ipsum blah blah blah')
        # Create an image
        folder1.invokeFactory('Image','img1')
        img1 = getattr(folder1,'img1')
        img1.setTitle('Test Image 01')
        # Get GNU License and stuff it in the Request object
        gnu_license = self.props.getProperty('license_gnuFree')
        folder1.REQUEST['license'] = gnu_license[0]
        folder1.REQUEST['license_cc_name'] = gnu_license[1]
        folder1.REQUEST['recurse_cc_url'] = gnu_license[2]
        folder1.REQUEST['recurse_cc_button'] = gnu_license[3]
        folder1.REQUEST['recurse_folders'] = True
        # Fire off the request
        notify(ObjectModifiedEvent(folder1))
        # Check that it worked
        self.assertEqual(self.clutil.getLicenseAndHolderFromObject(folder1)[1][0],
                         'GNU Free Documentation License')
        self.assertEqual(self.clutil.getLicenseAndHolderFromObject(folder1)[1],
                         self.clutil.getLicenseAndHolderFromObject(doc1)[1])
        self.assertEqual(self.clutil.getLicenseAndHolderFromObject(folder1)[1],
                         self.clutil.getLicenseAndHolderFromObject(img1)[1])
        # Get all rights reserved license and stuff it in the request
        ar_license = self.props.getProperty('license_allRights')
        req = {}
        for x in folder1.REQUEST.keys():
            if x != 'recurse_folders':
                req[x] = folder1.REQUEST[x]
        folder1.REQUEST = req
        folder1.REQUEST['crazy_parameter'] = True
        # Fire off the request without the recurse option set
        notify(ObjectModifiedEvent(folder1))
        # Check that the doc and image have not changed
        self.assertEqual(self.clutil.getLicenseAndHolderFromObject(doc1)[1][0],
                         'GNU Free Documentation License')
        self.assertEqual(self.clutil.getLicenseAndHolderFromObject(img1)[1][0],
                         'GNU Free Documentation License')


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestContentLicensing))
    return suite

