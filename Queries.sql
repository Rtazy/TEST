--For beneficiaries-
--Create table--
CREATE TABLE Beneficiaries (
    Beneficiary_ID SERIAL PRIMARY KEY,
    Full_Name VARCHAR(255),
    Birthdate DATE,
    Birth_Place VARCHAR(255),
    Disability_Start_Date DATE,
    Documents VARBINARY(MAX),
    Gender VARCHAR(10)
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
    Docs VARCHAR(255)
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
    Fax_Number VARCHAR(15)
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


