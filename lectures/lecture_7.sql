create table employee (
	Id varchar(5),
	Name varchar(50),
	Street varchar(255),
	City varchar(50),
	primary key (Id));
    
create table company (
	Company varchar(50),
	City varchar(50),
	primary key (Company));

-- works table with foreign key references to employee and company
create table works (
	Id varchar(5),
	Company varchar(50),
	Salary numeric(8,2) CHECK (salary >= 0),
	primary key (Id, Company),
	foreign key (Id) references employee(Id));

-- manager table with foreign key references to employee
create table manager (
	e_Id varchar(5),
	m_Id varchar(5),
	primary key (e_Id),
	foreign key (e_Id) references employee(Id),
	foreign key (m_Id) references employee(Id));
    

