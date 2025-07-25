Feature: favorite

  Background:
    Given I launch Edge with empty user data directory
    And I open a new tab

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
    And the Favorites button is hidden on the toolbar
    When I navigate to "edge://settings/appearance/toolbar"
    And I turn on Favorites button
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
