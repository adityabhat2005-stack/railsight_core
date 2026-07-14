// TARGET LOCATION: /static/app.js
document.addEventListener("DOMContentLoaded", () => {
    const mountPoint = document.getElementById("cards-mount-point");
    const liveClockBadge = document.getElementById("live-clock-badge");

    async function streamLiveRailwayData() {
        try {
            const res = await fetch('/api/live-corridor');
            if (!res.ok) throw new Error(`HTTP Status: ${res.status}`);
            const payload = await res.json();
            renderLiveInterface(payload.trains);
        } catch (err) {
            console.error("Fetch failed: ", err.message);
        }
    }

    function renderLiveInterface(trains) {
        mountPoint.innerHTML = "";
        
        trains.forEach(t => {
            const card = document.createElement("div");
            card.className = "card";
            
            const specBadge = t.train_no === 12836 
                ? `<div><span class="specialty-tag" style="background:var(--sky-accent); color:#000;">II ANTYODAYA UNIQUE FARE RAKE</span></div>` 
                : t.train_no === 13434 
                ? `<div><span class="specialty-tag" style="background:var(--clr-amber); color:#000;">AMRIT BHARAT SPEED RAKE</span></div>`
                : `<div><span class="specialty-tag">FULLY UNRESERVED EXPRESS</span></div>`;

            const delayStatus = t.delay > 0 
                ? `<span style="color:var(--clr-red); font-size:0.75rem; font-weight:bold;">(+${t.delay}m Delay)</span>` 
                : `<span style="color:var(--clr-green); font-size:0.75rem; font-weight:bold;">On Time</span>`;
            
            let colorState = "GREEN";
            let advisoryText = "FINE PROTECTION SECURED: Fully unreserved coach layout. Board cleanly with basic General class paper tickets.";
            if (t.train_no === 12836) { advisoryText = "FINE PROTECTION SECURED: Board safely ONLY with a specific 'II ANTYODAYA' counter ticket."; }
            if (t.train_no === 13434) { colorState = "ORANGE"; advisoryText = "TTE PENALTY ALERT: Ensure ticket explicitly includes the 'Superfast Surcharge' to avoid penalty fees."; }

            // Generate the vertical timeline nodes dynamically using real station data arrays
            let nodesHTML = "";
            t.nodes.forEach(node => {
                let nodeClass = "track-node";
                if (node.state === "passed") nodeClass += " passed";
                if (node.state === "current-location") nodeClass += " current-location";
                
                let icon = node.state === "current-location" ? "📍 " : "";
                nodesHTML += `<div class="${nodeClass}">${icon}${node.name}</div>`;
            });

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
                
                <!-- REAL TRACKING TIMELINE NODE LAYER -->
                <div class="live-tracker-panel">
                    <div class="tracker-header">
                        <span>🛰️ NTES Status: <strong style="color:var(--sky-accent);">${t.status_message}</strong></span>
                    </div>
                    <div class="vertical-track">
                        ${nodesHTML}
                    </div>
                </div>

                <div class="advisory alert-${colorState}">
                    ${advisoryText}
                </div>
            `;
            mountPoint.appendChild(card);
        });
    }

    setInterval(() => {
        const now = new Date();
        liveClockBadge.innerHTML = "Live Sync IST: " + now.toLocaleTimeString();
    }, 1000);

    streamLiveRailwayData();
    setInterval(streamLiveRailwayData, 15000);
});
