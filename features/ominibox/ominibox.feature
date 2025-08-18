Feature: ominibox
  As a Microsoft Edge user

  # Note: Vertical tabs are currently not supported.
  # Known issue: [Bug 57975310: win-auto-mcp not support vertical tab](https://microsoft.visualstudio.com/Edge/_workitems/edit/57975310)
  # This issue is under investigation and will be addressed in an upcoming release.
  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56908756
  @p0
  Scenario: Type a website URL and enter to navigate directly to site
    Given Edge is launched
    When I input "www.163.com" in address bar
    And I press the "Enter" key
    Then "163" website should be opened
    And the address bar should display the complete URL "https://www.163.com"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56908765
  @p0
  Scenario: Search keywords by default Bing engine in address bar
    Given Edge is launched
    And I open a new tab
    When I input "cat" in address bar
    And I press the "Enter" key
    And the page title should be "cat - Search"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56908759
  @p0
  Scenario: Type URL by autocompleting to navigate directly to site
    Given Edge is launched
    When I navigate to "https://www.apple.com"
    And I open a new tab
    When I type "www.app" in the address bar
    And I press the "Enter" key
    Then I should navigate to "https://www.apple.com" successfully
    And the address bar should display the complete URL "https://www.apple.com"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56908761
  @p0
  Scenario: Edit all URL to navigate to new site
    Given Edge is launched
    When I type "https://www.google.com" in the address bar
    And the address bar should display the complete URL "https://www.google.com"
    When I select all text in the address bar
    And I type "https://www.apple.com" in the address bar
    And I press the "Enter" key
    Then I should navigate to "https://www.apple.com" successfully
    And the address bar should display the complete URL "https://www.apple.com"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56908757
  @p0
  Scenario: Navigate to website by selecting from dropdown suggestions
    Given Edge is launched
    And I open a new tab
    When I type "www.apple.com" in the address bar
    Then a dropdown list should appear with URL suggestions
    When I click the top item "www.apple.com" in the dropdown list
    Then I should navigate to "https://www.apple.com" successfully
    And the address bar should display the complete URL "https://www.apple.com"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/58491144
  @p0
  Scenario: Navigate using partial URL without protocol
    Given Edge is launched
    When I input "apple.com" in address bar
    And I press the "Enter" key
    Then I should navigate to "https://www.apple.com" successfully
    And the address bar should display the complete URL "https://www.apple.com"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56908761
  @p0
  Scenario: Delete and edit all URL to navigate to new site
    Given Edge is launched
    When I navigate to "https://www.apple.com"
    And the address bar should display the complete URL "https://www.apple.com"
    When I select all text in address bar
    And I press the "Backspace" key
    And I input "www.expedia.com" in address bar
    And I press the "Enter" key
    Then I should navigate to "Expedia" page successfully
    And the address bar should display the complete URL "https://www.expedia.com"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56909857
  @p0
  Scenario: Use the shortcut key to copy or cut then paste part URL in address bar
    Given Edge is launched
    When I input "apple" in address bar
    And I select all in address bar
    And I press "cmd+C" to copy the selected text
    And I open a new tab
    And I press "cmd+V" to paste the copied text
    Then "apple" should be displayed in the address bar
    And I select all in address bar
    And I press "cmd+X" to cut the selected text
    And I open a new tab again
    And I press "cmd+V" to paste the cut text
    Then "apple" should be displayed in the address bar

# https://microsoft.visualstudio.com/Edge/_workitems/edit/56908764
# exisiting bug: Bug 50786254: [Mac] The shortcut keys for Redo are the same as the shortcut keys for opening history.
# @p0
# Scenario: Use the shortcut keyboard to Copy,Cut,Undo,Redo,Paste all URL in address bar
# Given edge is launched
# When I navigate to "https://www.apple.com"
# And the address bar should display the complete URL "https://www.apple.com"
# When I select all text in address bar
# And I press "delete" to delete the selected text
# Then the address bar should be empty
# When I press "cmd+Z" to undo the delete action
# Then "https://www.apple.com" should be displayed in the address bar
# When I press "cmd+Y" to redo the delete action
# Then the address bar should be empty
