    # README
    # Michaels Enterprise Database System

    ## Introduction
    The Michaels Enterprise Database System is a Python program that provides a user-friendly interface for managing a retail database. It allows customers, managers, vendors, and DBAs to perform various operations related to sales, inventory management, and data analysis.

    ## Features
    The program offers the following features:

    1. Customer Interface: Customers can log in, view products, add items to their cart, place orders, and view their order history.

    2. Manager Interface: Managers can log in, view sales data, check inventory levels, and reorder products.

    3. Vendor Interface: Vendors can log in, check reorders, confirm shipments, and view fulfilled orders.

    4. DBA Interface: DBAs can log in, run OLAP queries.

    ## Installation
    To run the Michaels Enterprise Database System, follow these steps:

    1. Make sure you have Python installed on your system.

    2. Install the required dependency for connecting mysql with python by running the following command:
        ```
        pip install mysql-connector-python
        ```

    3. Update the database connection details in the `DatabaseConnector` class constructor. Replace my values with your own database credentials (or not... I guess you wouldnt have to).

    4. Run the program by executing the following command:
        ```
        python DBSYS_final.py
        ```
        OR...
        ```
        python3 DBSYS_final.py
        ```
        Depending on what version of python you have

    ## Usage
    Upon running the program, you will be presented with a main menu where you can choose the type of login (customer, manager, vendor, DBA) or exit the program.

    The program authenticates users by checking the username and password in the actual database so you will have to use the following username/passwords:

        CUSTOMER:
            Username: russ
            Password: password123
        MANAGER:
            Username: manager
            Password: russell_man
        VENDOR:
            Username: vendor
            Password: russell_vend
        DBA:
            Username: dba
            Password: russell_dba

    Each interface provides a set of options that can be selected to perform specific tasks. Simply follow the prompts and enter the required information when prompted.

