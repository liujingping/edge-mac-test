Feature: favorite

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44656412
  @P0 @Regression
  Scenario: Add a website to favorites using the star icon
    Given Edge is launched
    When I click on search bar
    And I enter "https://www.bing.com" in the search bar
    And I press Enter key
    And I click the "Add this page to favorites(⌘D)" button in the address bar
    And I click "Done" button in the favorites dialog
    When I Press "alt+cmd+B" to open Favorite bar
    Then "Search - Microsoft Bing" should appear in my favorites list

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44525015
  @P0 @Regression
  Scenario: Open favorites hub from toolbar
    Given Edge is launched
    When I navigate to "edge://settings/appearance/toolbar"
    And I turn on Favorites button
    Then the Favorites button is displayed on the toolbar
    When I click Favorites button on toolbar
    Then the Favorites hub is opened
    And Favorites bar and Other favorites show on Favorites hub

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44692789
  @P0 @Regression
  Scenario: Add a folder to Favorites by clicking the Add button of hub
    Given Edge is launched
    And I click the Favorites button on the toolbar
    And I click "Add folder" button in Favorites hub
    When I press Enter key
    Then the "New folder" folder should be added to Favorites hub

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44656489
  @P0 @Regression
  Scenario: Open favorites page
    Given Edge is launched
    And the webpage "https://www.wikipedia.org" is added to Favorites
    When I open Favorites hub
    Then the Favorites hub is opened
    And I click the "https://www.wikipedia.org" item in Favorites hub
    Then the webpage should be opened in current tab

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/45837578
  @P0 @Regression
  Scenario: Add a webpage to Favorites by clicking the Add button of hub
    Given Edge is launched
    When I navigate to "https://www.wikipedia.org"
    And I open Favorites hub
    And I click "Add this page to favorites" button in Favorites hub
    When I press Enter key
    Then the current webpage should be added to Favorites with the default name

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44656560
  @P0 @Regression
  Scenario: Open favorites in a new tab
    Given Edge is launched
    When I navigate to "https://www.youtube.com/"
    And I click the "Favorites" button in the toolbar
    And I click the "More options" button in the favorites hub
    And I click the "Add this page to favorites" button in the more options menu
    And I press the Enter key
    Then the "YouTube" should be added to Favorites hub
    When I right-click on "https://www.youtube.com/" in Favorites hub
    And I click "Open in new tab" in the context menu
    Then the YouTube page should be opened in a new tab

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44763909
  @P0 @Regression
  Scenario: Close favorites pane
    Given Edge is launched
    When I click the "Favorites" button in the toolbar
    And I click the "Pin favorites" button in the favorites pane
    And I click the "Close favorites" button in the favorites pane
    Then the favorites pane should be closed
