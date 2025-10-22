# Feature: Online PDF
# # https://microsoft.visualstudio.com/Edge/_workitems/edit/56445945
# Scenario: Directly close online PDF tab after modifying pdf
# Given Edge is launched
# When I navigate to "https://www.adobe.com/support/products/enterprise/knowledgecenter/media/c4611_sample_explain.pdf"
# Then The tab title containing "PDF Bookmark Sample" is opened
# When I click "Draw" button in the PDF viewer toolbar
# And I select text containing "May 2001" in the PDF
# Then Analyze the screenshot to verify the selected text is drawn with blue color
# When I press "Cmd+W" keys
# Then The leave site dialog should be shown
# When I click "Leave" button in the leave site dialog
# Then The "PDF Bookmark Sample" tab should be closed
# # https://microsoft.visualstudio.com/Edge/_workitems/edit/56445852
# Scenario: Erase highlight and save in online PDF
# Given Edge is launched
# When I navigate to "https://www.adobe.com/support/products/enterprise/knowledgecenter/media/c4611_sample_explain.pdf"
# Then The tab title containing "PDF Bookmark Sample" is opened
# When I click "Highlight" button in the PDF viewer toolbar
# And I select text containing "May 2001" in the PDF
# Then Analyze the screenshot to verify the selected text is highlighted
# When I click "Erase" button in the PDF viewer toolbar
# And I select text containing "May 2001" in the PDF
# Then Analyze the screenshot to verify the selected text highlighting is removed
# When I click "Save" button in the PDF viewer toolbar
# Then The "Save" dialog should be shown
# When I click "Save" button in the "Save" dialog
# Then The tab title containing "c4611_sample_explain.pdf" is opened
