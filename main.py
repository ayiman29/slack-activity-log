from datetime import date, datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap

from split_log import split_log


SOURCE_LOG = Path("slack_activity_log.txt")
LOGS_DIR = Path("logs")


def collect_available_dates() -> list[str]:
    dates = {
        path.stem
        for path in LOGS_DIR.glob("*.txt")
        if len(path.stem) == 10
    }
    dates.add(date.today().isoformat())
    return sorted(dates)


def prompt_for_date() -> str:
    available_dates = collect_available_dates()
    default_date = date.today().isoformat()

    if default_date not in available_dates:
        available_dates.append(default_date)
        available_dates = sorted(set(available_dates))

    selected_date = {"value": default_date}

    root = tk.Tk()
    root.title("Select Activity Date")
    root.resizable(False, False)
    root.geometry("320x120")

    frame = ttk.Frame(root, padding=12)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Choose a date:").pack(anchor="w")

    combo_value = tk.StringVar(value=default_date)
    combo = ttk.Combobox(frame, values=available_dates, textvariable=combo_value, state="normal")
    combo.pack(fill="x", pady=(6, 10))

    def confirm() -> None:
        candidate = combo.get().strip() or default_date
        try:
            datetime.strptime(candidate, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Invalid date",
                "Enter a date in YYYY-MM-DD format.",
                parent=root,
            )
            return

        selected_date["value"] = candidate
        root.destroy()

    def cancel() -> None:
        selected_date["value"] = ""
        root.destroy()

    button_row = ttk.Frame(frame)
    button_row.pack(fill="x")

    ttk.Button(button_row, text="Cancel", command=cancel).pack(side="right")
    ttk.Button(button_row, text="Show", command=confirm).pack(side="right", padx=(0, 8))

    root.protocol("WM_DELETE_WINDOW", cancel)
    combo.bind("<Return>", lambda _event: confirm())
    combo.focus_set()
    root.mainloop()

    if not selected_date["value"]:
        raise SystemExit(0)

    datetime.strptime(selected_date["value"], "%Y-%m-%d")
    return selected_date["value"]


def load_day_log(day: str) -> pd.DataFrame:
    log_path = LOGS_DIR / f"{day}.txt"
    if not log_path.exists():
        raise FileNotFoundError(f"No log file found for {day}: {log_path}")

    df = pd.read_csv(log_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["active"] = df["active"].astype(int)
    return df


def build_grid(df: pd.DataFrame) -> np.ndarray:
    grid = np.zeros((24, 60), dtype=int)

    for _, row in df.iterrows():
        hour = row["timestamp"].hour
        minute = row["timestamp"].minute
        active = int(row["active"])

        if active == 0:
            grid[hour, minute] = 1
        else:
            grid[hour, minute] = 2

    return grid


def main() -> None:
    split_log(SOURCE_LOG, LOGS_DIR)

    day = prompt_for_date()

    try:
        df = load_day_log(day)
    except FileNotFoundError as error:
        messagebox.showerror("Missing log file", str(error))
        return

    grid = build_grid(df)

    cmap = ListedColormap([
        "lightgray",
        "black",
        "green",
    ])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)

    plt.figure(figsize=(15, 8))
    plt.imshow(
        grid,
        cmap=cmap,
        norm=norm,
        aspect="auto",
        interpolation="nearest",
    )

    plt.xlabel("Minute")
    plt.ylabel("Hour")
    plt.title(f"Daily Activity Grid for {day}")

    plt.xticks(range(0, 60, 5))
    plt.yticks(range(24))

    plt.grid(which="major", color="white", linewidth=0.5)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()