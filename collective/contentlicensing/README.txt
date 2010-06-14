Content Licensing Tool

 by the `Center for Open Sustainable Learning`_ at Utah State University.

  * "Center for Open Sustainable Learning":http://cosl.usu.edu

 This tool is used to manage copyright licenses within plone. It is a product built in response to `PLIP #136`_.

  * "PLIP #136":http://plone.org/products/plone/roadmap/136

Features

  * Configlet for setting default sitewide settings.

  * Citation hot link to the copyright byline.  Citation appears in full text for plain and print views.
  
  * Support for Creative Commons style RDF embedded in RSS feeds. Can use this feed in place of the standard default RSS feed shipped with Plone.

  * Support for jurisdiction setting, making it possible to choose a correct Creative Commons license based on your geographical location.

  * DublinCoreExtensions addon is now incorporated into the Content Licensing Product. 

  * Site wide defaults for Copyright, Copyright Holder, and Copyright License.

  * Custom settings for document, file and image objects.

  * Copyright Byline at the bottom of content object views.

  * RDF metadata and license info embedded in the view.

  * Support for search engine compatibility and content licensing.

  * Adds two Dublin Core metadata extensions to content objects.

  * Built using Zope annotations, with Zope 3 style configuration and views.

What's New

 * 

Installation

 Requires

  * Plone 3.0.0 and greater

  * Zope 2.10.4 and greater

 Buildout installation

  Using zc.buildout and the plone.recipe.zope2instance recipe to manage your project, you can do this:

  * Add ``collective.contentlicensing`` to the list of eggs to install, e.g.::
 
    [buildout]
    ...
    eggs =
        ...
        collective.contentlicensing
        
  * Tell the plone.recipe.zope2instance recipe to install a ZCML slug::
  
    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zcml =
        collective.contentlicensing
        
  * Re-run buildout, e.g. with::
  
    $ ./bin/buildout
        
 You can skip the ZCML slug if you are going to explicitly include the package from another package's configure.zcml file.


