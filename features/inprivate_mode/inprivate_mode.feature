Feature: InPrivate Mode

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59105730
  @p0 @regression @inprivate_mode
  Scenario: Browsing history isolation in InPrivate mode
    Given Edge is launched
    When I click "Settings and more" button in toolbar
    And I click "New InPrivate Window" button
    Then InPrivate Window should be opened
    When I navigate to "https://www.apple.com"
    And I click "InPrivate" button in toolbar
    And I click "Close InPrivate Window" button
    Then InPrivate Window should be closed
    When I press "cmd" and "Y" keys
    Then "https://www.apple.com" should not be displayed in History panel
