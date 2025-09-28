Feature: Read Aloud

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56499574
  @p0 @regression @read_aloud
  Scenario: Verify the basic function of read aloud
    Given Edge is launched
    When I navigate to "https://en.wikipedia.org/wiki/Main_Page"
    And I click on "More actions" button in address bar
    And I click "Read aloud"
    Then Read Aloud toolbar should appear
    And I can see playing audio icon in the tab
    And Analyze the screenshot to verify the webpage has highlighted text
    When I click "Pause Read Aloud" button in Read Aloud toolbar
    Then I can see "Continue Read Aloud" button in Read Aloud toolbar
    And Playing audio icon in the tab should disappear
    When I click "Close Read Aloud" button in Read Aloud toolbar
    Then Read Aloud toolbar should be closed
    And Analyze the screenshot to verify the webpage has highlighted text is cleared

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56499690
  @p0 @regression @read_aloud
  Scenario: Verify Read Aloud can work well in background
    Given Edge is launched
    When I navigate to "https://en.wikipedia.org/wiki/Main_Page"
    And I press "shift+cmd+U" keys
    Then Read Aloud toolbar should appear
    And I can see playing audio icon in the tab
    When I open a new tab
    Then I can see playing audio icon in the tab containing "Wikipedia"
    When I wait for 60 seconds
    Then I can see playing audio icon in the tab containing "Wikipedia"
    When I click on the tab name containing "Wikipedia"
    Then I can see Read Aloud toolbar
    And Analyze the screenshot to verify the webpage has highlighted text
    When I click "Close Read Aloud" button on address bar
    Then Read Aloud toolbar should be closed
