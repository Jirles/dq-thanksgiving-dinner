
# coding: utf-8

# In[1]:


import pandas as pd

data = pd.read_csv("thanksgiving.csv",encoding="Latin-1")
data[:3]


# In[3]:


columns_index = pd.Series(data.columns)
print(columns_index)


# In[4]:


data["Do you celebrate Thanksgiving?"].value_counts()


# In[6]:


data = data[data["Do you celebrate Thanksgiving?"]=="Yes"]


# In[7]:


data["Do you celebrate Thanksgiving?"].value_counts()


# In[8]:


data["What is typically the main dish at your Thanksgiving dinner?"].value_counts()


# In[9]:


tofurkey_eaters = data[data["What is typically the main dish at your Thanksgiving dinner?"]=="Tofurkey"]


# In[10]:


tofurkey_eaters["Do you typically have gravy?"]


# In[11]:


apple_isnull = data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Apple"].isnull()


# In[12]:


pumpkin_isnull = data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pumpkin"].isnull()

pecan_isnull = data["Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pecan"].isnull()


# In[25]:


ate_pies = apple_isnull & pumpkin_isnull & pecan_isnull


# In[28]:


ate_pies.value_counts()


# In[75]:


def convert_age_range(age_value):
    if pd.isnull(age_value):
        return None
    first_char = age_value.split()[0]
    first_char = first_char.replace('+', '')
    return int(first_char)


# In[76]:


int_data = data["Age"].apply(convert_age_range)


# In[77]:


int_data.describe()


# ## Age Breakdown
# 
# Above is a summary of the `int_data`, which only contains only the first number included in the original `Age` column in `data`. `Age` was recorded as age ranges. As such, the only values included in `int_data`, excluding null values, are `18` (`18-29`), `30` (`30-44`), `45` (`45-59`), and `60` (`60+`). So, the `pd.series.describe()` data above is not that helpful with regards to discerning Thanksgiving trends among certain age cohorts. 
# 
# It would be better to create 4 separate dataframes that had all rows where the `Age` column was equal to one age range. Then one can compare those for information on Thanksgiving dinner.

# In[84]:


def convert_income_range(income_value):
    if pd.isnull(income_value) or income_value == 'Prefer not to answer':
        return None
    first_char = income_value.split()[0]
    first_char = first_char.replace('$', '').replace(',', '')
    return int(first_char)


# In[85]:


int_income = data["How much total combined money did all members of your HOUSEHOLD earn last year?"].apply(convert_income_range)


# In[86]:


data['int_data'] = int_data
data['int_income'] = int_income


# In[87]:


data['int_income'].describe()


# ## Income breakdown
# 
# Converting and describing the income column in `data` was very similar ~identical~ to converting and describing the `Age` data. As such, `int_income`'s summary statistics suffer from the same problems that `int_data` does. Again, the data was originally collected as income ranges, but unlike `Age`, the income columns' ranges were not uniform. For example, the first explicit range, `0 to 9,999`, encompassed a step of 10,000. However, the second income group, `10,000 to 24,999`, was a step of 15,000. Every income group thereafter, with the exception of highest (`200,000 and up`), stepped up by 25,000. This might be why the `std` (standard deviation: `59068.636748`) is not equal to the range as it was for `int_data`.
# 
# I still don't think this is a true depiction of survey participants' incomes (or even the ranges they fall into). But it is better than the `Age` data. Based on the quartile information, we can see that most participants were grouped around the `75,000 to 99,000` range. Apply the standard deviation (which should encompass a little over 68% of survey participants if our data fits a bell curve), and most participants should fall within that range, +/- 60,000.
# 

# In[90]:


less_than_150k = data[data['int_income'] < 150000]


# In[91]:


less_than_150k['How far will you travel for Thanksgiving?'].value_counts()


# In[92]:


more_than_150k = data[data['int_income'] > 150000]
more_than_150k['How far will you travel for Thanksgiving?'].value_counts()


# ## Travel by Income Breakdown
# 
# DQ's assumption that people with less income would be more likely to travel farther for Thanksgiving was correct. Although I question their decision to split the incomes at 150k. I would have tried to split it between 5 figures and 6.
# 
# Still, those households with over 150k were split in about half between travelling and staying at home. For those households that make less than 150k, well over half travel for Thanksgiving.

# In[2]:


import pandas as pd

data = pd.read_csv("thanksgiving.csv",encoding="Latin-1")


# In[3]:


def convert_age_range(age_value):
    if pd.isnull(age_value):
        return None
    first_char = age_value.split()[0]
    first_char = first_char.replace('+', '')
    return int(first_char)

int_age = data["Age"].apply(convert_age_range)
data['int_age'] = int_age
friends_pt = data.pivot_table(index='Have you ever tried to meet up with hometown friends on Thanksgiving night?', columns='Have you ever attended a "Friendsgiving?"',values='int_age')


# In[5]:


friends_pt


# In[6]:


def convert_income_range(income_value):
    if pd.isnull(income_value) or income_value == 'Prefer not to answer':
        return None
    first_char = income_value.split()[0]
    first_char = first_char.replace('$', '').replace(',', '')
    return int(first_char)

int_income = data["How much total combined money did all members of your HOUSEHOLD earn last year?"].apply(convert_income_range)
data['int_income'] = int_income
friends_pt_income = data.pivot_table(index='Have you ever tried to meet up with hometown friends on Thanksgiving night?', columns='Have you ever attended a "Friendsgiving?"',values='int_income')


# In[7]:


friends_pt_income


# ## Friendsgiving Breakdown
# 
# These questions are definitely aimed at the young. Millienials, probably. The lowest averages in age and income occur when a participant replied `Yes` to both questions `Have you ever tried to meet up with hometown friends on Thanksgiving night?` and `Have you ever attended a "Friendsgiving?"`. The inverse is also true, the highest income and age averages occured when participants replied `No` to both questions.

# ## Links of interest
# 
# - Original [dataset](https://github.com/fivethirtyeight/data/tree/master/thanksgiving-2015) from [FiveThirtyEight](http://fivethirtyeight.com/).
# 
# - Dataquest solutions [notebook](https://github.com/dataquestio/solutions/blob/master/Mission219Solution.ipynb).
