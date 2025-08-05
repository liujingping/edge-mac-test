Feature: favorite

  Background:
    Given Edge is launched

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44656412
  @P0 @Regression @Favorites
  Scenario: Add a website to favorites using the star icon
    When I navigate to "https://www.bing.com"
    And I click the "Add this page to favorites(⌘D)" button in the address bar
    And I click "Done" button in the favorite added dialog
    Then the favorite added dialog should be closed
    When I Press "alt+cmd+B" to open Favorite hub
    Then "Search - Microsoft Bing" should appear in Favorites Bar

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44525015
  @P0 @Regression @Favorites
  Scenario: Open favorites hub from toolbar
    When I navigate to "edge://settings/appearance/toolbar"
    And I click on "Favorites" button in Settings page
    Then the Favorites button is displayed on the toolbar
    When I click Favorites button on toolbar
    Then the Favorites hub is opened
    And Favorites bar and Other favorites show on Favorites hub

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44692789
  @P0 @Regression @Favorites
  Scenario: Add a folder to Favorites by clicking the Add button of hub
    And I click the Favorites button on the toolbar
    And I click "Add folder" button in Favorites hub
    When I press Enter key
    Then the "New folder" folder should be added to Favorites hub

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44656489
  @P0 @Regression @Favorites
  Scenario: Open favorite item in current tab
    And the webpage "https://www.wikipedia.org" is added to Favorites
    When I open Favorites hub
    Then the Favorites hub is opened
    And I click the "https://www.wikipedia.org" item in Favorites hub
    Then the "https://www.wikipedia.org" should be opened in current tab

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/45837578
  @P0 @Regression @Favorites
  Scenario: Add a webpage to Favorites by clicking the Add button of hub
    When I navigate to "https://www.wikipedia.org"
    And I open Favorites hub
    And I click "Add this page to favorites" button in Favorites hub
    When I press Enter key
    Then the current webpage should be added to Favorites with the default name

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44763909
  @P0 @Regression @Favorites
  Scenario: Close Favorites pane
    When I click the "Favorites" button in the toolbar
    And I click the "Pin favorites" button in the favorites pane
    And I click the "Close favorites" button in the favorites pane
    Then the favorites pane should be closed

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/45697813
  @P0 @Regression @Favorites
  Scenario: Show and hide favorites bar
    When I press "Shift+cmd+B" to toggle Favorites bar
    Then Favorites bar should not be shown below the address bar
    When I press "Shift+cmd+B" to toggle Favorites bar again
    Then Favorites bar should be shown below the address bar

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44745292
  @P0 @Regression @Favorites
  Scenario: Search favorites item in Favorites hub
    And The "https://www.youtube.com" is added to Favorites
    When I open Favorites hub
    And I click the "Search favorites" button in Favorites hub
    And I enter "Youtube" into the search box
    Then the "Youtube" website should be displayed in search results of Favorites hub

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44780350
  @P0 @Regression @Favorites
  Scenario: Drag a favorites item from "Favorites bar" to "Other favorites"
    And I added "https://www.youtube.com" to "Favorites bar"
    When I open Favorites hub
    And I drag the "https://www.youtube.com" item from "Favorites bar" to "Other favorites"
    Then the "https://www.youtube.com" should be displayed in "Other favorites"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44656560
  @P0 @Regression @Favorites
  Scenario: Open a favorites item in a new tab when right-clicking on it in Favorites hub
    When I navigate to "https://www.youtube.com/"
    And I click "Favorites" button in the toolbar
    And I click the "More options" button in the favorites hub
    And I click the "Add this page to favorites" button in the more options menu
    And I press Enter key
    Then the "Youtube" website should be added to Favorites hub
    When I right-click on "https://www.youtube.com/" in "Favorites bar"
    And I click "Open in new tab" button in the context menu
    Then the "Youtube" website should be opened in a new tab

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/58466995
  @P0 @Regression @Favorites
  Scenario: Delete a favorite item from favorites bar
    And the "https://www.youtube.com" website is added to Favorites
    When I right-click on "https://www.youtube.com/" in Favorites bar
    And I click "Delete" button in the menu
    And I open Favorites hub
    And I click the "Search favorites" button in Favorites hub
    And I enter "Youtube" into the search box
    Then the "No results found" message should be displayed in Favorites hub

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44656862
  @P0 @Regression @Favorites
  Scenario: Edit an item name on Favorites bar
    And the website "https://www.bing.com" is added to Favorites bar
    When I right-click on "https://www.bing.com" in Favorites bar
    And I click "Edit" button in the drop-down menu
    Then the "Edit favorite" dialog should be opened
    When I clear the name field in "Edit favorite" dialog
    And I type "bingbing" into name field of "Edit favorite" dialog
    And I press Enter key
    Then the "bingbing" website name should be shown in Favorites bar

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/58593955
  @P0 @Regression @Favorites
  Scenario: Remove a website by clicking the star icon
    And the website "https://www.bing.com" is added to Favorites bar
    When I click the "https://www.bing.com" in Favorites bar
    And I click the "Edit favorite for this page(⌘D)" button in the address bar
    And I click "Remove" button in Edit favorite dialog
    Then the Edit favorite dialog should be closed
    When I open Favorites hub
    And "Search - Microsoft Bing" should not be shown in Favorites Bar

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44692423
  @P0 @Regression @Favorites
  Scenario: Copy link in Favorites hub
    And the website "https://www.bing.com" is added to Favorites bar
    When I open Favorites hub
    And I right-click on "https://www.bing.com" in Favorites bar of hub
    And I click "Copy link" button in the drop-down menu
    And I open a new tab
    And I press "Cmd+V" to paste the copied link in the address bar
    And I press Enter key
    Then the "https://www.bing.com" website should be opened in the new tab

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44779506
  @P0 @Regression @Favorites
  Scenario: Open a folder with 3 items in new window
    And the websites "https://www.bing.com", "https://www.youtube.com", and "https://www.wikipedia.org" are added to Favorites bar
    When I open Favorites hub
    And I right-click on "Favorites bar" folder in hub
    And I click "Open all(3) in new window" button in the drop-down menu
    Then the "https://www.bing.com" website should be opened in the new window
    And the "https://www.youtube.com" website should be opened in the new window
    And the "https://www.wikipedia.org" website should be opened in the new window

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/53826024
  @P0 @Regression @Favorites
  Scenario: Favorites sort by custom
    And the websites "https://www.bing.com", "https://www.youtube.com", and "https://www.wikipedia.org" are added to Favorites bar
    When I open Favorites hub
    And I click on "Sort favorites" button in Favorites hub
    And I select "Custom" from the drop-down menu
    Then the "https://www.bing.com" website should be displayed first
    And the "https://www.youtube.com" website should be displayed second
    And the "https://www.wikipedia.org" website should be displayed third

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/53826034
  @P0 @Regression @Favorites
  Scenario: Favorites sort by A to Z
    And the websites "https://www.youtube.com", "https://www.bing.com" are added to Favorites bar
    When I open Favorites hub
    And I click on "Sort favorites" button in Favorites hub
    And I select "A to Z" from the drop-down menu
    Then the "https://www.bing.com" website should be displayed first
    And the "https://www.youtube.com" website should be displayed second
