Feature: PWA China

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56211432
  Scenario: Install and open PWA from Facebook
    Given Edge is launched
    When I navigate to "https://www.facebook.com"
    And I click the install button in address bar
    Then The "Install Facebook App" dialog should be shown
    When I click the install button in the "Install Facebook App" dialog
    Then Analyze the screenshot to verify the installed "Facebook" app should be opened
    When I close and restart Edge
    And I navigate to "edge://apps"
    Then The "Facebook" app should be shown in the apps list

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59729025
  Scenario: Uninstall PWA from Facebook
    Given Edge is launched
    When I navigate to "https://www.facebook.com"
    And I click the install button in address bar
    Then The "Install Facebook App" dialog should be shown
    When I click the install button in the "Install Facebook App" dialog
    And I close and restart Edge
    And I navigate to "edge://apps"
    Then The "Facebook" app should be shown in the apps list
    When I click "More Options" on the right coner of the Facebook app
    And I click "Uninstall" button from the dropdown menu
    Then The "Uninstall app from Microsoft Edge on all synced devices?" dialog should be shown
    When I click the check box of "Delete app history and data" in the Uninstall Facebook dialog
    And I click the "Uninstall" button
    Then verify the "Facebook" app is not shown in the apps list
