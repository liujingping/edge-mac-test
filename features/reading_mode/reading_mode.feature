Feature: Reading Mode

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56499879
  @p0 @regression @reading_mode
  Scenario: Can open reading mode normally
    Given Edge is launched
    When I navigate to "https://en.wikipedia.org/wiki/Main_Page"
    And I open Reading Mode
    Then Reading Mode toolbar should appear
    And I can see reading mode icon in the address bar
    And Analyze the screenshot to verify the webpage is in reading mode
    When I click "Exit Immersive Reader" button in Reading Mode toolbar
    Then Reading Mode toolbar should be closed
    And Analyze the screenshot to verify the webpage is exited from reading mode

  # https://microsoft.visualstudio.com/Edge/_workitems/edit/56500049
  @p0 @regression @reading_mode
  Scenario: Read aloud of reading mode work normally
    Given Edge is launched
    When I navigate to "https://en.wikipedia.org/wiki/Main_Page"
    And I open Reading Mode
    Then Reading Mode toolbar should appear
    When I click "Read Aloud" button in Reading Mode toolbar
    Then Read Aloud toolbar should appear
    And I can see playing audio icon in the tab
    And Analyze the screenshot to verify the webpage in shadow mode
    When I click "Pause Read Aloud" button in Read Aloud toolbar
    Then I can see "Continue Read Aloud" button in Read Aloud toolbar
    And Playing audio icon in the tab should disappear
    And Analyze the screenshot to verify the webpage exit shadow mode
    When I click "Exit Immersive Reader" button on address bar
    Then Reading Mode toolbar should be closed

# # https://microsoft.visualstudio.com/Edge/_workitems/edit/56499944
# @p0 @regression @reading_mode
# Scenario: Text preferences of reading mode work normally
# Given Edge is launched
# When I navigate to "https://en.wikipedia.org/wiki/Main_Page"
# And I open Reading Mode
# Then Reading Mode toolbar should appear
# When I click "Text Preferences" button in Reading Mode toolbar
# Then Text Preferences panel should appear
# When I turn on "Text Spacing"
# Then Analyze the screenshot to verify the Text Spacing is increased
# When I click "Comic Sans" in Text Type
# Then Analyze the screenshot to verify the Text Type should change to Comic Sans font
# When I click "Wide column" in Text Column Style
# Then Analyze the screenshot to verify the Text Column Style should change to Wide column
# When I click "More Themes"
# And I click "Orchid" in Page Themes
# Then Analyze the screenshot to verify the Page Themes should change to Orchid theme
# When I press "Esc" key
# Then Text Preferences panel should be closed
