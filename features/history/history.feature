Feature: History functionality in Microsoft Edge

  Scenario: Click "X" to delete the browsing history
    Given Edge is launched
    When I navigate to "https://www.cgtn.com"
    Then the "cgtn" website should be opnened
    When I click "Settings and more" button in toolbar
    And I click "History" button
    And I hover over the "cgtn" website in History panel
    And I click "Delete" button in History panel
    Then the "cgtn" website should not be displayed in History panel

  Scenario: Set the History button show in toolbar
    Given Edge is launched
    When I click "Settings and more" button in toolbar
    And I right click "History" button in menu
    And I click "Show in toolbar" in menu
    Then "History" should be displayed in toolbar

  Scenario: Search words in history panel
    Given Edge is launched
    When I navigate to "https://www.cgtn.com"
    Then the "cgtn" website should be opnened
    When I click "Settings and more" button in toolbar
    And I click "History" button
    And I input "cgtn" in Search history box
    Then the "cgtn" website should be displayed in History panel
    When I input "mscaaa" in Search history box
    Then shows "No results found for 'mscaaa'" in history panel
