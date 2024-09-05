#!/usr/bin/env python
# coding: utf-8

# # Welcome and Introduction 
# 
# ## Prismia Chat
# 
# We will use these to monitor your participation in class and to gather information.
# Features:
# - instructor only
# - reply to you directly
# - share responses for all
# 
# 
# 
# ## How this class will work
# 
# **Participatory Live Coding**
# 
# 
# What is a topic you want to use data to learn about?
# 
# 
# [Debugging is both technical and a soft skill](https://twitter.com/b0rk/status/1403405539971842052?s=19)
# 
# 
# ## Programming for Data Science vs other Programming
# 
# The audience is different, so the form is different.
# 
# In Data Science our product is more often a report than a program.
# 
# ````{margin}
# ```{warning}
# Sometimes there will be points in the notes that were not made in class due to time or in response questions that came at the end of class.
# ```
# ````
# 
# ```{note}
# Also, in data science we are *using code* to interact with data, instead of having a plan in advance
# ```
# 
# So programming for data science is more like *writing* it has a narrative flow and is made to be seen more than some other programming thaat you may have done.
# 
# 
# 
# 
# ## Jupyter Notebooks
# 
# Launch a [`jupyter notebook` server](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html):
# - on Windows, use anaconda terminal
# - on Mac/Linux, use terminal
# 
# ```
# cd path/to/where/you/save/notes
# jupyter notebook
# ```
# 
# 
# ### What just happened?
# - launched a local web server
# - opened a new browser tab pointed to it
# 
# ![a diagram depicting a terminal window launching a local web server that reports back to the terminal and serves jupyter in the browser](https://raw.githubusercontent.com/rhodyprog4ds/rhodyds/main/img/jupyter_notebook_running.svg)
# 
# 
# ### Start a Notebook
# 
# Go to the new menu in the top right and choose Python 3
# 
# ![a screenshot of opening a new notebook in a jupyter noteboook](https://raw.githubusercontent.com/rhodyprog4ds/rhodyds/main/img/new_notebook.png)
# 
# 
# Now, it starts a python kernel on the webserver
# ![a diagram depicting a terminal window launching a local web server that reports back to the terminal and serves jupyter in the browser, with a python logo on the server](https://raw.githubusercontent.com/rhodyprog4ds/rhodyds/main/img/jupyter_notebook_running_python.svg)
# 
# 
# 
# ### A jupyter notebook tour
# 
# A Jupyter notebook has two modes. When you first open, it is in command mode. The border is blue in command mode.
# 
# ![screenshot of a code cell in command mode](../img/command_mode.png)
# 
# When you press a key in command mode it works like a shortcut. For example `p` shows the command search menu.
# 
# ![screenshot of the command menu](../img/command_menu.png)
# 
# 
# If you press `enter` (or `return`)  or click on the highlighted cell, which is the boxes we can type in,  it changes to edit mode. The border is green in edit mode
# 
# ![screenshot of a code cell in edit mode](../img/code_cell.png)
# 
# There are two type of cells that we will used: code and markdown. You can change that in command mode with `y` for code and `m` for markdown or on the cell type menu at the top of the notebook.
# 
# ![screenshot of the cell type menu](../img/cell_type_menu.png)
# 
# ++
# 
# This is a markdown cell
# - we can make
# - itemized lists of
# - bullet points
# 
# 1. and we can make nubmered
# 1. lists, and not have to worry
# 1. about renumbering them
# 1. if we add a step in the middle later

# In[1]:


# this is a comment in a code cell , we can run this to see output
3+4


# the output here is the value returned by the python interpretter for the last line of the cell
# 
# We set variables

# In[2]:


name = 'sarah'


# The notebook displays nothing when we do an assignment, bcause it returns nothing

# In[3]:


name


# we can put a variable there tosee it

# In[4]:


course = 'csc310'
course
name


# Note that this version doesn't show use the value for `course`

# In[5]:


name = 'Sarah'


# ```{important}
# In class, we ran these cells out of order and noticed how the value does not update unless we run the new version
# ```

# In[6]:


name


# In[7]:


course


# ### Notebook Reminders
# 
# Blue border is command mode, green border is edit mode
# 
# use Escape to get to command mode
# 
# 
# Common command mode actions:
# - m: switch cell to markdown
# - y: switch cell to code
# - a: add a cell above
# - b: add a cell below
# - c: copy cell
# - v: paste the cell
# - 0 + 0: restart kernel
# - p: command menu
# 
# use enter/return to get to edit mode

# In code cells, we can use a python interpreter, for example as a calculator.

# In[8]:


4+6


# It prints out the last line of code that it ran, even though it executes all of them

# In[9]:


name = 'sarah'
4+5
name *3


# ## Getting Help in Jupyter
# 
# Getting help is important in programming
# 
# 
# When your cursor is inside the `()` of a function if you hold the shift key and press tab it will open a popup with information. If you press tab twice, it gets bigger and three times will make a popup window. 
# 
# Python has a `print` function and we can use the help in jupyter to learn about
# how to use it in different ways.
# 
# We can print the docstring out, as a whole instead of using the shfit + tab to view it.

# In[10]:


help(print)


# The first line says that it can take multiple values, because it says `value, ..., sep`
# 
# It also has a
# keyword argument (must be used like `argument=value` and has a default) described as  `sep=' '`.
# This means that by default it adds a space as above.

# In[11]:


print(name)


# How do you use the `print` function to output: `Sarah_csc310`?

# In[12]:


print(name,course,sep='_')


# In[13]:


help(print)


# We can put as many values as we want there. Thats what the `...` in the function signature means

# In[14]:


print(name,course,'hello','bye',sep='_')


# In[15]:


print(name,course,'hello','bye',sep='\n')


# ```{important}
# Basic programming is a prereq and we will go faster soon, but the goal of this review was to understand notebooks, getting help, and reading docstrings 
# ```
# 
# 
# 
# ## What is Data Science?
# 
# Data Science is the combination of
# ![venn diagram of CS, Stats, & domain expertise with DS at the center](https://raw.githubusercontent.com/rhodyprog4ds/rhodyds/main/img/ds_venn.png)
# 
# 
# **statistics** is the type of math we use to make sense of data.
# Formally, a statistic is just a function of data.
# 
# **computer science** is so that we can manipulate visualize and automate the inferences we make.
# 
# **domain expertise** helps us have the intuition to know if what we did worked
# right. A statistic must be interpreted in context; the relevant context determines
# what they mean and which are valid.  The context will say whether automating something
# is safe or not, it can help us tell whether our code actually worked right or not.
# 
# ### In this class,
# 
# ![venn diagram of CS, Stats, & domain expertise with DS at the center, w/310 location marked](https://raw.githubusercontent.com/rhodyprog4ds/rhodyds/main/img/310_venn.png)
# 
# We'll focus on the programming as our main means of studying data science, but we will
# use bits of the other parts.  In particular, you're encouraged to choose datasets that you
# have domain expertise about, or that you want to learn about.
# 
# But there are many definitions.  We'll use this one, but you may come across others.
# 
# ### How does data science happen?
# 
# The most common way to think about what doing data science means is to think of this pipeline.  It is in the perspective of the data, these are all of the things that happen to the data.
# 
# ![DS pipeline: collect, clean, explore, model, deploy](https://raw.githubusercontent.com/rhodyprog4ds/rhodyds/main/img/process.png)
# 
# Another way to think about it
# 
# ![DS process: 3 major phases (prepare,build,finish) with many sub-phases. Prepare:set goals, explore, wrangle, assess; Build: Plan, analyze, engineer, optimize, execute; Finish: Deliver, revise, wrap up](https://drek4537l1klr.cloudfront.net/godsey/Figures/01fig02_alt.jpg)
# 
# ### how we'll cover Data Science, in depth
# 
# 
# ![DS pipeline: collect, clean, explore, model, deploy](https://raw.githubusercontent.com/rhodyprog4ds/rhodyds/main/img/process_course.png)
# 
# - *collect*: Discuss only a little; Minimal programming involved
# - *clean*: Cover the main programming techniques; Some requires domain knowledge beyond scope of course
# - *explore*: Cover the main programming techniques; Some requires domain knowledge beyond scope of course
# - *model*:Cover the main programming, basic idea of models; How to use models, not how learning algorithms work
# - *deploy*: A little bit at the end, but a lot of preparation for decision making around deployment
# 
# 
# ### how we'll cover it in, time
# 
# ![DS pipeline: collect, clean, explore, model, deploy](https://raw.githubusercontent.com/rhodyprog4ds/rhodyds/main/img/process_course_time.png)
# 
# We'll cover exploratory data analysis before cleaning because those tools will help us check how we've cleaned the data.
# 
# 
# ## Prepare for the next class
# 
# 
# - Read carefully the syllabus section of the [course website](https://rhodyprog4ds.github.io/BrownSpring23/syllabus/about)
# - skim the rest of the [course website](https://rhodyprog4ds.github.io/BrownSpring23/)
# - Bring questions about how the class will work to class on Thursday.
# - Review [Git & GitHub Fundamentals](https://classroom.github.com/a/axURjdPb)
# - Bring git/github questions on Thursday.
# - Begin reading [chapter 1 of think like a data scientist](https://www.manning.com/books/think-like-a-data-scientist#toc) (finish in time for it to help you with the assignment due Monday night)
# 
# On Thursday we will start with a review of the syllabus.
# You will answer an ungraded quiz to confirm that you understand and I'll answer
# all of your questions.
# Then we will do a little bit with Git/GitHub and start your first assignment in class.
# 
# 
# Think like a data scientist is written for practitioners; not as a text book for a class. It does not have a lot of prerequisite background, but the sections of it that I assign will help you build a better mental picture of what doing Data Science about.
# ````{margin}
# ```{tip}
# In chapter 1, focus most on sections 1.1, 1.3, and 1.7.
# ```
# ````
# 
# 
# ```{warning}
# Only the first assignment will be due this fast, it's a short review and setup assignment.  It's due quickly so that we know that you have everything set up and the prerequisite material before we start new material next week.
# ```
