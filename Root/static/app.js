// TARGET LOCATION: /static/app.js
// Purpose: Asynchronous Live Polling UI Component Re-Renderer

document.addEventListener("DOMContentLoaded", () => {
    const mountPoint = document.getElementById("cards-mount-point");
    const liveClockBadge = document.getElementById("live-clock-badge");

    // Continuously poll the backend for actual real train data updates every 15 seconds
    async function streamLiveRailwayData() {
        try {
            const res = await fetch('/api/live-corridor');
            if (!res.ok) throw new Error(`HTTP Error Status: ${res.status}`);
            const payload = await res.json();
            
            renderLiveInterface(payload.trains);
        } catch (err) {
            console.error("Live fetch failed, attempting retry: ", err.message);
        }
    }

    function renderLiveInterface(trains) {
        mountPoint.innerHTML = "";
        
        trains.forEach(t => {
            const card = document.createElement("div");
            card.className = "card";
            
            const specBadge = t.is_specialty ? `<div><span class="specialty-tag" style="background:var(--sky-accent); color:#000;">II ANTYODAYA UNIQUE FARE RAKE</span></div>` : "";
            const delayStatus = t.delay > 0 ? `<span style="color:var(--clr-red); font-size:0.75rem; font-weight:bold;">(+${t.delay}m Real Delay)</span>` : `<span style="color:var(--clr-green); font-size:0.75rem; font-weight:bold;">On Time</span>`;
            
            let colorState = "GREEN";
            let advisoryText = "FINE PROTECTION SECURED: Fully unreserved coach layout. Board safely ONLY with a specific 'II ANTYODAYA' counter ticket.";
            if (t.train_no === 13434) { colorState = "ORANGE"; advisoryText = "TTE PENALTY ALERT: Ensure your counter or UTS ticket explicitly includes the 'Superfast Surcharge'."; }

            card.innerHTML = `
                <div class="card-top">
                    <div>
                        <h3>${t.train_name}</h3>
                        ${specBadge}
                    </div>
                    <span class="train-id-badge">#${t.train_no}</span>
                </div>
                <div class="metrics-row">
                    <div class="metric-cell"><span>Class Required</span><strong>${t.category}</strong></div>
                    <div class="metric-cell"><span>Actual Dep</span><strong>${t.actual}</strong> ${delayStatus}</div>
                </div>
                <p class="fare-text">Unreserved Counter Fare: <span>₹${t.fare.toFixed(2)}</span></p>
                <div class="crowd-indicator">
                    <div class="dot dot-${t.crowd_id === 0 ? 'green' : t.crowd_id === 1 ? 'amber' : 'red'}"></div>
                    <span>AI Crowd Forecast: <strong>${t.crowd_level}</strong></span>
                </div>
                <div class="live-tracker-panel">
                    <div class="tracker-header">
                        <span>🛰️ Live Track Status: <strong style="color:var(--sky-accent);">${t.status_message}</strong></span>
                    </div>
                    <div style="font-size:0.85rem; padding:4px 0; color:#fff;">📍 Current Spot: <strong>${t.current_location}</strong></div>
                </div>
                <div class="advisory alert-${colorState}">
                    ${advisoryText}
                </div>
            `;
            mountPoint.appendChild(card);
        });
    }

    // Live local clock updating every second
    setInterval(() => {
        const now = new Date();
        liveClockBadge.innerHTML = "Live Sync IST: " + now.toLocaleTimeString();
    }, 1000);

    // Trigger initial pull and bind automated 15-second background updates
    streamLiveRailwayData();
    setInterval(streamLiveRailwayData, 15000);
});
