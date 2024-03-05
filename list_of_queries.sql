/*
    FunGeo Website SQL Queries
    --------------------------

    This SQL file contains queries for managing user accounts, geography data, exam records,
    user profiles, top performers, and various administrative tasks for the FunGeo website.

    Table of Contents:
    ------------------
    1. User Management
    2. Subject Management
    3. Exam Management
    4. Geography Data Management
    5. Top Performers
    6. Views for Each Subject
    7. Queries to Narrow Down Options for Answers
    8. Smart Queries for Exam Questions
*/

-- 1. User Management

-- Register a new user
INSERT INTO User (username, password) VALUES ($username, $password);

-- Authenticate a user
SELECT * FROM User WHERE username = $username AND password = $password;

-- Retrieve user information by username
SELECT * FROM User WHERE username = $username;

-- Update user password
UPDATE User SET password = $new_password WHERE username = $username;

-- Delete user's profile and related data
DELETE FROM User WHERE username = '$username';
DELETE FROM Exam WHERE user_id = 'user_id';

-- Count the number of registered users
SELECT COUNT(*) AS user_count FROM User;

-- 2. Subject Management

-- Add subjects if not exists
INSERT IGNORE INTO Subject (subject_name) VALUES 
('Flags'),
('Capital Cities'),
('Currency Types'),
('Flags - North America'),
('Flags - Asia'),
('Flags - Europe'),
('Flags - South America'),
('Flags - Oceania'),
('Flags - Africa'),
('Capital Cities - North America'),
('Capital Cities - Asia'),
('Capital Cities - Europe'),
('Capital Cities - South America'),
('Capital Cities - Oceania'),
('Capital Cities - Africa'),
('Currency Types - North America'),
('Currency Types - Asia'),
('Currency Types - Europe'),
('Currency Types - South America'),
('Currency Types - Oceania'),
('Currency Types - Africa'),
('Flags - Population > 100k'),
('Flags - Population > 1M'),
('Flags - Population > 10M'),
('Capital Cities - Population > 100k'),
('Capital Cities - Population > 1M'),
('Capital Cities - Population > 10M'),
('Currency Types - Population > 100k'),
('Currency Types - Population > 1M'),
('Currency Types - Population > 10M');

-- Retrieve all subjects
SELECT * FROM Subject;

-- 3. Exam Management

-- Record exam result
INSERT INTO Exam (user_id, subject_id, grade) VALUES ($user_id, $subject_id, $grade);

-- Enroll user in a subject
INSERT INTO Exam (user_id, subject_id, grade) VALUES ($user_id, $subject_id, NULL);

-- Check if user is enrolled in a subject
SELECT * FROM Exam WHERE user_id = $user_id AND subject_id = $subject_id;

-- Retrieve user's exam results
SELECT Subject.subject_name,
       Exam.grade
FROM Exam
JOIN Subject ON Exam.subject_id = Subject.subject_id
WHERE Exam.user_id = $user_id;

-- Unenroll exam for a user
DELETE FROM Exam WHERE user_id = $user_id AND subject_id = $subject_id;

-- Update user's grade for a subject
UPDATE Exam SET grade = $new_grade WHERE user_id = $user_id AND subject_id = $subject_id;

-- Delete user's attempt for a subject
DELETE FROM Exam WHERE user_id = $user_id AND subject_id = $subject_id;

-- 4. Geography Data Management

-- Retrieve all continents
SELECT * FROM Continent;

-- Retrieve country information by name
SELECT * FROM Country WHERE country_name = $country_name;

-- Retrieve all countries information by continent
SELECT * FROM Country WHERE continent_name = $continent_name;

-- Retrieve capital city information by country_code
SELECT City.city_name
FROM City
JOIN Capital ON City.city_id = Capital.city_id
WHERE Capital.country_code = $country_code;

-- Retrieve capital city information by country_name
SELECT City.city_name
FROM City
JOIN Capital ON City.city_id = Capital.city_id
JOIN Country ON Capital.country_code = Country.country_code
WHERE Country.country_name = $country_name;

-- Retrieve all cities in a country
SELECT * FROM City WHERE country_code = $country_code;

-- Search for a country by name
SELECT * FROM Country WHERE country_name LIKE %search_term%;

-- Retrieve specific country information for identity card display
SELECT
    Country.country_name,
    MAX(CASE WHEN City.city_id = Capital.city_id THEN City.city_name END) AS capital_city,
    MAX(Country.flag_image_url) AS flag_image_url,
    MAX(Country.currency) AS currency,
    GROUP_CONCAT(DISTINCT City.city_name ORDER BY City.city_name SEPARATOR ', ') AS city_names
FROM Country
JOIN Capital ON Country.country_code = Capital.country_code
JOIN City ON Capital.country_code = City.country_code
WHERE Country.country_name = $country_name
GROUP BY Country.country_name;

-- Search for a country by name without the need for registration
SELECT 
    Country.country_name,
    MAX(CASE WHEN City.city_id = Capital.city_id THEN City.city_name END) AS capital_city,
    MAX(Country.flag_image_url) AS flag_image_url,
    MAX(Country.currency) AS currency,
    GROUP_CONCAT(DISTINCT City.city_name ORDER BY City.city_name SEPARATOR ', ') AS city_names
FROM 
    Country
JOIN 
    Capital ON Country.country_code = Capital.country_code
JOIN 
    City ON Capital.city_id = City.city_id
WHERE 
    Country.country_name LIKE '%$search_term%'
GROUP BY 
    Country.country_name;
    
-- Retrieve all countries in a continent
SELECT * FROM Country WHERE continent_name = $continent_name;

-- Retrieve all cities in a country
SELECT * FROM City WHERE country_code = $country_code;

-- 5. Top Performers

-- Retrieve user's top 5 grades for user
SELECT Subject.subject_name, MAX(Exam.grade) AS max_grade
FROM Exam
JOIN Subject ON Exam.subject_id = Subject.subject_id
WHERE Exam.user_id = $user_id
GROUP BY Exam.subject_id
ORDER BY max_grade DESC
LIMIT 5;

-- Retrieve user's top 5 grades for each user
SELECT 
    e1.user_id,
    s.subject_name,
    e1.grade
FROM Exam e1
JOIN Subject s ON e1.subject_id = s.subject_id
WHERE (
    SELECT COUNT(*)
    FROM Exam e2
    WHERE e2.user_id = e1.user_id AND e2.grade >= e1.grade
) <= 5;

-- Retrieve top 5 grades for a specific subject
SELECT User.username , User.user_id , Exam.grade
FROM Exam
JOIN User ON Exam.user_id = User.user_id
WHERE Exam.subject_id = $subject_id
ORDER BY Exam.grade DESC
LIMIT 5;

-- Retrieve the usernames of users who have not attempted any exams
SELECT username
FROM User
WHERE user_id NOT IN (
    SELECT DISTINCT user_id
    FROM Exam
);

-- Retrieve the subject IDs of subjects that have not been enrolled by any user
SELECT subject_id
FROM Subject
WHERE subject_id NOT IN (
    SELECT DISTINCT subject_id
    FROM Exam
);

-- Retrieve the usernames of users who have not enrolled in any subjects
SELECT username
FROM User
WHERE user_id NOT IN (
    SELECT DISTINCT user_id
    FROM Exam
);

-- Retrieve the subject IDs of subjects that have no exam attempts recorded
SELECT subject_id
FROM Subject
WHERE subject_id NOT IN (
    SELECT DISTINCT subject_id
    FROM Exam
);

-- Retrieve the subject IDs of subjects that have no top performers recorded
SELECT subject_id
FROM Subject
WHERE subject_id NOT IN (
    SELECT DISTINCT subject_id
    FROM Exam
    WHERE grade = (SELECT MAX(grade) FROM Exam)
);

-- Retrieve usernames of users whose average exam grade is higher than the overall average grade
SELECT User.username
FROM User
JOIN (
    SELECT user_id, AVG(grade) AS avg_grade
    FROM Exam
    GROUP BY user_id
    HAVING AVG(grade) >= (
        SELECT AVG(grade) AS overall_avg_grade
        FROM Exam
    )
) AS user_avg_grade ON User.user_id = user_avg_grade.user_id;

-- 6. Views for Each Subject

-- View for Flags
CREATE OR REPLACE VIEW Flags_View AS
SELECT Country.country_name, Country.flag_image_url
FROM Country;

-- View for Capital Cities
CREATE OR REPLACE VIEW CapitalCities_View AS
SELECT Country.country_name, City.city_name AS capital_city
FROM Country
JOIN Capital ON Country.country_code = Capital.country_code
JOIN City ON Capital.city_id = City.city_id;

-- View for Currency Types
CREATE OR REPLACE VIEW CurrencyTypes_View AS
SELECT Country.country_name, Country.currency
FROM Country;

-- 7. Queries to Narrow Down Options for Answers

-- Retrieve random country for answer options
SELECT * FROM Country ORDER BY RAND() LIMIT 1;

-- Retrieve random countries excluding correct answer for options
SELECT * FROM Country WHERE country_name != $correct_country_name ORDER BY RAND() LIMIT 3;

-- Retrieve random capital city for answer options
SELECT City.city_name
FROM City
JOIN Capital ON City.city_id = Capital.city_id
ORDER BY RAND()
LIMIT 1;

-- Retrieve random capital cities excluding correct answer for options
SELECT City.city_name
FROM City
JOIN Capital ON City.city_id = Capital.city_id
WHERE City.city_name != $correct_city_name
ORDER BY RAND()
LIMIT 3;

-- Retrieve random currency type for answer options
SELECT currency
FROM Country
ORDER BY RAND()
LIMIT 1;

-- Retrieve random currency types excluding correct answer for options
SELECT currency
FROM Country
WHERE currency != $correct_currency
ORDER BY RAND()
LIMIT 3;

-- 8. Smart Queries for Exam Questions

-- Retrieve random flag question with options
-- Step 1: Select a random country along with its flag and continent
SELECT
    FQ.country_name AS question,
    FQ.flag_image_url,
    C.continent_name
FROM Flags_View AS FQ
JOIN Country AS C ON FQ.country_name = C.country_name
ORDER BY RAND()
LIMIT 1;
-- Step 2: Select three random countries from the same continent as the question country as options
SELECT DISTINCT
    FO1.country_name AS option_1,
    FO2.country_name AS option_2,
    FO3.country_name AS option_3
FROM
    Flags_View AS FO1
JOIN Country AS CO1 ON FO1.country_name = CO1.country_name
JOIN Flags_View AS FO2 
JOIN Country AS CO2 ON FO2.country_name = CO2.country_name
JOIN Flags_View AS FO3 
JOIN Country AS CO3 ON FO3.country_name = CO3.country_name
WHERE
    CO1.continent_name = $continent_name -- Replace $continent_name with the continent name from Step 1
    AND CO2.continent_name = $continent_name
    AND CO3.continent_name = $continent_name
    AND FO1.country_name != $country_name -- Replace $country_name with the continent name from Step 1
    AND FO2.country_name != $country_name 
    AND FO3.country_name != $country_name
ORDER BY RAND()
LIMIT 1;

-- Retrieve random capital city question with options
-- Step 1: Select a random country and its capital city
SELECT
    Country.country_name,
    Capital.city_id,
    Capital.country_code,
    City.city_name AS capital_city
FROM
    Country
JOIN
    Capital ON Country.country_code = Capital.country_code
JOIN
    City ON City.city_id = Capital.city_id
WHERE
	City.city_name <>'NaN'
ORDER BY
    RAND()
LIMIT 1;
-- Step 2: Select three random cities from the same country as options, excluding the capital city
SELECT
    City.city_name,
    City.city_id,
    City.country_code
FROM
    City
JOIN
    Country ON City.country_code = Country.country_code
JOIN
    Capital ON Country.country_code = Capital.country_code
WHERE
    City.country_code = $country_code -- Replace $country_code with the country code from the first section
    AND City.city_id != (SELECT capital.city_id FROM capital WHERE country_code = City.country_code)
    AND City.city_name <> 'NaN'
ORDER BY
    RAND()
LIMIT 3;


-- Retrieve random currency question with options
-- Step 1: Select a random currency and a country where it's used
SELECT
    Country.country_name,
    Country.currency
FROM
    Country
ORDER BY
    RAND()
LIMIT 1;
-- Step 2: Select three random countries from the same continent as options, excluding the country where the currency is used
SELECT DISTINCT
    CO1.country_name AS option_1,
    CO2.country_name AS option_2,
    CO3.country_name AS option_3
FROM
    Country AS CO1
JOIN
    Country AS CO2
JOIN
    Country AS CO3
JOIN
    Country AS MainCountry ON CO1.continent_name = MainCountry.continent_name
WHERE
    CO1.country_name != MainCountry.country_name
    AND CO2.country_name != MainCountry.country_name
    AND CO3.country_name != MainCountry.country_name
    AND CO1.currency !=  $selected_currency -- Exclude countries with currency currency
    AND CO2.currency !=  $selected_currency
    AND CO3.currency !=  $selected_currency
    AND MainCountry.country_name = $selected_country_name -- Ensure the country  $selected_country_name is on the same continent
    AND CO1.continent_name = MainCountry.continent_name -- Ensure same continent as  $selected_country_name
    AND CO2.continent_name = MainCountry.continent_name
    AND CO3.continent_name = MainCountry.continent_name
    AND CO1.country_name NOT IN (CO2.country_name, CO3.country_name) -- Ensure option 1 is different from option 2 and option 3
    AND CO2.country_name NOT IN (CO1.country_name, CO3.country_name) -- Ensure option 2 is different from option 1 and option 3
    AND CO3.country_name NOT IN (CO1.country_name, CO2.country_name) -- Ensure option 3 is different from option 1 and option 2
ORDER BY
    RAND()
LIMIT 1;
