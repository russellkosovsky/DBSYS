#!/usr/bin/env python
# coding: utf-8

# Import the database connector and initialise the connection

# In[37]:


import mysql.connector

cnx = mysql.connector.connect(user='root', password='abccom303123',
                              host='127.0.0.1',
                              database='com303')


# Create the cursor

# In[38]:


cursor = cnx.cursor()


# Set up a simple query and execute

# In[39]:


query = "select ID, name, dept_name, tot_cred from student order by name"

cursor.execute(query)


# Get the data from the database using a loop over the cursor

# In[40]:


print("ID", "Name", "Dept Name", "Tot Credits")
for (id, name, dept_name, tot_cred) in cursor:
  print(id, name, dept_name, tot_cred)


# Once you've created the cursor, you can use it for other SQL queries.  Of course, you can also create other cursors.
# 
# It is often the case that we might have a couple of cursors being used at the same time, with information from one feeding a query being handled by the other.

# Inserting into a table

# Before we do, let's see if the data is in the table already
# 
# Here, I'm only selecting on the id since that is the primary key for the table

# In[41]:


query = "select count(*) from student where id=3333"

cursor.execute(query)

# The fetch returns a list.
# Since we're only interested in the first (and only) value,
# I'm specifically looking at the first element in the list.
count = cursor.fetchone()
print("Count = ", count[0])

# and flush the cursor
# Putting the results of the fetchall into a variable so that it doesn't print
# (It's a Jupyter Notebook thing.)
rest_of_rows = cursor.fetchall()


# The count is 0, it does not exist in the database table
# 
# Let's insert into the table

# In[42]:


query = "insert into student(ID, name, dept_name, tot_cred) values (3333, 'John Adams', 'History', 1)"

cursor.execute(query)


# Let's check to see if the data is in the table.

# In[43]:


query = "select id, name, dept_name, tot_cred from student"

cursor.execute(query)

for (id, name, dept_name, tot_cred) in cursor:
    print(id, name, dept_name, tot_cred)


# Let's now delete that entry

# In[44]:


query = "delete from student where id=3333"

cursor.execute(query)


# And let's check again to see if it is gone

# In[45]:


query = "select count(*) from student where id=3333"

cursor.execute(query)

# The fetch returns a list.
# Since we're only interested in the first (and only) value,
# I'm specifically looking at the first element in the list.
count = cursor.fetchone()
print("Count = ", count[0])

# and flush the cursor
# Putting the results of the fetchall into a variable so that it doesn't print
# (It's a Jupyter Notebook thing.)
rest_of_rows = cursor.fetchall()


# And yes, it is gone.

# #### Using place holders

# Can use place holders in queries that will be filled in when executed: place holders interact with python variables.

# Important note: you must fetch all rows for a cursor before executing new statements using the same cursor

# In[46]:


query = "select ID, name, tot_cred from student where dept_name = %s order by name"

query_vals = ('Comp. Sci.',)

cursor.execute(query, query_vals)


# %s is the place holder
# 
# execute requires a list, tuple, or dictionary, it will not accept a single value.  Casting a single value as a list also does not work.
# 
# To get around this, we place the single value inside parentheses and put a comma after the value.

# In[47]:


print("ID", "Name", "Tot Credits")
for (id, name, tot_cred) in cursor:
  print(id, name, tot_cred)


# We can have multiple place holders in a query.
# 
# The values are used in sets as big as the number of place holders.  If there are 2 place holders, then the values are used in pairs.
# 
# But the values are still contained in a single list or tuple.

# In[48]:


query = "select ID, name, tot_cred from student where dept_name = %s and tot_cred > %s order by name"

query_vals = ('Comp. Sci.', 50)
cursor.execute(query, query_vals)


# In[49]:


print("ID", "Name", "Tot Credits")
for (id, name, tot_cred) in cursor:
  print(id, name, tot_cred)


# This is what it looks like if we get the rows using .fetchall()

# In[50]:


query = "select ID, name, tot_cred from student where dept_name = %s and tot_cred > %s order by name"

query_vals = ('Comp. Sci.', 50)
cursor.execute(query, query_vals)
cursor.fetchall()


# Or if we get just one row

# In[51]:


query = "select ID, name, tot_cred from student where dept_name = %s and tot_cred > %s order by name"

query_vals = ('Comp. Sci.', 50)
cursor.execute(query, query_vals)
cursor.fetchone()


# If we do anything other than get all of the rows, we have to flush the rest of the rows out of the cursor using .fetchall()

# In[52]:


rest_of_rows = cursor.fetchall()


# We can set the number of rows returned by using .fetchmany()

# In[53]:


query = "select ID, name, tot_cred from student where dept_name = %s and tot_cred > %s order by name"

query_vals = ('Comp. Sci.', 50)
cursor.execute(query, query_vals)
cursor.fetchmany(size=5)


# In[54]:


rest_of_rows = cursor.fetchall()


# And since we're good about working neatly and having tidy code, we clean up at the end of the code by closing both the cursor and the connection.

# In[55]:


cursor.close()
cnx.close()


# In[ ]:




