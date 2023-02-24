from Web.Live.CheckingSiteTitle import *
from Web.Live.LoginTest import *
import json

test_cases = {
	"case_1": {
		"site" : "https://si.gorenje.com/",
		"title" : "Gorenje | Domača Stran"
	},
	"case_2": {
		"site" : "https://si.gorenje.com/",
		"title" : "Gorenje | Veliki in mali gospodinjski aparati"
	}
}

login_values = {
	"usernamePath" : '/html/body/main/div[2]/div/div/div[2]/div/form/article/div/div[2]/div/div[1]/div[1]/div/div/input',
    "passwordPath" : '/html/body/main/div[2]/div/div/div[2]/div/form/article/div/div[2]/div/div[1]/div[2]/div[1]/div/input',
    "submitPath" : '/html/body/main/div[2]/div/div/div[2]/div/form/article/div/div[2]/div/div[2]/div/div[2]/button',
    "username" : "jedan70743@wireps.com",
    "password" : "gA5Z5KJxTLsb@u"
}

test_cases2 = {
	"case_1": {
		"site" : "https://si.gorenje.com/login",
		"values" : login_values
	}
}

def main():
	for case in test_cases:
		site = test_cases[case]["site"]
		title = test_cases[case]["title"]
		CheckingSiteTitle(site, title)
		print("Test case ", case, " passed")

	for case in test_cases2:
		site = test_cases2[case]["site"]
		values = test_cases2[case]["values"]
		LoginTest(site, values)
		print("Test case ", case, " passed")
	


if __name__ == "__main__":
	main()