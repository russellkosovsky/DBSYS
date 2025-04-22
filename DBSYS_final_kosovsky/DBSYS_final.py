###################################################################################################################
import mysql.connector
from mysql.connector import Error
###################################################################################################################

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='136.244.224.221',
            user='com303rkosovsky',
            password='rk3536rk',
            database='com303fprs'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# to execute SQL queries
def execute_query(connection, query, values=None):
    try:
        cursor = connection.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        return cursor
    except Error as e:
        print(f"Error: {e}")
        return None

###################################################################################################################

# What are the 20 top-selling products at each store? 
def query_1():
    connection = create_connection()
    if connection:
        query = """
        SELECT S.StoreName, P.ProductName, SUM(TI.Quantity) as TotalSold
        FROM TransactionItems TI
        JOIN Transactions T ON TI.TransactionID = T.TransactionID
        JOIN Products P ON TI.ProductID = P.ProductID
        JOIN Stores S ON T.StoreID = S.StoreID
        GROUP BY S.StoreName, P.ProductName
        ORDER BY S.StoreName, TotalSold DESC
        LIMIT 20;
        """
        cursor = execute_query(connection, query)
        if cursor:
            results = cursor.fetchall()
            for result in results:
                print(f"Store: {result[0]}, Product: {result[1]}, Total Sold: {result[2]}")
        connection.close()
    else:
        print("Connection failed.")

# What are the 20 top-selling products in each state?
def query_2():
    connection = create_connection()
    if connection:
        query = """
        SELECT S.StoreState AS State, P.ProductName, SUM(TI.Quantity) as TotalSold
        FROM TransactionItems TI
        JOIN Transactions T ON TI.TransactionID = T.TransactionID
        JOIN Products P ON TI.ProductID = P.ProductID
        JOIN Stores S ON T.StoreID = S.StoreID
        GROUP BY S.StoreState, P.ProductName
        ORDER BY S.StoreState, TotalSold DESC
        LIMIT 20;
        """
        cursor = execute_query(connection, query)
        if cursor:
            results = cursor.fetchall()
            for result in results:
                if not result[0] == None:
                    print(f"State: {result[0]}, Product: {result[1]}, Total Sold: {result[2]}")
        connection.close()
    else:
        print("Connection failed.")

# What are the 5 stores with the most sales so far this year? 
def query_3():
    connection = create_connection()
    if connection:
        query = """
        SELECT S.StoreName, SUM(TI.Quantity) as TotalSales
        FROM Transactions T
        JOIN TransactionItems TI ON T.TransactionID = TI.TransactionID
        JOIN Stores S ON T.StoreID = S.StoreID
        WHERE YEAR(T.TransactionDate) = YEAR(CURDATE())
        GROUP BY S.StoreName
        ORDER BY TotalSales DESC
        LIMIT 5;
        """
        cursor = execute_query(connection, query)
        if cursor:
            results = cursor.fetchall()
            for result in results:
                print(f"Store: {result[0]}, Total Sales: {result[1]}")
        connection.close()
    else:
        print("Connection failed.")

# In how many stores does Crayola outsell Fiskars?
def query_4():
    connection = create_connection()
    if connection:
        query = """
        SELECT S.StoreName, 
               SUM(CASE WHEN B.BrandName = 'Crayola' THEN TI.Quantity ELSE 0 END) AS CrayolaSales,
               SUM(CASE WHEN B.BrandName = 'Fiskars' THEN TI.Quantity ELSE 0 END) AS FiskarsSales
        FROM TransactionItems TI
        JOIN Transactions T ON TI.TransactionID = T.TransactionID
        JOIN Products P ON TI.ProductID = P.ProductID
        JOIN Brands B ON P.BrandID = B.BrandID
        JOIN Stores S ON T.StoreID = S.StoreID
        GROUP BY S.StoreName
        HAVING CrayolaSales > FiskarsSales
        """
        cursor = execute_query(connection, query)
        if cursor:
            results = cursor.fetchall()
            print(f"Number of stores where Crayola outsells Fiskars: {len(results)}")
            for result in results:
                print(f"Store: {result[0]}, Crayola Sales: {result[1]}, Fiskars Sales: {result[2]}")
        connection.close()
    else:
        print("Connection failed.")

# What are the top 3 types of product that customers buy in addition to Crayola Watercolor Set? 
def query_5():
    connection = create_connection()
    if connection:
        query = """
        SELECT PT.ProductTypeName, SUM(TI.Quantity) AS TotalQuantity
        FROM TransactionItems TI
        JOIN Transactions T ON TI.TransactionID = T.TransactionID
        JOIN Products P ON TI.ProductID = P.ProductID
        JOIN ProductTypes PT ON P.ProductTypeID = PT.ProductTypeID
        WHERE T.TransactionID IN (
            SELECT DISTINCT TI2.TransactionID
            FROM TransactionItems TI2
            JOIN Products P2 ON TI2.ProductID = P2.ProductID
            WHERE P2.ProductName = 'Crayola Watercolor Set'
        )
        AND P.ProductName != 'Crayola Watercolor Set'
        GROUP BY PT.ProductTypeID
        ORDER BY TotalQuantity DESC
        LIMIT 3;
        """
        cursor = execute_query(connection, query)
        if cursor:
            results = cursor.fetchall()
            if results:
                for result in results:
                    print("Product Type:", result[0], "-- Total Sold:", result[1])
            else:
                print("No additional products found purchased with Crayola Watercolor Set.")
        connection.close()
    else:
        print("Connection failed.")

def Test_Queries():
    print("Running query 1...")
    query_1()
    print("\nRunning query 2...")
    query_2()
    print("\nRunning query 3...")
    query_3()
    print("\nRunning query 4...")
    query_4()
    print("\nRunning query 5...")
    query_5()

###################################################################################################################

class DatabaseConnector:
    def __init__(self, host='136.244.224.221', database='com303fprs', user='com303rkosovsky', password='rk3536rk'):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            #print("MySQL connection is closed")

    def authenticate_user(self, username, entered_password):
        connection = self.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT password, role, VendorID FROM Users WHERE username = %s", (username,))
                result = cursor.fetchone()
                if result and result[0] == entered_password:
                    # Check if user is a vendor and has a VendorID
                    if result[2] is not None:
                        return result[1], result[2]  # role, VendorID
                    return result[1], None  # role, No VendorID for non-vendors
                return False, None
            finally:
                connection.close()

    def authenticate_cust(self, username, entered_password):
        connection = self.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT Password FROM Customers WHERE Username = %s", (username,))
                stored_password = cursor.fetchone()
                if stored_password is not None:
                    if stored_password[0] == entered_password:
                        cursor = connection.cursor()
                        cursor.execute("SELECT CustomerID FROM Customers WHERE Username = %s", (username,))
                        cust_id = cursor.fetchone()
                        return cust_id[0]
                    return False
                return False
            finally:
                connection.close()

###################################################################################################################

class DBAinterface(DatabaseConnector):

    def show_menu(self):
        while True:
            print("\n\n\n\n---------------------------------------------------")
            print("DBA Menu:")
            print("\t1. Run OLAP Query")
            print("\t2. Exit to Main Menu")
            choice = input("Select an option: ")
            if choice == '1':
                query = input("Enter the OLAP query: ")
                self.run_olap_query(query)
            elif choice == '2':
                break
            else:
                print("Invalid option, please try again.")

    def run_olap_query(self, query):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                print(row)
        finally:
            self.close_connection()

###################################################################################################################

class InventoryManager(DatabaseConnector):
    def check_inventory_levels(self):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT P.ProductID, P.ProductName, I.QuantityInStock, RT.Threshold
                FROM Products P
                JOIN Inventory I ON P.ProductID = I.ProductID
                JOIN ReorderThresholds RT ON P.ProductID = RT.ProductID
                WHERE I.QuantityInStock <= RT.Threshold
            """)
            results = cursor.fetchall()
            if results:
                for result in results:
                    print(f"Product: {result[1]}, Current Stock: {result[2]}, Threshold: {result[3]}")
                    if result[2] <= result[3]:
                        self.reorder_products(result[0], result[3] - result[2] + 50)  # Adding buffer to reorder quantity
            else:
                print("All inventory levels are within the threshold.")
        finally:
            self.close_connection()

    def reorder_products(self, product_id, quantity):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO ReorderRequests (ProductID, RequestedQuantity, RequestDate, Status) 
                VALUES (%s, %s, NOW(), 'Pending')
            """, (product_id, quantity))
            connection.commit()
            print(f"Reorder placed for Product ID: {product_id} for Quantity: {quantity}")
        finally:
            self.close_connection()

###################################################################################################################

class ManagerInterface(DatabaseConnector):
    def __init__(self):
        super().__init__()
        self.inventory_manager = InventoryManager()

    def show_menu(self):
        while True:
            print("\n\n\n\n---------------------------------------------------")
            print("Manager Menu:")
            print("\t1. View Sales Data")
            print("\t2. Check Inventory Levels")
            print("\t3. Exit to Main Menu")
            choice = input("Select an option: ")

            if choice == '1':
                self.view_sales_data()
            elif choice == '2':
                self.check_inventory_levels()
            elif choice == '3':
                main_menu()
                break
            else:
                print("Invalid option, please try again.")

    def view_sales_data(self):
        while True:
            print("---------------------------------------------------")
            print("\nSales Data:")
            print("\t1. View the 20 top-selling products at each store")
            print("\t2. View the 20 top-selling products in each state")
            print("\t3. View the 5 stores with the most sales so far this year")
            print("\t4. View how many stores Crayola outsell Fiskars")
            print("\t5. View the top 3 types of products that customers buy in addition to the Crayola Watercolor Set")
            print("\t6. Exit")
            print("---------------------------------------------------")
            choice = input("Select an option: ")
            if choice == '1':
                query_1()
            elif choice == '2':
                query_2()
            elif choice == '3':
                query_3()
            elif choice == '4':
                query_4()
            elif choice == '5':
                query_5()
            elif choice == '6':
                break
            else:
                print("Invalid option, please try again.")
        self.show_menu()

    def check_inventory_levels(self):
        self.inventory_manager.check_inventory_levels()
        self.show_menu()

###################################################################################################################

class VendorInterface(DatabaseConnector):
    
    def __init__(self, vendor_id):
        super().__init__()
        self.vendor_id = vendor_id

    def get_vendor_id(self):
        return self.vendor_id

    def show_menu(self):
        while True:
            print("\n\n\n\n---------------------------------------------------")
            print("Vendor Menu:")
            print("\t1. Check for reorders")
            print("\t2. Confirm a shipment")
            print("\t3. View fulfilled orders")
            print("\t4. Exit to Main Menu")
            print("---------------------------------------------------")
            choice = input("Select an option: ")
            if choice == '1':
                self.check_reorders()
            elif choice == '2':
                self.confirm_shipment()
            elif choice == '3':
                self.view_fulfilled_orders()
            elif choice == '4':
                main_menu()
                break
            else:
                print("Invalid option, please try again.")

    def check_reorders(self):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT RR.ReorderID, RR.ProductID, P.ProductName, RR.RequestedQuantity, RR.RequestDate, RR.Status, I.StoreID
                FROM ReorderRequests RR
                JOIN Products P ON RR.ProductID = P.ProductID
                JOIN Inventory I ON P.ProductID = I.ProductID
                WHERE RR.Status = 'Pending'
                GROUP BY I.StoreID, RR.ReorderID
            """)
            results = cursor.fetchall()
            if results:
                print("\n\n\n\n---------------------------------------------------")
                print("Pending Reorder Requests:")
                print("---------------------------------------------------")
                for (ReorderID, ProductID, ProductName, RequestedQuantity, RequestDate, Status, StoreID) in results:
                    print(f"\nReorder ID: {ReorderID}, \n\tProduct ID: {ProductID}, \n\tProduct Name: {ProductName}, \n\tQuantity: {RequestedQuantity}, \n\tRequest Date: {RequestDate}, \n\tStatus: {Status}, \n\tStore ID: {StoreID}")
            else:
                print("No pending reorders.")
        finally:
            self.close_connection()
        self.show_menu()

    def confirm_shipment(self):
        order_id = input("Enter Reorder ID to confirm: ")
        delivery_date = input("Enter delivery date (YYYY-MM-DD): ")
        store_id = input("Please specify the store for this shipment:\nEnter Store ID (e.g., 1 for Downtown, 2 for Uptown, 4 for Online): ")
        quantity = input("Please Confirm the quantity: ")
        try:
            connection = self.connect()
            cursor = connection.cursor()
            # Updating the status in the ReorderRequests table to 'Fulfilled'
            update_request_query = """
                UPDATE ReorderRequests
                SET Status = 'Fulfilled'
                WHERE ReorderID = %s
            """
            cursor.execute(update_request_query, (order_id,))

            # Inserting the fulfillment details into ReorderFulfillments table
            insert_fulfillment_query = """
                INSERT INTO ReorderFulfillments (ReorderID, VendorID, DeliveryDate, QuantityReceived)
                VALUES (%s, %s, %s, %s)
            """
            
            vendor_id = self.get_vendor_id()  
            cursor.execute(insert_fulfillment_query, (order_id, vendor_id, delivery_date, quantity))

            # Update inventory at the specified store
            update_inventory_query = """
                UPDATE Inventory
                SET QuantityInStock = QuantityInStock + %s
                WHERE ProductID = (SELECT ProductID FROM ReorderRequests WHERE ReorderID = %s) AND StoreID = %s
            """
            cursor.execute(update_inventory_query, (quantity, order_id, store_id))

            connection.commit()
            print(f"Shipment confirmed for Order ID: {order_id} with delivery on {delivery_date} to Store ID: {store_id}")
        except Error as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            if connection.is_connected():
                self.close_connection()
        self.show_menu()

    def view_fulfilled_orders(self):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT RR.ReorderID, P.ProductName, RF.DeliveryDate
                FROM ReorderRequests RR
                JOIN ReorderFulfillments RF ON RR.ReorderID = RF.ReorderID
                JOIN Products P ON RR.ProductID = P.ProductID
                WHERE RR.Status = 'Fulfilled'
                ORDER BY RF.DeliveryDate DESC
            """)
            results = cursor.fetchall()
            if results:
                print("\n\n\n\n---------------------------------------------------")
                print("Fulfilled Reorders:")
                print("---------------------------------------------------")
                for result in results:
                    print(f"\nReorder ID: {result[0]}, \n\tProduct: {result[1]}, \n\tDelivered On: {result[2]}")
            else:
                print("No fulfilled reorders found.")
        finally:
            self.close_connection()
        self.show_menu()

###################################################################################################################

class CustomerInterface(DatabaseConnector):
    
    def show_menu(self, cust_id):
        while True:
            print("\n\n\n\n---------------------------------------------------")
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(f"""
                SELECT FirstName
                FROM Customers
                WHERE Customers.CustomerID = {cust_id}
            """)
            results = cursor.fetchall()
            print(f"\t\t   Welcome, {results[0][0]}!")
            print("Customer Menu:")
            print("\t1. View Products")
            print("\t2. View Cart")
            print("\t3. Place Order")
            print("\t4. View Orders")
            print("\t5. Exit to Main Menu")
            print("---------------------------------------------------")
            choice = input("Select an option: ")
            
            if choice == '1':
                self.view_products(cust_id)
            elif choice == '2':
                self.view_cart(cust_id)
            elif choice == '3':
                self.place_order(cust_id)
            elif choice == '4':
                self.view_orders(cust_id)
            elif choice == '5':
                main_menu()
                break
            else:
                print("Invalid option, please try again.")
    
    def view_products(self, customer_id):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT P.ProductID, P.ProductName, PP.Price, I.QuantityInStock
                FROM Products P
                JOIN ProductPricing PP ON P.ProductID = PP.ProductID
                JOIN Stores S ON PP.StoreID = S.StoreID
                JOIN Inventory I ON P.ProductID = I.ProductID AND I.StoreID = S.StoreID
                WHERE S.IsWebOnly = TRUE
            """)
            results = cursor.fetchall()
            if results:
                print("Available Products:")
                for product in results:
                    print(f"ID: {product[0]}, \n\tName: {product[1]}, \n\tPrice: ${product[2]:.2f}, \n\tIn Stock: {product[3]}")
                print("\nEnter the ID of the product you want to add to your cart or type 'back' to return:")
                user_input = input()
                if user_input.lower() == 'back':
                    return
                self.add_to_cart(customer_id, user_input)
            else:
                print("No products available in the online store.")
        finally:
            self.close_connection()
        self.show_menu(customer_id)

    def add_to_cart(self, customer_id, product_id):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT P.ProductID, P.ProductName, PP.Price, I.QuantityInStock
                FROM Products P
                JOIN ProductPricing PP ON P.ProductID = PP.ProductID
                JOIN Stores S ON PP.StoreID = S.StoreID
                JOIN Inventory I ON P.ProductID = I.ProductID AND I.StoreID = S.StoreID
                WHERE S.IsWebOnly = TRUE AND P.ProductID = %s
            """, (product_id,))
            product = cursor.fetchone()
            if product:
                print(f"Selected Product: {product[1]}, Price: {product[2]}, In Stock: {product[3]}")
                quantity = int(input("Enter the quantity: "))
                if quantity <= product[3]:
                    cursor.execute("""
                        INSERT INTO ShoppingCart (CustomerID, ProductID, Quantity)
                        VALUES (%s, %s, %s)
                    """, (customer_id, product_id, quantity))
                    connection.commit()
                    print("Product added to your cart successfully!")
                else:
                    print("Insufficient stock available.")
            else:
                print("Product not available.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                self.close_connection()

    def view_cart(self, customer_id):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT SC.CartID, P.ProductName, SC.Quantity, PP.Price, (SC.Quantity * PP.Price) AS TotalPrice
                FROM ShoppingCart SC
                JOIN Products P ON SC.ProductID = P.ProductID
                JOIN ProductPricing PP ON P.ProductID = PP.ProductID
                WHERE SC.CustomerID = %s AND PP.StoreID = 4  # 4 is the ID for the online store
            """, (customer_id,))
            cart_items = cursor.fetchall()
            if cart_items:
                print("\nYour Shopping Cart:")
                for item in cart_items:
                    print(f"ID: {item[0]}, Product: {item[1]}, Quantity: {item[2]}, Price per Unit: ${item[3]:.2f}, Total Price: ${item[4]:.2f}")
                cart_id_to_remove = input("Enter ID to remove product(s) or 'back' to return: ")
                if cart_id_to_remove.lower() == 'back':
                    return
                self.remove_from_cart(customer_id, cart_id_to_remove)
            else:
                print("Your cart is currently empty.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                self.close_connection()

    def remove_from_cart(self, customer_id, cart_id):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("""
                DELETE FROM ShoppingCart WHERE CustomerID = %s AND CartID = %s
            """, (customer_id, cart_id))
            connection.commit()
            print("Item removed successfully from your cart.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                self.close_connection()

    def view_orders(self, customer_id):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT T.TransactionID, T.TransactionDate, P.ProductName, TI.Quantity, (TI.Quantity * PP.Price) AS TotalPrice
                FROM Transactions T
                JOIN TransactionItems TI ON T.TransactionID = TI.TransactionID
                JOIN Products P ON TI.ProductID = P.ProductID
                JOIN ProductPricing PP ON P.ProductID = PP.ProductID
                WHERE T.CustomerID = %s AND PP.StoreID = 4  # 4 for the online store
                ORDER BY T.TransactionDate DESC
            """, (customer_id,))
            orders = cursor.fetchall()
            if orders:
                print("\nYour Orders:")
                last_transaction = None
                for order in orders:
                    if last_transaction != order[0]:
                        if last_transaction is not None:
                            print()  # Extra newline for separation
                        print(f"Order ID: {order[0]}, Date: {order[1]}")
                        last_transaction = order[0]
                    print(f"\tProduct: {order[2]}, Quantity: {order[3]}, Total Price: ${order[4]:.2f}")
                print()
            else:
                print("You have no past orders.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                self.close_connection()
        self.show_menu(customer_id)

    def place_order(self, customer_id):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            # Retrieve cart items for the customer
            cursor.execute("""
                SELECT P.ProductID, P.ProductName, SC.Quantity, I.QuantityInStock, PP.Price
                FROM ShoppingCart SC
                JOIN Products P ON SC.ProductID = P.ProductID
                JOIN Inventory I ON P.ProductID = I.ProductID AND I.StoreID = 4 
                JOIN ProductPricing PP ON P.ProductID = PP.ProductID AND PP.StoreID = 4
                WHERE SC.CustomerID = %s
            """, (customer_id,))
            items = cursor.fetchall()
            if not items:
                print("Your cart is empty.")
                return

            # Confirm all items are in stock
            out_of_stock = []
            total_price = 0
            for item in items:
                if item[2] > item[3]:  # item[2] is cart quantity, item[3] is stock quantity
                    out_of_stock.append(item[1])
                else:
                    total_price += item[2] * item[4]  # item[2] is quantity, item[4] is price per unit
                
            if out_of_stock:
                print("The following items are out of stock and cannot be ordered: ", ", ".join(out_of_stock))
                return

            # Confirmation before proceeding to purchase
            print("Proceeding with the following items:")
            for item in items:
                print(f"{item[1]}: {item[2]} units at ${item[4]:.2f} each")
            print(f"Total price: ${total_price:.2f}")
            
            if input("Type 'yes' to confirm your order: ").lower() != 'yes':
                return

            # All checks passed, call process_purchase
            self.process_purchase(customer_id, items, total_price)
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                self.close_connection()
        self.show_menu(customer_id)

    def process_purchase(self, customer_id, items, total_price):
        try:
            connection = self.connect()
            connection.start_transaction()
            cursor = connection.cursor()
            
            # Create a new transaction record
            cursor.execute("""
                INSERT INTO Transactions (TransactionDate, CustomerID, StoreID, TotalPrice)
                VALUES (NOW(), %s, 4, %s)  # 4 for online store, including total price
            """, (customer_id, total_price))
            transaction_id = cursor.lastrowid

            # Add items to transaction items and update inventory
            for item in items:
                # Insert transaction item
                cursor.execute("""
                    INSERT INTO TransactionItems (TransactionID, ProductID, Quantity)
                    VALUES (%s, %s, %s)
                """, (transaction_id, item[0], item[2]))
                
                # Update inventory
                cursor.execute("""
                    UPDATE Inventory
                    SET QuantityInStock = QuantityInStock - %s
                    WHERE ProductID = %s AND StoreID = 4
                """, (item[2], item[0]))
            
            # Clear the shopping cart
            cursor.execute("""
                DELETE FROM ShoppingCart WHERE CustomerID = %s
            """, (customer_id,))

            # Commit transaction
            connection.commit()
            print("Your order has been placed successfully. Total charged: ${:.2f}".format(total_price))
        except Error as e:
            print(f"Error during purchase: {e}")
            connection.rollback()
        finally:
            if connection.is_connected():
                self.close_connection()

###################################################################################################################

def logo():
    m = [["@@@@@@@@@@@@@%%%%@@@@@@@@@@@@@@@@@@@@@@@%%%%%%@@@"],
        ["@@@@@@@@@@@@%%%%%%%%%@@@@@@@@@@@@@@@@@%%%%%%%%%%%@"],
        ["@@@@@@@@@@%%%%%%%%%%%%%@@@@@@@@@@@@@%%%%%%@@%%%%%%"],
        ["@@@@@@@@@%%%%%@@@@%%%%%@@@@@@@@@@@%%%%%@@@@@@%%%%%"],
        ["@@@@@@@@@%%%%@@@@@@%%%%%@@@@@@@@@%%%%%@@@@@@@@%%%%"],
        ["@@@@@@@@%%%%@@@@@@@@%%%%@@@@@@@@%%%%@@@@@@@@@%%%%%"],
        ["@@@@@@@@%%%%@@@@@@@@%%%%%@@@@@@%%%%@@@@@@@@@@%%%%@"],
        ["@@@@@@@%%%%%@@@@@@@@%%%%%@@@@@%%%%@@@@@@@@@@%%%%%@"],
        ["%%@@@@@%%%%@@@@@@@@@%%%%%@@@@%%%%@@@@@@@@@@%%%%%@@"],
        ["@%%%@@@%%%%@@@@@@@@@%%%%%@@@%%%%%@@@@@@@@@@%%%%%@@"],
        ["@@%%%%@%%%%@@@@@@@@@@%%%%@@@%%%%@@@@@@@@@@%%%%%@@@"],
        ["@@@%%%@%%%%@@@@@@@@@@%%%%@@%%%%@@@@@@@@@@@%%%%%@@@"],
        ["@@@@%%%%%%%@@@@@@@@@@%%%%@@%%%%@@@@@@@@@@@%%%%%@@@"],
        ["@@@@@%%%%%%@@@@@@@@@@%%%%@%%%%@@@@@@@@@@@@%%%%@@@@"],
        ["@@@@@%%%%%%@@@@@@@@@@%%%%@%%%%@@@@@@@@@@@@%%%%@@@@"],
        ["@@@@@@%%%%%@@@@@@@@@@%%%%%%%%@@@@@@@@@@@@@%%%%@@@@"],
        ["@@@@@@%%%%%@@@@@@@@@@@%%%%%%%@@@@@@@@@@@@@%%%%@@@@"],
        ["@@@@@@%%%%%@@@@@@@@@@@%%%%%@@@@@@@@@@@@@@@%%%%@@@@"],
        ["@@@@@@%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%@@@"],
        ["@@@@@@%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%@@@"]]
    for line in m:
        for ch in line[0]:
            if ch == "@":
                print(" ", end="")
            elif ch == "%":
                print("%", end="")
        print()

def main_menu():
    
    db_connection = DatabaseConnector()
    
    while True:

        print("\n\n\n")
        print("---------------------------------------------------")
        print("         Shoutout Faiz for the logo idea           ")
        print("---------------------------------------------------")
        logo()
        print("---------------------------------------------------")
        print("Welcome to the Michaels Enterprise Database System!")
        print("\t1. Customer Login")
        print("\t2. Manager Login")
        print("\t3. Vendor Login")
        print("\t4. DBA Login")
        print("\t5. Exit")
        print("---------------------------------------------------")
        
        vendor_id = None
        choice = input("Select an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            cust_id = db_connection.authenticate_cust(username, password)
            if cust_id is not False:
                print("Customer logged in successfully.")
                customer = CustomerInterface()
                customer.show_menu(cust_id)
            else:
                print("\n\n\n\n\n\n\n!!! Login failed !!!    Please check your credentials.")

        elif choice in ['2', '3', '4']:
            username = input("Enter username: ")
            password = input("Enter password: ")
            role, vendor_id = db_connection.authenticate_user(username, password)

            if choice == '2' and role == 'manager':
                print("Manager logged in successfully.")
                manager = ManagerInterface() 
                manager.show_menu()
            elif choice == '3' and role == 'vendor':
                print("Vendor logged in successfully.")
                vendor_interface = VendorInterface(vendor_id)
                vendor_interface.show_menu()
            elif choice == '4' and role == 'dba':
                print("DBA logged in successfully.")
                dba = DBAinterface()
                dba.show_menu()
            else:
                print("Login failed. Please check your credentials and role.")
        
        elif choice == '5':
            print("Exiting system.")
            exit()
        
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main_menu()