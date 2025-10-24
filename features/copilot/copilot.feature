Feature: Copilot

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59776417
  @p0 @regression @copilot
  Scenario: Typing anything on input box
    Given Edge is launched
    And I open a new tab
    When I click the Copilot icon in the toolbar
    And I wait 3 seconds
    # for Copilot pane to load
    Then the Copilot pane should open
    When I type "What gas do humans need to breathe?" in the copilot pane input box
    Then the copilot pane input box should contain "What gas do humans need to breathe?"
    When I click the "Submit message" button
    And I wait 10 seconds for Copilot to respond
    Then verify the Copilot response should contains the "oxygen"
    When I click the Copilot icon in the toolbar
    Then the Copilot pane should close

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59776442
  @p0 @regression @copilot
  Scenario: Create a new conversation in Copilot
    Given Edge is launched
    And I open a new tab
    When I press "shift+cmd+." to open Copilot pane
    And I wait 3 seconds
    # for Copilot pane to load
    Then the Copilot pane should open
    When I type "microsoft" in the copilot pane input box
    And I click the "Submit message" button
    And I click the "Open actions menu" button
    And I click the "Create new conversation" button
    Then verify the copilot pane input box is empty
    And verify the copilot have no history messages
    When I type "What does CPU mean?" in the copilot pane input box
    And I click the "Submit message" button
    And I wait 10 seconds for Copilot to respond
    Then verify the Copilot response should contains the "Central"
    When I press "shift+cmd+." to close Copilot pane
    Then the Copilot pane should close

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/53656064
  # @p0 @regression @copilot
  # Scenario: Check settings in Copilot
  #   Given Edge is launched
  #   And I open a new tab
  #   When I press "shift+cmd+." to open Copilot pane
  #   Then the Copilot pane should open
  #   And I click the "More options" button
  #   And I click the "Settings" button
  #   Then the "Settings" pane should be opened
  #   When I click the "Privacy" button
  #   Then the "Privacy" page should be opened with context "Context clues"
  #   When I click the "Back" button in privacy page
  #   And I click the "Preferences" button
  #   Then the "Preferences" page should be opened with context "Language"
  #   When I click the "Back" button in preferences page
  #   And I click the "Characters" button
  #   Then the "Characters" page should be opened with context "Mica"
  #   When I click the "Back" button in characters page
  #   And I click the "About" button
  #   Then the "About" page should be opened with context "Your privacy choices"
  #   When I press "shift+cmd+." to close Copilot pane
  #   Then the Copilot pane should close
