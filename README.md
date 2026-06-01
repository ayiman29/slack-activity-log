# Slack Activity Log

This folder contains two small browser-console scripts for tracking Slack presence and exporting the captured activity as a downloadable file.

## What each script does

- `monitor.js` checks the Slack page once per minute and logs whether the user looks active or offline.
- `download.js` turns the in-memory log into a CSV-style text file you can save locally.

The exported file looks like this:

```text
timestamp,active
2026-06-01T14:00:33.426Z,1
2026-06-01T14:01:34.007Z,1
2026-06-01T14:02:33.439Z,1
2026-06-01T14:03:34.007Z,0
```

## How to use it

1. Open Slack in your browser and go to the page you want to monitor. Open the profile of the user you want to keep a log of like this:
   
   <img width="1920" height="919" alt="image" src="https://github.com/user-attachments/assets/71dd9c3a-8a46-44a3-a47e-90dbd3b0e7e7" />


2. Open the browser Developer Tools console.
3. Paste the contents of `monitor.js` into the Console and press Enter.
4. Leave the tab open while monitoring is running.
5. When you are done, paste the contents of `download.js` into the same Console.
6. The browser will download `slack_activity_log.txt`.

## How to open the Console

Use one of these shortcuts:

- Windows/Linux: `Ctrl + Shift + I`
- macOS: `Cmd + Option + I`
- Or press `F12`

Then click the `Console` tab.

## Important notes

- Keep the same Slack tab open while monitoring. The log lives in the page session, so refreshing or closing the tab resets it.
- Run `download.js` in the same tab where you ran `monitor.js`.
- If Slack changes its layout, the status check may stop finding the presence element.

## Common problems

### It will not let me paste code

Some browsers block pasting into DevTools Console until you allow it.

- Click inside the Console.
- Type `allow pasting` and press Enter if the browser asks for it.
- Try pasting again.

If that still does not work, make sure the Console tab is focused and that the browser is not showing a security warning above the prompt.

### I see `Status element not found`

That usually means Slack changed its page structure or the expected status element is not visible on the page you opened.

- Stay on the main Slack page.
- Refresh Slack and run `monitor.js` again.
- If the message keeps appearing, the selector in `monitor.js` may need to be updated.

### `download.js` does nothing

This usually means `monitor.js` was not run first in the current tab, or the tab was refreshed.

- Run `monitor.js` again first.
- Then run `download.js` in the same tab.

### The downloaded file is empty

That means the monitor did not capture any samples yet.

- Wait at least one minute after running `monitor.js`.
- Then run `download.js` again.

## What the values mean

- `1` means the status looked active or online.
- `0` means the status looked inactive or offline.

## How it works

`monitor.js` stores each sample in an array called `activityLog`, then prints a CSV row to the console each time it checks Slack. `download.js` reads that same array and downloads it as a text file.

Because the data is stored in the page session, the simplest workflow is:

1. Run `monitor.js`.
2. Leave the Slack tab open.
3. When finished, run `download.js`.
