Feature: favorite

Scenario: Add a website to favorites using the star icon
 Given Edge is launched
 When I navigate to "https://www.microsoft.com"
 And I click the "Add this page to favorites" icon in the address bar
 And I click "Done" button in the favorites dialog
 When I Press "alt+cmd+B" to open Favorite bar
 Then "Microsoft" should appear in my favorites list


Scenario: Delete an item in Favorites hub
Given Edge is launched
When I navigate to "https://www.github.com"
And I click the "Add this page to favorites" icon in the address bar
And I click "Done" button in the favorites dialog
And I click "Favorites" to open Favorite pane
When I right click on the "https://www.github.com" website in Favorites hub
And I click "Delete" button in the drop-down menu
Then "github" should disappear in my favorites list