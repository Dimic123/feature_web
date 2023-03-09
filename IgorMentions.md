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



| **Selenium test** | **ID** |	**AssocID** | **Technical Assumption(s) and/or Customer Need(s)** |	**Functional Requirement** | **Overal Status** (Completed, Testing) | **Testing STATUS** (Passed, Failed, Passed with comments) | **Comment** |
| ----------- | ----------- | ----------- | ---------- | ------------------------- | ---------- | ---------- | -------- |
| Yes |	001 |	UC-SF-001 |	Storefront and backend systems availability (reachable through browser) | Check all storefronts and all backend sites after version upgrade to ensure everything is up and running. | 	| |
| Yes |	002 | UC-SF-002	| Registration process |	Go through registration process on storefronts for Gorenje, ASKO and ATAG website. <br> • After registration form submission confirming also subscription to the newsletter 2 pop-up windows with the message “thank you” and “check your email for email confirmation” appear <br> • Email with the link to confirm registration  <br> • After confirming the registration within the email the user is redirected to the homepage with “thank you” pop-up window. <br> • If the registration link in the email is not confirmed within 30 minutes period, the user is redirected to the homepage with pop-up message that the registration toke has inspired  |  |  |
| No | 003 |	UC-SF-002/1 |	Registration process via Social providers (Facebook, ASKO, Atag) |	Go through social registration (Facebook, ASKO, ATAG) process on storefronts for Gorenje, ASKO and ATAG website |	 |	 |
| Yes |	004 |	UC-SF-003 |	Login/logout process |	Go through login process on storefronts for Gorenje, ASKO and ATAG website |	 |	 |
| No |	005 |	UC-SF-003/1 |	Social login process |	Go through social login (Facebook, ASKO, ATAG) process on storefronts for Gorenje, ASKO and ATAG website |	 |	 |
| No |	006 |	UC-SF-004 |	Checkout process |	Go through checkout process with at least one product on all brands (Gorenje,ASKO,ATAG) |	 |  |
| Yes |	007 |	UC-SF-005 |	Search functionality for: Recipes, FAQ's, Products, Promo Data, Manuals |	Test search functionality for the following Recipes, FAQ's, Products, Promo Data and Manuals |	 |	 |
| No |	008 |	UC-SF-006 | 	Functionalities in the scope of the Selfcare portal |	editing user information |	  |	 |
|    | 009 |	UC-SF-007 | | adding products/recipes/comparison to favorites |	 |  |
|    | 010 |	UC-SF-008 | | orders, creation of the warranty claim |	 |  | 
|    | 011 |	UC-SF-009 | | subscribe/unsubscribe functionality and communication with Mailchimp |  |  |
|    | 012 |	UC-SF-010 | | Newsletter subscription / as guest |  | |
|    | 013 |	UC-SF-011 | | Managing recipes (Sending the ingredients list to the email) |  |  |
| No | 014 |	UC-SF-012 | Dealer Locator | Check dealer locator functionality on storefronts: Check locator marks for content and accuracy, Test dealer locator search |  | |
| Yes |	015 |	UC-SF-013 | Wizards |	Go through all wizard user journeys and check content, translations and functionality (Washing, Drying, Recipes, Storing Food, Refresh space) |	 | |
| Yes |	016 |	UC-SF-014 |	Advanced filters configuration |	Go through all filters on the left hand side of the product category page | |	 |
| No |	017 |	UC-SF-015 |	Bundles	| Check if bundles are displaying correctly |	 | |
| No |	018 |	UC-SF-016 |	PDP advanced settings for products and bundles |  |		 ||
| No |	019 |	UC-SF-017 |	Advanced localization	|  | |	 |
| Yes |	020 |	UC-SF-018 |	General behavior of the storefronts |	Test out user journey's and all sorts of clicks of all type (links, buttons, pictures, …). Check animations and general usability/performance of storefronts |	 |  |
| No |	021 |	UC-CC-001 |	General behavior of the backend system	| Check responsiveness, user permissions and general behaviour and speed | |	 |
| No |	022 |	UC-CC-002 |	Editors use cases scenarios |	Edit an existing content page/ category page/ product detail page in a brand content catalog (staged version)  | |  |
| No |	023 |	UC-CC-003 | |		Create a new content page and add various component |  	 | |
| No |	024 |	UC-CC-004 | |		Create a category page and restrict to a category   |	 |	 |
| No |	025 |	UC-CC-005 | |		Create a non-default product details page and restrict to a category |  | |
| No |	026 |	UC-CC-006 | |		Add localized content to components of a page (localized versions of a page)  | 	 | |
| No |	027 |	UC-CC-007 | |		Create breadcrumbs for Gorenje content pages (landing pages) |   | |
| No |	028 |	UC-CC-008 | |		Create forms |  |	 |
| No |	029 |	UC-CC-009 | |		Restrict the display of a page to a/several basestore |  |	 |
| No |	030 |	UC-CC-010 | |		Restrict the display of a component used on a page shared among websites to a basestore |   | |
| No |	031 |	UC-CC-011 | |	Create navigation menu restricted to a basestore | | |
| No |	032 |	UC-CC-012 | |		Create footer restricted to a basestore  | | |
| |	033 |	UC-CC-013 | |		Editing a navigation | 	 | |
| |	034 |	UC-CC-014 | |		Editing a footer | 	 | |
| |	035 |	UC-CC-015 | |		Sync the changes made on existing content page/ category page/ product detail page |	 |	 |
| |	036 |	UC-CC-016 | |		Page preview |	 |	 |
| No |	037 |	UC-CC-017 | |		Sync a component/ a page / a content catalog | 	 |	 |
| No |	038 |	UC-CC-018 |	Gorenje & Asko general usecases	| **Gorenje catalog staged version**  <br> • Search a page by page ID or name (example: page name Akcije Darilo ob nakupu MGA) <br> • Open the searched page  <br> • Edit breadcrumbs (GGBreadcrumbBuilderComponent = Breadcrumb Builder Component) <br> • Change the Main Banner component (GGMainIntroSliderComponent = . MainBanner)  <br> • Edit text in the box and add link to the banner Turquoise Box (GGTurquoiseTransparentBoxComponent = TransparentBoxComponent) <br> • Add additional banner to the main banner component (GGMainIntroSliderItemComponent = Main Banner Item)  <br> • Edit Navigation  <br> • Edit Footer   |	 |	 |
| No |	039 |	UC-CC-019 |	| **Asko content catalog staged version**  <br> • Create a new default content page shared among websites (localized content to be added) inserting all page elements (page name, page ID, page label, page title, page description = meta description, keywords – meta keywords, searchable status)  <br> • Add Main Banner component (GGMainIntroSliderComponent = . MainBanner)  <br> •  Add Colored Linked Paragraph Component (GGColouredSection)  <br> • Add Unfolded Section Item Component (UnfoldedSectionItemComponent)  <br> • Add Full Width In-Page Banner (GGVideoBannerComponent) with a video and a CMS basestore restriction to the component  |	 |	 |
| No |	040 |	UC-CC-020 |	Check user permission behavior |	• Check reading and editing with restricted user previously set and admin   <br> - Catalog (read, write - stg, online) <br> - Synchronization  <br> - Language (read, write) <br> - Site (read, write)<br> - Detailed type aware rights <br> - Detailed attribute aware rights <br>  - Login (enabled, disabled) <br> - Permissions set based on user group |	 |	 |
| No |	041 |	UC-CC-021 |	Check edit history |	Check history of editing |	 |	 |
| No |	042 |	UC-BO-001 |	General behavior of the backend system |	Check responsiveness, user permissions and general behavior and speed |	 |	 |
| No |	043 |	UC-BO-002 |	Checking permissons behavior |	•	Check different assignments of user rights on user and user group <br> - BO login (enable, disable) <br> - SE login (enable, disable) <br> - SE login, edit (enable, disable) <br> - Languages (readable, writable) <br> - Catalogs (read, write - stg, online) <br> - Synchronization <br> - User groups <br> - Detailed type aware rights <br> - Detailed attribute aware rights <br> - Personalization rules - restrictions <br> - Permissions set based on user group <br>•	Check reading and editing with restricted user previously set and admin <br> - Catalog (read, write - stg, online) <br> - Synchronization  <br> - Language (read, write) <br> - Site (read, write) <br> - Detailed type aware rights <br> - Detailed attribute aware rights <br> - Login (enabled, disabled) <br> - Permissions set based on user group |	 |	 |
| No |	044 |	UC-BO-003 |	Check edit history |	History of editing |	 |	 |
| No |	045 |	UC-BO-004 |	Check base functionalities of editing |	• Edit attribute, attribute values translations, units, colors <br> • Synchronization of catalogs an items <br> • Creating attribute groups and inserting translations <br> • Managing-setting views to attributes <br> • Creating rules / rule engine <br> • Creating brand translations <br> • (Creating summary)-not tested <br> • Adding a component to a content slot  <br> • Product export for particular market <br> • Generation of hex codes <br> • Impex, csv export |	 |	 |
| No |	046 |	UC-BO-005 |	Check additional features |	Check functionality and behavior of Adaptive search, Product cockpit, Commerce search, Data Hub	|  | |
| No |	047 |	UC-OT-001 |	OCC services | 	•Token <br> • Wizards <br> • Recipe  <br> • Menus <br> • FAQs <br> • Manuals <br> • SAPPI <br> • Styles <br> • Customers <br> • Wizards v2 <br> • General <br> • Profile <br> • Pairing |	 |	 |
| No |	048 |	UC-OT-002 |	Communication with DataHub | 	inbound (stock import/product import) and outbound (correct order transfer) |	 |	 |
| No |	049 |	UC-HC-001 |	General behavior of the backend system |	Check responsiveness, user permissions and general behavior and speed |	 |	 
| No |	050 |	UC-HC-002 |	Basic functionalities check |	Check property setting, scripting languages, impex import, flexible search |	 |	 |
| No |	051 |	UC-HC-003 |	Check permission behavior |	Check login with restricted and admin user |	 |	 |
| No |	052 |	UC-SM-001 |	General behavior of the backend system |	Check responsiveness, user permissions and general behaviour and speed |	 |	 |
| No |	053 |	UC-SM-002 |	Editors use cases scenarios |	Edit an existing content page/ category page/ product detail page in a brand content catalog (staged version)  |	 |	 |
| No |	054 |	UC-SM-003 | |		Create a new content page and add various component  |	 | |
| No |	055 |	UC-SM-004 | |		Create a category page and restrict to a category   |	|	 |
| No |	056 |	UC-SM-005 | |		Create a non-default product details page and restrict to a category |  	 |	 |
| No |	057 |	UC-SM-006 | |		Add localized content to components of a page (localized versions of a page)  | 	 |	 |
| No |	058 |	UC-SM-007 | |		Create breadcrumbs for Gorenje content pages (landing pages) | 	 |	 |
| No |	059 |	UC-SM-008 | |		Create forms  |	 |	|
| No |	060 |	UC-SM-009 | |		Restrict the display of a page to a/several basestore |	 | |
| No |	061 |	UC-SM-010 | |		Restrict the display of a component used on a page shared among websites to a basestore | 	 |	 |
| No |	062 |	UC-SM-011 | |		Create navigation menu restricted to a basestore |	 | |
| No |	063 |	UC-SM-012 | |		Create footer restricted to a basestore  |	 |	 |
| No |	064 |	UC-SM-013 | |		Sync a component/ a page / a content catalog | 	 |	 |
| No |	065 |	UC-SM-014 |	Gorenje & Asko general usecases |	<br> • Edit a page <br> • Gorenje catalog staged version  <br> • Search a page by page ID or name (example: page name Akcije Darilo ob nakupu MGA)  <br> • Open the searched page   <br> • Edit breadcrumbs (GGBreadcrumbBuilderComponent = Breadcrumb Builder Component)  <br> • Change the Main Banner component (GGMainIntroSliderComponent = . MainBanner)  <br> •Edit text in the box and add link to the banner Turquoise Box (GGTurquoiseTransparentBoxComponent = TransparentBoxComponent) <br> •Add additional banner to the main banner component (GGMainIntroSliderItemComponent = Main Banner Item)  <br> • Edit Navigation   <br> • Edit Footer  |	 |	 |
| No |	066 |	UC-SM-015 |	Create a new content page and add content (various localisations) | 	Asko content catalog staged version  <br> • Create a new default content page shared among websites (localized content to be added) inserting all page elements (page name, page ID, page label, page title, page description = meta description, keywords – meta keywords, searchable status)  <br> • Add Main Banner component (GGMainIntroSliderComponent = . MainBanner)  <br> • Add Colored Linked Paragraph Component (GGColouredSection)  <br> • Add Unfolded Section Item Component (UnfoldedSectionItemComponent)  <br> • Add Full Width In-Page Banner (GGVideoBannerComponent) with a video and a CMS basestore restriction to the component |  	 |	 |
| No |	067 |	UC-SM-016 |	Check permission behavior |	•	Check reading and editing with restricted user previously set and admin <br> • Catalog (read, write - stg, online) <br> • Synchronization  <br> • Language (read, write) <br> • Site (read, write) <br> • Detailed type aware rights <br> • Detailed attribute aware rights <br> • Login (enabled, disabled) <br> • Permissions set based on user group |		|  |
| No |	068 |	UC-SM-017 |	Check editing history | 	Check history of editing |





# 1. Testing Plan 

## 1.1 Registration process 

- Register new user and check in BO + confirmation email 

- Selenium test (negative test to check field specific limitations) 
---
## 1.2 Login  

- Login Page 

     - Selenium test 

     - Manual test 

- Social Login 
---
## 1.3 Checkout process 

- Go through entire user journey (Darja) 
---
## 1.4 Search for  

- Recipes (Selenium) 

- FAQ’s (Selenium) 

- Products (Selenium) 

- Promo Data 

- Manuals (Selenium) 
---
## 1.5 Functionalities in the scope of the Selfcare portal  

- editing user information (Zoran, Elizabeta, Darja) 

- adding products/recipes/comparison to favorites (Zoran, Elizabeta, Darja) 

- orders, creation of the warranty claim (Elizabeta, Darja) 

- subscribe/unsubscribe functionality and communication with Mailchimp (Zoran, Elizabeta, Darja) 
---
## 1.6 Appliance registration process 

- Go through entire user journey 

- Selenium test (negative test to check field specific limitations) 
---
## 1.7 Dealer locator (and advanced dealer locator for ATAG) 

- Go through entire user journey (Darja, Zoran) 
--- 
## 1.8 Wizards 

- Go through entire user journey 
---
## 1.9 Rule engine  

- Check functionality (Blanka) 
---
## 1.10 Views 

- Check functionality 
---
## 1.11 Advanced filters configuration 

- Check functionality 
---
## 1.12 Bundles 

- Check functionality 
---
## 1.13 PDP advanced settings for products and bundles 

- Check functionality 
---
## 1.14 Forms 

- Check functionality (Maja?, Elizabeta) 
---
## 1.15 Advanced localization 

- Check functionality 
---
## 1.16 OCC services -> Dejan   

- [ ] Token 
- [ ] Wizards 
- [ ] Recipe 
- [ ] Menus 
- [ ] FAQs 
- [ ] Manuals 
- [ ] SAPPI 
- [ ] Styles 
- [ ] Customers 
- [ ] Wizards v2 
- [ ] General 
---
## 1.17 Communication with DataHub (inbound (stock import/product import) and outbound (correct order transfer)) 

- Check functionality (Dejan) 
---
## 1.18 Editorial possibilities in BackOffice and CMSCockpit 

- At least one change on page or component (Elizabeta) 
- Sync of specific component, specific page and full sync (product, wizard, ..) (Elizabeta) 
---
## 1.19 General behavior of the storefronts (including editorial pages and components) 

- Run all Selenium tests on all storefronts 

- Manual check of all Storefronts: Correctly displayed components / design  

- Redirects 

- At least a few random menu clicks 

- At least a few random clicks of links  
    - [ ] contact, prizes 
    - [ ] employment 
    - [ ] warranty 
    - [ ] service 
    - [ ] help with purchase 
      - etc.  

- At least a few random clicks of follow us (Facebook, Instagram, Youtube):  

- At least a few random click of find a dealer  

- Language switcher 

- Search:  
    - [ ] some examples of products and search result page presented correctly 
    - [ ] filters and filtering on search result page, sorting on search result page  

- Subscribe to newsletter and check in BO 

- At least a random chat with chatbot 

- At least a few random PDP:  
    - [ ] Pictures 
    - [ ] Prices 
    - [ ] stocks (cart / send inquiry) 
    - [ ] opinions and ratings 
    - [ ] add to favorites 
    - [ ] badge 
    - [ ] technical details 
    - [ ] manuals 
    - [ ] similar products  

- At least a few random BUNDLE PDP:  
    - [ ] Pictures 
    - [ ] Prices 
    - [ ] stocks (cart / send inquiry) 
    - [ ] check other products in bundle  

- At least one test of every wizard:  
    - [ ] Washing laundry 
    - [ ] Tumble-dryer 
    - [ ] storing food 
    - [ ] refresh space 
    - [ ] dish washing 

- Recipes and at least one test configuration oven for recipe 

- 3 course diner 