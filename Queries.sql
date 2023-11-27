--For beneficiaries-
--Create table--
CREATE TABLE Beneficiaries (
    Beneficiary_ID SERIAL PRIMARY KEY,
    Full_Name VARCHAR(255),
    Birthdate DATE,
    Birth_Place VARCHAR(255),
    Disability_category VARCHAR(50),
    Disability_Start_Date DATE,
    Documents VARBINARY(MAX),
    Gender VARCHAR(10),
    Join_Date DATE
);
--Delete---
DELETE FROM Beneficiaries WHERE Beneficiary_ID = Benf_entered_ID;
--ADD new ---
INSERT INTO Beneficiaries (Full_Name, Birthdate, Birth_Place, Disability_Start_Date, Documents, Gender)
            VALUES (%(Full_Name)s, %(Birthdate)s, %(Birth_Place)s, %(Disability_Start_Date)s, %(Documents)s, %(Gender)s);
--Update--
UPDATE Beneficiaries
            SET
                Full_Name = %(Full_Name)s,
                Birthdate = %(Birthdate)s,
                Birth_Place = %(Birth_Place)s,
                Disability_Start_Date = %(Disability_Start_Date)s,
                Documents = %(Documents)s,
                Gender = %(Gender)s
            WHERE Beneficiary_ID = %(Beneficiary_ID)s;
--view--
Select * From Beneficiaries ;







--Donors--
--Create Table--
CREATE TABLE Donors (
    Donor_ID SERIAL PRIMARY KEY,
    Full_Name VARCHAR(255),
    Phone_Number VARCHAR(15),
    Email VARCHAR(255),
    Join_Date DATE,
    Birthdate DATE,
    Address VARCHAR(255),
    Docs VARBINARY(MAX),
    Gender  VARCHAR(255)
);
--Delete--
DELETE FROM Donors WHERE Donor_ID = Donor_entered_ID;
--Update--
 UPDATE Donors
            SET
                Full_Name = %(Full_Name)s,
                Phone_Number = %(Phone_Number)s,
                Email = %(Email)s,
                Join_Date = %(Join_Date)s,
                Birthdate = %(Birthdate)s,
                Address = %(Address)s,
                Docs = %(Docs)s
            WHERE Donor_ID = %(Donor_ID)s;
--Add New--
INSERT INTO Donors (Full_Name, Phone_Number, Email, Join_Date, Birthdate, Address, Docs)
            VALUES (%(Full_Name)s, %(Phone_Number)s, %(Email)s, %(Join_Date)s, %(Birthdate)s, %(Address)s, %(Docs)s);
--View--
select * from Donors;



--Authority--
--Create Table--
CREATE TABLE Authorities (
    Authority_ID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Address VARCHAR(255),
    Email VARCHAR(255),
    Phone_Number VARCHAR(15),
    Join_Date DATE
);
--view--
SELECT * FROM Authorities;
--Delete--
DELETE FROM Authorities WHERE Authority_ID = entred_Authority_ID;
--add--
INSERT INTO  Authorities (Name, Address, Email, Phone_Number, Fax_Number)
            VALUES (%(Name)s, %(Address)s, %(Email)s, %(Phone_Number)s, %(Fax_Number)s);
--Update--
UPDATE Authorities
SET
    Name = %(Name)s,
    Address =  %(Address)s,
    Email =  %(Email)s,
    Phone_Number = %(Phone_Number)s,
    Fax_Number = %(Fax_Number)s,
WHERE Authority_ID = %(Authority_ID)s;
-- Needs to be added: Forms,Donations,announcement,campaign,event, users.--
-- Create Monetary_Donation table
CREATE TABLE Monetary_Donation (
    Donation_ID SERIAL PRIMARY KEY,
    owner_ID INT,
    Amount DECIMAL(10, 2),  
    Payment_method VARCHAR(50),
    is_association BOOLEAN,
    Date_created DATE DEFAULT GETDATE()
);

-- Create Other_Donation table
CREATE TABLE Other_Donation (
    Donation_ID SERIAL PRIMARY KEY,
    owner_ID INT,
    Description TEXT,
    Is_Association BOOLEAN,
    Date_created DATE DEFAULT GETDATE()
);

-- Create Campaign table
CREATE TABLE Campaign (
    Campaign_ID SERIAL PRIMARY KEY,
    Title VARCHAR(100),
    Text TEXT,
    Img VARBINARY(MAX),
    Date_created DATE DEFAULT GETDATE(),
    start_date DATE,
    End_date DATE
);

-- Create Announcement table
CREATE TABLE Announcement (
    Announcement_ID SERIAL PRIMARY KEY,
    title VARCHAR(100),
    text TEXT,
    Date_created DATE DEFAULT GETDATE()
);

-- Create Admin table
CREATE TABLE Admin (
    Admin_ID SERIAL PRIMARY KEY,
    Admin_Name VARCHAR(100),
    Admin_PhoneNumber VARCHAR(25),  -- Assuming a standard phone number format
    Address VARCHAR(100),
    Email TEXT,
    Login VARCHAR(50),
    Password VARCHAR(50),
    Date_created DATE DEFAULT GETDATE()
);


