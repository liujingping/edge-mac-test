Feature: tab

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/43623996
  @p0
  Scenario: Close a tab in horizontal mode
    Given Edge is launched
    When I new a tab and navigate to "https://www.apple.com"
    And I click the "Close Tab" button on tab header
    Then the "Apple" tab should be closed

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/58453262
  @p0
  Scenario: Drag a tab in horizontal mode
    Given Edge is launched
    When I navigate to "https://www.apple.com"
    And I new a tab and navigate to "https://www.google.com"
    And I drag the "Google" tab to the far left of the "Apple" tab
    Then "Google" tab is on the left of the "Apple" tab

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/43625800
  @p0
  Scenario: Refresh in horizontal mode
    Given Edge is launched
    When I navigate to "https://www.youtube.com"
    And I right click on the tab header of "Youtube" tab
    And I click "Refresh" from the context menu
    Then the page should be refreshed
    And the address bar still displays the complete URL "https://www.youtube.com"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/43625694
  @p0
  Scenario: add tab to new tab group in horizontal mode
    Given Edge is launched
    When I new a tab and navigate to "https://www.youtube.com"
    And I right click on the tab header of "Youtube" tab
    And I click "Add tab to new group" from the right-click context menu
    Then a new tab group should be created with the "Youtube" tab
    And the tab group should be named "Youtube"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/43626630
  @p0
  Scenario: reopen a closed tab in horizontal mode
    Given Edge is launched
    When I new a tab and navigate to "https://www.apple.com"
    And I click the "Close Tab" button on the "Apple" tab header
    Then the "Apple" tab should be closed
    When I press "ctrl+shift+t" to reopen the closed tab
    Then the "Apple" tab should be reopened
    And the address bar should display the complete URL "https://www.apple.com"
