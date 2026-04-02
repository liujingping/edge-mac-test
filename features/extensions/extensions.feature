Feature: Extensions

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59105807
  @P0 @Regression @Extensions
  Scenario: Install iCloud Passwords extension
    Given Edge is launched
    When I navigate to "edge://extensions"
    And I click "Get extensions for Microsoft Edge" button in "Find new extensions"
    Then the website tab with title containing "Microsoft Edge Add-ons" should be opened
    When I click on "Search extensions, themes, and more" in "Microsoft Edge Add-ons" website
    And I input "icloud" into search box
    And I press Enter key
    And I click on "iCloud Passwords" extension in search results
    Then the website tab with title containing "iCloud Passwords" should be opened
    When I click "Get" button in "iCloud Passwords" website
    Then the Add "iCloud Passwords" to Microsoft Edge dialog should be shown
    When I click "Add Extension" button in Add "iCloud Passwords" to Microsoft Edge dialog
    Then the Add "iCloud Passwords" to Microsoft Edge dialog should be closed
    And the "iCloud passwords is now installed." dialog should be shown
    When I navigate to "edge://extensions" again
    Then "iCloud Passwords" should be shown in "Install extensions"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59105853
  @P0 @Regression @Extensions
  Scenario: Remove iCloud Passwords extension
    Given Edge is launched
    When I navigate to "https://microsoftedge.microsoft.com/addons/detail/icloud-passwords/mfbcdcnpokpoajjciilocoachedjkima"
    Then the website tab with title containing "iCloud Passwords" should be opened
    When I click "Get" button in "iCloud Passwords" website
    Then the Add "iCloud Passwords" to Microsoft Edge dialog should be shown
    When I click "Add Extension" button in Add "iCloud Passwords" to Microsoft Edge dialog
    Then the Add "iCloud Passwords" to Microsoft Edge dialog should be closed
    And the "iCloud passwords is now installed." dialog should be shown
    When I navigate to "edge://extensions"
    Then "iCloud Passwords" should be shown in "Install extensions"
    When I click "Remove" button in "iCloud Passwords" card
    And I click "Remove" button in Remove "iCloud Passwords" from Microsoft Edge dialog
    Then "iCloud Passwords" should be removed from "Install extensions"
