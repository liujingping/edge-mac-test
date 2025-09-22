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
