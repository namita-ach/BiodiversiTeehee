-- Create the Biodiversity Tracking database and tables, and insert initial data

-- Create Database
CREATE DATABASE BiodiversityTracking;

-- Use the created database
USE BiodiversityTracking;

-- Table for Species
CREATE TABLE Species (
    SpeciesID INT AUTO_INCREMENT PRIMARY KEY,
    CommonName VARCHAR(255) NOT NULL,
    ScientificName VARCHAR(255) NOT NULL,
    Habitat VARCHAR(255),
    ConservationStatus VARCHAR(100)
);

-- Table for Sustainability Initiatives
CREATE TABLE SustainabilityInitiative (
    InitiativeID INT AUTO_INCREMENT PRIMARY KEY,
    InitiativeName VARCHAR(255) NOT NULL,
    Description TEXT,
    StartDate DATE,
    EndDate DATE
);

-- Table for Biodiversity Metrics
CREATE TABLE BiodiversityMetric (
    MetricID INT AUTO_INCREMENT PRIMARY KEY,
    SpeciesID INT,
    InitiativeID INT,
    MetricValue DECIMAL(10, 2),
    MeasurementDate DATE,
    FOREIGN KEY (SpeciesID) REFERENCES Species(SpeciesID),
    FOREIGN KEY (InitiativeID) REFERENCES SustainabilityInitiative(InitiativeID)
);

-- Table for Users
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(100) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    UserRole ENUM('Researcher', 'City Planner', 'Conservationist', 'Administrator', 'Policy Maker', 'Citizen Scientist') NOT NULL
);

-- Table for Reports
CREATE TABLE Reports (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    ReportTitle VARCHAR(255) NOT NULL,
    ReportContent TEXT,
    CreationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Insert data into Species table
INSERT INTO Species (CommonName, ScientificName, Habitat, ConservationStatus) VALUES
('Eastern Bluebird', 'Sialia sialis', 'Open fields and woodlands', 'Least Concern'),
('American Robin', 'Turdus migratorius', 'Urban areas and forests', 'Least Concern'),
('Red-tailed Hawk', 'Buteo jamaicensis', 'Open fields and forests', 'Least Concern'),
('Northern Cardinal', 'Cardinalis cardinalis', 'Woodlands and gardens', 'Least Concern'),
('Bald Eagle', 'Haliaeetus leucocephalus', 'Near large bodies of water', 'Least Concern'),
('Great Horned Owl', 'Bubo virginianus', 'Forests and urban areas', 'Least Concern'),
('Eastern Chipmunk', 'Tamias striatus', 'Forests and gardens', 'Least Concern'),
('White-tailed Deer', 'Odocoileus virginianus', 'Forests and grasslands', 'Least Concern'),
('American Black Bear', 'Ursus americanus', 'Forests and mountains', 'Least Concern'),
('Common Snapping Turtle', 'Chelydra serpentina', 'Freshwater habitats', 'Least Concern');

-- Insert data into SustainabilityInitiative table
INSERT INTO SustainabilityInitiative (InitiativeName, Description, StartDate, EndDate) VALUES
('Urban Tree Planting Program', 'A program aimed at increasing green cover in urban areas.', '2023-01-15', '2024-01-15'),
('Community Clean-Up Day', 'An initiative to clean local parks and waterways.', '2023-03-20', NULL),
('Wildlife Habitat Restoration Project', 'Restoring habitats for local wildlife.', '2023-05-10', NULL),
('Pollinator Garden Initiative', 'Creating gardens to support local pollinators.', '2023-04-01', NULL),
('Sustainable Urban Farming Initiative', 'Promoting urban agriculture to enhance food security.', '2023-06-15', NULL),
('Rainwater Harvesting Program', 'Encouraging rainwater collection for irrigation.', '2023-07-01', NULL),
('Community Composting Program', 'A program to promote composting in neighborhoods.', '2023-08-01', NULL),
('Green Roof Initiative', 'Installing green roofs on public buildings.', '2023-09-01', NULL),
('Electric Vehicle Promotion Campaign', 'Promoting electric vehicles to reduce carbon footprint.', '2023-10-01', NULL),
('Local Biodiversity Awareness Campaign', 'Educating the community about local biodiversity.', '2023-11-01', NULL);

-- Insert data into BiodiversityMetric table
INSERT INTO BiodiversityMetric (SpeciesID, InitiativeID, MetricValue, MeasurementDate) VALUES
(1, 1, 150.00, '2023-02-01'),
(2, 1, 200.00, '2023-02-01'),
(3, 2, 50.00,  NULL),
(4, 2, 75.00,  NULL),
(5, 3, 30.00,  NULL),
(6, 3, 45.00,  NULL),
(7, 4, 100.00, NULL),
(8, 4, 120.00, NULL),
(9, 5, 10.00,  NULL),
(10, 5, 15.00,  NULL),
(1, 6, 160.00, NULL),
(2, 6, 210.00, NULL),
(1, 7, 140.00, NULL),
(2, 7, 190.00, NULL),
(8, 8, 80.00 ,NULL),
(9, 8 ,90.00 ,NULL),
(10 ,9 ,5.00 ,NULL),
(1 ,9 ,12.00 ,NULL),
(2 ,10 ,25.00 ,NULL),
(3 ,10 ,35.00 ,NULL);

-- Insert data into Users table
INSERT INTO Users (Username, PasswordHash, UserRole) VALUES
('researcher1','hashed_password_1','Researcher'),
('cityplanner1','hashed_password_2','City Planner'),
('conservationist1','hashed_password_3','Conservationist'),
('admin1','hashed_password_4','Administrator'),
('policymaker1','hashed_password_5','Policy Maker'),
('citizenscientist1','hashed_password_6','Citizen Scientist'),
('researcher2','hashed_password_7','Researcher'),
('cityplanner2','hashed_password_8','City Planner'),
('conservationist2','hashed_password_9','Conservationist'),
('admin2','hashed_password_10','Administrator');

-- Insert data into Reports table
INSERT INTO Reports (UserID, ReportTitle, ReportContent) VALUES
(1,'Biodiversity Trends in Urban Areas','This report analyzes the trends in urban biodiversity over the last year.'),
(2,'Impact of Tree Planting on Local Species','An assessment of how tree planting initiatives have affected local species diversity.'),
(3,'Wildlife Habitat Restoration Outcomes','Evaluating the success of habitat restoration projects in increasing species populations.'),
(4,'Pollinator Gardens: A Success Story','Documenting the positive impact of pollinator gardens on local bee populations.'),
(5,'Community Clean-Up Impact Report','An analysis of the effects of community clean-up days on local waterways.'),
(6,'Urban Agriculture Benefits Report','Exploring the benefits of urban farming initiatives on food security and biodiversity.');

-- Functions to manage biodiversity data

-- Create a biodiversity metric
INSERT INTO BiodiversityMetric (SpeciesID, InitiativeID, MetricValue, MeasurementDate)
VALUES (21, 5, 3, 40.00, '2024-01-01');

-- Read biodiversity metric for species
SELECT * FROM BiodiodiversityMetric WHERE SpeciesID = 1;

-- Update a biodiversity metric and log change
UPDATE BiodiversityMetric
SET MetricValue = 155.00
WHERE MetricID = 1;

INSERT INTO BiodiversityMetricLog (MetricID, ChangeDescription)
VALUES (1, 'MetricValue updated to 155.00');

-- Delete a biodiversity metric for cleanup with trigger prevention
DELIMITER //

CREATE TRIGGER PreventDeleteIfReferenced
BEFORE DELETE ON BiodiversityMetric
FOR EACH ROW
BEGIN
    DECLARE ref_count INT;

    -- Check if the MetricID being deleted is referenced in RelatedTable
    SELECT COUNT(*) INTO ref_count
    FROM RelatedTable
    WHERE MetricID = OLD.MetricID;

    -- If a reference exists prevent deletion by raising an error-like behavior 
    IF ref_count > 0 THEN 
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 
        'Cannot delete or update parent row: foreign key constraint fails. MetricID is still referenced in RelatedTable.'; 
    END IF; 
END//

DELIMITER ;

-- Set up triggers to automatically log changes whenever a BiodiversityMetric entry is updated or deleted.

DELIMITER //

CREATE TRIGGER LogMetricUpdate
AFTER UPDATE ON BiodiversityMetric 
FOR EACH ROW 
BEGIN 
   INSERT INTO BiodiversityMetricLog (MetricID , ChangeDescription ) 
   VALUES (NEW.MetricID , CONCAT ('Updated to ', NEW.MetricValue)); 
END// 

DELIMITER ;

DELIMITER // 
CREATE TRIGGER LogMetricDelete 
BEFORE DELETE ON BiodiversityMetric 
FOR EACH ROW 
BEGIN 
   INSERT INTO BiodiversityMetricLog (MetricID , ChangeDescription ) 
   VALUES (OLD.MetricID , ‘Metric entry deleted’); 
END// 

DELIMITER ;

-- Stored Procedure to retrieve biodiversity metrics for a given initiative with optional date filter.
DELIMITER //

CREATE PROCEDURE GetMetricsByInitiative(IN initiative_id INT , IN metric_date DATE ) 
BEGIN 
   SELECT * FROM BiodiversityMetric 
   WHERE InitiativeID = initiative_id AND (metric_date IS NULL OR MeasurementDate = metric_date); 
END// 

DELIMITER ;

-- Aggregate queries to give the range of metric value.
SELECT SpeciesID ,
       MAX(MetricValue) - MIN(MetricValue) AS MetricRange 
FROM BiodiversityMetric 
GROUP BY SpeciesID;

-- Manage user data with CRUD operations

-- Create new user
INSERT INTO Users (Username , PasswordHash , UserRole ) 
VALUES (11 ,'newresearcher' ,'hashed_password_11' ,'Researcher');

-- Update user roles (user to admin)
UPDATE Users SET UserRole = ‘Administrator’ WHERE UserID = 3;

-- Delete user if required.
DELETE FROM Users WHERE UserID = 10;

-- Stored procedure to retrieve all users by role.
CREATE PROCEDURE GetUsersByRole(IN role VARCHAR(255)) 
BEGIN 
   SELECT * FROM Users WHERE UserRole = role; 
END;

-- Contribute data with trigger logging contributions linking UserID and MetricID.
CREATE TABLE ContributionLog (
   ContributionID INT PRIMARY KEY AUTO_INCREMENT ,
   UserID INT ,
   MetricID INT ,
   ContributionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
   FOREIGN KEY (UserID) REFERENCES Users(UserID) ,
   FOREIGN KEY (MetricID) REFERENCES BiodiversityMetric(MetricID)
);

DELIMITER //

CREATE TRIGGER LogContribution 
AFTER INSERT ON BiodiversityMetric 
FOR EACH ROW 
BEGIN 

   INSERT INTO ContributionLog (UserID , MetricID ) 
   VALUES (@user_id , NEW.MetricID );  
END // 

DELIMITER ;

-- Generate reports with view summarizing biodiversity metrics per species and initiative.
CREATE VIEW SpeciesInitiativeMetrics AS 
SELECT S.CommonName , S.ScientificName , SI.InitiativeName , AVG(BM.MetricValue) AS AvgMetricValue 
FROM Species AS S 
JOIN BiodiversityMetric AS BM ON S.SpeciesID = BM.SpeciesID 
JOIN SustainabilityInitiative AS SI ON BM.InitiativeID = SI.InitiativeID 
GROUP BY S.CommonName , S.ScientificName , SI.InitiativeName;

-- Track initiatives with read operations.
SELECT SI.InitiativeName , S.CommonName , SI.StartDate , SI.EndDate 
FROM SustainabilityInitiative AS SI 
JOIN BiodiversityMetric AS BM ON SI.InitiativeID = BM.InitiativeID  
JOIN Species AS S ON BM.SpeciesID = S.SpeciesID  
WHERE S.SpeciesID = 1; -- Replace with the desired species ID

-- Nested query to track all initiatives involving species that have more than a specified number of recorded metrics.
SELECT InitiativeName  
FROM SustainabilityInitiative AS SI  
WHERE InitiativeID IN (
   SELECT InitiativeID  
   FROM BiodiversityMetric  
   GROUP BY InitiativeID  
   HAVING COUNT(*) >5  
);
