Feature: favorite

    Scenario: Add a website to favorites using the star icon
        Given Edge is launched
        When I navigate to "https://www.microsoft.com"
        And I click the "Add this page to favorites" icon in the address bar
        And I click "Done" button in the favorites dialog
        When I Press "alt+cmd+B" to open Favorite bar
        Then "Microsoft" should appear in my favorites list


    #https://microsoft.visualstudio.com/Edge/_workitems/edit/44525015
    @P0 @Regression
    Scenario: Open favorites hub from toolbar
        Given Edge is launched
        When I navigate to "edge://settings/appearance/toolbar"
        And I turn on Favorites button
        Then the Favorites button is displayed on the toolbar
        When I click Favorites button on toolbar
        Then the Favorites hub is opened
        And Favorites bar and Other favorites show on Favorites hub

    #https://microsoft.visualstudio.com/Edge/_workitems/edit/44692789
    @P0 @Regression
    Scenario: Add a folder to Favorites by clicking the Add button of hub
        Given Edge is launched
        And I click the Favorites button on the toolbar
        And I click "Add folder" button in Favorites hub
        When I press Enter key
        Then the "New folder" folder should be added to Favorites hub

    #https://microsoft.visualstudio.com/Edge/_workitems/edit/44656489
    Scenario: Open favorites page
        Given Edge is launched
        And the webpage "https://www.wikipedia.org" is added to Favorites
        When I open Favorites hub
        Then the Favorites hub is opened
        And I click the "https://www.wikipedia.org" item in Favorites hub
        Then the webpage should be opened in current tab