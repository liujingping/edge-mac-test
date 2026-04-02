Feature: History functionality in Microsoft Edge

  # Demo: Basic history operations
  @demo @history
  Scenario: Click "X" to delete the browsing history
    Given Edge is launched
    When I navigate to "https://www.cgtn.com"
    Then the "cgtn" website should be opened
    When I click "Settings and more" button in toolbar
    And I click "History" button
    And I hover over the "cgtn" website in History panel
    And I click "Delete" button in History panel
    Then the "cgtn" website should not be displayed in History panel

  @demo @history
  Scenario: Set the History button show in toolbar
    Given Edge is launched
    When I click "Settings and more" button in toolbar
    And I right click "History" button in menu
    And I click "Show in toolbar" in menu
    Then "History" should be displayed in toolbar