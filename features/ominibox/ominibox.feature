Feature: ominibox
  As a Microsoft Edge user

  # Note: Vertical tabs are currently not supported.
  # Known issue: [Bug 57975310: win-auto-mcp not support vertical tab](https://microsoft.visualstudio.com/Edge/_workitems/edit/57975310)
  # This issue is under investigation and will be addressed in an upcoming release.

Scenario: Type a website URL and enter to navigate directly to site
Given Edge is launched 
When I input "www.163.com" in address bar
And I press the "Enter" key
Then "163" website should be opened
And the address bar should display the complete URL "https://www.163.com"


Scenario: Search keywords by default Bing engine in address bar
Given Edge is launched
And I open a new tab
When I input "cat" in address bar 
And I press the "Enter" key
Then the tab should jump to the search results page related to "cat"
And the "cat" should be displayed in the Bing search box
	