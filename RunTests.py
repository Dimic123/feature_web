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

def main():
	# for case in test_cases:
	# 	site = test_cases[case]["site"]
	# 	title = test_cases[case]["title"]
	# 	CheckingSiteTitle(site, title)

	LoginTest()


if __name__ == "__main__":
	main()