// TARGET LOCATION: /static/app.js
document.addEventListener("DOMContentLoaded", () => {
    const trigger = document.getElementById("query-trigger");
    const timeVector = document.getElementById("time-vector");
    const mountPoint = document.getElementById("cards-mount-point");

    async function pullTransitTelemetryStream() {
        const timeVal = timeVector.value;
        mountPoint.innerHTML = `<p style="grid-column:1/-1; text-align:center; color:var(--text-slate);">Querying live schedules from serverless Neon datastore...</p>`;
        
        try {
            const endpoint = `/api/transit-window?time_now=${timeVal}:00`;
            const res = await fetch(endpoint);
            if (!res.ok) throw new Error(`Server returned code verification error: ${res.status}`);
            
            const payload = await res.json();
            renderLayoutView(payload.trains);
        } catch (err) {
            mountPoint.innerHTML = `<div style="grid-column:1/-1; padding:15px; border:1px solid var(--clr-red); color:var(--clr-red); border-radius:6px; background:rgba(239,64,64,0.1);"><strong>Informatics Vector Failure:</strong> ${err.message}</div>`;
        }
    }

    function renderLayoutView(trains) {
        mountPoint.innerHTML = "";
        if(trains.length === 0) {
            mountPoint.innerHTML = `<p style="grid-column:1/-1; text-align:center; padding:30px; color:var(--text-slate);">No upcoming trains matching unreserved access rules running inside this 3-hour operational grid window.</p>`;
            return;
        }

        trains.forEach(t => {
            const card = document.createElement("div");
            card.className = "card";
            
            const specBadge = t.is_specialty ? `<div><span class="specialty-tag">SPECIALTY UNRESERVED FLEET</span></div>` : "";
            const delayStatus = t.delay > 0 ? `<span style="color:var(--clr-red); font-size:0.7rem;">(+${t.delay}m Delay)</span>` : `<span style="color:var(--clr-green); font-size:0.7rem;">On Time</span>`;

            card.innerHTML = `
                <div class="card-top">
                    <div>
                        <h3>${t.train_name}</h3>
                        ${specBadge}
                    </div>
                    <span class="train-id-badge">#${t.train_no}</span>
                </div>
                <div class="metrics-row">
                    <div class="metric-cell"><span>Class</span><strong>${t.category}</strong></div>
                    <div class="metric-cell"><span>Actual Window</span><strong>${t.actual}</strong> ${delayStatus}</div>
                </div>
                <p class="fare-text">Unreserved Counter Fare: <span>₹${t.fare.toFixed(2)}</span></p>
                <div class="crowd-indicator">
                    <div class="dot dot-${t.crowd_id}"></div>
                    <span>AI Crowd Forecast: <strong>${t.crowd_level}</strong></span>
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
