const activityLog = [];

function checkStatus() {

    const statusEl = document.querySelector(
        'span.padding_left_50[aria-hidden="true"]'
    );

    if (!statusEl) {
        console.warn("Status element not found");
        return;
    }

    const statusText = statusEl.innerText.trim().toLowerCase();

    const active =
        statusText.includes("active") ||
        statusText.includes("online")
            ? 1
            : 0;

    // CHANGE THE TIMEZONE ACCORDING TO YOUR TIME!!!
    const timestamp = new Date().toLocaleString(
        "sv-SE",
        {
            timeZone: "Asia/Dhaka"
        }
    );

    const record = {
        timestamp: timestamp,
        active: active
    };

    activityLog.push(record);

    console.log(
        `${record.timestamp},${record.active}`
    );
}

checkStatus();


setInterval(checkStatus, 60 * 1000);