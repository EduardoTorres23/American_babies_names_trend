#!/usr/bin/env python
# coding: utf-8

# ## 1. Classic American names
# <p><img src="https://assets.datacamp.com/production/project_1441/img/name.jpg" alt="Lots of name tags piled on top of each other." width="600"></p>
# <p>Photo by Travis Wise on <a href="https://commons.wikimedia.org/wiki/File:Hello_My_Name_Is_(15283079263).jpg">Wikimedia</a>.</p>
# <p>How have American baby name tastes changed since 1920?  Which names have remained popular for over 100 years, and how do those names compare to more recent top baby names? These are considerations for many new parents, but the skills we'll practice while answering these queries are broadly applicable. After all, understanding trends and popularity is important for many businesses, too! </p>
# <p>We'll be working with data provided by the United States Social Security Administration, which lists first names along with the number and sex of babies they were given to in each year. For processing speed purposes, we've limited the dataset to first names which were given to over 5,000 American babies in a given year. Our data spans 101 years, from 1920 through 2020.</p>
# <h3 id="baby_names"><code>baby_names</code></h3>
# <table>
# <thead>
# <tr>
# <th style="text-align:left;">column</th>
# <th>type</th>
# <th>meaning</th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td style="text-align:left;"><code>year</code></td>
# <td>int</td>
# <td>year</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>first_name</code></td>
# <td>varchar</td>
# <td>first name</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>sex</code></td>
# <td>varchar</td>
# <td><code>sex</code> of babies given <code>first_name</code></td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>num</code></td>
# <td>int</td>
# <td>number of babies of <code>sex</code> given <code>first_name</code> in that <code>year</code></td>
# </tr>
# </tbody>
# </table>
# <p>Let's get oriented to American baby name tastes by looking at the names that have stood the test of time!</p>

# In[24]:


get_ipython().run_cell_magic('sql', '', 'postgresql:///names\nSELECT first_name,SUM(num)\nFROM baby_names\nGROUP BY first_name\nHAVING COUNT(year) = 101\nORDER BY 2 DESC;')


# In[25]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (8, 2), \\\n    "The query should return eight rows and two columns."\n    assert results.columns.tolist() == ["first_name", "sum"], \\\n    \'The results should have two columns: "first_name" and "sum".\'\n    assert last_output.DataFrame().loc[0, \'first_name\'] == \'James\', \\\n    "The first_name in the first row should be James."\n    assert last_output.DataFrame().loc[0, \'sum\'] == 4748138, \\\n    "There should be 4,748,138 babies ever named James."')


# ## 2. Timeless or trendy?
# <p>Wow, it looks like there are a lot of timeless traditionally male names! Elizabeth is holding her own for the female names, too. </p>
# <p>Now, let's broaden our understanding of the dataset by looking at all names. We'll attempt to capture the type of popularity that each name in the dataset enjoyed. Was the name classic and popular across many years or trendy, only popular for a few years? Let's find out. </p>

# In[26]:


get_ipython().run_cell_magic('sql', '', "SELECT first_name,SUM(num),\nCASE\n    WHEN COUNT(first_name) > 80 THEN 'Classic'\n    WHEN COUNT(first_name) > 50 THEN 'Semi-classic'\n    WHEN COUNT(first_name) > 20 THEN 'Semi-trendy'\n    ELSE 'Trendy'\n    END AS popularity_type\nFROM baby_names\nGROUP BY first_name\nORDER BY first_name;")


# In[27]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (547, 3), \\\n    "The query should return 547 rows and three columns."\n    assert results.columns.tolist() == ["first_name", "sum", "popularity_type"], \\\n    \'The results should have three columns: "first_name", "sum", and "popularity_type".\'\n    assert last_output.DataFrame().loc[0, \'first_name\'] == \'Aaliyah\', \\\n    "The first_name in the first row should be Aaliyah. Did you sort first names alphabetically?"\n    assert last_output.DataFrame().loc[0, \'sum\'] == 15870, \\\n    "There should be 15,870 babies ever named Aaliyah."\n    assert last_output.DataFrame().loc[0, \'popularity_type\'] == "Trendy", \\\n    "The name Aaliyah should be classified as \'Trendy\'."')


# ## 3. Top-ranked female names since 1920
# <p>Did you find your favorite American celebrity's name on the popularity chart? Was it classic or trendy? How do you think the name Henry did? What about Jaxon?</p>
# <p>Since we didn't get many traditionally female names in our classic American names search in the first task, let's limit our search to names which were given to female babies. </p>
# <p>We can use this opportunity to practice window functions by assigning a rank to female names based on the number of babies that have ever been given that name. What are the top-ranked female names since 1920?</p>

# In[28]:


get_ipython().run_cell_magic('sql', '', "SELECT RANK () OVER (PARTITION BY first_name ORDER BY SUM(num) DESC)as name_rank,\nfirst_name,\nSUM(num)\nFROM baby_names\nWHERE sex = 'F'\nGROUP BY first_name\nORDER BY SUM(num) DESC\nLIMIT 10;")


# In[29]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (10, 3), \\\n    "The query should return ten rows and three columns."\n    assert set(results.columns.tolist()) == set(["first_name", "sum", "name_rank"]), \\\n    \'The results should have three columns: "name_rank", "first_name", and "sum".\'\n    assert last_output.DataFrame().loc[0, \'first_name\'] == \'Mary\', \\\n    "The first_name in the first row should be Mary. Did you order so that names given to the most babies come first?"\n    assert last_output.DataFrame().loc[0, \'sum\'] == 3215850, \\\n    "There should be 3,215,850 babies ever named Mary."\n    assert last_output.DataFrame().loc[0, \'name_rank\'] == 1, \\\n    "The name Mary should be ranked number one."')


# ## 4. Picking a baby name
# <p>Perhaps a friend has heard of our work analyzing baby names and would like help choosing a name for her baby, a girl. She doesn't like any of the top-ranked names we found in the previous task. </p>
# <p>She's set on a traditionally female name ending in the letter 'a' since she's heard that vowels in baby names are trendy. She's also looking for a name that has been popular in the years since 2015. </p>
# <p>Let's see what we can do to find some options for this friend!</p>

# In[30]:


get_ipython().run_cell_magic('sql', '', "SELECT first_name\nFROM baby_names\nWHERE sex LIKE 'F'\n    AND year > 2015\n    AND first_name LIKE '%a'\nGROUP BY first_name\nORDER BY SUM(num) DESC;")


# In[31]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (19, 1), \\\n    "The query should return 19 rows and one column."\n    assert results.columns.tolist() == ["first_name"], \\\n    \'The results should have one column: "first_name".\'\n    assert last_output.DataFrame().loc[0, \'first_name\'] == \'Olivia\', \\\n    "The first_name in the first row should be Olivia."')


# ## 5. The Olivia expansion
# <p>Based on the results in the previous task, we can see that Olivia is the most popular female name ending in 'A' since 2015. When did the name Olivia become so popular?</p>
# <p>Let's explore the rise of the name Olivia with the help of a window function.</p>

# In[32]:


get_ipython().run_cell_magic('sql', '', "SELECT year,first_name,num,\nSUM(num) OVER (ORDER BY year) as cumulative_olivias\nFROM baby_names\nWHERE first_name LIKE 'Olivia'\nORDER BY year;")


# %%sql

# In[33]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (30, 4), \\\n    "The query should return thirty rows and four columns."\n    assert set(results.columns.tolist()) == set(["year", "first_name", "num", "cumulative_olivias"]), \\\n    \'The results should have four columns: "year", "first_name", "num", and "cumulative_olivias".\'\n    assert last_output.DataFrame().loc[0, \'first_name\'] == \'Olivia\', \\\n    "The first_name in the first row should be Olivia. Did you filter so that results only include data for the name Olivia?"\n    assert last_output.DataFrame().loc[0, \'num\'] == 5601, \\\n    "In 1991, there should have been 5,601 female babies named Olivia."\n    assert last_output.DataFrame().loc[0, \'year\'] == 1991, \\\n    "1991 should be the first year that Olivia appears in the results. Did you sort by year in ascending order?"\n    assert last_output.DataFrame().loc[1, \'cumulative_olivias\'] == 11410, \\\n    "In 1992, the cumulative_olivias column should read 11,410."')


# ## 6. Many males with the same name
# <p>Wow, Olivia has had a meteoric rise! Let's take a look at traditionally male names now. We saw in the first task that there are nine traditionally male names given to at least 5,000 babies every single year in our 101-year dataset! Those names are classics, but showing up in the dataset every year doesn't necessarily mean that the timeless names were the most popular. Let's explore popular male names a little further.</p>
# <p>In the next two tasks, we will build up to listing every year along with the most popular male name in that year. This presents a common problem: how do we find the greatest X in a group? Or, in the context of this problem, how do we find the male name given to the highest number of babies in a year? </p>
# <p>In SQL, one approach is to use a subquery. We can first write a query that selects the <code>year</code> and the maximum <code>num</code> of babies given any single male name in that year. For example, in 1989, the male name given to the highest number of babies was given to 65,339 babies. We'll write this query in this task. In the next task, we can use the code from this task as a subquery to look up the <code>first_name</code> that was given to 65,339 babies in 1989… as well as the top male first name for all other years!</p>

# In[34]:


get_ipython().run_cell_magic('sql', '', "SELECT year,MAX(num) as max_num\nFROM baby_names\nWHERE sex LIKE 'M'\nGROUP BY year;")


# In[35]:


get_ipython().run_cell_magic('nose', '', 'import numpy as np\nlast_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (101, 2), \\\n    "The query should return 101 rows and two columns."\n    assert set(results.columns.tolist()) == set(["year", "max_num"]), \\\n    \'The results should have two columns: "year" and "max_num".\'\n    assert last_output.DataFrame().loc[list(np.where(last_output.DataFrame() == 1964)[0])[0], \'max_num\'] == 82642, \\\n    "In 1964, the name given to the most babies was given 82,642 times."')


# ## 7. Top male names over the years
# <p>In the previous task, we found the maximum number of babies given any one male name in each year. Incredibly, the most popular name each year varied from being given to less than 20,000 babies to being given to more than 90,000! </p>
# <p>In this task, we find out what that top male name is for each year in our dataset. </p>

# In[36]:


get_ipython().run_cell_magic('sql', '', "SELECT b.year, b.first_name, b.num\nFROM baby_names AS b\nINNER JOIN (\n    SELECT year, MAX(num) as max_num\n    FROM baby_names\n    WHERE sex = 'M'\n    GROUP BY year) AS max_baby_name \nON max_baby_name.year = b.year \n    AND max_baby_name.max_num = b.num\nORDER BY year DESC;")


# In[37]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (101, 3), \\\n    "The query should return 101 rows and three columns."\n    assert set(results.columns.tolist()) == set(["year", "first_name", "num"]), \\\n    \'The results should have three columns: "year", "first_name", and "num".\'\n    assert last_output.DataFrame().loc[0, \'year\'] == 2020, \\\n    "The first year should be 2020. Did you sort so that the most recent years appear first?"\n    assert last_output.DataFrame().loc[0, \'first_name\'] == "Liam", \\\n    "In 2020, the name given to the most male babies was Liam."\n    assert last_output.DataFrame().loc[0, \'num\'] == 19659, \\\n    "In 2020, the name Liam was given to 19,659 babies."')


# ## 8. The most years at number one
# <p>Noah and Liam have ruled the roost in the last few years, but if we scroll down in the results, it looks like Michael and Jacob have also spent a good number of years as the top name! Which name has been number one for the largest number of years? Let's use a common table expression to find out. </p>

# In[38]:


get_ipython().run_cell_magic('sql', '', "WITH top_baby_name AS (\n    SELECT b.year, b.first_name, b.num\nFROM baby_names AS b\nINNER JOIN (\n    SELECT year, MAX(num) as max_num\n    FROM baby_names\n    WHERE sex = 'M'\n    GROUP BY year) AS max_baby_name \nON max_baby_name.year = b.year \n    AND max_baby_name.max_num = b.num\nORDER BY year DESC\n)\nSELECT first_name,COUNT(first_name) as count_top_name\nFROM top_baby_name\nGROUP BY first_name\nORDER BY count_top_name DESC;")


# In[39]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (8, 2), \\\n    "The query should return eight rows and two columns."\n    assert set(results.columns.tolist()) == set(["first_name", "count_top_name"]), \\\n    \'The results should have two columns: "first_name" and "count_top_name".\'\n    assert last_output.DataFrame().loc[0, \'first_name\'] == \'Michael\', \\\n    "The name that spent most years at number one should be Michael. Did you order from most to fewest years at the top?"\n    assert last_output.DataFrame().loc[0, \'count_top_name\'] == 44, \\\n    "Michael was the number one male name 44 times. It doesn\'t look like your results reflect this."')

