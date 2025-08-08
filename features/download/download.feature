Feature: Download functionality in Microsoft Edge

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56446007
  @p0 @regression @download
  Scenario: Download a file and open file by clicking "Open file" button
    Given Edge is launched
    When I navigate to "https://getsamplefiles.com/download/pdf/sample-1.pdf"
    Then the Downloads panel should appear
    When I click Downloads panel
    And I click on the file name containing "sample-1" in the Downloads panel
    Then I can see address bar contains "sample-1" in the new tab

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56446314
  @p0 @regression @download
  Scenario: Delete a downloaded file
    Given Edge is launched
    When I navigate to "https://getsamplefiles.com/download/pdf/sample-1.pdf"
    Then the Downloads panel should appear
    When I click Downloads panel
    And I hover over the file name containing "sample-1" in the Downloads panel
    And I click the "Delete file" button
    Then the file name containing "sample-1" should be removed from the Downloads panel
    When I click "Open Downloads folder" in the Downloads panel
    Then the file name containing "sample-1" should not be found in Downloads folder

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56533234
  @p0 @regression @download
  Scenario: Change the downloads path
    Given Edge is launched
    When I navigate to "edge://settings/downloads"
    And I click "Change" button in the Downloads Location section
    And I select the "Desktop" folder in Location window
    And I click "Select" button in Location window
    Then the Downloads Location path should contain "Desktop"
    When I navigate to "https://getsamplefiles.com/download/pdf/sample-1.pdf" on new tab
    And I click Downloads panel
    And I click on the file name containing "sample-1" in the Downloads panel
    Then I can see address bar contains "Desktop" in the new tab

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56533078
  @p0 @regression @download
  Scenario: Download a webpage file
    Given Edge is launched
    When I navigate to "www.bing.com"
    And I right click on the page without selecting any text or element
    And I click "Save As..." in the context menu
    Then Save As window should appear
    When I click "Save" button in Save As window
    Then the Downloads panel should appear
    When I click Downloads panel
    And I click on the file name containing "Bing.html" in the Downloads panel
    Then address bar contains "Bing.html" in the new tab

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56533112
  Scenario: Cancel downloading a webpage file
    Given Edge is launched
    When I navigate to "www.bing.com"
    And I right click on the page without selecting any text or element
    And I click "Save As..." in the context menu
    Then Save As window should appear
    When I click "Cancel" button in Save As window
    Then Save As window should be closed
    And the Downloads panel should not appear

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56446069
  @p0 @regression @download
  Scenario: Pause and Resume download file
    Given Edge is launched
    When I navigate to "https://msedge.sf.dl.delivery.mp.microsoft.com/filestreamingservice/files/2de44c02-6f01-4ed9-85f4-9e958c33f182/MicrosoftEdgeDev-140.0.3430.1.dmg?platform=Mac&channel=Dev&brand=M103&_.%25%E2%80%8B="
    Then the Downloads panel should appear
    When I click Downloads panel
    And I hover over the file name containing "MicrosoftEdgeDev" in the Downloads panel
    And I click the "Pause" button
    Then "Resume" button should be displayed in the Downloads panel
    When I click the "Resume" button
    And I wait for 90 seconds
    Then "Show in Finder" button should be displayed in the Downloads panel
