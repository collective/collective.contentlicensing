from base import prod, oflags, ContentLicensingFunctionalTestCase
from Testing.ZopeTestCase import FunctionalDocFileSuite
from unittest import TestSuite


def test_suite():
    suite = TestSuite()

    prefstest = FunctionalDocFileSuite('tests/prefs.txt',
                                       package=prod,
                                       test_class=ContentLicensingFunctionalTestCase,
                                       optionflags=oflags)
    prefstest = FunctionalDocFileSuite('tests/browse.txt',
                                       package=prod,
                                       test_class=ContentLicensingFunctionalTestCase,
                                       optionflags=oflags)
                                                         
    suite.addTests((prefstest,))

    return suite
