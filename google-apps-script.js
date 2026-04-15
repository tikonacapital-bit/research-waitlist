function doPost(e) {
  const sheet = SpreadsheetApp.openById("1qIMpXTC4rck-rtupmevuqWOZZQJA07wEOWRaNz9hf8U").getSheets()[0];
  const payload = JSON.parse(e.postData.contents || "{}");

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(["Timestamp", "Email", "Phone", "Source"]);
  }

  sheet.appendRow([
    payload.submittedAt || new Date().toISOString(),
    payload.email || "",
    payload.phone || "",
    payload.source || "website"
  ]);

  return ContentService
    .createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}
