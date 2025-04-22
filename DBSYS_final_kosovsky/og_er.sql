-- Create the Brands table
CREATE TABLE Brands (
    BrandID INT AUTO_INCREMENT PRIMARY KEY,
    BrandName VARCHAR(255)
);

-- Create the ProductTypes table
CREATE TABLE ProductTypes (
    ProductTypeID INT AUTO_INCREMENT PRIMARY KEY,
    ProductTypeName VARCHAR(255),
    ParentTypeID INT,
    FOREIGN KEY (ParentTypeID) REFERENCES ProductTypes(ProductTypeID)
);

-- Create the Products table
CREATE TABLE Products (
    UPC VARCHAR(255) PRIMARY KEY,
    ProductName VARCHAR(255),
    ProductSize VARCHAR(255),
    BrandID INT,
    ProductTypeID INT,
    FOREIGN KEY (BrandID) REFERENCES Brands(BrandID),
    FOREIGN KEY (ProductTypeID) REFERENCES ProductTypes(ProductTypeID)
);

-- Create the Vendors table
CREATE TABLE Vendors (
    VendorID INT AUTO_INCREMENT PRIMARY KEY,
    VendorName VARCHAR(255)
);

-- Create the Stores table
CREATE TABLE Stores (
    StoreID INT AUTO_INCREMENT PRIMARY KEY,
    StoreName VARCHAR(255),
    StoreAddress VARCHAR(255),
    StorePhone VARCHAR(255),
    StoreHours VARCHAR(255)
);

-- Create the Inventory table
CREATE TABLE Inventory (
    InventoryID INT AUTO_INCREMENT PRIMARY KEY,
    StoreID INT,
    UPC VARCHAR(255),
    QuantityInStock INT,
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID),
    FOREIGN KEY (UPC) REFERENCES Products(UPC)
);

-- Create the Customers table
CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Email VARCHAR(255),
    Address VARCHAR(255)
);

-- Create the Transactions table
CREATE TABLE Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    TransactionDate DATETIME,
    CustomerID INT,
    StoreID INT,
    UPC VARCHAR(255),
    Quantity INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID),
    FOREIGN KEY (UPC) REFERENCES Products(UPC)
);