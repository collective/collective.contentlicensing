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

__author__  = '''Brent Lambert, David Ray, Jon Thomas'''
__docformat__ = 'plaintext'
__version__   = '$ Revision 0.0 $'[11:-2]


"""
The following is based on code found in the Plone OpenPlans
application, which is licensed under GNU General Public License. 
Kudos to those folk who have figured out how
to make Zope 3 annotations work in a Zope 2 world!
"""

from Products.Archetypes.BaseObject import BaseObject
from zope.lifecycleevent import ObjectModifiedEvent
from zope.event import notify


def notifyObjectModified(obj):
    notify(ObjectModifiedEvent(obj))

def addDispatcherToMethod(func, dispatch):
    def new_func(*args, **kwargs):
        obj = args[0]
        value = func(*args, **kwargs)
        dispatch(obj)
        return value
    return new_func


BaseObject._processForm = addDispatcherToMethod(BaseObject._processForm,
                                                notifyObjectModified)

BaseObject.update = addDispatcherToMethod(BaseObject.update,
                                          notifyObjectModified)

BaseObject.edit = BaseObject.update
