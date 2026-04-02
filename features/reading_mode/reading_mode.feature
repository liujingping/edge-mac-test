Feature: Reading Mode

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56499879
  @p0 @regression @reading_mode
  Scenario: Can open reading mode normally
    Given Edge is launched
    When I navigate to "https://en.wikipedia.org/wiki/Main_Page"
    And I open Reading Mode
    Then Reading Mode toolbar should appear
    And I can see reading mode icon in the address bar
    And I can see address bar contains "read://"
    When I click "Exit Immersive Reader" button in Reading Mode toolbar
    Then Reading Mode toolbar should be closed
    And I can see address bar does not contain "read://"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56500049
  @p0 @regression @reading_mode
  Scenario: Read aloud of reading mode work normally
    Given Edge is launched
    When I navigate to "https://en.wikipedia.org/wiki/Main_Page"
    And I open Reading Mode
    Then Reading Mode toolbar should appear
    When I click "Read Aloud" button in Reading Mode toolbar
    Then Read Aloud toolbar should appear
    And I can see playing audio icon in the tab
    And Analyze the screenshot to verify the webpage in shadow mode
    When I click "Pause Read Aloud" button in Read Aloud toolbar
    Then I can see "Continue Read Aloud" button in Read Aloud toolbar
    And Playing audio icon in the tab should disappear
    And Analyze the screenshot to verify the webpage exit shadow mode
    When I click "Exit Immersive Reader" button on address bar
    Then Reading Mode toolbar should be closed

