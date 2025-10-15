Feature: Copilot

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59776417
  @p0 @regression @copilot
  Scenario: Typing anything on input box
    Given Edge is launched
    And I open a new tab
    When I click the Copilot icon in the toolbar
    Then the Copilot pane should open
    When I type "Commonly used software of Microsoft" in the input box
    Then the input box should contain "Commonly used software of Microsoft"
    When I click the "Submit message" button
    And I click "scroll to bottom" on the Copilot pane
    Then the Copilot response should contains "Windows" or "Office"
    When I click the Copilot icon in the toolbar
    Then the Copilot pane should close

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59776442
  @p0 @regression @copilot
  Scenario: Create a new conversation in Copilot
    Given Edge is launched
    And I open a new tab
    When I click the Copilot icon in the toolbar
    And I type "microsoft" in the input box
    And I click the "Submit message" button
    And I click the "Open actions menu" button
    And I click the "Create new conversation" button
    Then verify the copilot have no conversation history contains "microsoft"
    When I type "Larry Page create what company" in the input box
    And I click the "Submit message" button
    Then the Copilot response should contains  "Google"
    When I click the close button on the Copilot pane
    Then the Copilot pane should close

# # https://microsoft.visualstudio.com/Edge/_workitems/edit/53656064
# @p0 @regression @copilot
# Scenario: Check settings in Copilot
# Given Edge is launched
# And I open a new tab
# When I press "shift+cmd+." to open Copilot pane
# Then the Copilot pane should open
# And I click the "More options" button
# And I click the "Settings" button
# Then the "Settings" pane should be opened
# When I click the "Privacy" button
# Then the "Privacy" page should be opened with context "Context clues"
# When I click the "Back" button in privacy page
# And I click the "Preferences" button
# Then the "Preferences" page should be opened with context "Language"
# When I click the "Back" button in preferences page
# And I click the "Characters" button
# Then the "Characters" page should be opened with context "Mica"
# When I click the "Back" button in characters page
# And I click the "About" button
# Then the "About" page should be opened with context "Your privacy choices"
