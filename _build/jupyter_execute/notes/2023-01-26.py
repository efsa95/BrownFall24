#!/usr/bin/env python
# coding: utf-8

# # Syllabus and Python Review 
# 
# ## Course Logistics
# 
# 
# Class is designed to avoid this:
# 
# ![gif of man throwing computer monitor](https://i.gifer.com/5SNC.gif)
# 
# <blockquote class="twitter-tweet"><p lang="en" dir="ltr">we think about debugging as a technical skill (and it absolutely is!!) but a huge amount of it is managing your feelings so you don&#39;t get discouraged and being self-aware so you can recognize your incorrect assumptions</p>&mdash; 🔎Julia Evans🔍 (@b0rk) <a href="https://twitter.com/b0rk/status/1403405539971842052?ref_src=twsrc%5Etfw">June 11, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
# 
# Read more about how I'm designing this course to help you learn on the
# [how to learn](../resources/learning) page.
# 
# ## Check your understanding of the syllabus
# 
# It's easy when reading something long to lose track of it. Your eyes can go over each word, without actually retaining the information, but it's important to understand the syllabus for the course.
# 
# You can find the answers to the following questions on the syllabus. If you've already read it, try answering them to check your understanding. If you haven't read it yet, use these to guide you to get familiar with finding key facts about the course on the syllabus.
# 
# 1. What do you need to bring to class each day?
# 1. What is the basis of grading for this course?
# 1. How do you reference the course text?
# 1. What is the penalty for missing an assignment?
# 
# 
# More information about the course is available throughout the site, the next few questions will help you self-check that you've found the important things.  Remember, the goal is not necessarily to memorize all of this, but to be able to find it.
# 
# 1. When & what are you expected to read for this class?
# - [ ] read the text book before class
# - [ ] review notes & documentation after class
# - [ ] preview the notes  & documentation before class
# - [ ] read documentation and text book after class
# 1. Your assignment says to find a dataset that has variables of a specific type, which website can you use?
# 1. Your assignment says to find a dataset of any type about something you're interested in, which resource would you use?
# 
# 
# 
# ## Python Review
# 
# Official source on python: 
# - [pep8 official style](https://peps.python.org/pep-0008/)
# - [documentation](https://docs.python.org/3/) note that you can change which version you are using
# 
# 
# We will go quickly through these focusing on pythonic style, because the prerequisite is a programming course. 
# 
# ### Functions
# Syntax of a function in python:

# In[1]:


def greeting(name):
    '''
    say hi to a person
    
    Parameters
    ----------
    name : string
        the name of who to greet
    '''
    return "hi "+ name


# A few things to note:
# - the `def` keywords starts a function
# - then the name of the function
# - parameters in `()` then `:`
# - the body is indented
# - the first thing in the body should be a docstring, denoted in `'''` which is a multiline comment
# - returning is more reliable than printing in a function
# 
# ```{tip}
# In python, [PEP 257](https://peps.python.org/pep-0257/) says how to write a docstring, but it is very broad.
# 
# In Data Science, [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) style docstrings are popular.
# 
# - [Pandas](https://pandas.pydata.org/) [follows numpydoc](https://pandas.pydata.org/docs/development/contributing_docstring.html)
# - [Numpy uses it]
# - [Scipy](https://scipy.org/) [follows numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard)
# ```
# 
# 
# 
# Once the cell with the function definition is run, we can use the function

# In[2]:


greeting('sarah')


# With a return this works to check that it does the right thing

# In[3]:


assert greeting('sarah') == "hi sarah"


# ### Conditionals

# In[4]:


def greeting2(name,formal=False):
    '''
    say hi to a person
    
    Parameters
    ----------
    name : string
        the name of who to greet
    formal : bool
        if the greeting should be formal (hello) or not (hi)
    '''
    if formal: 
        message = 'hello ' + name
    else:
        message = "hi "+ name
    return  message


# key points in this function: 
# - an `if` also has the conditional part indented
# - for a `bool` variable we can just use the variable
# - we can set a default value

# In[5]:


greeting2('sarah',True)


# In[6]:


greeting2('sarah',False)


# because of the default value we do not have to pass the second variable:

# In[7]:


greeting2('sarah')


# In[8]:


help(greeting)


# ## Questions After Class
# 
# ### Why is indentation important in python but not other languages like C++?
# 
# Python is a newer language than C and C++.  Older languages had to contend with the fact that a space character uses the same amount of memory as any other character, so they were not used.  However, whitespace is easy to read.  
# 
# 
# Python was started in [1989](https://docs.python.org/3/faq/general.html#why-was-python-created-in-the-first-place), compared to C in [1972](https://ieeexplore.ieee.org/document/6499601), C++ was started in 1985ish, but stuck with a lot of things from C, so tht 1972 is strongly operative.  
# 
# Python is designed to be easy. It is designed to make complex tasks easier to do.  C is designed to be efficient and to compeile well, even if it is hard to learn and do.
# 
# 
# 
# ###  Why is python so much slower as well?
# Python is slower because it is an interpreted language. That means another program called the Python interpreter (which mostly are written in C) is actually running on your computer, that program parses the text of your source code and then executes the code. The interpreter cannot look ahead and change things in how you wrote your code while it runs. 
# 
# In contrast, C++ (like C) is a compiled language.  This means that a program called a compiler parses your code and translates it into assembly then to machine code. During this process it can optimize your code to make sure that it is fast.  
# 
# ### Are portfolios simply whatever we submit, such as assignments, to Github or are there other things that need to be submitted to the portfolios for level 3?
# 
# Assignments are separate from the portfolio checks.  It will become more clear what to do in your portfolio after you get feedback on assignment 2, and start working on assignment 3.  
# 
# 
# ### Will we know the specific criteria to fulfill a level 3 achievement when doing the portfolio?
# 
# The evaluation criteria are already listed on the [](checklists). 
# 
# 
# ### when is the Assignment 1 due?
# 
# Monday, end of day. See the details: [](../assignments/01-syllabus-install)
# 
# ### how many large scale programs are we going to write in jupyter?
# 
# We won't actually write large scale programs, per se, but we will write some long analyses.
