Feature: Settings functionality
  As a user
  I want to access Edge browser settings
  So that I can configure my browser preferences

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56498591
  @regression @p0 @settings
  Scenario: Open settings page
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I select "Settings" button from the dropdown menu
    Then the settings page should be opened
    When I open a new tab by clicking the "New Tab" button
    And I input "edge://settings" to the address bar
    Then the settings page should be opened

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56498771
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

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511459
  @regression @p0 @settings
  Scenario: Change to dark successfully
    Given Edge is launched
    And I input "edge://settings/appearance" to the address bar
    Given the theme is set to "Light" Mode
    When I click the "Dark" theme option
    Then Edge should change to dark Mode
    Given the theme is currently set to "Dark" Mode
    When I click the "Light" theme option
    Then Edge should change to light Mode
    Given the theme is currently set to "Light" Mode
    When I click the "System" theme option
    Then Edge should change to system Mode
    And the settings page color should follow the system Mode

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511650
  @regression @p0 @settings
  Scenario: Restore previous session tabs
    Given Edge is launched
    And I input "edge://settings/startHomeNTP" to the address bar
    When I select the option "Open tabs from the previous session"
    Then the option should be selected successfully
    When I open multiple tabs
    And I close and restart Edge
    Then previously opened tabs should be restored automatically
