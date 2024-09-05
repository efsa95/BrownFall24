#!/usr/bin/env python
# coding: utf-8

# # Reparing values
# So far, we've dealt with structural issues in data. but there's a lot more to
# cleaning.  
# 
# Today,  we'll deal with how to fix the values within  the data.
# ## Cleaning Data review
# 
# Instead of more practice with these manipulations, below are more
# examples of cleaning data to see how these types of manipulations get used.  
# Your goal here is not to memorize every possible thing, but to build a general
# idea of what good data looks like and good habits for cleaning data and keeping
# it reproducible.  
# - [Cleaning the Adult Dataset](https://ryanwingate.com/projects/machine-learning-data-prep/adult/adult-cleaning/)
# - [All Shades](https://github.com/the-pudding/data/tree/master/foundation-names#allshadescsv--allshadesr)
# Also here are some tips on general data management and organization.
# 
# This article is a comprehensive [discussion of data cleaning](https://towardsdatascience.com/the-ultimate-guide-to-data-cleaning-3969843991d4).
# 
# ### A Cleaning Data Recipe
# 
# __not everything possible, but good enough for this course__
# 
# 
# 1. Can you use parameters to read the data in better?
# 1. Fix the index and column headers (making these easier to use makes the rest easier)
# 1. Is the data strucutred well?
# 1. Are there missing values?
# 1. Do the datatypes match what you expect by looking at the head or a sample?
# 1. Are categorical variables represented in usable way?
# 1. Does your analysis require filtering or augmenting the data?

# In[1]:


import pandas as pd
import seaborn as sns
import numpy as np #
na_toy_df_np = pd.DataFrame(data = [[1,3,4,5],[2 ,6, np.nan]])
na_toy_df_pd = pd.DataFrame(data = [[1,3,4,5],[2 ,6, pd.NA]])

# make plots look nicer and increase font size
sns.set_theme(font_scale=2)
arabica_data_url = 'https://raw.githubusercontent.com/jldbc/coffee-quality-database/master/data/arabica_data_cleaned.csv'

coffee_df = pd.read_csv(arabica_data_url,index_col=0)


rhodyprog4ds_gh_events_url = 'https://api.github.com/orgs/rhodyprog4ds/events'
course_gh_df = pd.read_json(rhodyprog4ds_gh_events_url)


# ## What is clean enough?
# 
# This is a great question, without an easy answer.
# 
# It depends on what you want to do.  This is why it's important to have potential
# questions in mind if you are cleaning data for others *and* why we often have to
# do a little bit more preparation after a dataset has been "cleaned"
# 
# ## Fixing Column names

# In[2]:


coffee_df.columns


# In[3]:


col_name_mapper = {col_name:col_name.lower().replace('.','_') for col_name in coffee_df.columns}


# In[4]:


coffee_df.rename(columns=col_name_mapper).head(1)


# In[5]:


coffee_df.head(1)


# In[6]:


coffee_df_fixedcols = coffee_df.rename(columns=col_name_mapper)
coffee_df_fixedcols.head(1)


# In[7]:


coffee_df_fixedcols['unit_of_measurement'].value_counts()


# In[8]:


coffee_df_fixedcols['unit_of_measurement'].replace({'m':'meters','ft':'feet'})


# In[9]:


coffee_df_fixedcols['unit_of_measurement_long'] = coffee_df_fixedcols['unit_of_measurement'].replace(
                                    {'m':'meters','ft':'feet'})
coffee_df_fixedcols.head(1)


# ## Missing Values
# 
# 
# Dealing with missing data is a whole research area. There isn't one solution.
# 
# 
# [in 2020 there was a whole workshop on missing](https://artemiss-workshop.github.io/)
# 
# one organizer is the main developer of [sci-kit learn](https://scikit-learn.org/stable/) the ML package we will use soon.  In a [2020 invited talk](https://static.sched.com/hosted_files/ray2020/08/Keynote-%20Easier%20Machine%20Learning%20Thoughts%20From%20Scikit-Learn%20-%20Ga%C3%ABl%20Varoquaux%2C%20Research%20Director%2C%20Inria.pdf) he listed more automatic handling as an active area of research  and a development goal for sklearn.
# 
# There are also many classic approaches both when training and when [applying models](https://www.jmlr.org/papers/volume8/saar-tsechansky07a/saar-tsechansky07a.pdf).
# 
# [example application in breast cancer detection](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.701.4234&rep=rep1&type=pdf)
# 
# Even in pandas, dealing with [missing values](https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html) is under [experimentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html#missing-data-na)
#  as to how to represent it symbolically
# 
# 
# Missing values even causes the [datatypes to change](https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html#missing-data-casting-rules-and-indexing)
# 
# 
# That said, there are are om
# Pandas gives a few basic tools:
# 
# - dropna
# - fillna
# 
# 
# Dropping is a good choice when you otherwise have a lot of data and the data is
# missing at random.
# 
# Dropping can be risky if it's not missing at random. For example, if we saw in
# the coffee data that one of the scores was missing for all of the rows from one
# country, or even just missing more often in one country, that could bias our
# results.  
# 
# Filling can be good if you know how to fill reasonably, but don't have data to
# spare by dropping.  For example
# - you can approximate with another column
# - you can approximate with that column from other rows
# 
# Special case, what if we're filling a summary table?
# - filling with a symbol for printing can be a good choice, but not for analysis.
# 
# **whatever you do, document it**

# In[10]:


coffee_df_fixedcols.info()


# ### Filling missing values 
# The 'Lot.Number' has a lot of NaN values, how can we explore it?
# 
# We can look at the type:

# In[11]:


coffee_df_fixedcols['lot_number'].dtype


# And we can look at the value counts.

# In[12]:


coffee_df_fixedcols['lot_number'].value_counts()


# We see that a lot are '1', maybe we know that when the data was collected, if the Farm only has one lot, some people recorded '1' and others left it as missing. So we could fill in with 1:

# In[13]:


coffee_df_fixedcols['lot_number'].fillna('1')


# Note that even after we called `fillna` we display it again and the original data is unchanged.
# To save the filled in column we have a few choices:
# - use the `inplace` parameter. This doesn't offer performance advantages, but does It still copies the object, but then reassigns the pointer. Its under discussion to [deprecate](https://github.com/pandas-dev/pandas/issues/16529)
# - write to a new DataFrame
# - add a column
# 
# 
# We'll use adding a column:

# In[14]:


coffee_df_fixedcols['lot_number_clean'] = coffee_df_fixedcols['lot_number'].fillna('1')


# In[15]:


coffee_df_fixedcols['lot_number_clean'].value_counts()


# ### Dropping missing values
# To illustrate how `dropna` works, we'll use the `shape` method:

# In[16]:


coffee_df_fixedcols.shape


# In[17]:


coffee_df_fixedcols.dropna().shape


# By default, it drops any row with one or more `NaN` values.
# 
# We could instead tell it to only drop rows with `NaN` in a subset of the columns.

# In[18]:


coffee_df_fixedcols.dropna(subset=['altitude_low_meters']).shape


# In[19]:


coffee_alt_df = coffee_df_fixedcols.dropna(subset=['altitude_low_meters'])


# In the [Open Policing Project Data Summary](https://openpolicing.stanford.edu/data/) we saw that they made a summary information that showed which variables had at least 70% not missing values.  We can similarly choose to keep only variables that have more than a specific threshold of data, using the `thresh` parameter and `axis=1` to drop along columns.

# In[20]:


n_rows, n_cols = coffee_df_fixedcols.shape
coffee_df_fixedcols.dropna(thresh = .7*n_rows, axis=1).shape


# This dataset is actually in pretty good shape, but if we use a more stringent threshold it drops more columns.

# In[21]:


coffee_df_fixedcols.dropna(thresh = .85*n_rows, axis=1).shape


# ## Inconsistent values
# 
# 
# This was one of the things that many of you anticipated or had observed.  A useful way to investigate for this, is to use `value_counts` and sort them alphabetically by the values from the original data, so that similar ones will be consecutive in the list. Once we have the `value_counts()` Series, the values from the `coffee_df` become the index, so we use `sort_index`.
# 
# Let's look at the `in_country_partner` column

# In[22]:


coffee_df_fixedcols['in_country_partner'].value_counts().sort_index()


# We can see there's only one `Blossom Valley International\n` but 58 `Blossom Valley International`, the former is likely a typo, especially since `\n` is a special character for a newline. Similarly, with 'Specialty Coffee Ass' and 'Specialty Coffee Association'.

# In[23]:


partner_corrections = {'Blossom Valley International\n':'Blossom Valley International',
  'Specialty Coffee Ass':'Specialty Coffee Association'}


# In[24]:


coffee_df_clean = coffee_df_fixedcols.replace(partner_corrections)


# ## Example: Unpacking Jsons

# In[25]:


rhodyprog4ds_gh_events_url


# In[26]:


gh_df = pd.read_json(rhodyprog4ds_gh_events_url)
gh_df.head()


# Some datasets have a nested structure
# 
# We want to transform each one of those from a dictionary like thing into a
# row in a data frame.
# 
# We can see each row is a Series type.

# In[27]:


type(gh_df.loc[0])


# In[28]:


a= '1'
type(a)


# Recall, that base python types can be used as function, to cast an object from
# type to another.

# In[29]:


type(int(a))


# This works with Pandas Series too

# In[30]:


pd.Series(gh_df.loc[0]['actor'])


# We can use [pandas `apply`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html) to do the same thing to every item in a dataset (over rows or columns as items )
# For example

# In[31]:


gh_df['actor'].apply(pd.Series).head()


# compared to the original:

# In[32]:


gh_df.head(1)


# We want to handle several columns this way, so we'll make alist of the names.

# In[33]:


js_cols = ['actor','repo','payload','org']


# `pd.concat` takes a list of dataframes and puts the together in one DataFrame.

# In[34]:


pd.concat([gh_df[col].apply(pd.Series) for col in js_cols],axis=1).head()


# This is close, but a lot of columns have the same name. To fix this we will
#  rename the new columns so that they have the original column
# name prepended to the new name.
# 
# pandas has a rename method for this.
# 
# and this is another job for lambdas.

# In[35]:


pd.concat([gh_df[col].apply(pd.Series).rename(lambda c: '_'.join([c,col])) for col in js_cols],axis=1).head()


# In[36]:


gh_df['actor'].apply(pd.Series).rename(columns=lambda c: '_'.join([c,'actor']))


# In[37]:


json_cols_df = pd.concat([gh_df[col].apply(pd.Series).rename(columns=lambda c: '_'.join([c,col])) for col in js_cols],axis=1).head()


# In[38]:


gh_df.columns


# In[39]:


json_cols_df.columns


# Then we can put the two parts of the data together

# In[40]:


pd.concat([gh_df[['id','type','public','created_at']],json_cols_df],)


# and finally save this

# In[41]:


gh_df_clean = pd.concat([gh_df[['id','type','public','created_at']],json_cols_df],axis=1)
gh_df_clean.head()


# If we want to analyze this data, this is a good place to save it to disk and start an analysis in  separate notebook.

# In[42]:


gh_df_clean.to_csv('gh_events_unpacked.csv')


# ## Questions After Class
# 
# ### How the apply function works/use cases?
# 
# A4 will give you some examples, espeically the airline dataset. We will also keep seing it come up as we manipulate data more. 
# 
# the [apply docs](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html) have tiny examples that help illustrate what it does and some of how it works. The [pandas faq has a section on apply and similar methods](https://pandas.pydata.org/docs/user_guide/gotchas.html#mutating-with-user-defined-function-udf-methods) that gives some more use cases.  
# 
# ### Is there a better way to see how many missing values?
# 
# There are lots of ways. All are fine. We used `info` in class because I was trying to use the way we had already seen.
# Info focuses on how many values are *present* instead of what is missing because it makes more sense in most cases. The more common question is: are there enough values to make decisions with?
# 
# If you wanted to get counts of the missing values, you can use the pandas [`isna`](https://pandas.pydata.org/docs/reference/api/pandas.isna.html) function.  It is a pandas function, the docs say `pandas.isna` not a DataFrame method (which would be described like `pandas.DataFrame.methodname`). 
# This means we use it like

# In[43]:


value_to_test = 4
pd.isna(value_to_test)


# ```{admonition} Try it Yourself
# pass different values like: `False`, `np.nan` (also `import numpy as np`) and, `pd.NA`, `hello` to this function
# ```

# In[44]:


help(pd.isna)


# The docstring says that it returns "bool or array-like of bool" but if we go to the website docs that have more examples, we can find out what that it will [return a DataFrame if we pass it a DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.isna.html#:~:text=For%20Series%20and%20DataFrame%2C%20the%20same%20type%20is%20returned%2C%20containing%20booleans). Then we can use the [`pandas.DataFrame.sum`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sum.html) method.

# In[45]:


pd.isna(coffee_df_clean).sum()


# ###  in `col_name_mapper = {col_name:col_name.lower().replace('.','_') for col_name in coffee_df.columns}` what is the `{}` for?
# 
# This is called a dictionary comphrehension. It is very similar to a [list comprehension](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions). It is one of the [defined ways to build a `dict` type object](https://docs.python.org/3/library/stdtypes.html#dict)
# 
# We also saw one when we looked at different types in a [previous class](2023-02-02.md).

# In[46]:


{char:i for i,char in enumerate('abcde')}


# [`enumerate`](https://docs.python.org/3/library/functions.html#enumerate) is a built in function that 
# iterates over items in an iterable type(list-like) and pops the each value paired with its index within
# the structure.  
# 
# This way we get each character and it's position. We could use this as follows

# In[47]:


num_chars = {char:i for i,char in enumerate('abcde')}
alpha_data = ['a','d','e','c','b',']

