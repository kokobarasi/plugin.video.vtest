# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Addon: First 
# Author: "Kokobarasi"

# -*- coding: utf-8 -*-
import sys, re, urllib, os
import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
 
line1 = "Hello World!"
line2 = "We can write anything we want here"
line3 = "Using Python"
 
xbmcgui.Dialog().ok(addonname, line1, line2, line3)        
