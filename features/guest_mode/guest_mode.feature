Feature: guest_mode

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59105773
  @p0 @regression @guest_mode
  Scenario: Bookmarks/Favorites isolation in Guest mode
    Given Edge is launched
    When I press "cmd" and "alt" and "B" keys
    Then I can see Favorites panel should appear
    When I open Guest browsing mode
    Then Guest Window should be opened
    When I press "cmd" and "alt" and "B" keys
    Then Favorites panel should not appear

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59105767
  @p0 @regression @guest_mode
  Scenario: Browsing history isolation in Guest mode
    Given Edge is launched
    When I open Guest browsing mode
    Then Guest Window should be opened
    When I navigate to "https://www.bing.com"
    And I navigate to "https://www.baidu.com"
    And I press "cmd" and "Y" keys
    Then History panel should not appear
    When I close the Guest Window
    Then Guest Window should be closed
    When I press "cmd" and "Y" keys
    Then "https://www.bing.com" should not be displayed in History panel
    And "https://www.baidu.com" should not be displayed in History panel

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59105778
  @p0 @regression @guest_mode
  Scenario: Settings isolation in Guest mode
    Given Edge is launched
    When I open Guest browsing mode
    Then Guest Window should be opened
    When I navigate to "edge://settings/privacy/services/search/searchEngines"
    And I click "More actions" button for "Google"
    And I click "Make default" button for "Google"
    Then I can see "Google" is default search engine
    When I close the Guest Window
    Then Guest Window should be closed
    When I navigate to "edge://settings/privacy/services/search/searchEngines"
    Then I can see "Google" is not default search engine
