function downloadLog() {
    const text =
        "timestamp,active\n" +
        activityLog
            .map(r => `${r.timestamp},${r.active}`)
            .join("\n");

    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "slack_activity_log.txt";
    a.click();

    URL.revokeObjectURL(url);
}