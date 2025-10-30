Feature: New Copilot

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59983733
  @p0 @regression @copilot
  Scenario: Turn on Copilot Mode from Settings and open Copilot pane
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
