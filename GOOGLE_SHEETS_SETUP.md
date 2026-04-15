# Google Sheets Setup

This project can store waitlist submissions in your Google Sheet instead of only saving to `data/waitlist.xlsx`.

Your sheet ID is already wired into [google-apps-script.js](C:/Users/YADAV%20KISHAN%20KUMAR/OneDrive/Desktop/waitlist/google-apps-script.js).

## 1. Create the Google Apps Script

1. Open your Google Sheet:
   `https://docs.google.com/spreadsheets/d/1qIMpXTC4rck-rtupmevuqWOZZQJA07wEOWRaNz9hf8U/edit`
2. Click `Extensions` -> `Apps Script`.
3. Replace the default code with the contents of [google-apps-script.js](C:/Users/YADAV%20KISHAN%20KUMAR/OneDrive/Desktop/waitlist/google-apps-script.js).
4. Save the script.

## 2. Deploy it as a Web App

1. Click `Deploy` -> `New deployment`.
2. Choose `Web app`.
3. Set `Execute as` to your Google account.
4. Set access to `Anyone`.
5. Deploy and copy the Web App URL.

## 3. Run this project with Google Sheets storage

In PowerShell:

```powershell
$env:STORAGE_MODE="google"
$env:GOOGLE_SHEETS_WEBHOOK_URL="PASTE_YOUR_WEB_APP_URL_HERE"
npm start
```

If you want both Google Sheets and local Excel backup:

```powershell
$env:STORAGE_MODE="google+excel"
$env:GOOGLE_SHEETS_WEBHOOK_URL="PASTE_YOUR_WEB_APP_URL_HERE"
npm start
```

## Modes

- `excel`: save only to `data/waitlist.xlsx`
- `google`: save only to Google Sheets
- `google+excel`: save to both Google Sheets and Excel
