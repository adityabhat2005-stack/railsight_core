# 🚂 Rail Sight: An Independent Operational Intelligence Portal for Unreserved Train Commuters

> ⚠️ **Status: Active Work-in-Progress (WIP)**  
> This academic project is under active phase-wise development at St Joseph Engineering College. Files are continuously being modified and updated.

---

## 📋 Project Overview
Rail Sight is a specialized pre-travel decision support web application engineered to protect general-class railway passengers from accidental ticketing class violations and severe TTE statutory financial penalties. Focused on high-density regional corridors—specifically the interstate route between Manjeshwar (MJS) and Mangalore Central (MAQ)—the platform aggregates raw schedules and processes real-time 3-hour local operational matrices while filtering out restricted premium fleets.

## 🛠️ Tech Stack & Deployment Architecture
* **Frontend Interface**: Lightweight HTML5, CSS3, and JavaScript/React engineered for ultra-low latency page rendering over weak platform cellular connections.
* **Backend Services**: Python FastAPI framework executing high-performance server-side filtering algorithms and ticket tier/fare translation matrices.
* **Database Engine**: Hosted on **[Neon Serverless Postgres](https://neon.tech)**.
* **Cloud Hosting & Deployment**: Automatically deployed and hosted on **Render** directly via GitHub integration for seamless continuous delivery.

### ⚡ How this project utilizes Neon
* **Relational Mapping**: Leveraging Neon's cloud Postgres engine to map relational entities cleanly (`Trainmaster`, `Train Category`, and `Live_Schedules`) with normalized foreign key constraints to preserve transit data integrity.
* **Environment Branching**: Utilizing Neon’s instant database branching features during active development to securely write, iterate, and run database migration tests without impacting core schemas.

---
*Developed by Aditya A Bhat — Department of Computer Applications, SJEC.*
