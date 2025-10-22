Feature: Split Screen

    # https://microsoft.visualstudio.com/Edge/_workitems/edit/58971665
    @p0 @regression @split_screen
    Scenario: Click "X" button on the left screen on horizontal tab
        Given Edge is launched
        When I navigate to "https://www.bing.com"
        And I open Split Screen
        Then Split Screen icon should appear in toolbar
        When I navigate to "https://www.apple.com" on right screen
        And I hover on Microsoft Bing screen
        Then I can see "Close split screen" button on Microsoft Bing screen
        When I click "Close split screen" button on Microsoft Bing screen
        Then Split Screen icon should disappear from toolbar
        And I can not see tab name contains "Microsoft Bing"

    # # https://microsoft.visualstudio.com/Edge/_workitems/edit/58971654
    # @p0 @regression @split_screen
    # Scenario: Click the left URL on address bar
    # Given Edge is launched
    # When I navigate to "https://www.bing.com"
    # And I open Split Screen
    # And I navigate to "https://www.apple.com" on right screen
    # Then Analyze the screenshot to verify the right screen is focused
    # When I click Microsoft Bing URL on address bar
    # Then Analyze the screenshot to verify the left screen is focused
    # When I navigate to "https://www.office.com"
    # Then Analyze the screenshot to verify left screen is "Office"

    # https://microsoft.visualstudio.com/Edge/_workitems/edit/58971651
    @p0 @regression @split_screen
    Scenario: Enter some keywords in the search box on horizontal tab
        Given Edge is launched
        When I open Split Screen
        And I click "Search or enter web address" box on right screen
        And I type "work" on right screen
        When I press "Enter" key on right screen
        Then I can see right screen tab name contains "work"

    # https://microsoft.visualstudio.com/Edge/_workitems/edit/58971661
    @p0 @regression @split_screen
    Scenario: Link tabs from left screen to right screen on horizontal tab
        Given Edge is launched
        When I navigate to "https://www.bing.com"
        And I open Split Screen
        Then Split Screen icon should appear in toolbar
        When I turn on "Open Left link To The right" button
        And I click on the "Images" button on Microsoft Bing screen
        Then I can see right screen tab name contains "Bing Images"

    # https://microsoft.visualstudio.com/Edge/_workitems/edit/58971652
    @p0 @regression @split_screen
    Scenario: Open this webpage in a new tab on horizontal tab
        Given Edge is launched
        When I navigate to "https://www.bing.com"
        And I open Split Screen
        Then Split Screen icon should appear in toolbar
        When I navigate to "https://www.apple.com" on right screen
        And I hover on Microsoft Bing screen
        Then I can see "More options" button on Microsoft Bing screen
        When I click "More options" button on Microsoft Bing screen
        And I click "Open This Webpage In A New Tab" button on Microsoft Bing screen
        Then I can see new tab name contains "Microsoft Bing"

    # https://microsoft.visualstudio.com/Edge/_workitems/edit/58971653
    @p0 @regression @split_screen
    Scenario: Separate two tabs on vertical tab
        Given Edge is launched
        When I right click on the tab
        And click "Turn On Vertical Tabs"
        And I press escape to close popup
        Then Analyze the screenshot to verify vertical tabs are enabled
        When I navigate to "https://www.bing.com"
        And I open Split Screen
        Then Split Screen icon should appear in toolbar
        When I navigate to "https://www.apple.com" on right screen
        And I hover on Microsoft Bing screen
        Then I can see "More options" button on Microsoft Bing screen
        When I click "More options" button on Microsoft Bing screen
        And I click "Separate Two Tabs" button on Microsoft Bing screen
        Then Split Screen icon should disappear from toolbar
        And I can see tab name contains "Microsoft Bing"
        And I can see tab name contains "Apple"

    # https://microsoft.visualstudio.com/Edge/_workitems/edit/58971657
    @p0 @regression @split_screen
    Scenario: Switch left and right tabs on vertical tab
        Given Edge is launched
        When I right click on the tab
        And click "Turn On Vertical Tabs"
        And I press escape to close popup
        Then Analyze the screenshot to verify vertical tabs are enabled
        When I navigate to "https://www.bing.com"
        And I open Split Screen
        Then Split Screen icon should appear in toolbar
        When I navigate to "https://www.apple.com" on right screen
        And I hover on Microsoft Bing screen
        Then I can see "More options" button on Microsoft Bing screen
        When I click "More options" button on Microsoft Bing screen
        And I click "Switch Left and Right Tabs" button on Microsoft Bing screen
        Then Analyze the screenshot to verify left screen is "Apple"
        And Analyze the screenshot to verify right screen is "Microsoft Bing"

    # https://microsoft.visualstudio.com/Edge/_workitems/edit/58971658
    @p0 @regression @split_screen
    Scenario: Split screen horizontally on vertical tab
        Given Edge is launched
        When I right click on the tab
        And click "Turn On Vertical Tabs"
        And I press escape to close popup
        Then Analyze the screenshot to verify vertical tabs are enabled
        When I navigate to "https://www.bing.com"
        And I open Split Screen
        Then Split Screen icon should appear in toolbar
        When I navigate to "https://www.apple.com" on right screen
        And I hover on Microsoft Bing screen
        Then I can see "More options" button on Microsoft Bing screen
        When I click "More options" button on Microsoft Bing screen
        And I click "Switch To Vertical" button on Microsoft Bing screen
        Then Analyze the screenshot to verify top screen is "Microsoft Bing"
        And Analyze the screenshot to verify bottom screen is "Apple"
