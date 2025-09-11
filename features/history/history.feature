Feature: History functionality in Microsoft Edge

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/58465442
  @p0 @regression @history
  Scenario: Click "X" to delete the browsing history
    Given Edge is launched
    When I navigate to "https://www.cgtn.com"
    Then the "cgtn" website should be opened
    When I click "Settings and more" button in toolbar
    And I click "History" button
    And I hover over the "cgtn" website in History panel
    And I click "Delete" button in History panel
    Then the "cgtn" website should not be displayed in History panel

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/52566629
  # @p0 @regression @history
  # Scenario: Set the History button show in toolbar
  #   Given Edge is launched
  #   When I click "Settings and more" button in toolbar
  #   And I right click "History" button in menu
  #   And I click "Show in toolbar" in menu
  #   Then "History" should be displayed in toolbar

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/52566662
  # @p0 @regression @history
  # Scenario: Search words in history panel
  #   Given Edge is launched
  #   When I navigate to "https://www.cgtn.com"
  #   Then the "cgtn" website should be opened
  #   When I click "Settings and more" button in toolbar
  #   And I click "History" button
  #   And I input "cgtn" in Search history box
  #   Then the "cgtn" website should be displayed in History panel
  #   When I input "mscaaa" in Search history box
  #   Then shows "No results found for 'mscaaa'" in History panel

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/58477901
  # @p0 @regression @history
  # Scenario: Find closed website in Recently closed
  #   Given Edge is launched
  #   When I navigate to "https://www.cgtn.com"
  #   Then the "cgtn" website should be opened
  #   When I open a new tab
  #   And I click "Close tab" button on the "cgtn" tab
  #   Then the "cgtn" tab cannot be found in the tab bar
  #   When I press "cmd" and "Y" keys
  #   And I click "Recently closed" in History panel
  #   Then the "cgtn" website should be displayed in "Recently closed" in History panel

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/58480065
  # @p0 @regression @history
  # Scenario: Open viewed website in history hub
  #   Given Edge is launched
  #   When I navigate to "https://www.cgtn.com"
  #   Then the "cgtn" website should be opened
  #   When I open a new tab
  #   And I click "Close tab" button on the "cgtn" tab
  #   And I press "cmd" and "Y" keys
  #   Then the "cgtn" website should be displayed in "All" in History panel
  #   And I click "cgtn" website in "All" in History panel
  #   Then the "cgtn" website should be opened

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/52566640
  # @p0 @regression @history
  # Scenario: Click the Pin history button
  #   Given Edge is launched
  #   When I click "Settings and more" button in toolbar
  #   And I click "History" button
  #   Then History panel should appear
  #   When I click "Pin history" button in History panel
  #   Then History pane should be displayed
  #   When I navigate to "https://www.cgtn.com"
  #   Then History pane still should be displayed
  #   When I click "Close history" button in History pane
  #   And I press "cmd" and "Y" keys
  #   And I open a new tab
  #   Then History pane still should be displayed

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/52566627
  # @p0 @regression @history
  # Scenario: Click "..." to open History pane then close
  #   Given Edge is launched
  #   When I click "Settings and more" button in toolbar
  #   And I click "History" button
  #   Then History panel should appear
  #   When I click "History" in toolbar
  #   Then History panel should be closed
