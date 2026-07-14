// TARGET LOCATION: /static/app.js
// Purpose: Explicit Parameter-Checking Layout Controller Matrix

document.addEventListener("DOMContentLoaded", () => {
    const trigger = document.getElementById("query-trigger");
    const timeVector = document.getElementById("time-vector");
    const mountPoint = document.getElementById("cards-mount-point");

    async function pullTransitTelemetryStream() {
        const rawTimeVal = timeVector.value; // Extracts text like "15:00" or "07:30"
        
        // Fail-safe formatting validation: Ensure the string has seconds attached
        let formattedTimeParam = rawTimeVal;
        if (rawTimeVal && rawTimeVal.split(':').length === 2) {
            formattedTimeParam = `${rawTimeVal}:00`; // Converts "15:00" to "15:00:00"
        }

        mountPoint.innerHTML = `<p style="grid-column:1/-1; text-align:center; color:var(--text-slate);">Querying 3-hour timetable frame for parameter: ${formattedTimeParam}...</p>`;
        
        try {
            // Fetch directly from the endpoint with the updated time parameter string
            const endpoint = `/api/transit-window?time_now=${formattedTimeParam}`;
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
        
        if (!trains || trains.length === 0) {
            mountPoint.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 30px; background: rgba(255,255,255,0.02); border-radius: 8px; border: 1px dashed var(--text-slate);">
                    <p style="color: var(--text-slate); font-size: 1.1rem;">No upcoming unreserved trains found running inside this 3-hour timetable window.</p>
                    <p style="color: var(--sky-accent); font-size: 0.85rem; margin-top: 5px;">Try checking <strong>06:00</strong>, <strong>14:00</strong>, or <strong>15:00</strong> to match your database seed data parameters.</p>
                </div>`;
            return;
        }

        trains.forEach(t => {
            const card = document.createElement("div");
            card.className = "card";
            
            const actualTimeStr = t.actual || "00:00";
            const scheduledTimeStr = t.scheduled || "00:00";
            const fareCost = t.fare || 0.00;
            const alertColor = t.color_state || "GRAY";

            const specBadge = t.is_specialty 
                ? `<div><span class="specialty-tag">SPECIALTY UNRESERVED FLEET</span></div>` 
                : "";
                
            const delayStatus = t.delay > 0 
                ? `<span style="color:var(--clr-red); font-size:0.7rem; font-weight:bold;">(+${t.delay}m Delay)</span>` 
                : `<span style="color:var(--clr-green); font-size:0.7rem; font-weight:bold;">On Time</span>`;

            card.innerHTML = `
                <div class="card-top">
                    <div>
                        <h3 style="color:#fff; font-size:1.2rem; font-weight:bold; margin-bottom:4px;">${t.train_name}</h3>
                        ${specBadge}
                    </div>
                    <span class="train-id-badge">#${t.train_no}</span>
                </div>
                <div class="metrics-row">
                    <div class="metric-cell"><span>Class</span><strong>${t.category}</strong></div>
                    <div class="metric-cell"><span>Actual Window</span><strong>${actualTimeStr}</strong> ${delayStatus}</div>
                </div>
                <p class="fare-text">Unreserved Counter Fare: <span style="color:var(--sky-accent); font-weight:bold;">₹${Number(fareCost).toFixed(2)}</span></p>
                <div class="crowd-indicator">
                    <div class="dot dot-${t.crowd_id}"></div>
                    <span>AI Crowd Forecast: <strong>${t.crowd_level}</strong></span>
                </div>
                <div class="advisory alert-${alertColor}">
                    ${t.fine_advisory}
                </div>
            `;
            mountPoint.appendChild(card);
        });
    }

    trigger.addEventListener("click", pullTransitTelemetryStream);
    // Initialize default lookup window on initial page initialization
    pullTransitTelemetryStream();
});
