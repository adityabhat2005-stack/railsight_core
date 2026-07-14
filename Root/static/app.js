// TARGET LOCATION: /static/app.js
// Purpose: Defensive Key-Checking Live Rendering Engine

document.addEventListener("DOMContentLoaded", () => {
    const mountPoint = document.getElementById("cards-mount-point");
    const liveClockBadge = document.getElementById("live-clock-badge");

    async function streamLiveRailwayData() {
        try {
            const res = await fetch('/api/live-corridor');
            if (!res.ok) throw new Error(`HTTP System Code Verification Error: ${res.status}`);
            const payload = await res.json();
            renderLiveInterface(payload.trains);
        } catch (err) {
            mountPoint.innerHTML = `<div style="grid-column:1/-1; padding:15px; border:1px solid var(--clr-red); color:var(--clr-red); border-radius:6px; background:rgba(239,64,64,0.1);"><strong>Handshake Vector Breakdown:</strong> ${err.message}</div>`;
        }
    }

    function renderLiveInterface(trains) {
        mountPoint.innerHTML = "";
        
        if (!trains || trains.length === 0) {
            mountPoint.innerHTML = `<p style="grid-column:1/-1; text-align:center; color:var(--text-slate);">No operational streams dispatched from core gateway.</p>`;
            return;
        }

        trains.forEach(t => {
            const card = document.createElement("div");
            card.className = "card";
            
            // Handle different variations of fare naming keys defensively to prevent crashes
            const rawFare = t.fare || t.base_fare || 0.00;
            const fareDisplay = Number(rawFare).toFixed(2);

            let specBadge = `<div><span class="specialty-tag">FULLY UNRESERVED EXPRESS</span></div>`;
            if (t.train_no === 12836) {
                specBadge = `<div><span class="specialty-tag" style="background:var(--sky-accent); color:#000;">II ANTYODAYA UNIQUE FARE RAKE</span></div>`;
            } else if (t.train_no === 13434) {
                specBadge = `<div><span class="specialty-tag" style="background:var(--clr-amber); color:#000;">AMRIT BHARAT SPEED RAKE</span></div>`;
            }

            const delayStatus = t.delay > 0 
                ? `<span style="color:var(--clr-red); font-size:0.75rem; font-weight:bold;">(+${t.delay}m Delay)</span>` 
                : `<span style="color:var(--clr-green); font-size:0.75rem; font-weight:bold;">On Time</span>`;
            
            let colorState = "GREEN";
            let advisoryText = "FINE PROTECTION SECURED: Fully unreserved coach layout. Board cleanly with basic General class paper tickets.";
            if (t.train_no === 12836) { advisoryText = "FINE PROTECTION SECURED: Board safely ONLY with a specific 'II ANTYODAYA' counter ticket."; }
            if (t.train_no === 13434) { colorState = "ORANGE"; advisoryText = "TTE PENALTY ALERT: Ensure ticket explicitly includes the 'Superfast Surcharge' to avoid penalty fees."; }

            let nodesHTML = "";
            if (t.nodes && t.nodes.length > 0) {
                t.nodes.forEach(node => {
                    let nodeClass = "track-node";
                    if (node.state === "passed") nodeClass += " passed";
                    if (node.state === "current-location") nodeClass += " current-location";
                    
                    let prefixIcon = node.state === "current-location" ? "📍 " : "";
                    nodesHTML += `<div class="${nodeClass}">${prefixIcon}${node.name}</div>`;
                });
            }

            let dotClass = "dot-green";
            if (t.crowd_id === 1) dotClass = "dot-amber";
            if (t.crowd_id === 2) dotClass = "dot-red";

            card.innerHTML = `
                <div class="card-top">
                    <div>
                        <h3>${t.train_name || "Unknown Train"}</h3>
                        ${specBadge}
                    </div>
                    <span class="train-id-badge">#${t.train_no}</span>
                </div>
                <div class="metrics-row">
                    <div class="metric-cell"><span>Class Required</span><strong>${t.category || "General"}</strong></div>
                    <div class="metric-cell"><span>Actual Dep</span><strong>${t.actual || t.scheduled}</strong> ${delayStatus}</div>
                </div>
                <p class="fare-text">Unreserved Counter Fare: <span>₹${fareDisplay}</span></p>
                <div class="crowd-indicator">
                    <div class="dot ${dotClass}"></div>
                    <span>AI Crowd Forecast: <strong>${t.crowd_level || "Normal volume"}</strong></span>
                </div>
                
                <div class="live-tracker-panel">
                    <div class="tracker-header">
                        <span>🛰️ NTES Status: <strong style="color:var(--sky-accent);">${t.status_message || "Active"}</strong></span>
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

    // Ticking visual navbar clock implementation loop
    setInterval(() => {
        const now = new Date();
        liveClockBadge.innerHTML = "Live Sync IST: " + now.toLocaleTimeString();
    }, 1000);

    // Bootstrap app sequence loops
    streamLiveRailwayData();
    setInterval(streamLiveRailwayData, 15000);
});
