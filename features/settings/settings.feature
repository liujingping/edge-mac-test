Feature: Settings functionality
    As a user
    I want to access Edge browser settings
    So that I can configure my browser preferences

@regression @p0 @settings
Scenario: Open settings page
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I select "Settings" button from the dropdown menu
    Then the settings page should be opened
    When I open a new tab by clicking the "New Tab" button
    And I navigate to "edge://settings"
    Then the settings page should be opened

@regression @p0 @settings
    Scenario: Search in settings search box
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I select "Settings" button from the dropdown menu
    Then the settings page should be opened
    When I input "Privacy" in the settings search box
    Then the search results should display relevant settings related to "Privacy"
    When I clear the search box
    Then the search results should reset to show all settings
    When I input "123" in the settings search box
    Then the search results should display "No search results found"