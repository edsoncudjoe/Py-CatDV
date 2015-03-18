# Py-CatDV
Python wrapper for the CatDV Server API 

CatDVlib.py
-----------
This library acts as a wrapper for CatDV's Server API. It was designed to 
quickly download information from the server and acts as a replacement to
manually exporting data from the CatDV GUI.

To use you would have to first set the URL of the location of the CatDV
server. This could possibly be 'localhost:8080' if the server is installed 
on your local machine.

Once the URL is set you can then login to the server to get access to the
stored clips and catalog information.

example:

	from CatDVlib import Cdvlib

	user = Cdvlib()

	url = user.setUrl() # Sets the location of the CatDV Server API

	# Stores the login session key once the user has logged in
	key = user.getSessionKey()   

	# Get clips of any given catalog.
	clips = user.getCatalogClips(user.catalog_names[0][1])

The Latest Version
------------------

	1.0.0 Initial Build
	
You need to have the Requests python library installed for this to work.
