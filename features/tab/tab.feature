Feature: tab

Scenario: Close a tab in horizontal mode
 Given Edge is launched in horizontal mode
 When I navigate to "https://www.apple.com"
 And I click the "Close Tab" button on tab header
 Then the "Apple" tab should be closed