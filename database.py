# database.py

CRYO_STATION_DATABASE = {
    "supported_corridor": {"from": "MAJN", "to": "CLT"},
    "trains": [
        {
            "trainNumber": "16330",
            "name": "MANGALURU JN - NAGERCOIL AMRIT BHARAT EXP",
            "departure": "08:00 AM",
            "arrival": "11:07 AM",
            "duration": "3h 07m",
            "tier": "AMRIT BHARAT (GS)",
            "baseFare": 90,
            "liveDensity": "HEAVY RUSH",
            "densityColor": "text-red-600 bg-red-50 border-red-200",
            "justificationText": "Rake relies entirely on general walk-on tickets. IRCTC excludes local point-to-point unreserved booking options for this run."
        },
        {
            "trainNumber": "16356",
            "name": "MANGALURU JN - KOCHUVELI ANTYODAYA EXP",
            "departure": "08:10 PM",
            "arrival": "11:15 PM",
            "duration": "3h 05m",
            "tier": "ANTYODAYA EXPRESS",
            "baseFare": 95,
            "liveDensity": "HEAVY RUSH",
            "densityColor": "text-red-600 bg-red-50 border-red-200",
            "justificationText": "Entire train consists strictly of unreserved cars. Completely invisible to conventional IRCTC booking options."
        },
        {
            "trainNumber": "16603",
            "name": "MAVELI EXPRESS (DE-RESERVED ZONE)",
            "departure": "05:30 PM",
            "arrival": "08:45 PM",
            "duration": "3h 15m",
            "tier": "DE-RESERVED SLEEPER",
            "baseFare": 80,
            "liveDensity": "MODERATE RUSH",
            "densityColor": "text-amber-600 bg-amber-50 border-amber-200",
            "justificationText": "Specifically designated Sleeper cars function as open Unreserved coaches for regional commuters on this stretch."
        },
        {
            "trainNumber": "16630",
            "name": "MALABAR EXPRESS",
            "departure": "06:15 PM",
            "arrival": "09:35 PM",
            "duration": "3h 20m",
            "tier": "EXPRESS TIER",
            "baseFare": 80,
            "liveDensity: "LOW RUSH",
            "densityColor": "text-green-600 bg-green-50 border-green-200",
            "justificationText": "Standard regional express offering front and rear unreserved generic layout attachment rakes."
        }
    ]
}
