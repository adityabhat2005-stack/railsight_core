// TARGET LOCATION: /static/app.js
// Purpose: Factual Time-Aware Tracking Engine & Array Matrix Layout Controller

document.addEventListener("DOMContentLoaded", () => {
    const masterCorridorFleets = [
        {
            no: 12836, name: "Antyodaya Express", tier: "Superfast", dep: "04:15", delay: "15m Delay", fare: 187.85, badge: "II ANTYODAYA FARE RAKE", badgeBg: "var(--sky-accent)",
            crowd: "Available Seating Tiers Present", dot: "green", alert: "GREEN", startMin: 255, endMin: 442,
            adv: "FINE PROTECTION SECURED: Board safely ONLY with a specific 'II ANTYODAYA' counter ticket.",
            nodes: [ {n: "MAJN (04:15)", m: 255}, {n: "KGQ (04:58)", m: 298}, {n: "CAN (06:12)", m: 372}, {n: "CLT (07:22)", m: 442} ]
        },
        {
            no: 16649, name: "Parasuram Express", tier: "Mail/Express", dep: "05:05", delay: "On Time", fare: 143.65, badge: "STANDARD UNRESERVED RAKE", badgeBg: "var(--text-slate)",
            crowd: "Heavy Volume - Expect High Density", dot: "red", alert: "ORANGE", startMin: 305, endMin: 512,
            adv: "TTE PENALTY ALERT: Mail/Express ticket required. Basic Ordinary counter tickets are completely invalid.",
            nodes: [ {n: "MAQ (05:05)", m: 305}, {n: "KGQ (05:47)", m: 347}, {n: "CAN (07:07)", m: 427}, {n: "CLT (08:32)", m: 512} ]
        },
        {
            no: 16610, name: "MAQ - Palakkad Passenger Local", tier: "Ordinary Passenger", dep: "05:30", delay: "15m Delay", fare: 110.00, badge: "PASSENGER COUPLING LOCAL", badgeBg: "rgba(56,189,248,0.3)",
            crowd: "Moderate Commuter Standee Load", dot: "amber", alert: "GREEN", startMin: 330, endMin: 552,
            adv: "COMPLIANCE SECURED: Cheapest Ordinary general ticket fully accepted. Lowest operation pricing tier applied.",
            nodes: [ {n: "MAQ (05:30)", m: 330}, {n: "KGQ (06:20)", m: 380}, {n: "CAN (07:45)", m: 465}, {n: "CLT (09:12)", m: 552} ]
        },
        {
            no: 6486, name: "Mangaluru - Kozhikode MEMU Special", tier: "MEMU Service", dep: "06:45", delay: "On Time", fare: 110.00, badge: "HIGH-CAPACITY MEMU SERVICE", badgeBg: "var(--clr-green)",
            crowd: "Moderate Commuter Standee Load", dot: "amber", alert: "GREEN", startMin: 405, endMin: 670,
            adv: "COMPLIANCE SECURED: Cheapest Ordinary general ticket or MEMU pass fully accepted.",
            nodes: [ {n: "MAQ (06:45)", m: 405}, {n: "KGQ (07:40)", m: 460}, {n: "PAY (08:35)", m: 515}, {n: "CAN (09:15)", m: 555}, {n: "CLT (11:10)", m: 670} ]
        },
        {
            no: 16160, name: "MAJN - Chennai Passenger Local", tier: "Ordinary Passenger", dep: "07:15", delay: "20m Delay", fare: 110.00, badge: "PASSENGER COUPLING LOCAL", badgeBg: "rgba(56,189,248,0.3)",
            crowd: "Moderate Commuter Standee Load", dot: "amber", alert: "GREEN", startMin: 435, endMin: 647,
            adv: "COMPLIANCE SECURED: Cheapest Ordinary general ticket fully accepted.",
            nodes: [ {n: "MAJN (07:15)", m: 435}, {n: "KGQ (08:12)", m: 492}, {n: "CAN (09:30)", m: 570}, {n: "CLT (10:47)", m: 647} ]
        },
        {
            no: 15102, name: "Jan Sadharan Express", tier: "Express Run", dep: "10:45", delay: "On Time", fare: 143.65, badge: "STANDARD UNRESERVED RAKE", badgeBg: "var(--text-slate)",
            crowd: "Available Seating Tiers Present", dot: "green", alert: "GREEN", startMin: 645, endMin: 850,
            adv: "FINE PROTECTION SECURED: Basic Unreserved ticket fully valid. Board any available general coach safely.",
            nodes: [ {n: "MAQ (10:45)", m: 645}, {n: "KGQ (11:28)", m: 688}, {n: "PAY (12:15)", m: 735}, {n: "CLT (14:10)", m: 850} ]
        },
        {
            no: 16348, name: "Mangaluru - Trivandrum Express", tier: "Mail/Express", dep: "14:35", delay: "10m Delay", fare: 143.65, badge: "STANDARD UNRESERVED RAKE", badgeBg: "var(--text-slate)",
            crowd: "Heavy Volume - Expect High Density", dot: "red", alert: "ORANGE", startMin: 875, endMin: 1057,
            adv: "TTE PENALTY ALERT: Mail/Express ticket required. Basic Ordinary Passenger counter tickets are completely invalid.",
            nodes: [ {n: "MAQ (14:35)", m: 875}, {n: "KGQ (15:20)", m: 920}, {n: "CAN (16:40)", m: 1000}, {n: "CLT (17:37)", m: 1057} ]
        },
        {
            no: 13434, name: "Amrit Bharat Express", tier: "Superfast", dep: "16:15", delay: "30m Delay", fare: 187.85, badge: "AMRIT BHARAT SPEED RAKE", badgeBg: "var(--clr-amber)",
            crowd: "Heavy Volume - Expect High Density", dot: "red", alert: "RED", startMin: 975, endMin: 1165,
            adv: "CRITICAL LEGAL ADVISORY: Superfast Surcharge Ticket Required. Boarding with ordinary ticket incurs fines.",
            nodes: [ {n: "MAQ (16:15)", m: 975}, {n: "KGQ (17:05)", m: 1025}, {n: "PAY (17:48)", m: 1068}, {n: "CAN (18:25)", m: 1105}, {n: "TLY (18:48)", m: 1128}, {n: "CLT (19:25)", m: 1165} ]
        },
        {
            no: 16630, name: "Malabar Express (Night Corridor)", tier: "Mail/Express", dep: "18:15", delay: "On Time", fare: 143.65, badge: "STANDARD UNRESERVED RAKE", badgeBg: "var(--text-slate)",
            crowd: "Moderate Commuter Standee Load", dot: "amber", alert: "ORANGE", startMin: 1095, endMin: 1300,
            adv: "TTE PENALTY ALERT: Mail/Express ticket required. Basic Passenger counter tickets are invalid.",
            nodes: [ {n: "MAQ (18:15)", m: 1095}, {n: "KGQ (18:55)", m: 1135}, {n: "CAN (20:15)", m: 1215}, {n: "CLT (21:40)", m: 1300} ]
        },
        {
            no: 16604, name: "Maveli Express (Night Corridor)", tier: "Mail/Express", dep: "19:50", delay: "15m Delay", fare: 143.65, badge: "STANDARD UNRESERVED RAKE", badgeBg: "var(--text-slate)",
            crowd: "Heavy Volume - Expect High Density", dot: "red", alert: "ORANGE", startMin: 1190, endMin: 1395,
            adv: "TTE PENALTY ALERT: Mail/Express ticket required. Basic Passenger counter tickets are invalid.",
            nodes: [ {n: "MAQ (19:50)", m: 1190}, {n: "KGQ (20:35)", m: 1235}, {n: "CAN (21:55)", m: 1315}, {n: "CLT (23:15)", m: 1395} ]
        }
    ];

    const mountPoint = document.getElementById("cards-mount-point");

    function processCorridorGridRefresh() {
        const now = new Date();
        const currentHour = now.getHours();
        const currentMinute = now.getMinutes();
        const totalSysMins = (currentHour * 60) + currentMinute;
        
        // Update Live System Time Badge Clock
        document.getElementById("live-clock-badge").innerHTML = "Live Sync IST: " + now.toLocaleTimeString();
        mountPoint.innerHTML = "";

        masterCorridorFleets.forEach(t => {
            const card = document.createElement("div");
            card.className = "card";

            let liveStatusString = "";
            let currentActiveNodeIndex = -1;

            // Compute dynamic tracking states using the live clock matrix parameters
            if (totalSysMins < t.startMin) {
                liveStatusString = "Awaiting Start from yard.";
            } else if (totalSysMins > t.endMin) {
                liveStatusString = "Run Completed on Schedule - Rake Terminated.";
            } else {
                liveStatusString = `In Transit along the corridor. (${t.delay})`;
                // Determine the highest node index passed by the live system time
                t.nodes.forEach((node, idx) => {
                    if (totalSysMins >= node.m) {
                        currentActiveNodeIndex = idx;
                    }
                });
            }

            let nodesHTML = "";
            t.nodes.forEach((node, idx) => {
                let nodeStateClass = "track-node";
                let prefixIcon = "";
                
                if (totalSysMins > t.endMin) {
                    nodeStateClass += " passed";
                } else if (totalSysMins < t.startMin) {
                    // Stays normal upcoming state
                } else {
                    if (idx === currentActiveNodeIndex) {
                        nodeStateClass += " current-location";
                        prefixIcon = "📍 ";
                    } else if (idx < currentActiveNodeIndex) {
                        nodeStateClass += " passed";
                    }
                }
                nodesHTML += `<div class="${nodeStateClass}">${prefixIcon}${node.n}</div>`;
            });

            card.innerHTML = `
                <div class="card-top">
                    <div>
                        <h3>${t.name}</h3>
                        <div><span class="specialty-tag" style="background:${t.badgeBg}; color:#000;">${t.badge}</span></div>
                    </div>
                    <span class="train-id-badge">#${t.no}</span>
                </div>
                <div class="metrics-row">
                    <div class="metric-cell"><span>Service Tier</span><strong>${t.tier}</strong></div>
                    <div class="metric-cell"><span>Actual Dep</span><strong>${t.dep}</strong></div>
                </div>
                <p class="fare-text">UTS Counter Fare: <span>₹${t.fare.toFixed(2)}</span></p>
                <div class="crowd-indicator">
                    <div class="dot dot-${t.dot}"></div>
                    <span>AI Crowd Forecast: <strong>${t.crowd}</strong></span>
                </div>
                <div class="live-tracker-panel">
                    <div class="tracker-header"><span>🛰️ Live Track: ${liveStatusString}</span></div>
                    <div class="vertical-track">${nodesHTML}</div>
                </div>
                <div class="advisory alert-${t.alert}">${t.adv}</div>
            `;
            mountPoint.appendChild(card);
        });
    }

    // Run execution loops to recalculate tracker nodes every second seamlessly
    processCorridorGridRefresh();
    setInterval(processCorridorGridRefresh, 1000);
});
