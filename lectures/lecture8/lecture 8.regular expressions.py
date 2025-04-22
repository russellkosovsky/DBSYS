#!/usr/bin/env python
# coding: utf-8

# ### String Matching

# #### Regular expressions (RegEx)

# How to use regular expressions
# 
# We will focus on:
# 
# Any letter a-z A-Z and number will match to itself. Many other characters will as well.
# 
# \w = match any "word" character: a-z A-Z numbers, but will not match a period (.)
# 
# \d = match any number digit
# 
# \s = match any whitespace (space, tab)
# 
# \S = match any non=whitespace (not a space or tab)
# 
# . = match any character or number or whitespace
# 
# 
# [ ] = create a set of characters or numbers or symbols to match.  Automatic "or"
# 
# Quantifiers
# 
# "+" = add to any of the above to match 1 or more times
# 
# "*" = add to any of the above to match 0 or more times.
# 
# {m} = m is a number, add to any of the above to match m times
# 
# {m,n} = m and n are a numbers, add to any of the above to match at least m times and at most n times
# 
# 
# 
# ^ = start match at the beginnning of the input string
# 
# $ = end match at the end of the input string
# 
# ? = make the match not greedy
# 
# . ^ $ * + ? { [ ] \ | ( )  are all "special" characters.  If you want to match to any of them, put a backslash, \, in front of it.  \ is an "escape" character and using it is called "escaping" a character.

# Will start looking at RegEx from the python point of view

# Start by importing the re package

# In[2]:


import re


# Let's start simple, a character matching to itself

# In[2]:


line = "J"
m = re.findall("J", line)
m


# If it is in the input line multiple times, it will be found multiple times.
# 
# Note that what will be returned is only what is in the regex pattern.

# In[4]:


line = "JJ J"
m = re.findall("J ", line)
m


# To find just the first one, we can use ^ to tell it to match starting at the beginning of the line

# In[9]:


line = "JJ J"
m = re.findall("^J", line)
m


# To find the 3rd one, there are 2 options.
# 1) We can tell it to match at the end of the line

# In[11]:


line = "JJ J"
m = re.findall("J$", line)
m


# 2) we could tell it to match to the 3rd J either by telling it to include the space preceeding it

# In[13]:


line = "JJ J"
m = re.findall("\sJ", line)
m


# But note that the space is included in what is returned.  Do we want that?
# 
# To tell it to match to the 2nd one, we can include the space in the match

# In[14]:


line = "JJ J"
m = re.findall("J\s", line)
m


# Note that the space is included in what is returned.  Do we want that?
# 
# Everything that is inside of the quotes will be returned in the match.  Unless, we specify what we want returned, this will come later.
# 
# What if we want matches of different lengths?
# 
# Here, we will compare Jon to Jonathan.  We will start by just matching Jon.

# In[ ]:


mylist  = ["Jon", "Jonathan"]
outlist = []
for this in mylist:
    m = re.findall("Jon", this)
    outlist += m
outlist


# Notice that when it matches to the Jon in Jonathan, it only returns the Jon part.  What is returned is only the portion that is in the regex pattern. 
# 
# What if they were in the same line?

# In[ ]:


mylist  = ["Jon Jonathan"]
outlist = []
for this in mylist:
    m = re.findall("Jon", this)
    outlist += m
outlist


# Just like in the earlier example with the J's, you will get back all of the matches to the regex pattern in the string.
# 
# If we want both Jon and Jonathan, we need to adjust the pattern. To do this, we'll bring \w into play and add the * to it to indicate that we want 0 or more word characters after Jon.

# In[ ]:


mylist  = ["Jon", "Jonathan"]
outlist = []
for this in mylist:
    m = re.findall("Jon\w*", this)
    outlist += m
outlist


# Now we're getting both Jon and Jonathan.
# 
# It is important to note that it is not restricted to just Jon and Jonathan, if we had another word that had Jon in it, that would be returned too.  We'll also add in a word with some non-word characters in it.

# In[ ]:


mylist  = ["Jon", "Jonathan", "Jona", "Jon123", "Jonny", "JonJo", "Jon%$"]
outlist = []
for this in mylist:
    m = re.findall("Jon\w*", this)
    outlist += m
outlist


# I could use a couple of other matching options.
# 
# First we'll try \S which matches to any non-whitespace.

# In[ ]:


mylist  = ["Jon", "Jonathan", "Jona", "Jon123", "Jonny", "JonJo", "Jon%$"]
outlist = []
for this in mylist:
    m = re.findall("Jon\S*", this)
    outlist += m
outlist


# Now we're also picking up the work with the non-word characters in it.
# 
# I could also use . which matches to any character

# In[16]:


mylist  = ["Jon", "Jonathan", "Jona", "Jon123", "Jonny", "JonJo", "Jon%$"]
outlist = []
for this in mylist:
    m = re.findall("Jon.*", this)
    outlist += m
outlist


# Let's extend this example by adding middle and last names. What happens?
# 
# Starting using the \w*

# In[ ]:


mylist  = ["Jon Adam Smith", "Jonathan Adam Smith"]
outlist = []
for this in mylist:
    m = re.findall("Jon\w*", this)
    outlist += m
outlist


# Notice that with the \w, the matching stops at the space
# 
# What about with \S

# In[ ]:


mylist  = ["Jon Adam Smith", "Jonathan Adam Smith"]
outlist = []
for this in mylist:
    m = re.findall("Jon\S*", this)
    outlist += m
outlist


# The same thing happens: the matching stops at the space.
# 
# What about with .

# In[ ]:


mylist  = ["Jon Adam Smith", "Jonathan Adam Smith"]
outlist = []
for this in mylist:
    m = re.findall("Jon.*", this)
    outlist += m
outlist


# Hmmmm.... it matched the entire name.  Why? Because . matches any character including the spaces.  By default, matching is "greedy": it wants to match as much as possible.  Matching starts with the left-most characters in the pattern and works its way to the right.
# 
# We can make it not be greedy by including a ? in the pattern.

# In[17]:


mylist  = ["Jon Adam Smith", "Jonathan Adam Smith"]
outlist = []
for this in mylist:
    m = re.findall("Jon.*?", this)
    outlist += m
outlist


# Notice that this isn't quite what we want either because now it stopped as soon as it could.
# 
# Bottom line: using . in matching can be very useful, but it can also be problematic.

# Next problem: allowing for variability at a position in a string.
# 
# Let's look at matching to Grey and Gray.  This is where the [ ] come in handy.  We can put any characters we want inside the [ ] and the matching will automatically try using them with an "or".
# 
# First, we'll do the matching with \w

# In[ ]:


mylist  = ["Grey", "Gray"]
outlist = []
for this in mylist:
    m = re.findall("Gr\wy", this)
    outlist += m
outlist


# And again with \S

# In[ ]:


mylist  = ["Grey", "Gray"]
outlist = []
for this in mylist:
    m = re.findall("Gr\Sy", this)
    outlist += m
outlist


# Now we'll use the [ ].  Note that I don't have an "or" in there.

# In[ ]:


mylist  = ["Grey", "Gray"]
outlist = []
for this in mylist:
    m = re.findall("Gr[ea]y", this)
    outlist += m
outlist


# The [ ] allows us to control which characters can be present at a specific position.  We can also use the + and * on it.
# 
# For example, let's look at Greey, Graay, and for fun Greay and Graey

# In[ ]:


mylist  = ["Grey", "Gray", "Greey", "Graay", "Greay", "Graey"]
outlist = []
for this in mylist:
    m = re.findall("Gr[ea]+y", this)
    outlist += m
outlist


# It allowed all combinations of the characters inside the [ ].
# 
# Important note: upper vs lower case matters.  For instance:

# In[ ]:


mylist  = ["Grey", "Gray"]
outlist = []
for this in mylist:
    m = re.findall("Gr[EA]y", this)
    outlist += m
outlist


# This found nothing since we put upper case letters in the [ ], and they won't match against the lower case letters.  If case will be issue, then we could do [eaEA]

# In[ ]:


mylist  = ["Grey", "Gray"]
outlist = []
for this in mylist:
    m = re.findall("Gr[eaEA]y", this)
    outlist += m
outlist


# Here's another example of mixed case.  The input line has mixed case, but we only have lower case in the [ ]

# In[ ]:


line = "AAAAAbbbbb"
m = re.findall("[a-z]+", line)
m


# Whilst now we include both upper and lower case in the [ ]

# In[ ]:


line = "AAAAAbbbbb"
m = re.findall("[A-Za-z]+", line)
m


# To drive home the point about matching multiple characters, here's an example of matching multiples of a specific character

# In[ ]:


line = "Hellolooloooloooo"
m = re.findall("o+", line)
m


# What if I'm only interested in matching 3 O's? You can inidicate the number of the character using {m} or {m,n}

# In[ ]:


line = "Hellolooloooloooo"
m = re.findall("o{3}", line)
m


# Or 3 or 4 O's?

# In[ ]:


line = "Hellolooloooloooo"
m = re.findall("o{3,4}", line)
m


# Let's go back and talk some more about greedy vs. non-greedy.
# 
# In this example, we're trying to get the html tags. The first one is the usual greedy match

# In[ ]:


line = "<b>foo</b> and <i>so on</i>"
m = re.findall("<.*>", line)
m


# The pattern found the < and then the .* took over in the matching trying to match as many characters as it could.  Because of this, it skipped the first > and continued on to the final >
# 
# Here's the non-greedy version where we use the ? after the .*

# In[ ]:


line = "<b>foo</b> and <i>so on</i>"
m = re.findall("<.*?>", line)
m


# Let's at getting the email address of the sender of an email by parsing the line
# From: vmartinez@winstead.com
# 
# Note that @ is a special character, so we'll need to escape it using a backslash \
# We will set up a pattern of
#    \w+\@\w+

# In[ ]:


line = "From: vmartinez@winstead.com"
m = re.findall("\w+\@\w+", line)
m


# Notice that the .com is missing.  That is because the period (".") is not considered to be a word character.
# There are a couple of ways to solve this.
# One is to explicitly put .com

# In[18]:


line = "From: vmartinez@winstead.com"
m = re.findall("\w+\@\w+\.com", line)
m


# Another is to use the \S for a non-whitespace character.  We'll start the email domain with a word character, then finish it with the \S

# In[ ]:


line = "From: vmartinez@winstead.com"
m = re.findall("\w+\@\w\S+", line)
m


# If the regex pattern is bigger than then part of the text that we're wanting, we can use parentheses to indicate the part(s) we want.  If there are more than one set of (), the parts they match will be in the output in the order they occur in the regex pattern.
# 
# Here, we include From: in the pattern, but we only want the email address

# In[ ]:


line = "From: vmartinez@winstead.com"
m = re.findall("From\:\s+(\w+\@\w\S+)", line)
m


#  If there are more than one set of parentheses, you will get a list of tuples.
#  Here, we'll grab the username and email address separately

# In[ ]:


line = "From: vmartinez@winstead.com"
m = re.findall("From\:\s+(\w+)\@(\w\S+)", line)
m


# In[ ]:


line = "From: V. Martinez <vmartinez@winstead.com>"
m = re.findall("From\:\s+(\S.*?)\s+<(\w+)\@(\w\S+)>", line)
m


# Using start and end of line
# 
# Using an example from bioinformatics / computational biology
# This is a type of data entry for a gene sequence called FASTA.  The '>' line is the comment line and contains information like an id for the sequence and then, hopefully, some information like a description.  The actual gene sequence follows the comment line.
# 
# >NM_001302688.2 Homo sapiens apolipoprotein E (APOE), transcript variant 1, mRNA
# CTACTCAGCCCCAGCGGAGGTGAAGGACGTCCTTCCCCAGGAGCCGGTGAGAAGCGCAGTCGGGGGCACG
# GGGATGAGCTCAGGGGCCTCTAGAAAGAGCTGGGACCCTGGGAACCCCTGGCCTCCAGACTGGCCAATCA
# CAGGCAGGAAGATGAAGGTTCTGTGGGCTGCGTTGCTGGTCACATTCCTGGCAGGATGCCAGGCCAAGGT
# GGAGCAAGCGGTGGAGACAGAGCCGGAGCCCGAGCTGCGCCAGCAGACCGAGTGGCAGAGCGGCCAGCGC
# ... and continues on....

# In[ ]:


line = ">NM_001302688.2 Homo sapiens apolipoprotein E (APOE), transcript variant 1, mRNA"
m = re.findall("^>(\S+)\s+(\S.*)$", line)
m


# Sometimes the name of the gene is in parentheses at the end of the description

# In[ ]:


line = ">NM_001302688.2 Homo sapiens apolipoprotein E, transcript variant 1, mRNA (APOE)"
m = re.findall("^>(\S+)\s+(\S.*)\s\((\w+)\)$", line)
m


# And sometimes the name comes before the organism

# In[ ]:


line = ">NM_001302688.2 Homo sapiens apolipoprotein E, transcript variant 1, mRNA (APOE) [Homo sapiens]"
m = re.findall("^>(\S+)\s+(\S.*)\s\((\w+)\)\s\[(\w.*?)\]$", line)
m


# If I want just the id and the version

# In[ ]:


line = ">NM_001302688.2 Homo sapiens apolipoprotein E, transcript variant 1, mRNA (APOE)"
m = re.findall("^>(\S+?)\.(\d+)\s+", line)
m


# A note about setting up a regex pattern: look for what's the same between the input lines and what is different.  I will quite often put a couple of the input lines in my code so that I can stare at them whilst coding.  For example:
# 
# gene_id ENSSSCG00005029396 transcript_id ENSSSCT00005050136  protein_id ENSSSCP00005030958
# gene_id ENSSSCG00005029396 transcript_id ENSSSCT00005050136  exon_id ENSSSCE00005185090
# gene_id ENSSSCG00005029396 transcript_id ENSSSCT00005050136  protein_id ENSSSCP00005030958
# gene_id ENSSSCG00005029396 transcript_id ENSSSCT00005050136  exon_id ENSSSCE00005185437
# gene_id ENSSSCG00005029396 transcript_id ENSSSCT00005050136  protein_id ENSSSCP00005030958
# gene_id ENSSSCG00005029396 transcript_id ENSSSCT00005050136  exon_id ENSSSCE00005185900
# 
# If I'm wanting to get the transcript_id, I can see that it starts off with E followed by some text which is followed by some numbers. But the gene_id, protein_id, and exon_id all start also all start with E followed by some text which is followed by some numbers.
# 
# Looking more carefully, I can see that the transcript_id has a T right before the numbers, whereas the gene_id has a G, the protein_id has a P, and the exon_id has an E.
# 
# This tells me that a regex pattern of E\w+T\d+ could work.  Let's try it

# In[ ]:


mylist  = ["gene_id ENSSSCG00005029396 transcript_id ENSSSCT00005050136  protein_id ENSSSCP00005030958",
           "gene_id ENSSSCG00005029396 transcript_id ENSSSCT00005050136  exon_id ENSSSCE00005185090",
           "gene_id ENSSSCG00005029396 transcript_id ENSSSCT00005050136  protein_id ENSSSCP00005030958",
           "gene_id ENSSSCG00005029396 transcript_id ENSSSCT00005050136  exon_id ENSSSCE00005185437",
           "gene_id ENSSSCG00005029396 transcript_id ENSSSCT00005050136  protein_id ENSSSCP00005030958",
           "gene_id ENSSSCG00005029396 transcript_id ENSSSCT00005050136  exon_id ENSSSCE00005185900"]
outlist = []
for this in mylist:
    m = re.findall("E\w+T\d+", this)
    outlist += m
outlist


# Perfect!

# In[ ]:




