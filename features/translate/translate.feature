Feature: Translate functionality in Microsoft Edge

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56473119
  @p0 @regression @translate
  Scenario: Show Translation popup when display language=EN and visit non-EN websites
    Given Edge is launched
    When I navigate to "www.sina.com.cn"
    Then Translate popup should appear
    When I click "Translate" button in Translate popup
    Then webpage should be displayed in English language
    When I click "Translated" button on the address bar
    And I select "Show original" in Translate popup
    Then webpage should be displayed in Chinese language
    And Translate popup should be closed

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56473134
  @p0 @regression @translate
  Scenario: Translate by right-clicking menu when display language=EN and browse non-EN websites
    Given Edge is launched
    When I navigate to "www.sina.com.cn"
    And I right click on the page without selecting any text or element
    And I select "Translate to English" on context menu
    Then webpage should be displayed in English language
