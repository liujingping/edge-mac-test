Feature: Feedback functionality

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56445272
  Scenario: Fill out issue information and send feedback
    Given Edge is launched
    When I click settings and more button
    And I click help and feedback button
    And I click send feedback button
    Then the "Send feedback" dialog should be shown
    When I input "This is a test feedback." into the feedback text area
    And I select "Yes" for the question "Include this screenshot"
    And I check the "Send diagnostic data to Microsoft" and select "Yes" if it is not checked
    And I click the send button
    Then The "Send feedback" dialog should not be shown
    And The "Thank you for sharing!" message should be shown
