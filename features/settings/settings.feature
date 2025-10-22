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

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511650
  @regression @p0 @settings
  Scenario: Restore previous session tabs
    Given Edge is launched
    When I input "edge://settings/startHomeNTP" to the address bar
    And I select the option "Open tabs from the previous session"
    And I open a new tab
    And I navigate to "https://www.bing.com"
    And I close and restart Edge
    Then "edge://settings/startHomeNTP" website should be restored
    And "https://www.bing.com" website should be restored

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511626
  @regression @p0 @settings
  Scenario: Restore by new tab
    Given Edge is launched
    And I input "edge://settings/startHomeNTP" to the address bar
    When I select the option "Open the new tab page"
    And I open a new tab
    And I navigate to "https://www.bing.com"
    And I close and restart Edge
    Then edge should open with a page titled "New Tab"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511520
  @regression @p0 @settings
  Scenario: Show/hide home button
    Given Edge is launched
    And I input "edge://settings/appearance/toolbar" to the address bar
    When I click on "Home" button on the settings page
    Then the home button should be visible on the toolbar
    When I click on "Home" button on the settings page
    Then the home button should be hidden on the toolbar

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56612273
  @regression @p0 @settings
  Scenario: Cancel add custom site
    Given Edge is launched
    And I input "edge://settings/startHomeNTP" to the address bar
    When I select the option "Open custom sites"
    And I click the "Add site" button
    Then the "Add site" dialog should be opened
    When I input "https://www.bing.com" in the URL field on the "Add site" dialog
    And I click the "Cancel" button on the "Add site" dialog
    Then the "Add site" dialog should be closed

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511529
  @regression @p0 @settings
  Scenario: Show/hide Split screen button
    Given Edge is launched
    And I input "edge://settings/appearance/toolbar" to the address bar
    When I click on "Split screen" button switch in Toolbar Settings page
    Then the Split screen button should be visible on the toolbar
    When I click on "Split screen" button switch in Toolbar Settings page
    Then the Split screen button should be hidden on the toolbar

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56511558
  @regression @p0 @settings
  Scenario: Show/hide sidebar
    Given Edge is launched
    And I input "edge://settings/appearance/copilotAndSidebar" to the address bar
    When I select "Always on" option in Settings page
    Then the sidebar should be visible
    When I select "Off" option in Settings page
    Then the sidebar should be hidden

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56612246
  @regression @p0 @settings
  Scenario: Restore by custom sites
    Given Edge is launched
    And I input "edge://settings/startHomeNTP" to the address bar
    When I select the option "Open custom sites"
    And I click the "Add site" button
    Then the "Add site" dialog should be opened
    When I input "https://www.bing.com" in the URL field on the "Add site" dialog
    And I click the "Add" button on the "Add site" dialog
    Then the "Add site" dialog should be closed
    And url "https://www.bing.com" should be added to the custom sites list
    When I close and restart Edge
    Then edge should open with "https://www.bing.com"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56612834
  @regression @p0 @settings
  Scenario: Delete custom sites
    Given Edge is launched
    And I input "edge://settings/startHomeNTP" to the address bar
    When I select the option "Open custom sites"
    And I click the "Add site" button
    Then the "Add site" dialog should be opened
    When I input "https://www.bing.com" in the URL field on the "Add site" dialog
    And I click the "Add" button on the "Add site" dialog
    Then the "Add site" dialog should be closed
    And url "https://www.bing.com" should be added to the custom sites list
    When I click the "More actions" button next to the custom site "https://www.bing.com"
    And I click the "Delete" button from the dropdown menu
    When I close and restart Edge
    Then edge should open with a page titled "New Tab"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56612878
  @regression @p0 @settings
  Scenario: Restore by use all open tabs
    Given Edge is launched
    And I input to "www.google.com" to the address bar
    And I navigate to "edge://settings/startHomeNTP" in a new tab
    When I select the option "Open custom sites"
    And I click the "Use all open tabs" button
    Then url "https://www.google.com" should be added to the custom sites list
    When I close and restart Edge
    Then edge should open a tab and the address bar contain "www.google.com"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56614562
  @settings @smoke @p0
  Scenario: Set custom site as home page
    Given Edge is launched
    And I input "edge://settings/startHomeNTP" to the address bar
    When I turn on the option "show home button on the toolbar"
    And I select the option "Set custom site"
    Then the input box under "Set custom site" can be clicked
    When I input "https://www.apple.com" to the input box
    And I select the option "Set custom site"
    And I click "Home" button to the left of the address bar
    Then should open "https://www.apple.com" site

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56614547
  @settings @smoke @p0
  Scenario: Set NTP as home page
    Given Edge is launched
    And I input "edge://settings/startHomeNTP" to the address bar
    When I turn on the option "show home button on the toolbar"
    And I select the option "New tab page"
    When I click "Home" button to the left of the address bar
    Then should open a page titled "New Tab"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/58971089
  @settings @smoke @p0
  Scenario: Change browser theme in light mode
    Given Edge is launched
    When I navigate to "edge://settings/appearance"
    And I select the option "light"
    Then Analyze the screenshot to verify the Edge browser theme is light
    When I select the "Juicy plum" in the theme color
    Then Analyze the screenshot to verify the title bar and toolbar change color to purple

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/58971090
  @settings @smoke @p0
  Scenario: Change browser theme in dark mode
    Given Edge is launched
    When I navigate to "edge://settings/appearance"
    And I select the option "Dark"
    Then Analyze the screenshot to verify the Edge browser theme is dark
    When I select the "Mystical forest" in the theme color
    Then Analyze the screenshot to verify the title bar and toolbar change color to green


  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863843
  @settings @regression @p0
  Scenario: Add an empty profile in the settings page
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I click the "Settings" button from the dropdown menu
    And I click the "Profiles" tab on the left side
    Then verify the address bar is "edge://settings/profiles"
    And the profile is "Profile 1"
    When I click the "Add profile" button
    And I click the "Add" button on the "Add profile" dialog
    And I click "Settings and more" button on toolbar in the new edge window
    And I click the "Settings" button from the dropdown menu in the new edge window
    And I click the "Profiles" tab on the left side in the new edge window
    Then verify the profile is "Profile 2" in the new edge window

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863851
  @settings @regression @p0
  Scenario: Add a password in the settings page
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I click the "Settings" button from the dropdown menu
    And I click the "Passwords and autofill" tab on the left side
    Then verify the address bar is "edge://settings/autofill"
    When I click "Microsoft Password Manager" button
    And I click "Add password" button
    Then the "Add password" dialog should be opened
    When I input "https://www.bing.com" in the "Website URL" field
    And I input "testuser" in the "Username" field
    And I input "P@ssw0rd!" in the "Password" field
    And I click the "Add" button
    Then 1 account with bing.com should be appeared in the password list

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863855
  @settings @regression @p0
  Scenario: Clear browsering data in the settings page
    Given Edge is launched
    When I open a new tab
    And I navigate to "https://www.apple.com"
    And I wait 3 seconds
    # for page to load
    And I press "cmd+y" to open history pane
    Then I can see "apple" in history pane
    And I press "cmd+w" to close the current tab
    When I click "Settings and more" button on toolbar
    And I click the "Settings" button from the dropdown menu
    And I click the "Privacy, search and services" tab on the left side
    Then verify the address bar is "edge://settings/privacy"
    When I click "Clear browsing data" section
    And I click "Choose what to clear" button
    Then the "Clear browsing data" dialog should be opened
    When I select "All time" option in the "Time range" dropdown menu
    When I click "Clear now" button in the "Clear browsing data" dialog
    And I press "cmd+y" to open history pane
    Then I can see "apple" is disappeared in the history pane

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863857
  @settings @regression @p0
  Scenario: Check default browser entrance in the settings page
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I click the "Settings" button from the dropdown menu
    And I click the "Default browser" tab on the left side
    Then verify the address bar is "edge://settings/defaultBrowser"
    And the "Make default" button is shown on the page

    # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863862
  @settings @regression @p0
  Scenario: Add language in the settings page
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I click the "Settings" button from the dropdown menu
    And I click the "Languages" tab on the left side
    Then verify the address bar is "edge://settings/languages"
    And I click "Add languages" button
    And the "Add languages" dialog should be opened
    When I click "Search languages" box in the pop up "Add languages" dialog
    And I input "German" option in the add languages page
    Then "German - Deutsch" language should be shown in the add languages page
    When I select the check box of "German - Deutsch" language
    And I click "Add" button in the "Add languages" dialog
    Then "German - Deutsch" language should be added to the languages list
    When I click the "More actions" button next to the "German" language
    And I click "Move to the top" button from the dropdown menu
    Then verify "German" language should be moved to the top of the languages list

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863864
  @settings @regression @p0
  Scenario: Check start and downloads and entrance in the settings page
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I click the "Settings" button from the dropdown menu
    And I click the "Downloads" tab on the left side
    Then verify the address bar is "edge://settings/downloads"
    And the page contains "Location" and "Ask where to save each file before downloading" sections
    When I click "Start, home, and new tabs" tab on the left side
    Then verify the address bar is "edge://settings/startHomeNTP"
    And the page contains "On startup" and "Home button" and "New tab page" sections

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863869
  @settings @regression @p0
    Scenario: Click System and performance in the settings page
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I click the "Settings" button from the dropdown menu
    And I click "System and performance" tab on the left side
    Then verify the address bar is "edge://settings/system"
    When I click "Graphics acceleration" button in the System and performance page
    Then the "Graphics acceleration" page should be opened
    And verify system page contains "Use graphics acceleration when available" option
    When I click back button to return to the System and performance page
    And I click "Proxy settings" button in the System and performance page
    Then verify the page contains "Open proxy settings"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863875
  @settings @regression @p0
    Scenario: Reset settings in the settings page
    Given Edge is launched
    When I navigate to "https://www.google.com"
    And I right click on the tab header of "Google" tab
    And I select "Pin tab" option from the context menu
    Then verify the "Google" tab should be pinned on the tab bar
    When I click "Settings and more" button on toolbar
    And I click the "Settings" button from the dropdown menu
    And I click "Reset settings" tab on the left side
    Then verify the address bar is "edge://settings/reset"
    When I click "Restore settings to their default values" button
    Then the "Reset settings" dialog should be opened
    When I click "Reset" button in the "Reset settings" dialog
    Then the "Reset settings" dialog should be closed
    And verify the "Google" tab is unpinned on the tab bar

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863878
  @settings @regression @p0
  Scenario: check edge version entrance in the settings page
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I click the "Settings" button from the dropdown menu
    And I click "About Microsoft Edge" tab on the left side
    Then verify the address bar is "edge://settings/help"
    And the page contains "Microsoft Edge is up to date." text

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59888824
  @settings @regression @p0
  Scenario: check accessibility entrance in the settings page
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I click the "Settings" button from the dropdown menu
    And I click "Accessibility" tab on the left side
    Then verify the address bar is "edge://settings/accessibility"
    And the page contains "Visibility" and "Usability" sections
    
