// TARGET LOCATION: /static/app.js
document.addEventListener("DOMContentLoaded", () => {
    const trigger = document.getElementById("query-trigger");
    const timeVector = document.getElementById("time-vector");
    const mountPoint = document.getElementById("cards-mount-point");
    const windowIndicator = document.getElementById("window-indicator");

    async function pullTransitTelemetryStream() {
        let rawTimeVal = timeVector.value;
        if (rawTimeVal && rawTimeVal.split(':').length === 2) {
            rawTimeVal = `${rawTimeVal}:00`;
        }

        mountPoint.innerHTML = `<p style="grid-column:1/-1; text-align:center; color:var(--text-slate);">Querying database system layers...</p>`;
        
        try {
            const res = await fetch(`/api/transit-window?time_now=${rawTimeVal}`);
            if (!res.ok) throw new Error(`HTTP status: ${res.status}`);
            const payload = await res.json();
            
            if (payload.meta && payload.meta.diagnostic_override) {
                windowIndicator.innerHTML = `<span style="color:var(--clr-amber); font-weight:bold;">⚠️ DIAGNOSTIC MODE ACTIVE: Showing next available trains regardless of time boundaries!</span>`;
            } else {
                windowIndicator.innerHTML = `Rolling Horizon: 3 Hours Window`;
            }

            renderLayoutView(payload.trains);
        } catch (err) {
            mountPoint.innerHTML = `<div style="grid-column:1/-1; padding:15px; border:1px solid var(--clr-red); color:var(--clr-red); font-weight:bold;">Handshake Error: ${err.message}</div>`;
        }
    }

    function renderLayoutView(trains) {
        mountPoint.innerHTML = "";
        if (!trains || trains.length === 0) {
            mountPoint.innerHTML = `<p style="grid-column:1/-1; text-align:center; padding:20px; color:var(--text-slate);">Zero records exist inside your Neon database instance tables.</p>`;
            return;
        }

        trains.forEach(t => {
            const card = document.createElement("div");
            card.className = "card";
            const specBadge = t.is_specialty ? `<div><span class="specialty-tag">SPECIALTY UNRESERVED FLEET</span></div>` : "";
            
            card.innerHTML = `
                <div class="card-top">
                    <div>
                        <h3 style="color:#fff; font-size:1.15rem; font-weight:bold;">${t.train_name}</h3>
                        ${specBadge}
                    </div>
                    <span class="train-id-badge">#${t.train_no}</span>
                </div>
                <div class="metrics-row">
                    <div class="metric-cell"><span>Class</span><strong>${t.category}</strong></div>
                    <div class="metric-cell"><span>Actual Dep</span><strong>${t.actual}</strong></div>
                </div>
                <p class="fare-text">Fare: <span>₹${t.fare.toFixed(2)}</span></p>
                <div class="crowd-indicator">
                    <div class="dot dot-${t.crowd_id}"></div>
                    <span>AI Volume Predict: <strong>${t.crowd_level}</strong></span>
                </div>
                <div class="advisory alert-${t.color_state}">
                    ${t.fine_advisory}
                </div>
            `;
            mountPoint.appendChild(card);
        });
    }

    trigger.addEventListener("click", pullTransitTelemetryStream);
    pullTransitTelemetryStream();
});
