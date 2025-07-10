Feature: favorite

Scenario: Add a website to favorites using the star icon
 Given Edge is launched
 When I navigate to "https://www.microsoft.com"
 And I click the "Add this page to favorites" icon in the address bar
 And I click "Done" button in the favorites dialog
 When I Press "alt+cmd+B" to open Favorite bar
 Then "Microsoft" should appear in my favorites list
	