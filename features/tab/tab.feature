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
