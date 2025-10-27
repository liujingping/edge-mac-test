Feature: Settings and more functionality

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59014401
  @regression @p0 @settings_and_more @tabs
  Scenario: Open a new Tab and Turn on vertical tab by clicking the "Settings and more" button
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I select "New Tab" button from the dropdown menu
    Then a new edge tab should be opened
    When I right click on "New Tab" tab header
    And I select "Turn On Vertical Tabs" option from the context menu
    And I press escape to close popup
    Then Analyze the screenshot to verify that the vertical tabs shown on the left side of the window

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59014428
  @regression @p0 @settings_and_more @address_bar
  Scenario: Open a new Window by clicking the "Settings and more" button
    Given Edge is launched
    When I navigate to "https://www.bing.com"
    Then the address bar should contain "bing"
    When I click "Settings and more" button on toolbar
    And I select "New Window" button from the dropdown menu
    Then a new edge window should be opened
    And the address bar should be empty in the new window

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59014435
  @regression @p0 @settings_and_more @inprivate_mode
  Scenario: Open a new Inprivate window by clicking the "Settings and more" button
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I select "New InPrivate window" button from the dropdown menu
    Then a new InPrivate edge window should be opened
    And the InPrivate icon should be shown on the top right corner of the new window
    When I click the InPrivate icon on the top right corner
    Then the pop up should contain the text "You have one InPrivate window"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59014510
  @regression @p0 @settings_and_more @downloads
  Scenario: Open a new tab and check Downloads history by clicking the "Settings and more" button
    Given Edge is launched
    When I navigate to "https://getsamplefiles.com/download/pdf/sample-1.pdf"
    Then the Downloads panel should appear
    When I click "Settings and more" button on toolbar
    And I select "New Tab" button from the dropdown menu
    When I click "Settings and more" button on toolbar
    And I select "Downloads" button from the dropdown menu
    Then the Downloads panel should appear
    And "sample-1.pdf" should be listed in downloads

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59014449
  @regression @p0 @settings_and_more @favorites
  Scenario: Rename a favorite by clicking the "Favorites" in "Settings and more" button
    Given Edge is launched
    When I navigate to "https://www.apple.com"
    And I click the "Add this page to favorites(⌘D)" button in the address bar
    And I press Enter key
    Then "Apple" should be listed in favorites bar
    When I click "Settings and more" button on toolbar
    And I click "Favorites" button from the dropdown menu
    When I click "Pin favorites" button in favorites hub
    And I click the "Favorites Bar" tab in favorites pane to expand it
    And I right click on "Apple" in favorites pane
    And I select "Rename" option from the context menu
    And I enter "Apple Inc." as the new name
    And I press Enter key
    Then "Apple Inc." should be listed in favorites bar

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59014579
  @regression @p0 @screenshot @settings_and_more
  Scenario: Capture and save a screenshot by clicking the "screenshot" in "Settings and more" button
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I select "Screenshot" button from the dropdown menu
    Then "Web capture toolbar" should be shown
    When I click "Capture full page" button in "Web capture toolbar"
    And I click "Save" button in "Screenshot" window
    And I click "Settings and more" button on toolbar
    And I click "Downloads" button from the dropdown menu
    Then the file name containing "Screenshot" should exist in the Downloads

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59014459
  @regression @p0 @settings_and_more @history
  Scenario: Restore a tab by clicking the "History" in "Settings and more" button
    Given Edge is launched
    When I open a new tab
    And I navigate to "https://www.apple.com"
    And I click the "Close Tab" button on the "Apple" tab header
    Then the "Apple" tab should be closed
    When I click "Settings and more" button on toolbar
    And I select "History" button from the dropdown menu
    Then history hub should be opened
    When I click "Recently closed" in history hub
    And I click "Apple" in "Recently closed"
    Then the "Apple" tab should be reopened

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59014556
  @regression @p0 @settings_and_more
  Scenario: Delete browsing data dialog by clicking "Delete browsing data" in "Settings and more" button
    Given Edge is launched
    When I navigate to "https://www.google.com"
    And I click "Settings and more" button on toolbar
    And I select "Delete browsing data" button from the dropdown menu
    Then the "Delete Browsing Data" dialog should be opened
    When I click "Clear now" button on the "Delete Browsing Data" dialog
    And I click "Settings and more" button on toolbar
    And I select "History" button from the dropdown menu
    Then history hub should be opened
    And no history item should be listed in history hub

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59014506
  @regression @p0 @settings_and_more @tab_groups
  Scenario: Create a tab group by clicking "Tab group" in "Settings and more" button
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I select "Tab Groups" button from the dropdown menu
    And I click "Create New Tab Group" button in the "Tab group" dialog
    And I enter "FSQ" as the group name
    And I press Enter key
    Then verify the "FSQ" tab group should appear on the tab bar

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59014573
  @regression @p0 @settings_and_more @print
  Scenario: Print a webpage in "Settings and more" button
    Given Edge is launched
    And I clean Edge downloads file "Apple-FSQ.pdf"
    When I navigate to "https://www.apple.com"
    And I click "Settings and more" button on toolbar
    And I select "Print" button from the dropdown menu
    Then "Print" dialog should be opened
    When I click "Save" button in "Print" dialog
    And I enter "Apple-FSQ" as the file name
    And I click "Save" button in "Save Print Output As" dialog
    And I click "Settings and more" button on toolbar
    And I click "Downloads" button from the dropdown menu
    Then verify "Apple-FSQ.pdf" should be listed in downloads

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59014442
  @regression @p0 @settings_and_more
  Scenario: Zoom out and full screen by "Settings and more" button
    Given Edge is launched
    When I navigate to "https://www.apple.com"
    When I click "Settings and more" button on toolbar
    And I click "Zoom out" button for 5 times from the dropdown menu
    Then Analyze the screenshot to verify that the page is zoomed out
    When I click "Full screen" button from the dropdown menu
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59349303
  @regression @p0 @settings_and_more
  Scenario: Zoom in and full screen by "Settings and more" button
    Given Edge is launched
    When I navigate to "https://www.apple.com"
    And I click "Settings and more" button on toolbar
    And I click "Zoom in" button for 5 times from the dropdown menu
    Then Analyze the screenshot to verify that the page is zoomed in
    When I click "Full screen" button from the dropdown menu
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59939645
  @regression @p0 @screenshot
  Scenario: Capture and save a screenshot by shortcuts
    Given Edge is launched
    When I open a new tab
    And I press "shift+cmd+s" to open the Screenshot toolbar
    Then "Web capture toolbar" should be shown
    When I click "Capture full page" button in "Web capture toolbar"
    And I click "Save" button in "Screenshot" window
    And I click "Settings and more" button on toolbar
    And I click "Downloads" button from the dropdown menu
    Then the file name containing "Screenshot" should exist in the Downloads

# # https://microsoft.visualstudio.com/Edge/_workitems/edit/59014579
# @regression @p0 @screenshot
# Scenario: Check entrance in the develpoer tools
# Given Edge is launched
# When I open a new tab and navigate to "edge://settings/profiles"
# And I click "Settings and more" button on toolbar
# And I click "More Tools" button from the dropdown menu
# And I click "Developer Tools" in the more tools dropdown menu
# Then verify the developer tools open in the right
# When I click the "Welcome" in the developer tools
# Then verify "Welcome to Microsoft Edge DevTools" shown in the welcome page
# When I click the "Elements" in the developer tools
# Then verify I can see the "<head>" and "<body>" in the elements page
# When I click "Console" in the developer tools
# Then verify I can see the "Intervention" in the console page
# When I click "Sources" in the developer tools
# Then verify I can see the "Top" and "settings" in the sources page
# When I click "Network" in the console page
# Then verify I can see the "Name" and "Status" in the network page
# When I click "Performance" in the developer tools
# Then verify I can see the "Local metrics" in the performance page
