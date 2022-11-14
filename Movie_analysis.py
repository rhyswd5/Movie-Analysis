#import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn')

# read movie data
movie_data = pd.read_csv('../data/imdb_top_1000.csv')

# inspect data for any errors or null values
movie_data.head()
movie_data.info()

# remove rows with null Gross values and format Gross column to change to integers
movie_data = movie_data[movie_data['Gross'].notna()]
movie_data['Gross'] = movie_data['Gross'].str.replace(',', '').astype(int)

# join all 4 Star columns with their revenue value using concat then
# calculate the average revenue for each actor

Star1 = movie_data[['Gross', 'Star1']]
Star2 = movie_data[['Gross', 'Star2']]
Star3 = movie_data[['Gross', 'Star3']]
Star4 = movie_data[['Gross', 'Star4']]

Star1.columns = ['Avg_revenue', 'Stars']
Star2.columns = ['Avg_revenue', 'Stars']
Star3.columns = ['Avg_revenue', 'Stars']
Star4.columns = ['Avg_revenue', 'Stars']

Stars_gross = pd.concat([Star1, Star2, Star3, Star4], ignore_index=True)
Stars_grossdf = pd.DataFrame(Stars_gross.groupby('Stars')['Avg_revenue'].mean())
Stars_grossdf = Stars_grossdf.reset_index(level=0)

# each value for genre column contains upto 4 genres so needed to split each string at the comma
# and create a new row
Genre_grossdf = pd.concat([movie_data['Genre'],movie_data['Gross']], axis=1)
lst_col = 'Genre' 
x = Genre_grossdf.assign(**{lst_col:Genre_grossdf[lst_col].str.split(',')})
Genre_grossdf = pd.DataFrame({
    col:np.repeat(x[col].values, x[lst_col].str.len())
    for col in x.columns.difference([lst_col])
    }).assign(**{lst_col:np.concatenate(x[lst_col].values)})[x.columns.tolist()]

Genre_grossdf['Genre'] = Genre_grossdf['Genre'].map(lambda x: x.lstrip(' ').rstrip(''))
Genre_grossdf = pd.DataFrame(Genre_grossdf.groupby('Genre')['Gross'].mean())
Genre_grossdf = Genre_grossdf.reset_index(level=0)
Genre_grossdf.rename(columns={'Gross':'Avg_revenue'}, inplace=True)

# group by director and calculate mean gross for each director
Director_gross = movie_data.groupby('Director')['Gross'].mean()
Director_grossdf = pd.DataFrame({'Director':Director_gross.index, 'Avg_revenue':Director_gross.values})

# limiting each set of values to the top ten results
Director_grossdf_top_10 = Director_grossdf.sort_values(by = 'Avg_revenue', ascending=False).head(10)
Stars_grossdf_top_10 = Stars_grossdf.sort_values(by = 'Avg_revenue', ascending=False).head(10)
Genre_grossdf_top_10 = Genre_grossdf.sort_values(by = 'Avg_revenue', ascending=False).head(10)

# plotting each set of values on its own horizontal bar chart
fig, ax = plt.subplots(2, 2)

ax[0, 0].axis('off')
ax[0, 0].text(0.3, 0.5, 'Testing how different\nfactors effect a movies\nrevenue', horizontalalignment='center',
        verticalalignment='center', fontsize=20, color = '#333333')

ax[0, 1].barh(Director_grossdf_top_10['Director'], Director_grossdf_top_10['Avg_revenue']/1e6)
ax[0, 1].set_title('Average Revenue by Director')
ax[0, 1].set_xlabel('Average revenue ($1M)')
ax[0, 1].set_ylabel('Director')

ax[1, 0].barh(Stars_grossdf_top_10['Stars'], Stars_grossdf_top_10['Avg_revenue']/1e6) 
ax[1, 0].set_title('Average Revenue by Actor')
ax[1, 0].set_xlabel('Average revenue ($1M)')
ax[1, 0].set_ylabel('Actor')

ax[1, 1].barh(Genre_grossdf_top_10['Genre'], Genre_grossdf_top_10['Avg_revenue']/1e6)
ax[1, 1].set_title('Average Revenue by Genre')
ax[1, 1].set_xlabel('Average revenue ($1M)')
ax[1, 1].set_ylabel('Genre')

plt.tight_layout()
plt.show()
