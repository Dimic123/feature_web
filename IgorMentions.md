Use python 3.11 (hitrejsi)
1.Web
RunTests  (only for web browsers) ---> requirements.txt
RunTestsMobile  ---> requirementsMobile.txt

Vsi testi v Web,Live  , v /Data txt files s seznami  ?! (ali json??)

Pipeline , parameters

Seleniu test za call API?


Output:
output.txt

Summary:
Sklop1: 100 PASS, 2 FAILED
...
prilepljen raw log.

Posiljanje reporta/output.txt -- teams kanal, smtp,...

Managiranje:
nekdo spreminja, dodaja samo urlje v txt file?
ce je treba dodatno funkcnioanlnoist, se pac napise posebni py.


2.Mobile
narediti VM za android?? ali lahko kar kot deploy

Razlicni sklopi: (glej wiki)


Selenium	Description
Base Site	Just check base site url
Checking header links	Check all header links one by one
Checking footer links	Check all footer links one by one
Login/logout	Login test as well as log out
Registration	enter wrong information format in registration (negative test)
Wizards	Check functionality of all wizards one by one
Redirects	Check all redirects by entering url in browser and checking destination url
Comparison	Compare two products and go to comparison page
Favorites	Add products to favorites and then remove them
Basket	Add product to basket
Social links	Check all social links (Social login and social links)
Recipe	Check functionality of Recipe wizard
Forms	submit a form
Newsletter	Subscribe to newsletter
Product filters	Checking product filters depending on category