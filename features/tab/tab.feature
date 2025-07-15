Feature: tab

Scenario: Close a tab in horizontal mode
 Given Edge is launched in horizontal mode
 When I navigate to "https://www.apple.com"
 And I click the "Close Tab" button on tab header
 Then the "Apple" tab should be closed


Scenario: Drag a tab in horizontal mode
Given Edge is launched in horizontal mode
When I navigate to "https://www.github.com"
And I new a tab
And I navigate to "https://www.microsoft.com"
And I drag the "Microsoft" tab to the left of the "Github" tab
Then tab order should be "Microsoft", "Github"
 