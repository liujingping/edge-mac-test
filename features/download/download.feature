Feature: Download functionality in Microsoft Edge

  # Demo: Basic download operations
  @demo @download
  Scenario: Download a file and open file
    Given Edge is launched
    When I navigate to "https://getsamplefiles.com/download/pdf/sample-1.pdf"
    Then the Downloads panel should appear
    When I click "Search downloads" in Downloads panel
    And I click on the file name containing "sample-1" in the Downloads panel
    Then I can see address bar contains "sample-1" in the new tab

  @demo @download
  Scenario: Delete a downloaded file
    Given Edge is launched
    When I navigate to "https://getsamplefiles.com/download/pdf/sample-1.pdf"
    Then the Downloads panel should appear
    When I click "Search downloads" in Downloads panel
    And I hover over the file name containing "sample-1" in the Downloads panel
    And I click the "Delete file" button
    Then the file name containing "sample-1" should be removed from the Downloads panel

  @demo @download
  Scenario: Download a file and open in Finder
    Given Edge is launched
    And I clean Edge downloads file "sample-1.pdf"
    When I navigate to "https://getsamplefiles.com/download/pdf/sample-1.pdf"
    Then the Downloads panel should appear
    When I click "Search downloads" in Downloads panel
    And I hover over the file name containing "sample-1" in the Downloads panel
    And I click the "Show in Finder" button
    Then Analyze the screenshot to verify the Finder window should appear
    And Analyze the screenshot to verify that the file "sample-1.pdf" is present in the Finder window
