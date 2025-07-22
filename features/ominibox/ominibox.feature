Feature: ominibox
  As a Microsoft Edge user

  # Note: Vertical tabs are currently not supported.
  # Known issue: [Bug 57975310: win-auto-mcp not support vertical tab](https://microsoft.visualstudio.com/Edge/_workitems/edit/57975310)
  # This issue is under investigation and will be addressed in an upcoming release.
  Scenario: Type a website URL and enter to navigate directly to site
    Given Edge is launched
    When I input "www.163.com" in address bar
    And I press the "Enter" key
    Then "163" website should be opened
    And the address bar should display the complete URL "https://www.163.com"

  Scenario: Search keywords by default Bing engine in address bar
    Given Edge is launched
    And I open a new tab
    When I input "cat" in address bar
    And I press the "Enter" key
    Then the tab should jump to the search results page related to "cat"
    And the "cat" should be displayed in the Bing search box

  Scenario: Type URL by autocompleting to navigate directly to site
    Given I have visited "https://www.apple.com"
    And I open a new tab
    When I type "www.app" in the address bar
    And I press the "Enter" key
    Then I should navigate to "https://www.apple.com" successfully
    And the address bar should display the complete

  Scenario: Edit all URL to navigate to new site
    Given Edge is launched
    When I type "https://www.google.com" in the address bar
    And the address bar should display the complete URL "https://www.google.com"
    When I select all text in the address bar
    And I type "https://www.apple.com" in the address bar
    And I press the "Enter" key
    Then I should navigate to "https://www.apple.com" successfully
    And the address bar should display the complete URL "https://www.apple.com"
