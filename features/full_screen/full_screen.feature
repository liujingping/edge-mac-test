Feature: Full Screen Mode Tests

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59390173
  @p0 @regression @download @full_screen
  Scenario: Download a file and click file name to open in full screen mode
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I click "Full screen" button from the dropdown menu
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://getsamplefiles.com/download/pdf/sample-1.pdf"
    Then the Downloads panel should appear
    When I click "Search downloads" in Downloads panel
    And I click on the file name containing "sample-1" in the Downloads panel
    Then I can see address bar contains "sample-1" in the new tab
    When I click on the Address and search bar
    And move the mouse to the top left corner and hover on the Zoom button
    And I click "Exit Full Screen" button from the dropdown menu
    Then Verify the full screen mode has been exited

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59390204
  @p0 @regression @download @full_screen
  Scenario: Search favorites item in Favorites hub in full screen mode
    Given Edge is launched
    And I press "ctrl+cmd+f" keys to enter full screen mode
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://www.youtube.com/"
    And I click "Favorites" button in the toolbar
    And I click the "More options" button in the favorites hub
    And I click the "Add this page to favorites" button in the more options menu
    And I press Enter key
    And I click the "Search favorites" button in Favorites hub
    And I enter "Youtube" into the search box
    Then the "Youtube" website should be displayed in search results of Favorites hub
    When I click on the Address and search bar
    And I press "ctrl+cmd+f" keys to exit full screen mode
    Then Verify the full screen mode has been exited

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59390208
  @P0 @Regression @Favorites @full_screen
  Scenario: Delete a favorite item from favorites bar in full screen mode
    Given Edge is launched
    And I press "ctrl+cmd+f" keys to enter full screen mode
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://www.youtube.com/"
    And I click "Favorites" button in the toolbar
    And I click the "More options" button in the favorites hub
    And I click the "Add this page to favorites" button in the more options menu
    And I press Enter key
    Then the "Youtube" website should be added to Favorites hub
    When I press "Shift+cmd+B" to toggle Favorites bar
    And I right-click on "https://www.youtube.com/" in Favorites bar
    And I click "Delete" button in the menu
    And I open Favorites hub
    And I click the "Search favorites" button in Favorites hub
    And I enter "Youtube" into the search box
    Then the "No results found" message should be displayed in Favorites hub
    When I click on the Address and search bar
    And I press "ctrl+cmd+f" keys to exit full screen mode
    Then Verify the full screen mode has been exited

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59390228
  @P0 @Regression @Favorites @full_screen
  Scenario: Edit an item name on Favorites bar in full screen mode
    Given Edge is launched
    When I click "Settings and more" button on toolbar
    And I click "Full screen" button from the dropdown menu
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://www.bing.com"
    And I click the "Add this page to favorites(⌘D)" button in the address bar
    And I press Enter key
    And I open Favorites hub
    And I click "Favorites bar" folder in hub
    Then "Search - Microsoft Bing" should appear in Favorites Bar
    When I press "Shift+cmd+B" to toggle Favorites bar
    And I right-click on "https://www.bing.com" in Favorites bar
    And I click "Edit" button in the drop-down menu
    Then the "Edit favorite" dialog should be opened
    When I clear the name field in "Edit favorite" dialog
    And I type "bingbing" into name field of "Edit favorite" dialog
    And I press Enter key
    Then the "bingbing" website name should be shown in Favorites bar
    When I click on the Address and search bar
    And I press "ctrl+cmd+f" keys to exit full screen mode
    Then Verify the full screen mode has been exited

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59390252
  @p0 @regression @history @full_screen
  Scenario: Search words in history panel in full screen mode
    Given Edge is launched
    When I move the mouse to the top left corner and hover on the Zoom button in the small screen
    And click "Full Screen" button from the dropdown menu
    And click "Entire Screen" button from next dropdown menu
    Then move the mouse to the top left corner and hover on the Zoom button
    And verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://www.cgtn.com"
    And I click "Settings and more" button in toolbar
    And I select "History" button from the dropdown menu
    And I input "cgtn" in Search history box
    Then the "cgtn" website should be displayed in History panel
    When I input "aaaaaa" in Search history box
    Then shows No results found for "aaaaaa" in History panel
    When I click on the Address and search bar
    And I press "ctrl+cmd+f" keys to exit full screen mode
    Then Verify the full screen mode has been exited

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59390256
  @p0 @regression @history @full_screen
  Scenario: Restore a tab by clicking the "History" in full screen
    Given Edge is launched
    And I press "ctrl+cmd+f" keys to enter full screen mode
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
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
    When I click on the Address and search bar
    And I press "ctrl+cmd+f" keys to exit full screen mode
    Then Verify the full screen mode has been exited

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59390267
  @p0 @regression @history @full_screen
  Scenario: Click "X" to delete the browsing history in full screen
    Given Edge is launched
    When I click the Zoom button on the top left corner in small screen
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://www.cgtn.com"
    Then the "cgtn" website should be opened
    When I click "Settings and more" button in toolbar
    And I click "History" button
    And I hover over the "cgtn" website in History panel
    And I click "Delete" button in History panel
    Then the "cgtn" website should not be displayed in History panel
    When I click on the Address and search bar
    And I click the Zoom button on the top left corner in full screen
    Then Verify the full screen mode has been exited

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59390283
  @p0 @regression @tab_management @full_screen
  Scenario: Close a tab in vertical mode in full screen
    Given Edge is launched
    When I press "cmd+t" to open a new tab
    And I click the Zoom button on the top left corner in small screen
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I click on the address and search bar
    And I navigate to "https://www.google.com"
    And I right click on the tab header of "Google" tab
    And I click "Turn on vertical tabs" from the right-click context menu
    And I press "esc" to close the vertical tabs pop up
    Then Analyze the screenshot to verify that the vertical tabs shown on the left side of the window
    When I press "cmd+w" to close the current tab
    Then the "Google" tab should be closed
    When I click the Zoom button on the top left corner in full screen
    Then Verify the full screen mode has been exited

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59390280
  @p0 @regression @tab_management @full_screen
  Scenario: Drag a tab in horizontal mode in full screen
    Given Edge is launched
    When I click the Zoom button on the top left corner in small screen
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://www.apple.com"
    And I new a tab and navigate to "https://www.google.com"
    And I drag the "Google" tab to the far left of the "Apple" tab
    Then "Google" tab is on the left of the "Apple" tab
    When I click the Zoom button on the top left corner in full screen
    Then Verify the full screen mode has been exited

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/57534406
  @p0 @regression @ominibox @full_screen
  Scenario: Use the shortcut key to copy or cut then paste part URL in address bar in full screen
    Given Edge is launched
    When I click the Zoom button on the top left corner in small screen
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I input "apple" in address bar
    And I select all in address bar
    And I press "cmd+C" to copy the selected text
    And I open a new tab
    And I press "cmd+V" to paste the copied text
    Then "apple" should be displayed in the address bar
    And I select all in address bar
    And I press "cmd+X" to cut the selected text
    And I open a new tab again
    And I press "cmd+V" to paste the cut text
    Then "apple" should be displayed in the address bar
    When I click the Zoom button on the top left corner in full screen
    Then Verify the full screen mode has been exited

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59411821
  @p0 @regression @full_screen
  Scenario: Back and forward a webpage in full screen
    Given Edge is launched
    When I press "fn+f" to enter full screen mode
    And move the mouse to the top left corner and hover on the Zoom button
    Then verify the tooltip text contains "Exit Full Screen"
    When I navigate to "https://www.apple.com"
    And I navigate to "https://www.bing.com"
    And I click Back button in the toolbar
    Then the address bar should display the complete URL "https://www.apple.com"
    When I click Forward button in the toolbar
    Then the address bar should display the complete URL "https://www.bing.com"
    When I press the "fn+f" to exit the full screen mode
    Then Verify the full screen mode has been exited
