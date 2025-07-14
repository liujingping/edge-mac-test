Feature: tab

Scenario: Close a tab in horizontal mode
 Given Edge is launched in horizontal mode
 When I navigate to "https://www.apple.com"
 And I click the "Close Tab" button on tab header
 Then the "Apple" tab should be closed


Scenario: Drag a tab in horizontal mode
Given Edge is launched in horizontal mode
When I navigate to "https://www.apple.com"
And I new a tab and navigate to "https://163.com"
And I drag the "网易" tab to the far left of the "Apple" tab
Then "网易" tab is on the left, "Apple" tab is on the right
 