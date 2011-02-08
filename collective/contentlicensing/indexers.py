from plone.indexer import indexer
from collective.contentlicensing.DublinCoreExtensions.interfaces import ILicensable, ILicense

@indexer(ILicensable)
def getCopyrightHolder(object):
    lic = ILicense(object)
    return lic.holder

@indexer(ILicensable)
def getCopyrightLicense(object):
    lic = ILicense(object)
    return lic.license
