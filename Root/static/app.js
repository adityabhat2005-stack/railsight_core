// TARGET LOCATION: /static/app.js
document.addEventListener("DOMContentLoaded", () => {
    const masterCorridorFleets = [
        {
            no: 12836, name: "Antyodaya Express", tier: "Superfast", dep: "04:15", delay: "15m Delay", fare: 187.85, badge: "II ANTYODAYA FARE RAKE", badgeBg: "var(--sky-accent)",
            crowd: "Available Seating Tiers Present", dot: "green", status: "Run Completed", alert: "GREEN",
            adv: "FINE PROTECTION SECURED: Board safely ONLY with a specific 'II ANTYODAYA' counter ticket.",
            nodes: [ {n: "MAJN (04:15)", s: "passed"}, {n: "KGQ (04:58)", s: "passed"}, {n: "CAN (06:12)", s: "passed"}, {n: "CLT (07:22)", s: "passed"} ]
        },
        {
            no: 16649, name: "Parasuram Express", tier: "Mail/Express", dep: "05:05", delay: "On Time", fare: 143.65, badge: "STANDARD UNRESERVED RAKE", badgeBg: "var(--text-slate)",
            crowd: "Heavy Volume - Expect High Density", dot: "red", status: "Run Completed", alert: "ORANGE",
            adv: "TTE PENALTY ALERT: Mail/Express ticket required. Basic Ordinary counter tickets are completely invalid.",
            nodes: [ {n: "MAQ (05:05)", s: "passed"}, {n: "KGQ (05:47)", s: "passed"}, {n: "CAN (07:07)", s: "passed"}, {n: "CLT (08:32)", s: "passed"} ]
        },
        {
            no: 16610, name: "MAQ - Palakkad Passenger Local", tier: "Ordinary Passenger", dep: "05:30", delay: "15m Delay", fare: 110.00, badge: "PASSENGER COUPLING LOCAL", badgeBg: "rgba(56,189,248,0.3)",
            crowd: "Moderate Commuter Standee Load", dot: "amber", status: "Run Completed", alert: "GREEN",
            adv: "COMPLIANCE SECURED: Cheapest Ordinary general ticket fully accepted. Lowest operation pricing tier applied.",
            nodes: [ {n: "MAQ (05:30)", s: "passed"}, {n: "KGQ (06:20)", s: "passed"}, {n: "CAN (07:45)", s: "passed"}, {n: "CLT (09:12)", s: "passed"} ]
        },
        {
            no: 6486, name: "Mangaluru - Kozhikode MEMU Special", tier: "MEMU Service", dep: "06:45", delay: "On Time", fare: 110.00, badge: "HIGH-CAPACITY MEMU SERVICE", badgeBg: "var(--clr-green)",
            crowd: "Moderate Commuter Standee Load", dot: "amber", status: "Run Completed", alert: "GREEN",
            adv: "COMPLIANCE SECURED: Cheapest Ordinary general ticket or MEMU pass fully accepted.",
            nodes: [ {n: "MAQ (06:45)", s: "passed"}, {n: "KGQ (07:40)", s: "passed"}, {n: "PAY (08:35)", s: "passed"}, {n: "CAN (09:15)", s: "passed"}, {n: "CLT (11:10)", s: "passed"} ]
        },
        {
            no: 16160, name: "MAJN - Chennai Passenger Local", tier: "Ordinary Passenger", dep: "07:15", delay: "20m Delay", fare: 110.00, badge: "PASSENGER COUPLING LOCAL", badgeBg: "rgba(56,189,248,0.3)",
            crowd: "Moderate Commuter Standee Load", dot: "amber", status: "Run Completed", alert: "GREEN",
            adv: "COMPLIANCE SECURED: Cheapest Ordinary general ticket fully accepted.",
            nodes: [ {n: "MAJN (07:15)", s: "passed"}, {n: "KGQ (08:12)", s: "passed"}, {n: "CAN (09:30)", s: "passed"}, {n: "CLT (10:47)", s: "passed"} ]
        },
        {
            no: 15102, name: "Jan Sadharan Express", tier: "Express Run", dep: "10:45", delay: "On Time", fare: 143.65, badge: "STANDARD UNRESERVED RAKE", badgeBg: "var(--text-slate)",
            crowd: "Available Seating Tiers Present", dot: "green", status: "Run Completed", alert: "GREEN",
            adv: "FINE PROTECTION SECURED: Basic Unreserved ticket fully valid. Board any available general coach safely.",
            nodes: [ {n: "MAQ (10:45)", s: "passed"}, {n: "KGQ (11:28)", s: "passed"}, {n: "PAY (12:15)", s: "passed"}, {n: "CLT (14:10)", s: "passed"} ]
        },
        {
            no: 16348, name: "Mangaluru - Trivandrum Express", tier: "Mail/Express", dep: "14:35", delay: "10m Delay", fare: 143.65, badge: "STANDARD UNRESERVED RAKE", badgeBg: "var(--text-slate)",
            crowd: "Heavy Volume - Expect High Density", dot: "red", status: "Run Completed", alert: "ORANGE",
            adv: "TTE PENALTY ALERT: Mail/Express ticket required. Basic Ordinary Passenger counter tickets are completely invalid.",
            nodes: [ {n: "MAQ (14:35)", s: "passed"}, {n: "KGQ (15:20)", s: "passed"}, {n: "CAN (16:40)", s: "passed"}, {n: "CLT (17:37)", s: "passed"} ]
        },
        {
            no: 13434, name: "Amrit Bharat Express", tier: "Superfast", dep: "16:15", delay: "30m Delay", fare: 187.85, badge: "AMRIT BHARAT SPEED RAKE", badgeBg: "var(--clr-amber)",
            crowd: "Heavy Volume - Expect High Density", dot: "red", status: "In Transit", alert: "RED",
            adv: "CRITICAL LEGAL ADVISORY: Superfast Surcharge Ticket Required. Boarding with ordinary ticket incurs fines.",
            nodes: [ {n: "MAQ (16:15)", s: "passed"}, {n: "KGQ (17:05)", s: "passed"}, {n: "PAY (17:48)", s: "current-location"}, {n: "CAN (18:25)", s: "upcoming"}, {n: "TLY (18:48)", s: "upcoming"}, {n: "CLT (19:25)", s: "upcoming"} ]
        },
        {
            no: 16630, name: "Malabar Express (Night Corridor)", tier: "Mail/Express", dep: "18:15", delay: "On Time", fare: 143.65, badge: "STANDARD UNRESERVED RAKE", badgeBg: "var(--text-slate)",
            crowd: "Moderate Commuter Standee Load", dot: "amber", status: "Awaiting Start", alert: "ORANGE",
            adv: "TTE PENALTY ALERT: Mail/Express ticket required. Basic Passenger counter tickets are invalid.",
            nodes: [ {n: "MAQ (18:15)", s: "current-location"}, {n: "KGQ (18:55)", s: "upcoming"}, {n: "CAN (20:15)", s: "upcoming"}, {n: "CLT (21:40)", s: "upcoming"} ]
        },
        {
            no: 16604, name: "Maveli Express (Night Corridor)", tier: "Mail/Express", dep: "19:50", delay: "15m Delay", fare: 143.65, badge: "STANDARD UNRESERVED RAKE", badgeBg: "var(--text-slate)",
            crowd: "Heavy Volume - Expect High Density", dot: "red", status: "Awaiting Start", alert: "ORANGE",
            adv: "TTE PENALTY ALERT: Mail/Express ticket required. Basic Passenger counter tickets are invalid.",
            nodes: [ {n: "MAQ (19:50)", s: "current-location"}, {n: "KGQ (20:35)", s: "upcoming"}, {n: "CAN (21:55)", s: "upcoming"}, {n: "CLT (23:15)", s: "upcoming"} ]
        }
    ];

    const mountPoint = document.getElementById("cards-mount-point");
    mountPoint.innerHTML = "";

    masterCorridorFleets.forEach(t => {
        const card = document.createElement("div");
        card.className = "card";

        let nodesHTML = "";
        t.nodes.forEach(node => {
            let nodeClass = "track-node";
            if (node.s === "passed") nodeClass += " passed";
            if (node.s === "current-location") nodeClass += " current-location";
            let prefixIcon = node.s === "current-location" ? "📍 " : "";
            nodesHTML += `<div class="${nodeClass}">${prefixIcon}${node.n}</div>`;
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
                <div class="metric-cell"><span>Actual Dep</span><strong>${t.dep}</strong> <span style="font-size:0.75rem; font-weight:bold; color:${t.delay === 'On Time' ? 'var(--clr-green)' : 'var(--clr-red)'};">(${t.delay})</span></div>
            </div>
            <p class="fare-text">UTS Counter Fare: <span>₹${t.fare.toFixed(2)}</span></p>
            <div class="crowd-indicator">
                <div class="dot dot-${t.dot}"></div>
                <span>AI Crowd Forecast: <strong>${t.crowd}</strong></span>
            </div>
            <div class="live-tracker-panel">
                <div class="tracker-header"><span> Live Track: ${t.status}</span></div>
                <div class="vertical-track">${nodesHTML}</div>
            </div>
            <div class="advisory alert-${t.alert}">${t.adv}</div>
        `;
        mountPoint.appendChild(card);
    });

    setInterval(() => {
        const now = new Date();
        document.getElementById("live-clock-badge").innerHTML = "Live Sync IST: " + now.toLocaleTimeString();
    }, 1000);
});
