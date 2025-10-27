Feature: Right_click

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56422520
  @p0 @regression @right_click
  Scenario: Back/Forward to the next page using the right click menu
    Given Edge is launched
    When I navigate to "https://www.bing.com"
    And I navigate to "https://www.sina.com.cn"
    And I right click on the page without selecting any text or element
    And I click "Back" in the context menu
    Then I should be on "https://www.bing.com"
    When I right click on the page without selecting any text or element
    And I click "Forward" in the context menu
    Then I should be on "https://www.sina.com.cn"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56423043
  @p0 @regression @right_click
  Scenario: Cut the input using right click menu
    Given Edge is launched
    When I input "microsoft" in the address bar
    And I select "microsoft" in the address bar
    And I right click on the address bar
    And I click "Cut" in the context menu
    Then The address bar is empty
    When I open a new tab
    And I right click on the address bar
    And I click "Paste" in the context menu
    Then The address bar contains "microsoft"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56479238
  @p0 @regression @right_click
  Scenario: Open link in InPrivate Window using right click menu
    Given Edge is launched
    When I navigate to "https://www.bing.com"
    And I right click on the "News"
    And I click "Open in InPrivate Window" in the context menu
    Then InPrivate Window should be opened
    And I can see tab name contains "News"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/57944617
  @p0 @regression @right_click
  Scenario: Open link in new tab using right click menu
    Given Edge is launched
    When I navigate to "https://www.bing.com"
    And I right click on the "Maps"
    And I click "Open Link in New Tab" in the context menu
    Then I can see new tab name contains "Maps" in new tab

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56422540
  @p0 @regression @right_click
  Scenario: Refresh the page using the right click menu
    Given Edge is launched
    When I navigate to "https://www.bing.com"
    And I right click on the page without selecting any text or element
    And I click "Refresh" in the context menu
    Then I should be on "https://www.bing.com"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59939600
  @p0 @regression @right_click @mini_menu
  Scenario: Copy /Paste the selected text by mini menu
    Given Edge is launched
    When I navigate to "https://example.com/"
    And I select the text "Domain" in this webpage
    And I click "Copy" in the mini menu popup
    And I open a new tab
    And I right click on the address bar
    And I click "Paste" in the context menu
    Then verify the address bar should contains "Domain"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59262254
  @p0 @regression @right_click @mini_menu
  Scenario: Search the web for the selected text by mini menu
    Given Edge is launched
    When I navigate to "https://example.com/"
    And I select the text "Domain" in this webpage
    And I click "Search" in the mini menu popup
    And I wait 3 seconds
    # for page loading, wait 3s
    Then verify a tab title contains "Domain" should be opened
    And verify the address bar should contains "Domain"

  # # https://microsoft.visualstudio.com/Edge/_workitems/edit/59262254
  # @p0 @regression @right_click @mini_menu
  # Scenario: Ask copilot for the selected text using right click mini menu
  # Given Edge is launched
  # When I navigate to "https://example.com/"
  # And I select the text "Domain" in this webpage
  # And I click "Ask Copilot" in the mini menu popup
  # Then the Copilot pane should open
  # When I click the Copilot icon in the toolbar
  # Then the Copilot pane should close
  # When I select the text "Domain" in this webpage
  # And I click "Ask Copilot" in the mini menu popup
  # Then the Copilot pane should open
  # And I click the "Continue" button in the copilot pane
  # When I click the Copilot icon in the toolbar
  # Then the Copilot pane should close
  # When I select the text "Domain" in this webpage
  # And I click "Ask Copilot" in the mini menu popup
  # Then the Copilot pane should open
  # And I wait 10 seconds for Copilot to respond
  # And verify the question I asked should contains "Domain"
  # And verify the copilot response should contains "Domain"
  # When I press "shift+cmd+." to close Copilot pane
  # Then the Copilot pane should close
  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56422923
  @p0 @regression @right_click @mini_menu
  Scenario: Copy /Paste the selected text using right click menu
    Given Edge is launched
    When I navigate to "edge://settings/appearance/contextMenus"
    And I click the "Show mini menu when selecting text" toggle button to disable it
    Then Analyze the screenshot to verify the colour of the "Show mini menu when selecting text" toggle button is greyed out
    When I open a new tab
    And I navigate to "https://example.com/"
    And I select the text "Domain" in this webpage
    And I right click on the "Domain"
    And I click "Copy" in the context menu
    And I press "cmd+t" to open a new tab
    And I right click on the address bar
    And I click "Paste" in the context menu
    Then verify the address bar should contains "Domain"

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56422911
  @p0 @regression @right_click @mini_menu
  Scenario: Search the web for the selected using right click menu
    Given Edge is launched
    When I navigate to "edge://settings/appearance/contextMenus"
    And I click the "Show mini menu when selecting text" toggle button to disable it
    Then Analyze the screenshot to verify the colour of the "Show mini menu when selecting text" toggle button is greyed out
    When I open a new tab
    And I navigate to "https://example.com/"
    And I select the text "Domain" in this webpage
    And I right click on the "Domain"
    And I click Search the Web for "Domain" in the context menu
    And I wait 3 seconds
    # for page loading, wait 3s
    Then verify a tab title contains "Domain" should be opened
    And verify the address bar should contains "Domain"
