# Slack Activity Log

This project tracks Slack presence, saves the results into date-based log files, and plots the activity as a heatmap.

## Project Files

- `monitor.js` checks the Slack page once per minute and logs whether the user looks active or offline.
- `download.js` turns the in-memory log into a CSV-style text file.
- `split_log.py` reads `slack_activity_log.txt` and writes one file per day into `logs/`.
- `main.py` opens a date picker, splits the log, then shows the selected day as a matplotlib heatmap.

## Log Format

The exported file uses a simple two-column format:

```text
timestamp,active
2026-06-04 20:00:36,0
2026-06-04 20:01:36,1
2026-06-04 20:02:36,0
```

`split_log.py` saves rows into files named like `logs/2026-06-04.txt`. If the same date already exists, new rows are appended without duplicating timestamps.

## Requirements

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

The project uses `pandas`, `numpy`, and `matplotlib`. `tkinter` is part of the Python standard library.

## How to Use It


1. Open Slack in your browser and go to the page you want to monitor. Open the profile of the user you want to keep a log of like this:
   
   <img width="1846" height="912" alt="image" src="https://github.com/user-attachments/assets/6abaf9ef-35b1-4a13-88e5-764e1f1be5a6" />

2. Open the browser Developer Tools console.
3. Paste the contents of `monitor.js` into the Console and press Enter.
4. Leave the tab open while monitoring is running.
5. When you are done, paste the contents of `download.js` into the same Console.
6. Run `downloadLog()` in the console to download `slack_activity_log.txt`.
7. Run `main.py` to pick a date, split the log into `logs/`, and display the heatmap.

## Heatmap Screenshot

<img width="1920" height="1030" alt="image" src="https://github.com/user-attachments/assets/208d9ae3-886c-4b90-9d9c-7ce5b9447d86" />


Here,

- 🟩 Green → Active
- ⬛ Black → Away
- ⬜ Grey → No logs


## Console Shortcuts

- Windows/Linux: `Ctrl + Shift + I`
- macOS: `Cmd + Option + I`
- Or press `F12`

Then click the `Console` tab.

## Notes

- Keep the same Slack tab open while monitoring. The log lives in the page session, so refreshing or closing the tab resets it.
- Run `download.js` in the same tab where you ran `monitor.js`.
- If Slack changes its layout, the status check may stop finding the presence element.
- `monitor.js` records timestamps in local time using the IANA timezone `"Asia/Dhaka"` by default. Change the `timeZone` value in `monitor.js` if you want a different timezone.

## Common Problems

### It will not let me paste code

Some browsers block pasting into DevTools Console until you allow it.

- Click inside the Console.
- Type `allow pasting` and press Enter if the browser asks for it.
- Try pasting again.

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

## What the Values Mean

- `1` means the status looked active or online.
- `0` means the status looked inactive or offline.

## How It Works

`monitor.js` stores each sample in an array called `activityLog`, then prints a CSV row to the console each time it checks Slack.

`download.js` reads that same array and downloads it as a text file.

`main.py` uses the saved log files under `logs/`, lets you pick or type a date, and plots that date as a heatmap.
