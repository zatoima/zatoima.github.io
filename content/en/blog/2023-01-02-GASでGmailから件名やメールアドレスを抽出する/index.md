---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Extracting Subjects and Email Addresses from Gmail with GAS"
subtitle: ""
summary: " "
tags: ["GAS"]
categories: ["GAS"]
url: gas-mail-address-list
date: 2023-01-02
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

### Overview

Using Google Apps Script (GAS) to extract email subjects and sender addresses from starred Gmail messages and output them to a Google Spreadsheet.

### GAS Code

```javascript
function extractStarredEmails() {
  // Get starred threads
  var threads = GmailApp.getStarredThreads();

  // Get active spreadsheet
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

  // Write header row
  sheet.getRange(1, 1).setValue("Subject");
  sheet.getRange(1, 2).setValue("From");
  sheet.getRange(1, 3).setValue("Date");

  var row = 2;

  for (var i = 0; i < threads.length; i++) {
    var messages = threads[i].getMessages();

    for (var j = 0; j < messages.length; j++) {
      var message = messages[j];

      // Extract subject, sender, and date
      var subject = message.getSubject();
      var from = message.getFrom();
      var date = message.getDate();

      // Write to spreadsheet
      sheet.getRange(row, 1).setValue(subject);
      sheet.getRange(row, 2).setValue(from);
      sheet.getRange(row, 3).setValue(date);

      row++;
    }
  }

  Logger.log("Extraction complete. " + (row - 2) + " messages processed.");
}
```

### Usage

1. Open Google Spreadsheet
2. Go to **Extensions > Apps Script**
3. Paste the code above
4. Click **Run**
5. Grant necessary permissions when prompted
6. The script will extract all starred email subjects and addresses to the spreadsheet

### Notes

- `GmailApp.getStarredThreads()` retrieves all starred threads
- By default, it retrieves up to 500 threads; use the second parameter to specify a limit:
  ```javascript
  var threads = GmailApp.getStarredThreads(0, 100); // Start at 0, get 100
  ```
- `message.getFrom()` returns the full sender string including name and email address (e.g., `"John Doe <john@example.com>"`)
- To extract just the email address, parse the string:
  ```javascript
  var fromFull = message.getFrom();
  var emailMatch = fromFull.match(/<(.+)>/);
  var email = emailMatch ? emailMatch[1] : fromFull;
  ```

### Reference

- [GmailApp | Apps Script | Google Developers](https://developers.google.com/apps-script/reference/gmail/gmail-app)
