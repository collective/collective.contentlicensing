from zope.interface import Interface
from zope.schema import TextLine
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

class IATTopic(Interface):
    pass

class IPortalObject(Interface):
    pass

class IContentLicensingLayer(IDefaultBrowserLayer):
    """ A layer specific to this product
    """
