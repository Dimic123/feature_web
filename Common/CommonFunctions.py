def expectedPageTitle(titlexp, expectedTitle):
	if  titlexp.lower() == expectedTitle:
		print("PASSED - Page title is as expected: \"" + expectedTitle + "\"")
	else:
		print("FAILED - Expected page title was \"" + expectedTitle + "\", but actual title is: \"" + titlexp + "\"")
	
	
