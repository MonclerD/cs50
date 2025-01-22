-- Keep a log of any SQL queries you execute as you solve the mystery.

-- To see crime scene reports took place on July 28, 2023
   SELECT *
   FROM crime_scene_reports
   WHERE year = 2023
   AND day = 28
   AND month = 7
   AND street = 'Humphrey Street';

-- To see interviews
   SELECT *
   FROM interviews
   WHERE year = 2023
   AND day = 28
   AND month = 7;

-- To see bakery parking lot security logs on that day
   SELECT *
   FROM bakery_security_logs
   WHERE year = 2023
   AND month = 7
   AND day = 28
   AND hour = 10
   AND minute >= 15 AND minute <= 25
   AND activity = 'exit';

-- To see atm transactions on that day
   SELECT *
   FROM atm_transactions
   WHERE year = 2023
   AND month = 7
   AND day = 28
   AND atm_location = 'Leggett Street'
   AND transaction_type = 'withdraw';

-- To see phone calls made in that day
   SELECT *
   FROM phone_calls
   WHERE year = 2023
   AND month = 7
   AND day = 28
   AND duration <= 60;

-- To see earliest flight that day
   SELECT *
   FROM flights
   WHERE year = 2023
   AND month = 7
   AND day = 28
   AND hour >= 10 ORDER BY hour ASC;

-- Too see passengers on the earliest flight that day
   SELECT *
   FROM passengers
   JOIN flights
   ON passengers.flight_id = flights.id
   WHERE flights.origin_airport_id = 1
   AND flights.destination_airport_id = 8
   AND flights.year = 2023
   AND flights.month = 7
   AND flights.day = 28
   AND flights.hour >= 10;

-- Too see phone calls made in that day with names of callers
   SELECT people.name, phone_calls.caller, phone_calls.receiver, phone_calls.year, phone_calls.month, phone_calls.day, phone_calls.duration
   FROM phone_calls
   JOIN people
   ON phone_calls.caller = people.phone_number
   WHERE phone_calls.year = 2023
   AND phone_calls.month = 7
   AND phone_calls.day = 28
   AND phone_calls.duration <= 60;

-- To find Fiftyville airport
   SELECT * FROM airports WHERE city = 'Fiftyville';

-- Flights out From Fiftyville airport (First)
   SELECT f.*, origin.full_name AS origin_airport, destination.full_name AS destination_airport
   FROM flights AS f
   JOIN airports AS origin ON f.origin_airport_id = origin.id
   JOIN airports AS destination ON f.destination_airport_id = destination.id
   WHERE origin.id = 8 AND f.year = 2023 AND f.month = 7 AND f.day = 28 ORDER BY f.hour, f.minute;
-- in 29
   SELECT f.*, origin.full_name AS origin_airport, destination.full_name AS destination_airport
   FROM flights AS f
   JOIN airports AS origin ON f.origin_airport_id = origin.id
   JOIN airports AS destination ON f.destination_airport_id = destination.id
   WHERE origin.id = 8 AND f.year = 2023 AND f.month = 7 AND f.day = 29 ORDER BY f.hour, f.minute;


-- All interviews information about theft

   SELECT p.name
   FROM bakery_security_logs AS logs
   JOIN people AS p ON p.license_plate = logs.license_plate
   JOIN bank_accounts AS bank ON bank.person_id = p.id
   JOIN atm_transactions AS atm ON atm.account_number = bank.account_number
   JOIN phone_calls AS calls ON calls.caller = p.phone_number
   WHERE logs.year = 2023 AND logs.month = 7 AND logs.day = 28 AND logs.hour = 10 AND logs.minute BETWEEN 15 AND 35
   AND atm.atm_location = 'Leggett Street' AND atm.year = 2023 AND atm.month = 7 AND atm.day = 28 AND atm.transaction_type = 'withdraw'
   AND calls.year = 2023 AND calls.month = 7 AND calls.day = 28 AND calls.duration <= 60;

-- Find who is in flight
   SELECT p.name
   FROM people AS p
   JOIN passengers AS ps ON p.passport_number = ps.passport_number
   WHERE ps.flight_id = 36
   AND p.name IN ('Bruce', 'Diana');

-- Bruce called on that day
   SELECT p2.name AS receiver
   FROM phone_calls AS calls
   JOIN people AS p1 ON calls.caller = p1.phone_number
   JOIN people AS p2 ON calls.receiver = p2.phone_number
   WHERE p1.name = 'Bruce' AND calls.year = 2023 AND calls.month = 7 AND calls.day = 28 AND calls.duration < 60;
