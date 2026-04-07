Feature: Tab functionality in Microsoft Edge

  # Demo: Basic tab operations
  @demo @tab
  Scenario: Close a tab in horizontal mode
    Given Edge is launched
    When I new a tab and navigate to "https://www.apple.com"
    And I click the "Close Tab" button on tab header
    Then the "Apple" tab should be closed

  @demo @tab
  Scenario: Drag a tab in horizontal mode
    Given Edge is launched
    When I navigate to "https://www.apple.com"
    And I new a tab and navigate to "https://www.google.com"
    And I drag the "Google" tab to the far left of the "Apple" tab
    Then "Google" tab is on the left of the "Apple" tab

  @demo @tab
  Scenario: Refresh in horizontal mode
    Given Edge is launched
    When I navigate to "https://www.youtube.com"
    And I right click on the tab header of "Youtube" tab
    And I click "Refresh" from the context menu
    Then the page should be refreshed
    And the address bar still displays the complete URL "https://www.youtube.com"

  @demo @tab
  Scenario: Open new tab using plus button
    Given Edge is launched
    When I click the "New tab" plus button
    Then a new tab should be created
    And the new tab should display the "New tab" page

  @demo @tab
  Scenario: Pin and unpin a tab
    Given Edge is launched
    When I navigate to "https://www.bing.com"
    And I right click on the tab header of "Bing" tab
    And I click "Pin tab" from the context menu
    Then the "Bing" tab should be pinned and show only the favicon
    When I right click on the pinned "Bing" tab
    And I click "Unpin tab" from the context menu
    Then the "Bing" tab should be unpinned and show the full title

  @demo @tab
  Scenario: Restore recently closed tab
    Given Edge is launched
    When I navigate to "https://www.github.com"
    And I click the "Close Tab" button on tab header
    Then the "GitHub" tab should be closed
    When I press "cmd+shift+t"
    Then the "GitHub" tab should be restored

  @demo @tab
  Scenario: Duplicate a tab
    Given Edge is launched
    When I navigate to "https://www.wikipedia.org"
    And I right click on the tab header of "Wikipedia" tab
    And I click "Duplicate tab" from the context menu
    Then a new "Wikipedia" tab should be created
    And both tabs should display the same URL "https://www.wikipedia.org"
