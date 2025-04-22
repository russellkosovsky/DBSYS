-- This SQL scripts resets the database

-- DROPPING TABLES --
DROP TABLE IF EXISTS ReorderFulfillments;
DROP TABLE IF EXISTS TransactionItems;
DROP TABLE IF EXISTS ShoppingCart;
DROP TABLE IF EXISTS ReorderRequests;
DROP TABLE IF EXISTS ReorderThresholds;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS ProductPricing;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS VendorBrands;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS ProductTypes;
DROP TABLE IF EXISTS Brands;
DROP TABLE IF EXISTS Stores;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Vendors;



-- RE-GENERATING TABLES --
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role VARCHAR(255) NOT NULL,
    VendorID INT NULL,
    FOREIGN KEY (VendorID) REFERENCES Vendors(VendorID)
);

CREATE TABLE Vendors (
    VendorID INT AUTO_INCREMENT PRIMARY KEY,
    VendorName VARCHAR(255)
);

CREATE TABLE Brands (
    BrandID INT AUTO_INCREMENT PRIMARY KEY,
    BrandName VARCHAR(255),
    VendorID INT,
    FOREIGN KEY (VendorID) REFERENCES Vendors(VendorID)
);

CREATE TABLE ProductTypes (
    ProductTypeID INT AUTO_INCREMENT PRIMARY KEY,
    ProductTypeName VARCHAR(255),
    ParentTypeID INT,
    FOREIGN KEY (ParentTypeID) REFERENCES ProductTypes(ProductTypeID)
);

CREATE TABLE Stores (
    StoreID INT AUTO_INCREMENT PRIMARY KEY,
    StoreName VARCHAR(255),
    StoreAddress VARCHAR(255),
    StoreState VARCHAR(255),
    StorePhone VARCHAR(255),
    StoreHours VARCHAR(255),
    IsWebOnly BOOLEAN DEFAULT FALSE
);

CREATE TABLE Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    UPC VARCHAR(255) UNIQUE,
    ProductName VARCHAR(255),
    ProductSize VARCHAR(255),
    BrandID INT,
    ProductTypeID INT,
    FOREIGN KEY (BrandID) REFERENCES Brands(BrandID),
    FOREIGN KEY (ProductTypeID) REFERENCES ProductTypes(ProductTypeID)
);

-- allows for flexible pricing strategies across different stores, accommodating possible regional pricing variations
CREATE TABLE ProductPricing (
    PricingID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    StoreID INT,
    Price DECIMAL(10, 2),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID)
);

CREATE TABLE Inventory (
    InventoryID INT AUTO_INCREMENT PRIMARY KEY,
    StoreID INT,
    ProductID INT,
    QuantityInStock INT,
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Email VARCHAR(255),
    Address VARCHAR(255),
    Username VARCHAR(255) UNIQUE,
    Password VARCHAR(255)
);

CREATE TABLE ShoppingCart (
    CartID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    Quantity INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);


CREATE TABLE Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    TransactionDate DATETIME,
    CustomerID INT,
    StoreID INT,
    TotalPrice DECIMAL(10, 2),  -- Added column for storing the total price of the transaction
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);


CREATE TABLE TransactionItems (
    TransactionItemID INT AUTO_INCREMENT PRIMARY KEY,
    TransactionID INT,
    ProductID INT,
    Quantity INT,
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- VendorBrands manages the many-to-many relationship between vendors and brands
CREATE TABLE VendorBrands (
    VendorID INT,
    BrandID INT,
    FOREIGN KEY (VendorID) REFERENCES Vendors(VendorID),
    FOREIGN KEY (BrandID) REFERENCES Brands(BrandID),
    PRIMARY KEY (VendorID, BrandID)
);

CREATE TABLE ReorderThresholds (
    ProductID INT PRIMARY KEY,
    Threshold INT,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE ReorderRequests (
    ReorderID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    RequestedQuantity INT,
    RequestDate DATETIME,
    Status VARCHAR(255),  -- e.g., 'Pending', 'Fulfilled'
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- Table to track fulfillment of reorders by vendors
CREATE TABLE ReorderFulfillments (
    FulfillmentID INT AUTO_INCREMENT PRIMARY KEY,
    ReorderID INT,
    VendorID INT,
    DeliveryDate DATETIME,
    QuantityReceived INT,
    FOREIGN KEY (ReorderID) REFERENCES ReorderRequests(ReorderID),
    FOREIGN KEY (VendorID) REFERENCES Vendors(VendorID)
);


-- INSERTING DATA --
INSERT INTO Users (Username, Password, Role) VALUES
('manager', 'russell_man', 'manager'),
('customer', 'russell_cust', 'customer'),
('vendor', 'russell_vend', 'vendor'),
('dba', 'russell_dba', 'dba');

INSERT INTO Vendors (VendorName) VALUES
('Creative Arts Suppliers'),
('Craft Essentials Inc.'),
('Global Crafts Distributors');

INSERT INTO Brands (BrandName, VendorID) VALUES
('Crayola', 1),
('Fiskars', 2),
('Loops & Threads', 1),
('Winsor & Newton', 3);

INSERT INTO VendorBrands (VendorID, BrandID) VALUES
(1, 1),  -- Vendor 1 supplies Brand 1 (Crayola)
(1, 3),  -- Vendor 1 supplies Brand 3 (Loops & Threads)
(2, 2),  -- Vendor 2 supplies Brand 2 (Fiskars)
(3, 4);  -- Vendor 3 supplies Brand 4 (Winsor & Newton)

INSERT INTO ProductTypes (ProductTypeName, ParentTypeID) VALUES
('Art Supplies', NULL),
('Sewing Supplies', NULL),
('Painting Supplies', NULL),
('Colored Pencils', 1),
('Fabric Scissors', 2),
('Acrylic Paints', 3),
('Yarn', 2),
('Sketch Pads', 1);

INSERT INTO Products (UPC, ProductName, ProductSize, BrandID, ProductTypeID) VALUES
('000111222333', 'Crayola Colored Pencils 24 Pack', '24 Pack', 1, 4),
('000111222334', 'Fiskars Fabric Scissors', '8 inch', 2, 5),
('000111222335', 'Loops & Threads Woolen Yarn', '100g', 3, 7),
('000111222336', 'Winsor & Newton Professional Acrylic', '500ml', 4, 6),
('000111222337', 'Crayola Watercolor Set', '12 Colors', 1, 3),
('000111222338', 'Generic Sketch Pad', 'A4', 1, 8),
('000111222339', 'Crayola Oil Pastels', '24 Pack', 1, 1),
('000111222340', 'Fiskars Crafting Scissors', '5 inch', 2, 5),
('000111222341', 'Winsor & Newton Gouache', '250ml', 4, 6),
('000111222342', 'Generic Acrylic Brushes', 'Set of 10', 1, 6);

INSERT INTO Stores (StoreName, StoreAddress, StoreState, StorePhone, StoreHours, IsWebOnly) VALUES
('Michaels Downtown', '1200 Main St, Downtown City', 'CT', '555-0102', '9AM-9PM', FALSE),
('Michaels Uptown', '450 Uptown Blvd, Metro City', 'CT', '555-0203', '10AM-8PM', FALSE),
('Michaels Mass', '114 Lincoln St, Northboro', 'MA', '555-0203', '10AM-8PM', FALSE),
('Michaels Online', NULL, NULL, NULL, '24/7', TRUE);

INSERT INTO ProductPricing (ProductID, StoreID, Price) VALUES
(1, 1, 4.99),
(1, 2, 4.99),
(2, 1, 14.99),
(2, 2, 15.99),
(3, 1, 2.99),
(4, 1, 19.99),
(4, 3, 18.99),
(5, 1, 7.99),
(5, 2, 8.49),
(6, 3, 5.99),
(1, 4, 5.49), -- Crayola Colored Pencils 24 Pack in the Online Store
(2, 4, 16.99), -- Fiskars Fabric Scissors in the Online Store
(3, 4, 3.49), -- Loops & Threads Woolen Yarn in the Online Store
(4, 4, 21.99), -- Winsor & Newton Professional Acrylic in the Online Store
(5, 4, 9.99), -- Crayola Watercolor Set in the Online Store
(6, 4, 6.99), -- Generic Acrylic Brushes in the Online Store
(7, 4, 10.99), -- Crayola Oil Pastels in the Online Store
(8, 4, 11.99); -- Generic Sketch Pad in the Online Store

INSERT INTO Inventory (StoreID, ProductID, QuantityInStock) VALUES
(1, 1, 150),
(1, 2, 100),
(2, 2, 80),
(1, 3, 200),
(1, 4, 90),
(1, 5, 120),
(2, 5, 140),
(3, 6, 150),
(4, 1, 120),  -- Crayola Colored Pencils 24 Pack
(4, 2, 85),   -- Fiskars Fabric Scissors
(4, 3, 150),  -- Loops & Threads Woolen Yarn
(4, 4, 75),   -- Winsor & Newton Professional Acrylic
(4, 5, 90),   -- Crayola Watercolor Set
(4, 6, 100),  -- Generic Acrylic Brushes
(4, 7, 80),   -- Crayola Oil Pastels
(4, 8, 95);   -- Generic Sketch Pad

INSERT INTO Customers (FirstName, LastName, Email, Address, Username, Password) VALUES
('Emily', 'Smith', 'emily.smith@example.com', '35 Oak Ave, Suburb City', 'emily', 'password123'),
('David', 'Johnson', 'david.johnson@example.com', '202 Pine Rd, Nearby Town', 'david', 'password123'),
('Alice', 'Wonderland', 'alice.w@example.com', '123 Fantasy Rd', 'alice', 'password123'),
('Bob', 'Builder', 'bob.b@example.com', '456 Construction Pl', 'bob', 'builder123'),
('Russell', 'Kosovsky', 'rkosovsky@conncoll.edu', '114 Lincoln St', 'russ', 'password123');

INSERT INTO Transactions (TransactionDate, CustomerID, StoreID, TotalPrice) VALUES
('2024-05-01 14:30:00', 1, 1, 99.97),
('2024-05-01 15:00:00', 2, 2, 69.97),
('2024-05-02 10:00:00', 1, 1, 26.68),
('2024-05-02 11:30:00', 2, 3, 92.63),
('2024-05-01 10:00:00', 3, 1, 27.99),
('2024-05-02 12:30:00', 4, 2, 1000.00),
('2024-05-03 15:45:00', 3, 1, 101.12),
('2024-05-04 09:15:00', 4, 3, 7.42);

INSERT INTO TransactionItems (TransactionID, ProductID, Quantity) VALUES
(1, 1, 2),   -- Crayola Colored Pencils 24 Pack
(2, 2, 1),   -- Fiskars Fabric Scissors
(3, 5, 1),   -- Crayola Watercolor Set
(4, 6, 3),   -- Winsor & Newton Professional Acrylic
(5, 5, 1),   -- Crayola Watercolor Set (same transaction different item)
(5, 7, 2),   -- Crayola Oil Pastels
(5, 9, 1),   -- Winsor & Newton Gouache
(6, 5, 1),   -- Crayola Watercolor Set (another transaction)
(6, 10, 1),  -- Generic Acrylic Brushes
(6, 8, 1),   -- Fiskars Crafting Scissors
(7, 6, 3),   -- Generic Sketch Pad
(7, 7, 1),   -- Crayola Oil Pastels
(8, 8, 2);   -- Fiskars Crafting Scissors


-- Inserting data into ReorderThresholds
INSERT INTO ReorderThresholds (ProductID, Threshold) VALUES
(1, 50),  -- Assuming Crayola Colored Pencils should be reordered when stock falls below 50
(2, 30),  -- Fiskars Fabric Scissors
(3, 20),  -- Loops & Threads Woolen Yarn
(4, 40),  -- Winsor & Newton Professional Acrylic
(5, 10);  -- Crayola Watercolor Set

-- Inserting data into ReorderRequests
INSERT INTO ReorderRequests (ProductID, RequestedQuantity, RequestDate, Status) VALUES
(1, 100, '2024-05-10', 'Pending'),  -- Requesting more Crayola Colored Pencils
(2, 50, '2024-05-12', 'Fulfilled'),  -- More Fiskars Fabric Scissors
(3, 60, '2024-05-15', 'Pending'),   -- More Loops & Threads Woolen Yarn
(4, 20, '2023-08-7', 'Pending');

-- Inserting data into ReorderFulfillments
INSERT INTO ReorderFulfillments (ReorderID, VendorID, DeliveryDate, QuantityReceived) VALUES
(2, 2, '2024-05-20', 50);  -- Fulfilled order of Fiskars Fabric Scissors



-- Additional Product Entries
INSERT INTO Products (UPC, ProductName, ProductSize, BrandID, ProductTypeID) VALUES
('000111222343', 'Crayola Marker Set', '10 Pack', 1, 1),
('000111222344', 'Fiskars Detail Scissors', '4 inch', 2, 5),
('000111222345', 'Loops & Threads Merino Yarn', '200g', 3, 7),
('000111222346', 'Winsor & Newton Watercolor Pan Set', '24 colors', 4, 3),
('000111222347', 'Generic Oil Paints', '500ml', 1, 3),
('000111222348', 'Crayola Fabric Markers', '20 Pack', 1, 1),
('000111222349', 'Fiskars Heavy Duty Scissors', '9 inch', 2, 5),
('000111222350', 'Loops & Threads Cotton Yarn', '50g', 3, 7),
('000111222351', 'Winsor & Newton Ink Set', '6 Pack', 4, 6);

-- Additional Product Pricing
INSERT INTO ProductPricing (ProductID, StoreID, Price) VALUES
(9, 1, 12.99),
(10, 1, 11.99),
(11, 1, 8.99),
(12, 1, 49.99),
(13, 1, 20.99),
(9, 2, 12.99),
(10, 2, 11.99),
(11, 2, 8.99),
(12, 2, 49.99),
(13, 2, 20.99),
(9, 3, 13.49),
(10, 3, 12.49),
(11, 3, 9.49),
(12, 3, 51.99),
(13, 3, 21.99),
(9, 4, 13.99),
(10, 4, 12.99),
(11, 4, 9.99),
(12, 4, 52.99),
(13, 4, 22.99);

-- Additional Inventory
INSERT INTO Inventory (StoreID, ProductID, QuantityInStock) VALUES
(1, 9, 100),
(1, 10, 150),
(1, 11, 200),
(1, 12, 50),
(1, 13, 40),
(2, 9, 90),
(2, 10, 120),
(2, 11, 180),
(2, 12, 30),
(2, 13, 50),
(3, 9, 95),
(3, 10, 130),
(3, 11, 190),
(3, 12, 55),
(3, 13, 60),
(4, 9, 110),
(4, 10, 140),
(4, 11, 210),
(4, 12, 45),
(4, 13, 35);

-- Additional Customers
INSERT INTO Customers (FirstName, LastName, Email, Address, Username, Password) VALUES
('Jane', 'Doe', 'jane.doe@example.com', '789 West St, Metro City', 'jane', 'pass987'),
('John', 'Doe', 'john.doe@example.com', '101 East St, Suburb City', 'john', 'doe123');

-- Additional Transactions
INSERT INTO Transactions (TransactionDate, CustomerID, StoreID, TotalPrice) VALUES
('2024-05-05 15:30:00', 5, 1, 195.00),
('2024-05-06 16:00:00', 6, 2, 75.00);
('2023-04-05 15:30:00', 5, 3, 95.00),
('2023-07-06 16:00:00', 6, 4, 75.00);

-- Additional Transaction Items
INSERT INTO TransactionItems (TransactionID, ProductID, Quantity) VALUES
(9, 9, 1),  -- Crayola Marker Set
(11, 10, 2),  -- Fiskars Detail Scissors
(11, 11, 63),
(11, 3, 17),
(11, 4, 22),
(10, 7, 13),
(10, 2, 30),
(10, 8, 40),
(10, 10, 12);  

-- Update Reorder Thresholds
INSERT INTO ReorderThresholds (ProductID, Threshold) VALUES
(9, 30),  -- Crayola Marker Set
(10, 50),  -- Fiskars Detail Scissors
(11, 25);  -- Loops & Threads Merino Yarn

-- New Reorder Requests (Reflecting Continued Business Operations)
INSERT INTO ReorderRequests (ProductID, RequestedQuantity, RequestDate, Status) VALUES
(9, 100, '2024-05-20', 'Pending'),
(10, 50, '2024-05-21', 'Pending'),
(11, 60, '2024-05-22', 'Pending');




