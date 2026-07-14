// TARGET LOCATION: /static/app.js
document.addEventListener("DOMContentLoaded", () => {
    const mountPoint = document.getElementById("cards-mount-point");
    const liveClockBadge = document.getElementById("live-clock-badge");

    async function streamLiveRailwayData() {
        try {
            const res = await fetch('/api/live-corridor');
            if (!res.ok) throw new Error(`HTTP Status Vector Error: ${res.status}`);
            const payload = await res.json();
            
            if (payload && payload.trains) {
                renderLiveInterface(payload.trains);
            }
        } catch (err) {
            mountPoint.innerHTML = `<div style="grid-column:1/-1; padding:15px; border:1px solid var(--clr-red); color:var(--clr-red); border-radius:6px; background:rgba(239,64,64,0.1);"><strong>Handshake Vector Breakdown:</strong> ${err.message}</div>`;
        }
    }

    function renderLiveInterface(trains) {
        mountPoint.innerHTML = "";
        
        trains.forEach(t => {
            if (!t) return;
            const card = document.createElement("div");
            card.className = "card";
            
            const rawFare = t.fare || 0.00;
            const fareDisplayStr = Number(rawFare).toFixed(2);

            // 1. Dynamic Badge Generation Layer
            let specBadge = `<div><span class="specialty-tag" style="background:var(--text-slate); color:#000;">STANDARD UNRESERVED RAKE</span></div>`;
            if (t.train_no === 12836) {
                specBadge = `<div><span class="specialty-tag" style="background:var(--sky-accent); color:#000;">II ANTYODAYA UNIQUE FARE RAKE</span></div>`;
            } else if (t.train_no === 13434) {
                specBadge = `<div><span class="specialty-tag" style="background:var(--clr-amber); color:#000;">AMRIT BHARAT SPEED RAKE</span></div>`;
            } else if (t.category === "MEMU Service") {
                specBadge = `<div><span class="specialty-tag" style="background:var(--clr-green); color:#000;">HIGH-CAPACITY MEMU SERVICE</span></div>`;
            } else if (t.category === "Ordinary Passenger") {
                specBadge = `<div><span class="specialty-tag" style="background:rgba(56,189,248,0.2); color:var(--sky-accent);">PASSENGER COUPLING LOCAL</span></div>`;
            }

            const currentDelay = t.delay || 0;
            const delayStatus = currentDelay > 0 
                ? `<span style="color:var(--clr-red); font-size:0.75rem; font-weight:bold;">(+${currentDelay}m Delay)</span>` 
                : `<span style="color:var(--clr-green); font-size:0.75rem; font-weight:bold;">On Time</span>`;
            
            // 2. Dynamic TTE Fine Advisory Rule Evaluator
            let colorState = "GREEN";
            let advisoryText = "FINE PROTECTION SECURED: Basic Unreserved ticket fully valid. Board any available general coach safely.";
            
            if (t.train_no === 12836) { 
                advisoryText = "FINE PROTECTION SECURED: Board safely ONLY with a specific 'II ANTYODAYA' counter ticket. Normal tickets will face fines."; 
            } else if (t.category === "Superfast") {
                colorState = "RED";
                advisoryText = "CRITICAL LEGAL ADVISORY: Superfast Surcharge Ticket Required. Traveling on this fleet with an ordinary general ticket incurs an automatic penalty fine.";
            } else if (t.category === "Mail/Express") {
                colorState = "ORANGE";
                advisoryText = "TTE PENALTY ALERT: Mail/Express ticket required. Basic Ordinary Passenger counter tickets are completely invalid.";
            } else if (t.category === "Ordinary Passenger" || t.category === "MEMU Service") {
                colorState = "GREEN";
                advisoryText = "COMPLIANCE SECURED: Cheapest Ordinary general ticket or MEMU pass fully accepted. Lowest operation pricing tier applied.";
            }

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
                        <h3 style="margin-bottom:2px;">${t.train_name}</h3>
                        ${specBadge}
                    </div>
                    <span class="train-id-badge">#${t.train_no}</span>
                </div>
                <div class="metrics-row">
                    <div class="metric-cell"><span>Service Tier</span><strong>${t.category}</strong></div>
                    <div class="metric-cell"><span>Actual Dep</span><strong>${t.actual}</strong> ${delayStatus}</div>
                </div>
                <p class="fare-text">UTS Counter Fare: <span>₹${fareDisplayStr}</span></p>
                <div class="crowd-indicator">
                    <div class="dot ${dotClass}"></div>
                    <span>AI Crowd Forecast: <strong>${t.crowd_level}</strong></span>
                </div>
                
                <div class="live-tracker-panel">
                    <div class="tracker-header">
                        <span>🛰️ Live Track: <strong style="color:var(--sky-accent);">${t.status_message}</strong></span>
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
