Feature: Settings Privacy

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/59203294
  @regression @p0 @settings
  Scenario: Click Allow button to allow website location
    Given Edge is launched
    When I navigate to "https://www.weather.com"
    Then the "weather.com wants to:know you location" dialog should appear
    When I click "Allow" button on the "weather.com wants to:know you location" dialog
    Then the "weather.com wants to:know you location" dialog should be closed
    When I navigate to "edge://settings/privacy/sitePermissions/allPermissions/location"
    Then the website "https://weather.com:443" should be listed under "Allowed to see your location"
