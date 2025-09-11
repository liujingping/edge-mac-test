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
  # @regression @p0 @settings
  # Scenario: Search in settings search box
  #   Given Edge is launched
  #   When I click "Settings and more" button on toolbar
  #   And I select "Settings" button from the dropdown menu
  #   Then the settings page should be opened
  #   When I input "Privacy" in the settings search box
  #   Then the search results should display relevant settings related to "Privacy"
  #   When I clear the search box
  #   Then the search results should reset to show all settings
  #   When I input "123" in the settings search box
  #   Then the search results should display "No search results found"

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511650
  # @regression @p0 @settings
  # Scenario: Restore previous session tabs
  #   Given Edge is launched
  #   When I input "edge://settings/startHomeNTP" to the address bar
  #   And I select the option "Open tabs from the previous session"
  #   And I open a new tab
  #   And I navigate to "https://www.bing.com"
  #   And I close and restart Edge
  #   Then "edge://settings/startHomeNTP" website should be restored
  #   And "https://www.bing.com" website should be restored

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511626
  # @regression @p0 @settings
  # Scenario: Restore by new tab
  #   Given Edge is launched
  #   And I input "edge://settings/startHomeNTP" to the address bar
  #   When I select the option "Open the new tab page"
  #   And I open a new tab
  #   And I navigate to "https://www.bing.com"
  #   And I close and restart Edge
  #   Then edge should open with a page titled "New Tab"

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511520
  # @regression @p0 @settings
  # Scenario: Show/hide home button
  #   Given Edge is launched
  #   And I input "edge://settings/appearance/toolbar" to the address bar
  #   When I click on "Home" button on the settings page
  #   Then the home button should be visible on the toolbar
  #   When I click on "Home" button on the settings page
  #   Then the home button should be hidden on the toolbar

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56612273
  # @regression @p0 @settings
  # Scenario: Cancel add custom site
  #   Given Edge is launched
  #   And I input "edge://settings/startHomeNTP" to the address bar
  #   When I select the option "Open custom sites"
  #   And I click the "Add site" button
  #   Then the "Add site" dialog should be opened
  #   When I input "https://www.bing.com" in the URL field on the "Add site" dialog
  #   And I click the "Cancel" button on the "Add site" dialog
  #   Then the "Add site" dialog should be closed

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511529
  # @regression @p0 @settings
  # Scenario: Show/hide Split screen button
  #   Given Edge is launched
  #   And I input "edge://settings/appearance/toolbar" to the address bar
  #   When I click on "Split screen" button switch in Toolbar Settings page
  #   Then the Split screen button should be visible on the toolbar
  #   When I click on "Split screen" button switch in Toolbar Settings page
  #   Then the Split screen button should be hidden on the toolbar

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511558
  # @regression @p0 @settings
  # Scenario: Show/hide sidebar
  #   Given Edge is launched
  #   And I input "edge://settings/appearance/copilotAndSidebar" to the address bar
  #   When I select "Always on" option in Settings page
  #   Then the sidebar should be visible
  #   When I select "Off" option in Settings page
  #   Then the sidebar should be hidden

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56612246
  # @regression @p0 @settings
  # Scenario: Restore by custom sites
  #   Given Edge is launched
  #   And I input "edge://settings/startHomeNTP" to the address bar
  #   When I select the option "Open custom sites"
  #   And I click the "Add site" button
  #   Then the "Add site" dialog should be opened
  #   When I input "https://www.bing.com" in the URL field on the "Add site" dialog
  #   And I click the "Add" button on the "Add site" dialog
  #   Then the "Add site" dialog should be closed
  #   And url "https://www.bing.com" should be added to the custom sites list
  #   When I close and restart Edge
  #   Then edge should open with "https://www.bing.com"

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56612834
  # @regression @p0 @settings
  # Scenario: Delete custom sites
  #   Given Edge is launched
  #   And I input "edge://settings/startHomeNTP" to the address bar
  #   When I select the option "Open custom sites"
  #   And I click the "Add site" button
  #   Then the "Add site" dialog should be opened
  #   When I input "https://www.bing.com" in the URL field on the "Add site" dialog
  #   And I click the "Add" button on the "Add site" dialog
  #   Then the "Add site" dialog should be closed
  #   And url "https://www.bing.com" should be added to the custom sites list
  #   When I click the "More actions" button next to the custom site "https://www.bing.com"
  #   And I click the "Delete" button from the dropdown menu
  #   When I close and restart Edge
  #   Then edge should open with a page titled "New Tab"

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56612878
  # @regression @p0 @settings
  # Scenario: Restore by use all open tabs
  #   Given Edge is launched
  #   And I input to "www.google.com" to the address bar
  #   And I navigate to "edge://settings/startHomeNTP" in a new tab
  #   When I select the option "Open custom sites"
  #   And I click the "Use all open tabs" button
  #   Then url "https://www.google.com" should be added to the custom sites list
  #   When I close and restart Edge
  #   Then edge should open a tab and the address bar contain "www.google.com"

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56614562
  # @settings @smoke @p0
  # Scenario: Set custom site as home page
  #   Given Edge is launched
  #   And I input "edge://settings/startHomeNTP" to the address bar
  #   When I turn on the option "show home button on the toolbar"
  #   And I select the option "Set custom site"
  #   Then the input box under "Set custom site" can be clicked
  #   When I input "https://www.apple.com" to the input box
  #   And I select the option "Set custom site"
  #   And I click "Home" button to the left of the address bar
  #   Then should open "https://www.apple.com" site

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/56614547
  # @settings @smoke @p0
  # Scenario: Set NTP as home page
  #   Given Edge is launched
  #   And I input "edge://settings/startHomeNTP" to the address bar
  #   When I turn on the option "show home button on the toolbar"
  #   And I select the option "New tab page"
  #   When I click "Home" button to the left of the address bar
  #   Then should open a page titled "New Tab"

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/58971089
  # @settings @smoke @p0
  # Scenario: Change browser theme in light mode
  #   Given Edge is launched
  #   When I navigate to "edge://settings/appearance"
  #   And I select the option "light"
  #   Then Analyze the screenshot to verify the Edge browser theme is light
  #   When I select the "Juicy plum" in the theme color
  #   Then Analyze the screenshot to verify the title bar and toolbar change color to purple

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/58971090
  # @settings @smoke @p0
  # Scenario: Change browser theme in dark mode
  #   Given Edge is launched
  #   When I navigate to "edge://settings/appearance"
  #   And I select the option "Dark"
  #   Then Analyze the screenshot to verify the Edge browser theme is dark
  #   When I select the "Mystical forest" in the theme color
  #   Then Analyze the screenshot to verify the title bar and toolbar change color to green
