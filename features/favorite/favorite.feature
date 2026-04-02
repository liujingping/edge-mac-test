Feature: favorite

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44656412
  @P0 @Regression @Favorites
  Scenario: Add a website to favorites using the star icon
    Given Edge is launched
    When I navigate to "https://www.bing.com"
    And I click the "Add this page to favorites (Cmd+D)" button in the address bar
    And I click "Done" button in the favorite added dialog
    Then the favorite added dialog should be closed
    When I press "alt+cmd+B" to open Favorite hub
    And I click "Favorites bar" folder in hub
    Then "Search - Microsoft Bing" should appear in Favorites Bar

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44525015
  @P0 @Regression @Favorites
  Scenario: Open favorites hub from toolbar
    Given Edge is launched
    When I click Favorites button on toolbar
    Then the Favorites hub is opened
    And Favorites bar and Other favorites show on Favorites hub

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44692789
  @P0 @Regression @Favorites
  Scenario: Add a folder to Favorites by clicking the Add button of hub
    Given Edge is launched
    And I click the Favorites button on the toolbar
    And I click "Add folder" button in Favorites hub
    When I press Enter key
    Then the "New folder" folder should be added to Favorites hub

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/44656489
  @P0 @Regression @Favorites
  Scenario: Open favorite item in current tab
    Given Edge is launched
    When I navigate to "https://www.wikipedia.org"
    And I click the "Add this page to favorites (Cmd+D)" button in the address bar
    And I press Enter key
    And I open a new tab
    And I open Favorites hub
    Then the Favorites hub is opened
    When I click "Favorites bar" folder in hub
    And I click the "https://www.wikipedia.org" item in Favorites hub
    Then the "https://www.wikipedia.org" should be opened in current tab

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/45837578
  @P0 @Regression @Favorites
  Scenario: Add a webpage to Favorites by clicking the Add button of hub
    Given Edge is launched
    When I navigate to "https://www.wikipedia.org"
    And I open Favorites hub
    And I click "Add this page to favorites" button in Favorites hub
    When I press Enter key
    Then the current webpage should be added to Favorites with the default name
