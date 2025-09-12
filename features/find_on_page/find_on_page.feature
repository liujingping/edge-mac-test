Feature: Find on Page

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56200550
  @regression @p0 @findonpage
  Scenario: Multiple results are matched when searching for a common word
    Given Edge is launched
    When I navigate to "edge://settings/profiles"
    And I click "Settings and more" button in toolbar
    And I click "Find on page" button in context menu
    Then "Find on page" dialog should appear
    When I input "settings" into "Find on page" dialog
    Then the indicator containing "1/7" should be shown in "Find on page" dialog
    And Analyze the screenshot to verify the multiple matched results are highlighted in current page

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56200491
  @regression @p0 @findonpage
  Scenario: No results are matched when searching for a non-existent word
    Given Edge is launched
    When I navigate to "edge://settings/profiles"
    And I press "Cmd+F" keys
    Then "Find on page" dialog should appear
    When I input "nonexistentword" into "Find on page" dialog
    Then the indicator containing "0/0" should be shown in "Find on page" dialog
    And Analyze the screenshot to verify no matched results are highlighted in current page
