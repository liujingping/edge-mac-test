Feature: tab action menu functionality

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863912
  @tab_action_menu @regression @p0 @vertical_tab
  Scenario: Switch VT and HT in tab action menu
    Given Edge is launched
    When I navigate to "https://www.google.com"
    And I click "Search tabs" button on the tab bar
    Then the "Search tabs" dialog should be opened
    When I click "Turn on vertical tabs" button in the "Search tabs" dialog
    And I press escape to close popup
    Then Analyze the screenshot to verify that the vertical tabs shown on the left side of the window
    When I click "Search tabs" button in the vertical tab mode
    Then the "Search tabs" dialog should be opened in the vertical tab mode
    When I click "Turn off vertical tabs" button in the "Search tabs" dialog
    Then Analyze the screenshot to verify that the horizontal tabs shown on the top of the window

   # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863916
  @tab_action_menu @regression @p0 
  Scenario: Organize tabs in horizontal tab mode in tab action menu
    Given Edge is launched
    When I navigate to "https://www.google.com"
    And I open a new tab
    And I navigate to "https://www.bing.com"
    And I press "cmd+t" to open a new tab
    And I navigate to "https://www.duckduckgo.com"
    And I click "Search tabs" button on the tab bar
    Then the "Search tabs" dialog should be opened
    When I click "Organize tabs" button in the "Search tabs" dialog
    And I click "Group Tabs" button in the "Organize tabs" pop
    Then verify a tab group created with the name of "Search Engines" on the tab bar
    And the tab group contains 3 tabs

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863919
  @tab_action_menu @regression @p0 
  Scenario: Search tabs in horizontal tab mode in tab action menu
    Given Edge is launched
    When I navigate to "https://www.google.com"
    And I open a new tab
    And I navigate to "https://www.apple.com"
    And I wait 3 seconds
    And I press "cmd+w" to close the current tab
    And I click "Search tabs" button on the tab bar
    Then the "Search tabs" dialog should be opened
    When I input "google" in the "Search Tabs" input box
    Then verify a tab name contains "google" shown in the "Search tabs" open tabs dialog
    When I clear the input in the "Search Tabs" input box
    And I input "Apple" in the "Search Tabs" input box
    Then verify a tab name contains "Apple" shown in the "Search tabs" recently closed dialog

    # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863927
  @tab_action_menu @regression @p0 @vertical_tab
  Scenario: Organize tabs in vertical tab mode in tab action menu
    Given Edge is launched
    When I navigate to "https://www.google.com"
    And I click "Search tabs" button on the tab bar
    Then the "Search tabs" dialog should be opened
    When I click "Turn on vertical tabs" button in the "Search tabs" dialog
    And I press escape to close popup
    And I press "cmd+t" to open a new tab
    And I navigate to "https://www.bing.com"
    And I press "cmd+t" to open a new tab
    And I navigate to "https://www.duckduckgo.com"
    When I click "Search tabs" button in the vertical tab mode
    Then the "Search tabs" dialog should be opened
    When I click "Organize tabs" button in the "Search tabs" dialog
    And I click "Group Tabs" button in the "Organize tabs" pop
    Then verify a tab group created with the name of "Search Engines" on the tab bar
    And the tab group contains 3 tabs

    # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863936
  @tab_action_menu @regression @p0 @vertical_tab
  Scenario: Search tabs in vertical tab mode in tab action menu
    Given Edge is launched
    When I navigate to "https://www.google.com"
    And I click "Search tabs" button on the tab bar
    Then the "Search tabs" dialog should be opened
    When I click "Turn on vertical tabs" button in the "Search tabs" dialog
    And I press escape to close popup
    And I press "cmd+t" to open a new tab
    And I navigate to "https://www.apple.com"
    And I wait 3 seconds
    And I press "cmd+w" to close the current tab
    And I click "Search tabs" button on the tab bar
    Then the "Search tabs" dialog should be opened
    When I input "google" in the "Search Tabs" input box
    Then verify a tab name contains "google" shown in the "Search tabs" open tabs dialog
    When I clear the input in the "Search Tabs" input box
    And I input "Apple" in the "Search Tabs" input box
    Then verify a tab name contains "Apple" shown in the "Search tabs" recently closed dialog

   # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863940
  @tab_action_menu @regression @p0 @vertical_tab @full_screen
  Scenario: Switch VT and HT in full screen mode in tab action menu
    Given Edge is launched
    When I press "fn+f" to enter full screen mode
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://www.google.com"
    And I click "Search tabs" button on the tab bar
    Then the "Search tabs" dialog should be opened
    When I click "Turn on vertical tabs" button in the "Search tabs" dialog
    And I press escape to close popup
    Then Analyze the screenshot to verify that the vertical tabs shown on the left side of the window
    When I click "Search tabs" button in the vertical tab mode
    Then the "Search tabs" dialog should be opened in the vertical tab mode
    When I click "Turn off vertical tabs" button in the "Search tabs" dialog
    Then Analyze the screenshot to verify that the horizontal tabs shown on the top of the window
    When I press the "fn+f" to exit the full screen mode
    Then Verify the full screen mode has been exited

    # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863949
  @tab_action_menu @regression @p0 @full_screen
  Scenario: Organize tabs in horizontal tab in full screen mode in tab action menu
    Given Edge is launched
    When I click the Zoom button on the top left corner in small screen
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://www.google.com"
    And I open a new tab
    And I navigate to "https://www.bing.com"
    And I press "cmd+t" to open a new tab
    And I navigate to "https://www.duckduckgo.com"
    And I click "Search tabs" button on the tab bar
    Then the "Search tabs" dialog should be opened
    When I click "Organize tabs" button in the "Search tabs" dialog
    And I click "Group Tabs" button in the "Organize tabs" pop
    Then verify a tab group created with the name of "Search Engines" on the tab bar
    And the tab group contains 3 tabs
    When I press the "fn+f" to exit the full screen mode
    Then Verify the full screen mode has been exited

     # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863957
  @tab_action_menu @regression @p0 @full_screen
  Scenario: Search tabs in horizontal tab in full screen mode in tab action menu
    Given Edge is launched
    When I press "ctrl+cmd+f" keys to enter full screen mode
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://www.google.com"
    And I open a new tab
    And I navigate to "https://www.apple.com"
    And I wait 3 seconds
    And I press "cmd+w" to close the current tab
    And I click "Search tabs" button on the tab bar
    Then the "Search tabs" dialog should be opened
    When I input "google" in the "Search Tabs" in full screen mode
    Then verify a tab name contains "google" shown in the "Search tabs" open tabs dialog
    When I clear the input in the "Search Tabs" input box
    And I input "Apple" in the "Search Tabs" in full screen mode
    Then verify a tab name contains "Apple" shown in the "Search tabs" recently closed dialog
    When I press escape to close popup
    And I press "ctrl+cmd+f" keys to exit full screen mode
    Then Verify the full screen mode has been exited

     # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863959
  @tab_action_menu @regression @p0 @vertical_tab @full_screen
  Scenario: Organize tabs in vertical tab in full screen mode in tab action menu
    Given Edge is launched
    When I press "ctrl+cmd+f" keys to enter full screen mode
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://www.google.com"
    And I click "Search tabs" button on the tab bar
    Then the "Search tabs" dialog should be opened
    When I click "Turn on vertical tabs" button in the "Search tabs" dialog
    And I press escape to close popup
    And I press "cmd+t" to open a new tab
    And I navigate to "https://www.bing.com"
    And I press "cmd+t" to open a new tab
    And I navigate to "https://www.duckduckgo.com"
    When I click "Search tabs" button in the vertical tab mode
    Then the "Search tabs" dialog should be opened
    When I click "Organize tabs" button in the "Search tabs" dialog
    And I click "Group Tabs" button in the "Organize tabs" pop
    Then verify a tab group created with the name of "Search Engines" on the tab bar
    And the tab group contains 3 tabs
    When I press "ctrl+cmd+f" keys to exit full screen mode
    Then Verify the full screen mode has been exited

    # https://microsoft.visualstudio.com/Edge/_workitems/edit/59863960
  @tab_action_menu @regression @p0 @vertical_tab @full_screen
  Scenario: Search tabs in vertical tab in full screen mode in tab action menu
    Given Edge is launched
    When I press "ctrl+cmd+f" keys to enter full screen mode
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://www.google.com"
    And I click "Search tabs" button on the tab bar
    Then the "Search tabs" dialog should be opened
    When I click "Turn on vertical tabs" button in the "Search tabs" dialog
    And I press escape to close popup
    And I press "cmd+t" to open a new tab
    And I navigate to "https://www.apple.com"
    And I wait 3 seconds
    And I press "cmd+w" to close the current tab
    And I click "Search tabs" button on the tab bar
    Then the "Search tabs" dialog should be opened
    When I input "google" in the "Search Tabs" in full screen mode
    Then verify a tab name contains "google" shown in the "Search tabs" open tabs dialog
    When I clear the input in the "Search Tabs" input box
    And I input "Apple" in the "Search Tabs" in full screen mode
    Then verify a tab name contains "Apple" shown in the "Search tabs" recently closed dialog
    When I press escape to close popup
    And I press "ctrl+cmd+f" keys to exit full screen mode
    Then Verify the full screen mode has been exited
