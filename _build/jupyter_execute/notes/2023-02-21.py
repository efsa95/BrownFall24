#!/usr/bin/env python
# coding: utf-8

# # Merging  and Databases
# 
# 
# ## Announcements
# 
# Assignment 3 is graded, but only today, so A4 is extended until tomorrow so that you can incorporate your A3 feedback into A4 (in particular, extending you EDA if you did not earn level 2 for summarize and visualize in A3). 
# 
# 
# Your achievement trackers are updated.
# 
# Take a few minutes to think about the following questions and make a few notes
# for yourself whereever you need them to be (a planner, calendar, etc).
# 1. What achievements have you earned?
# 1. Does your tracking repo  seem accurate to what you've done? If not, make an issue to ask about it. 
# 2. Are you on track to earn the grade you want in this class?
# 1. If not, what will you need to do (respond more in class, submit more
#    assignments, use your portfolio to catch up) to get back on track?
# 1. If you are on track and you want to earn above a B, take a minute to think
# about your portfolio. (tip: post an idea as an issue to get early feedback and help shaping your idea)
# 
# 
# ## Merging Data 
# 
# Focus this week is on how to programmatically combine sources of data
# 
# We will start by looking at combining multiple tabular data formats and see how to get data from other sources.

# In[1]:


import pandas as pd
import sqlite3
from urllib import request


# we're going to work with a set of datasets today that are stored in a repo.

# In[2]:


course_data_url = 'https://raw.githubusercontent.com/rhodyprog4ds/rhodyds/main/data/'


#  We can load in two data sets of player information.

# In[3]:


df_18 = pd.read_csv(course_data_url+'2018-players.csv')
df_19 = pd.read_csv(course_data_url+'2019-players.csv')


# and take a peek at each

# In[4]:


df_18.head()


# In[5]:


df_19.head()


# ```{important}
# Remember `columns` is an attribute, so it does not need `()`
# ```

# In[6]:


df_19.columns


# Let's make note of the shape of each

# In[7]:


df_18.shape, df_19.shape


# ### What if we want to analyze them together?
# 
# We can stack them, but this does not make it easy to see , for example, who changed teams.

# In[8]:


pd.concat([df_18,df_19])


# In[9]:


pd.concat([df_18,df_19]).shape


# Note that this has the maximum number of columns (because both had some overlapping
#   columns) and the total number of rows.
# 
# 
# 
# ### How can we find which players changed teams?
# 
# To do this we want to have one player column and a column with each year's team.
# 
# We can use a merge to do that.

# In[10]:


pd.merge(df_18,df_19,).head(2)


# if we merge them without any parameters, it tries to merge on all shared columns.  We want to merge them using the `PLAYER_ID` column though, we would say that we are "merging on player ID" and we use the `on` parameter to do it.  In this case, it looks for the values in the `PLAYER_ID` column that appear in both DataFrames and combines them into a single row.

# In[11]:


pd.merge(df_18,df_19,on='PLAYER_ID')


# Since there are other columns that appear in both DataFrames, they get a suffix, which by default is `x` or `y`, we can specify them though.

# In[12]:


df_1819_inner = pd.merge(df_18,df_19,on='PLAYER_ID',suffixes=('_2018','_2019'))
df_1819_inner.shape


# By default, this uses an *inner* merge, so we get the players that are in both datasets only. If we want to see differences, we need another type of merge. 
# 
# Some players still appear twice, because they were in one of the datsets twice, this
# happens when a player plays for two team in one season.
# 
# ### Which players played in 2018, but not 2019?
# 
# We have different types of merges, inner is both, out is either.  Left and right keep all the rows of one dataFrame.  We can use left with `df_18` as the left DataFrame to see which players played only in 18.

# In[13]:


df_1819_outer = pd.merge(df_18,df_19,how='outer',on='PLAYER_ID',suffixes=('_2018','_2019'),)
df_1819_outer


# Also, note that this has different types than before.  There are some players who only played one season, so they have a NaN value in some colums. pandas always casts a whole column.

# In[14]:


df_1819_inner.dtypes


# In[15]:


df_1819_outer.dtypes


# [nan](https://en.wikipedia.org/wiki/NaN) is a float

# In[16]:


import numpy as np
type(np.nan)


# Back the the question, we can also use a left merge. To pick out those rows:

# In[17]:


df_1819left = pd.merge(df_18,df_19,how='left',on='PLAYER_ID',suffixes=('_2018','_2019'),)
df_18only = df_1819left[df_1819left['SEASON_2019'].isna()]
df_18only


# In[18]:


len(df_18only['PLAYER_ID'].unique())


# In[19]:


df_18only['PLAYER_ID'].value_counts()


# ## Getting Data from Databases
# 
# 
# ### What is a Database?
# 
# 
# A common attitude in Data Science is:
# 
# > If your data fits in memory there is no advantage to putting it in a database: it will only be slower and more frustrating.     —[ Hadley Wickham](https://dbplyr.tidyverse.org/articles/dbplyr.html)
# 
# 
# Businesses and research organizations nearly always have too much data to feasibly work without a database.
# Instead, they use different tools which are designed to scale to very large amounts of data. These tools are largely databases like Snowflake or Google's BigQuery and distributed computing frameworks like Apache Spark.
# 
# 
# ```{warning}
# We are going to focus on the case of getting data out of a Database so that you
# can use it and making sure you know what a Database is.  
# 
# 
# You could spend a whole semester on databases:
# - CSC436 covers how to implement them in detail (recommended, but requires CSC212)
# - BAI456 only how to use them (counts for DS majors, but if you want to
#       understand them deeper, the CSC one is recommended)
# 
# ```
# 
# For the purpose of this class the key attributes of a database are:
# - it is a collection of tables
# - the data is accessed live from disk (not RAM)
# - you send a query to the database to get the data (or your answer)
# 
# 
# Databases can be designed in many different ways.  For examples two popular ones.
# 
# - [SQLite](https://www.sqlite.org/index.html) is optimized for transactional workloads, which means a high volume of requests that involving inserting or reading a couple things. This is good for eg a webserver.
# - [DuckDB](https://duckdb.org/) is optimized for analytical workloads, which means a small number of requests that each require reading many records in the database. This is better for eg: data science
# 
# **Experimenting with [DuckDB](https://duckdb.org/docs/guides/python/install) is a way to earn construct level 3**
# 
# 
# ### Accessing a Database from Python
# 
# We will use pandas again, as well as the `request` module from the `urllib`
# package and `sqlite3`.
# 
# Off the shelf, pandas cannot read databased by default. We'll use the
# [`sqlite3`](https://docs.python.org/3/library/sqlite3.html) library, but there
# are others, depending on the type of database.
# 
# First we need to download the database to work with it.

# In[20]:


request.urlretrieve('https://github.com/rhodyprog4ds/rhodyds/raw/main/data/nba1819.db',
      'nba1819.db')


# Next, we set up a connection, that links the the notebook to the database.
#  To use it, we add a cursor.

# In[21]:


conn = sqlite3.connect('nba1819.db')
cursor = conn.cursor()


# We can use execute to pass SQL queries through the cursor to the database.

# In[22]:


cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")


# Then we use `fetchall` to get the the results of the query.

# In[23]:


cursor.fetchall()


# If we fetch again, there is nothing to fetch.  Fetch pulls what was queued by
# execute.

# In[24]:


cursor.fetchall()


# We can run another query with execute then fetch that result.  This query gives
# us the column names.  
# 
# The schema of a database is the description of its setup and layout. The `*` means to get all.

# In[25]:


cursor.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS ")


# Then we use `fetchall` to get the the results of the query.

# In[26]:


cursor.fetchall()


# ## Querying with pandas
# 
# We can use `pd.read_sql` to send queries, get the result sand transform them
# into a DataFrame all at once
# 
# We can pass the exact same queries if we want.

# In[27]:


pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';",conn)


# In[28]:


pd.read_sql('SELECT * FROM teams',conn).head(1)


# ### Which player was traded the most during the 2018 season? How many times?  
# 
# 
# There is one row in players per team a played for per season, so if a
# player was traded (changed teams), they are in there multiple times.
# 
# First, we'll check the column names

# In[29]:


pd.read_sql("SELECT * FROM playerTeams2018 LIMIT 1",conn)


# then get the 2018 players, we only need the `PLAYER_ID` column for this question

# In[30]:


p18 =pd.read_sql("SELECT PLAYER_ID FROM playerTeams2018 ",conn)


# Then we can use value counts

# In[31]:


p18.value_counts().sort_values(ascending=False).head(10)


# and we can get the player's name from the player name **remember our first query told us all the tables**

# In[32]:


pd.read_sql("SELECT PLAYER_NAME FROM playerNames WHERE PLAYER_ID = 1629150",conn)


# ### Did more players who changed teams from the 2018 season to the 2019 season stay in the same conferences or switch conferences?
# 
# In the NBA, there are 30 teams organized into two conferences: East and West;
# the `conferences` table has the columns `TEAM_ID` and `CONFERENCE`
# 
# Let's build a Dataframe that could answer the question. 
# 
# I first pulled 1 row from each table I needed to see the columns.

# In[33]:


pd.read_sql('SELECT * FROM conferences LIMIT 1',conn)


# In[34]:


pd.read_sql('SELECT * FROM playerTeams2018 LIMIT 1',conn)


# In[35]:


pd.read_sql('SELECT * FROM playerTeams2019 LIMIT 1',conn)


# Then I pulled the columns I needed from each of the 3 tables into a separate DataFrame.
# `````{margin}
# ```{note}
# You can do the merging in SQL and pull only the merged table technically, but I use pandas more than sql so I did the minimum in SQL and the rest in pandas.  
# ```
# `````

# In[36]:


conf_df = pd.read_sql('SELECT TEAM_ID,CONFERENCE FROM conferences',conn)
df18 = pd.read_sql('SELECT TEAM_ID,PLAYER_ID FROM playerTeams2018',conn)
df19 = pd.read_sql('SELECT TEAM_ID,PLAYER_ID FROM playerTeams2019',conn)
df18_c = pd.merge(df18,conf_df,on='TEAM_ID')
df19_c = pd.merge(df19,conf_df,on='TEAM_ID')
df1819_conf = pd.merge(df18_c,df19_c, on='PLAYER_ID',suffixes=('_2018','_2019'))
df1819_conf


# Then I merged the conference with each set of player informationon the teams. Then I merged the two expanded single year DataFrames together. 
# 
# Now, to answer the question, we have a bit more work to do.  I'm going to use a `lambda` and `apply` to make a column that says same or new for the relative conference of the two seasons.

# In[37]:


labels = {False:'new',True:'same'}
change_conf = lambda row: labels[row['CONFERENCE_2018']==row['CONFERENCE_2019']]
df1819_conf['conference_1819']= df1819_conf.apply(change_conf,axis=1)
df1819_conf.head()


# Then I can use this DataFrame grouped by my new column to get the unique players in each situation new or same conference.

# In[38]:


df1819_conf.groupby('conference_1819')['PLAYER_ID'].apply(pd.unique)


# And finally, get the length of each of those lists.

# In[39]:


df1819_conf.groupby('conference_1819')['PLAYER_ID'].apply(pd.unique).apply(len)


# This, however, includes players who stayed on the same team, so we also need to split for who changed teams. First we add the team comparison column, then groupby by both and count unique players.

# In[40]:


new_team = lambda row: labels[row['TEAM_ID_2018']==row['TEAM_ID_2019']]
df1819_conf['team_1819']= df1819_conf.apply(new_team,axis=1)
df1819_conf.groupby(['conference_1819','team_1819'])['PLAYER_ID'].apply(pd.unique).apply(len)


# This is good, we could read the answer from here.  It's good practice, though, to be able to pull that value out programmatically.

# In[41]:


player_counts_1819_team =  df1819_conf.groupby(['conference_1819','team_1819'])['PLAYER_ID'].apply(pd.unique).apply(len)
player_counts_1819_team.idxmax()


# This tells us that the largest number of players stayed on the same team (and therefore same conference).  We're not interested inthis thoug, we're itnerested in those that changed teams, so we can drop the `(same,same)` value and then do this again.

# In[42]:


player_counts_1819_team.drop(('same','same')).idxmax()


# This tells us that more players changed teams within the same conference than changed teams and conferences. We can compare the two directly:

# In[43]:


player_counts_1819_team['new','new'], player_counts_1819_team['same','new']


# Again 135 is more than 119.  
# 
# We can also make this a little neater to print it as a DataFrame.  If we use `reset_index` it will make a DataFrame, but the count column will still be named `PLAYER_ID` so we can rename it.

# In[44]:


player_counts_1819_team.reset_index().rename(columns={'PLAYER_ID':'num_players'})


# All in all, this gives us a good answer that we can get with data and display answers and this is one way that using multiple data sources can help answer richer questions.

# In[ ]:





# ## Questions After Class
# 
# ###  Is there a max DB size? 
# 
# Generally, no.  In specific instances, yes.  For example, [MSFT SQL Server](https://learn.microsoft.com/en-us/sql/sql-server/maximum-capacity-specifications-for-sql-server?view=sql-server-ver16) has a max size of 524,272 terabytes. 
# 
# ### when can pandas not use SQL databases?
# 
# The most important limit here is realy that the cmoputer you are working on will have limits on how much data you can pull from the database into local RAM. 
# 
# 
# ### how do you learn more about different quieries you can use for sql?
# 
# [Wizard zines](https://wizardzines.com/zines/sql/) has a good reference, but it is not free. I have some of their other work though and it is all high quality. [this preview is especially helpful for me](https://wizardzines.com/comics/sql-query-order/) If the cost is prohibitive for you, but the preview of this looks like something you would like, send me an e-mail. 
# 
# [This cheatsheet is also good](https://learnsql.com/blog/sql-basics-cheat-sheet/).
# 
# 
# ### What other SQL 'keywords' in the queries are there? ex: SELECT, FROM, WHERE
# 
# [quick reference](https://www.w3schools.com/sql/sql_quickref.asp)
