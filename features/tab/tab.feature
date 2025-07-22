Feature: tab

  @p0
  Scenario: Close a tab in horizontal mode
    Given Edge is launched in horizontal mode
    When I new a tab and navigate to "https://www.apple.com"
    And I click the "Close Tab" button on tab header
    Then the "Apple" tab should be closed

  @p0
  Scenario: Drag a tab in horizontal mode
    Given Edge is launched in horizontal mode
    When I navigate to "https://www.apple.com"
    And I new a tab and navigate to "https://www.amazon.com/"
    And I drag the "Amanon.com" tab to the far left of the "Apple" tab
    Then "Amanon.com" tab is on the left, "Apple" tab is on the right

  @p0
  Scenario: Refresh in horizontal mode
    Given Edge is launched in horizontal mode
    When I navigate to "https://www.youtube.com"
    And I right click on the tab header of "Youtube" tab
    And I click "Refresh" from the context menu
    Then the page should be refreshed
    And the address bar still displays the complete URL "https://www.youtube.com"

  # Scenario: add tab to new tab group in horizontal mode
  # Given Edge is launched in horizontal mode
  # When I navigate to "https://www.apple.com"
  # And I new a tab and navigate to "https://www.amazon.com/"
  # And I right click on the tab header of "Amazon.com" tab
  # And I click "Add tab to new group" from the context menu
  # Then a new tab group should be created with the "Amazon.com" tab
  # And the tab group should be named "shopping"
  @p0
  Scenario: reopen a closed tab in horizontal mode
    Given Edge is launched
    When I new a tab and navigate to "https://www.apple.com"
    And I click the "Close Tab" button on the "Apple" tab header
    Then the "Apple" tab should be closed
    When I press "ctrl+shift+t" to reopen the closed tab
    Then the "Apple" tab should be reopened
    And the address bar should display the complete URL "https://www.apple.com"
