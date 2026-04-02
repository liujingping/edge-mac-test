Feature: Favorites functionality in Microsoft Edge

  # Demo: Basic favorites operations
  @demo @favorites
  Scenario: Add a website to favorites using the star icon
    Given Edge is launched
    When I navigate to "https://www.bing.com"
    And I click the "Add this page to favorites (Cmd+D)" button in the address bar
    And I click "Done" button in the favorite added dialog
    Then the favorite added dialog should be closed
    When I press "alt+cmd+B" to open Favorite hub
    And I click "Favorites bar" folder in hub
    Then "Search - Microsoft Bing" should appear in Favorites Bar

  @demo @favorites
  Scenario: Open favorites hub from toolbar
    Given Edge is launched
    When I click Favorites button on toolbar
    Then the Favorites hub is opened
    And Favorites bar and Other favorites show on Favorites hub

  @demo @favorites
  Scenario: Search favorites in Favorites hub
    Given Edge is launched
    When I navigate to "https://www.youtube.com/"
    And I click "Favorites" button in the toolbar
    And I click the "More options" button in the favorites hub
    And I click the "Add this page to favorites" button in the more options menu
    And I press Enter key
    And I click the "Search favorites" button in Favorites hub
    And I enter "Youtube" into the search box
    Then the "Youtube" website should be displayed in search results of Favorites hub
