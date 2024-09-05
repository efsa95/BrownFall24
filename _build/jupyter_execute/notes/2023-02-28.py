#!/usr/bin/env python
# coding: utf-8

# # Evaluating ML Algorithms
# 
# This week we are going to start learning about machine learning.
# 
# We are going to do this by looking at how to tell if machine learning has worked.
# 
# This is because:
# - you have to check if one worked after you build one
# - if you do not check carefully, it might only sometimes work
# - gives you a chance to learn *only* evaluation instead of evaluation + an ML task
# 
# ## What is a Machine Learning Algorithm? 
# 
# 
# First, what is an Algorithm?
# 
# > An algorithm is a set of ordered steps to complete a task.
# 
# Note that when people outside of CS talk about algorithms that impact people's lives these are often *not written directly by people* anymore.  THey are often the result of machine learning.
# 
# In machine learning, people write an algorithm for how to write an algorithm based on data.  This often comes in the form of a statitistical model of some sort.
# 
# ![Ml overview: training data goes into the learning algorithm, which outputs the prediction algorithm. the prediciton algorithm takes a sampleand outputs a prediction](../img/MLdataflow.svg)
# 
# When we *do* machine learning, this can also be called:
# - data mining
# - pattern recognition
# - modeling
# 
# because we are looking for patterns in the data and typically then planning to
# use those patterns to make predictions or automate a task.  
# 
# Each of these terms does have slightly different meanings and usage, but
# sometimes they're used close to exchangeably.
# 
# 
# 
# ## How can we tell if ML is working?  
# 
# We measure the performance of the prediction algorithm, to determine if the learning algorithm worked. 
# 
# 
# ## Replicating the COMPAS Audit
# We are going to replicate the audit from ProPublica [Machine Bias](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing)
# 
# ### Why COMPAS?
# 
# 
# Propublica started the COMPAS Debate with the article [Machine Bias](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencin).  With their article, they also released details of their methodology and their [data and code](https://github.com/propublica/compas-analysis).  This presents a real data set that can be used for research on how data is used in a criminal justice setting without researchers having to perform their own requests for information, so it has been used and reused a lot of times.
# 
# 
# ### Propublica COMPAS Data
# 
# 
# The dataset consists of COMPAS scores assigned to defendants over two years 2013-2014 in Broward County, Florida, it was released by Propublica in a [GitHub Repository](https://github.com/propublica/compas-analysis/). These scores are determined by a proprietary algorithm designed to evaluate a persons recidivism risk - the likelihood that they will reoffend. Risk scoring algorithms are widely used by judges to inform their sentencing and bail decisions in the criminal justice system in the United States.
# 
# The journalists collected, for each person arreste din 2013 and 2014:
# - basic demographics
# - details about what they were charged with and priors
# - the COMPAS score assigned to them
# - if they had actually been re-arrested within 2 years of their arrest
# 
# This means that we have what the COMPAS algorithm predicted (in the form of a score from 1-10) and what actually happened (re-arrested or not). We can then measure how well the algorithm worked, in practice, in the real world.

# In[1]:


import pandas as pd
from sklearn import metrics
import seaborn as sns


# We're going to work with a cleaned copy of the data released by Propublica that also has a minimal subset of features.
# 
# * `age`: defendant's age
# * `c_charge_degree`: degree charged (Misdemeanor of Felony)
# * `race`: defendant's race
# * `age_cat`: defendant's age quantized in "less than 25", "25-45", or "over 45"
# * `score_text`: COMPAS score: 'low'(1 to 5), 'medium' (5 to 7), and 'high' (8 to 10).
# * `sex`: defendant's gender
# * `priors_count`: number of prior charges
# * `days_b_screening_arrest`: number of days between charge date and arrest where defendant was screened for compas score
# * `decile_score`: COMPAS score from 1 to 10 (low risk to high risk)
# * `is_recid`: if the defendant recidivized
# * `two_year_recid`: if the defendant within two years
# * `c_jail_in`: date defendant was imprisoned
# * `c_jail_out`: date defendant was released from jail
# * `length_of_stay`: length of jail stay

# In[2]:


compas_clean_url = 'https://raw.githubusercontent.com/ml4sts/outreach-compas/main/data/compas_c.csv'
compas_df = pd.read_csv(compas_clean_url)
compas_df.head()


# ## One-hot Encoding
# 
# We will audit first to see how good the algorithm is by treating the predictions as either high or not high.  One way we can get to that point is to transform the `score_text` column from one column with three values, to 3 binary columns.

# In[3]:


pd.get_dummies(compas_df['score_text'])


# In[4]:


compas_onehot = pd.concat([compas_df,pd.get_dummies(compas_df['score_text'])],axis=1)


# We could have done the above line in one neater step, but in class I for this was an option.

# In[5]:


compas_df_onehot = pd.get_dummies(compas_df,columns=['score_text'])


# Next lets look at the thresholds that were used so that we know what the mean

# In[6]:


compas_onehot.groupby('score_text')['decile_score'].agg(['min','max'])


# We will also audit with respect to second threshold.

# In[7]:


compas_onehot['MedHigh'] = compas_onehot['High'] + compas_onehot['Medium']


# ## Sklearn Performance metrics 
# 
# 
# 
# The first thing we usually check is the accuracy: the percentage of all samples that are correct.

# In[8]:


metrics.accuracy_score(compas_onehot['two_year_recid'],compas_onehot['High'])


# ````{margin}
# ```{note}
# the wikipedia page for confusion matrix is a really good reference
# ```
# ````
# However this does not tell us anything about what *types* of mistakes the algorithm made.  The type of mistake often matters in terms of how we trust or deploy an algorithm.  We use a [confusion matrix](https://en.wikipedia.org/wiki/Confusion_matrix) to describe the performance in more detail.
# 
# 
# 
# A confusion matrix counts the number of samples of each *true* category that wre predicted to be in each category. In this case we have a binary prediction problem: people either are re-arrested (truth) or not and were given a high score or not(prediction).  In binary problems we adopt a common language of labeling one outcome/predicted value positive and the other negative.  We do this not based on the social value of the outcome, but on the numerical encoding.  
# 
# In this data, being re-arrested is indicated by a 1 in the `two_year_recid` column, so this is the *positive class* and not being re-arrested is 0, so the *negative class*.  Similarly a high score is 1, so that's the *positive prediction* and not high is 0, so that is the a *negative prediction*.

# In[9]:


metrics.accuracy_score(compas_onehot['two_year_recid'],compas_onehot['MedHigh'])


# [docs](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)

# In[10]:


metrics.confusion_matrix(compas_onehot['two_year_recid'],compas_onehot['MedHigh'])


# ```{note}
# these terms can be used in any sort of detection problem, whether machine learning is used or not
# ```
# 
# `sklearn.metrics` provides a `[confusion matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)` function that we can use.
# 
# 
# Since this is binary problem we have 4 possible outcomes:
# - true negatives($C_{0,0}$): did not get a high score and were not re-arrested
# - false negatives($C_{1,0}$):: did not get a high score and were re-arrested
# - false positives($C_{0,1}$):: got a high score and were not re-arrested
# - true positives($C_{1,1}$):: got a high score and were re-arrested
# 
# 
# With these we can revisit accuracy:
# 
# $$ A = \frac{C_{0,0} + C_{1,1}}{C_{0,0}+ C_{1,0} + C_{0,1} + C_{1,1}} $$
# 
# 
# and we can define new scores. Two common ones in CS are recall and precision.
# 
# Recall is:
# 
# $$ R = \frac{C_{1,1}}{C_{1,0} + C_{1,1}} $$

# In[11]:


metrics.recall_score(compas_df['two_year_recid'],compas_df['score_text_High'])


# That is, among the truly positive class how many were correctly predicted?  In COMPAS, it's the percentage of the re-arrested people who got a high score.
# 
# 
# Precision is
# $$ P = \frac{C_{1,1}}{C_{0,1} + C_{1,1}} $$

# In[12]:


metrics.recall_score(compas_onehot['two_year_recid'],compas_onehot['MedHigh'])


# In[13]:


metrics.precision_score(compas_onehot['two_year_recid'],compas_onehot['MedHigh'])


# ## Per Group Scores 
# 
# To groupby and then do the score, we can use a lambda again, with apply

# In[14]:


acc_fx  = lambda d: metrics.accuracy_score(d['two_year_recid'],d['MedHigh'])
compas_onehot.groupby('race').apply(acc_fx)


# That lambda + apply is equivalent to:

# In[15]:


race_acc = []
for race, rdf in compas_race:
    acc = skmetrics.accuracy_score(rdf['two_year_recid'],
             rdf['score_text_MedHigh'])
    race_acc.append([race,acc])

pd.DataFrame(race_acc, columns =['race','accuracy'])


# In[16]:


recall_fx  = lambda d: metrics.recall_score(d['two_year_recid'],d['MedHigh'])
compas_onehot.groupby('race').apply(recall_fx)


# In[17]:


precision_fx  = lambda d: metrics.precision_score(d['two_year_recid'],d['MedHigh'])
compas_onehot.groupby('race').apply(precision_fx)


# The recall tells us that the model has very different impact on people.  On the other hand the precision tells us the scores mean about the same thing for Black and White people. 
# 
# Researchers established that these are mutually exclusive, provably.  We cannot have both, so it is very important to think about what the performance metrics mean and how your algorithm will be used in order to choose how to prepare a model.  We will train models starting next week, but knowing these goals in advance is essential.
# 
# Importantly, this is not a statistical, computational choice that data can answer for us. This is about *human* values (and to some extent the law; certain domains have legal protections that require a specific condition).
# 
# The Fair Machine Learning book's classificaiton Chapter has a [section on relationships between criteria](https://fairmlbook.org/classification.html#relationships-between-criteria) with the proofs.
# 
# 
# 
# ```{important}
# 
# We used ProPublica's COMPAS dataset to replicate (parts of, with different tools) their analysis. That is, they collected the dataset in order to audit the COMPAS algorithm and we used it for the same purpose (and to learn model evaluation).  This dataset is not designed for *training* models, even though it has been used as such many times.  This is [not the best way](https://openreview.net/pdf?id=qeM58whnpXM) to use this dataset and for future assignments I do not recommend using this dataset.
# ```
# 
# ````{margin}
# ```{note}
# If you are interested in fairness in ML, that is what my research is. Reach out to me if you want to know more!
# ```
# ````

# In[ ]:





# ## Prepare for Next Class 
# 
# [install aif360](https://github.com/Trusted-AI/AIF360#install-with-pip) 
# 
# ## Portfolio
# 
# Audience is not *me*, but a generally knowledgable person.  For example:
# - a student deciding if they want to take this course or not.  They know how to code, but not datascience.
# - a person familiar with the domain your data is from (eg a sports fan if sports data)
# - a future employer who wants to know about your skills
# 
# any of these people know big ideas, but not exactly what happened in class. You
# can specify which audience you're targetting in the introduction (which is the
#   one piece that I'm the audience for)
# 
# 
# Goal is to show what you understand and are able to do
# not only what you *can* do, because you can do a lot of simple things by finding answers online. we want you to understand enough that when you start seeing new, real problems, you're able to do  these things on your own
#  - level 1: you can follow a conversation
#  - level 2: you can do it if someone gives you a rough plan
#  - level 3: you can do it, given only an end goal
# Think of this more like a report with code as the figures than a coding assignment. To see what you've learned we should be able to read through on piece of text, not compare two files so it could be like:
