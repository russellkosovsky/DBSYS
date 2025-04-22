# HW: 6
create table Patients (
	PatientID int,
	FirstName varchar(50),
	LastName varchar(50),
	DOB DATE,
    primary key(PatientID));

create table Doctors (
	DoctorID int,
	FirstName varchar(50),
	LastName varchar(50),
	Specialty varchar(100),
	primary key(DoctorID));

create table Tests (
	TestID int,
	TestName varchar(100),
	TestDescription text,
	primary key(TestID));

create table PatientTests (
	DateRun datetime,
    foreign key(PatientID) references Patients(PatientID),
	foreign key(DoctorID) references Doctors(DoctorID),
	foreign key(TestID) references Tests(TestID),
	primary key(PatientID, DoctorID, TestID, DateRun));

    

