from zope.publisher.browser import BrowserView
from zope.component import getUtility
from collective.contentlicensing.utilities.interfaces import IContentLicensingUtility
from urlparse import urlsplit
from xml.dom import minidom
from Products.CMFPlone.utils import safe_unicode


class RDFMetadataView(BrowserView):
    """ Express Dublin Core As Rdf  """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.document = minidom.Document()
        self.props = self.context.portal_url.portal_properties.content_licensing_properties
        self.clutil = getUtility(IContentLicensingUtility)
        self.holder, self.license = self.clutil.getLicenseAndHolderFromObject(context)        
        if self.license and 'Site Default' == self.license[0]:
            self.license = self.props.DefaultSiteLicense

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/rdf+xml')
        return self.writeRDF()

    def writeRDF(self):
        """ Write RDF metadata """
        if 'Creative Commons License' == self.license[0]:
            data = self.getCCLicenseRDF()
        else:
            data = self.getRDFMetadata()
        # Remove the XML header
        index = data.find('\n')
        if (index > -1):
            data = data[index + 1:]
        return data

    def getRDFMetadata(self):
        """ Write metadata fields as RDF. """
        rdf_node = self._createNode(self.document, 'rdf:RDF',
                       attrs=[('xmlns:rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
                              ('xmlns:dc', 'http://purl.org/dc/elements/1.1/'),
                              ('xmlns:dcterms', 'http://purl.org/dc/terms')])
        desc_node = self._createNode(rdf_node, 'rdf:Description',
                        attrs=[('rdf:about', self.context.renderBase())])
        self._writeDCMetadata(desc_node)
        return self.document.toprettyxml()        
                                

    def getCCLicenseRDF(self):
        """ Write into RDF CC License elements. """

        holder, license = self.clutil.getLicenseAndHolderFromObject(self.context)
        licenseId = ''
        if len(self.license) >= 3:
            lid = urlsplit(self.license[2])
            if len(lid) >= 3:
                lid = lid[2].split('/')
                if len(lid) >= 3:
                    licenseId = lid[2]

        if licenseId and self.clutil.hasCCLicenseInfo(licenseId):
            cc_rdf = self.clutil.getCCLicenseInfo(licenseId)
        
            rdf_node = self._createNode(self.document, 'rdf:RDF',
                           attrs=[('xmlns', 'http://creativecommons.org/ns#'),
                                  ('xmlns:dc', 'http://purl.org.dc/elements/1.1/'),
                                  ('xmlns:rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')])
            work_node = self._createNode(rdf_node, 'Work', attrs=[('rdf:about',
                                                                   self.context.renderBase())])
            self._writeDCMetadata(work_node)
            self._createNode(work_node, 'license', attrs=[('rdf:resource', self.license[2])])
            return self.document.toprettyxml()
        else:
            return ''

    def _writeDCMetadata(self, node):
        """ Write the dublin core metadata in RDF. """

        # Identifier
        self._createNode(node, 'dc:identifier', self.context.renderBase())

        # Title
        self._createNode(node, 'dc:title', self.context.title )

        # Description
        desc = self.context.Description()
        if desc:
            self._createNode(node, 'dc:description', self.context.Description() )

        # Subject
        self._renderList(node, 'dc:subject', [sub for sub in self.context.Subject() ] )

        # Publisher
        self._createNode(node, 'dc:publisher', self.context.portal_url.getPortalObject().Publisher() )
        
        # Creators
        self._renderList(node, 'dc:creator', [creat for creat in self.context.Creators() ], True )

        # Contributors
        self._renderList(node, 'dc:contributor', [contrib for contrib in self.context.Contributors() ] )

        # Rights
        rights = self.context.Rights()
        if not rights:
            rights = self.props.DefaultSiteCopyright
        holder = self.props.DefaultSiteCopyrightHolder
        if self.context != self.context.portal_url.getPortalObject():
            result = self.clutil.getLicenseAndHolderFromObject(self.context)
            if result:
                if result[0] != '(site default)':
                    holder = license[0]            
        self._createNode(node, 'dc:rights', '%s, %s' % (rights, holder))

        # Language
        lang = self.context.Language()
        if not lang:
            po = self.context.portal_url.getPortalObject()
            lang = po.portal_properties.site_properties.getProperty('default_language')
        self._createNode(node, 'dc:language', lang )

        # Type
        self._createNode(node, 'dc:type', self.context.Type())

        # Format
        self._createNode(node, 'dc:format', self.context.Format())


    def _renderList(self, node, element, value, instflagstrip=False):
        """ Render a list of items in RDF. """
        if value:
            if len(value) > 1:
                value_node = self._createNode(node, element)
                bag_node = self._createNode(value_node, 'rdf:Bag')
                for x in value:
                    # If creator is marked as an institution and not a person
                    if instflagstrip and '@' == x[0]:
                        x = x[1:]
                    self._createNode(bag_node, 'rdf:li', x )
            else:
                self._createNode(node, element, value[0] )
        

    def _createNode(self, parent, ename, value=None, attrs=None):
        """ Create a node in the document. """
        newNode = self.document.createElement(ename)
        parent.appendChild(newNode)
        if value:
            newNode.appendChild(self.document.createTextNode(safe_unicode(value)))
        if attrs:
            for x in attrs:
                newNode.setAttribute(x[0], x[1] )
        return newNode

