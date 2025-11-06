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

  Scenario: Turn on Copilot Mode from Settings and open flex pane
    Given Edge is launched
    When I open a new tab
    And I click "Settings and more" button on toolbar
    And I select "Settings" button from the dropdown menu
    And I click "AI innovations" tab in the left sidebar
    And I click "Explore Copilot Mode" button
    And I wait 10 seconds
    # for Copilot welcome page to load
    Then verify a tab name contains "Copilot Mode" is opened
    When I click "Turn on Copilot Mode" button on the copilot mode page
    And I open a new tab
    When I click the new copilot -chat icon in the toolbar
    And I wait 3 seconds
    Then the Copilot flex pane should open
    When I press "shift+cmd+." to close Copilot pane
    Then the Copilot flex pane should close