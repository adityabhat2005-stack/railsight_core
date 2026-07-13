-- Neon Console SQL - Insert Sample Train Railway Data
-- Run this in your Neon console to populate train tracking data

-- 1. Insert Train Categories (Skip if already exists)
INSERT INTO train_category (category_id, category_name, base_fare_per_km) VALUES
(1, 'AMRIT BHARAT (GS)', 2.50),
(2, 'ANTYODAYA EXPRESS', 3.00),
(3, 'DE-RESERVED SLEEPER', 3.50),
(4, 'EXPRESS TIER', 2.00)
ON CONFLICT (category_id) DO NOTHING;

-- 2. Insert Train Masters (MAJN to CLT route trains) - Skip if already exists
INSERT INTO train_master (train_no, train_name, category_id) VALUES
('12621', 'Mangaluru Express', 1),
('16590', 'Antyodaya Coastal', 2),
('17339', 'Coastal Suryanagari', 1),
('18633', 'KK Express', 3),
('11040', 'Amrit Bharat Fast', 1),
('12589', 'Express Rajya', 4)
ON CONFLICT (train_no) DO NOTHING;

-- 3. Insert Live Schedules (Routes with distances and timings) - Delete old ones first
DELETE FROM live_schedules WHERE train_no IN ('12621', '16590', '17339', '18633', '11040', '12589');

INSERT INTO live_schedules (train_no, source_station, dest_station, distance_km, scheduled_departure, delay_minutes) VALUES
('12621', 'MAJN', 'CLT', 380.00, '08:00:00', 5),
('16590', 'MAJN', 'CLT', 380.00, '10:30:00', 0),
('17339', 'MAJN', 'CLT', 380.00, '14:15:00', 15),
('18633', 'MAJN', 'CLT', 380.00, '16:45:00', 8),
('11040', 'MAJN', 'CLT', 380.00, '06:00:00', 0),
('12589', 'MAJN', 'CLT', 380.00, '20:30:00', 12);

-- 4. INSERT LIVE TRACKING DATA - 3 HOUR HISTORY (6 data points per train)
-- Clear old tracking data first
DELETE FROM train_tracking WHERE train_no IN ('12621', '16590', '17339', '18633', '11040', '12589');
INSERT INTO train_tracking (train_no, current_station, current_latitude, current_longitude, distance_covered_km, distance_remaining_km, current_speed_kmph, delay_minutes, timestamp, status) VALUES
('12621', 'Udupi Junction', 13.3500, 74.7421, 150.00, 230.00, 62.5, 5, NOW() - INTERVAL '180 minutes', 'RUNNING'),
('12621', 'Kundapura', 13.5224, 74.6787, 170.00, 210.00, 65.0, 3, NOW() - INTERVAL '150 minutes', 'RUNNING'),
('12621', 'Byndoor', 13.6854, 74.6432, 200.00, 180.00, 68.0, 4, NOW() - INTERVAL '120 minutes', 'RUNNING'),
('12621', 'Honnavar', 13.8765, 74.4321, 240.00, 140.00, 70.5, 5, NOW() - INTERVAL '90 minutes', 'RUNNING'),
('12621', 'Kumta', 14.0123, 74.3012, 280.00, 100.00, 72.0, 8, NOW() - INTERVAL '45 minutes', 'RUNNING'),
('12621', 'Karwar', 14.8091, 74.3107, 320.00, 60.00, 75.0, 5, NOW(), 'RUNNING');

-- Train 16590 - Antyodaya Coastal (Currently at 50% progress)
INSERT INTO train_tracking (train_no, current_station, current_latitude, current_longitude, distance_covered_km, distance_remaining_km, current_speed_kmph, delay_minutes, timestamp, status) VALUES
('16590', 'Perdur', 13.1234, 74.9876, 80.00, 300.00, 58.0, 0, NOW() - INTERVAL '180 minutes', 'RUNNING'),
('16590', 'Kundapura', 13.5224, 74.6787, 130.00, 250.00, 62.0, 0, NOW() - INTERVAL '150 minutes', 'RUNNING'),
('16590', 'Byndoor', 13.6854, 74.6432, 160.00, 220.00, 64.5, 2, NOW() - INTERVAL '120 minutes', 'RUNNING'),
('16590', 'Honnavar', 13.8765, 74.4321, 200.00, 180.00, 66.0, 0, NOW() - INTERVAL '90 minutes', 'RUNNING'),
('16590', 'Kumta', 14.0123, 74.3012, 240.00, 140.00, 68.5, 1, NOW() - INTERVAL '45 minutes', 'RUNNING'),
('16590', 'Karwar', 14.8091, 74.3107, 280.00, 100.00, 70.0, 0, NOW(), 'RUNNING');

-- Train 17339 - Coastal Suryanagari (Currently at 30% progress)
INSERT INTO train_tracking (train_no, current_station, current_latitude, current_longitude, distance_covered_km, distance_remaining_km, current_speed_kmph, delay_minutes, timestamp, status) VALUES
('17339', 'Kundapura', 13.5224, 74.6787, 80.00, 300.00, 55.0, 15, NOW() - INTERVAL '180 minutes', 'DELAYED'),
('17339', 'Byndoor', 13.6854, 74.6432, 110.00, 270.00, 57.5, 18, NOW() - INTERVAL '150 minutes', 'DELAYED'),
('17339', 'Honnavar', 13.8765, 74.4321, 140.00, 240.00, 59.0, 20, NOW() - INTERVAL '120 minutes', 'DELAYED'),
('17339', 'Kumta', 14.0123, 74.3012, 165.00, 215.00, 61.0, 15, NOW() - INTERVAL '90 minutes', 'RUNNING'),
('17339', 'Karwar', 14.8091, 74.3107, 200.00, 180.00, 62.5, 12, NOW() - INTERVAL '45 minutes', 'RUNNING'),
('17339', 'Sirsi Road', 14.6234, 75.1890, 230.00, 150.00, 64.0, 10, NOW(), 'RUNNING');

-- Train 18633 - KK Express (Currently at 80% progress)
INSERT INTO train_tracking (train_no, current_station, current_latitude, current_longitude, distance_covered_km, distance_remaining_km, current_speed_kmph, delay_minutes, timestamp, status) VALUES
('18633', 'Perdur', 13.1234, 74.9876, 130.00, 250.00, 70.0, 8, NOW() - INTERVAL '180 minutes', 'RUNNING'),
('18633', 'Udupi Junction', 13.3500, 74.7421, 160.00, 220.00, 72.0, 6, NOW() - INTERVAL '150 minutes', 'RUNNING'),
('18633', 'Kundapura', 13.5224, 74.6787, 190.00, 190.00, 74.0, 8, NOW() - INTERVAL '120 minutes', 'RUNNING'),
('18633', 'Honnavar', 13.8765, 74.4321, 240.00, 140.00, 75.5, 10, NOW() - INTERVAL '90 minutes', 'RUNNING'),
('18633', 'Kumta', 14.0123, 74.3012, 280.00, 100.00, 76.0, 8, NOW() - INTERVAL '45 minutes', 'RUNNING'),
('18633', 'Karwar', 14.8091, 74.3107, 320.00, 60.00, 78.0, 8, NOW(), 'RUNNING');

-- Train 11040 - Amrit Bharat Fast (Currently at 20% progress)
INSERT INTO train_tracking (train_no, current_station, current_latitude, current_longitude, distance_covered_km, distance_remaining_km, current_speed_kmph, delay_minutes, timestamp, status) VALUES
('11040', 'Mangaluru Central', 12.8675, 74.8568, 40.00, 340.00, 50.0, 0, NOW() - INTERVAL '180 minutes', 'RUNNING'),
('11040', 'Perdur', 13.1234, 74.9876, 60.00, 320.00, 52.0, 0, NOW() - INTERVAL '150 minutes', 'RUNNING'),
('11040', 'Udupi Junction', 13.3500, 74.7421, 95.00, 285.00, 54.0, 0, NOW() - INTERVAL '120 minutes', 'RUNNING'),
('11040', 'Kundapura', 13.5224, 74.6787, 115.00, 265.00, 56.0, 0, NOW() - INTERVAL '90 minutes', 'RUNNING'),
('11040', 'Byndoor', 13.6854, 74.6432, 140.00, 240.00, 58.0, 0, NOW() - INTERVAL '45 minutes', 'RUNNING'),
('11040', 'Honnavar', 13.8765, 74.4321, 165.00, 215.00, 60.0, 0, NOW(), 'RUNNING');

-- Train 12589 - Express Rajya (Currently at 90% progress)
INSERT INTO train_tracking (train_no, current_station, current_latitude, current_longitude, distance_covered_km, distance_remaining_km, current_speed_kmph, delay_minutes, timestamp, status) VALUES
('12589', 'Kumta', 14.0123, 74.3012, 300.00, 80.00, 75.0, 12, NOW() - INTERVAL '180 minutes', 'RUNNING'),
('12589', 'Sirsi Road', 14.6234, 75.1890, 320.00, 60.00, 76.0, 10, NOW() - INTERVAL '150 minutes', 'RUNNING'),
('12589', 'Karwar', 14.8091, 74.3107, 335.00, 45.00, 77.0, 12, NOW() - INTERVAL '120 minutes', 'RUNNING'),
('12589', 'Kasaragod', 12.4761, 75.4744, 350.00, 30.00, 78.0, 15, NOW() - INTERVAL '90 minutes', 'DELAYED'),
('12589', 'Kannur', 12.0079, 75.3704, 365.00, 15.00, 72.0, 12, NOW() - INTERVAL '45 minutes', 'RUNNING'),
('12589', 'Kozhikode Main', 11.2588, 75.6355, 378.00, 2.00, 65.0, 12, NOW(), 'RUNNING');

-- VERIFY DATA WAS INSERTED
SELECT COUNT(*) as total_tracking_records FROM train_tracking;
SELECT * FROM train_master;
SELECT * FROM train_tracking ORDER BY train_no, timestamp DESC LIMIT 10;
