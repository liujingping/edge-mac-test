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

  # skip
  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511459
  # @regression @p0 @settings
  # Scenario: Change to dark successfully
  # Given Edge is launched
  # And I input "edge://settings/appearance" to the address bar
  # Given the theme is set to "Light" Mode
  # When I click the "Dark" theme option
  # Then Edge should change to dark Mode
  # Given the theme is currently set to "Dark" Mode
  # When I click the "Light" theme option
  # Then Edge should change to light Mode
  # Given the theme is currently set to "Light" Mode
  # When I click the "System" theme option
  # Then Edge should change to system Mode
  # And the settings page color should follow the system Mode
  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511650
  # @regression @p0 @settings
  # Scenario: Restore previous session tabs
  # Given Edge is launched
  # And I navigate to "edge://settings/startHomeNTP"
  # When I select the option "Open tabs from the previous session"
  # Then the option should be selected successfully
  # When I new a tab navigate to "www.bing.com"
  # And I new a tab navigate to "www.google.com"
  # And I close and restart Edge
  # Then edge open with "edge://settings/startHomeNTP","www.bing.com" and "www.google.com"
  
  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511626
  @regression @p0 @settings
  Scenario: Restore by new tab
    Given Edge is launched
    And I input "edge://settings/startHomeNTP" to the address bar
    When I select the option "Open the new tab page"
    Then the option should be selected successfully
    When I new a tab
    And I navigate to "www.bing.com"
    And I close and restart Edge
    Then should open new tab page automatically

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511520
  @regression @p0 @settings
  Scenario: Show/hide home button
    Given Edge is launched
    And I input "edge://settings/appearance/toolbar" to the address bar
    When I click on "Home" button
    Then the option should be turned on successfully
    And the home button should be visible on the toolbar
    When I click on "Home" button again
    Then the option should be turned off successfully
    And the home button should be hidden on the toolbar

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56499157
  # @regression @p0 @settings
  # Scenario: Verify clear browsing data successfully
  # Given Edge is launched
  # And I have created a new profile
  # When I have navigated to "edge://settings/privacy" page
  # Then all text elements should display correctly
  # When I click the "Clear browsing data" button
  # Then the "Delete browsing data" dialog should be displayed
  # And all UI elements in the dialog should render properly
  
  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56612273
  @regression @p0 @settings
  Scenario: Cancel add custom site
    Given Edge is launched
    And I input "edge://settings/startHomeNTP" to the address bar
    When I select the option "Open custom sites"
    Then the option should be selected successfully
    When I click the "Add site" button
    Then the "Add site" dialog should be opened
    When I input "https://www.bing.com" in the URL field
    And I click the "Cancel" button
    Then the "Add site" dialog should be closed
