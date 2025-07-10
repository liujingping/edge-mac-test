Feature: download
  
Scenario: Download PDF file
  Given Edge is launched
  When I navigate to "https://getsamplefiles.com/download/pdf/sample-1.pdf"
  Then the Downloads pane should appear
  When I navigate to "edge://downloads"
  Then "sample-1.pdf" should appear in download list