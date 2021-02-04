import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'],index_col='date')

# Clean data
df = df.drop(df[(df['value'] < df['value'].quantile(0.025)) | (df['value'] > df['value'].quantile(0.975))].index)


def draw_line_plot():
    # Draw line plot
    yr_mo_fmt = mdates.DateFormatter('%Y-%m')
    fig, ax = plt.subplots(figsize=(19,6))
    ax.plot(df, color='crimson')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.xaxis.set_major_locator(mdates.MonthLocator([1,7]))
    ax.xaxis.set_major_formatter(yr_mo_fmt)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.resample('M').mean()
    df_bar = df_bar.reset_index()
    df_bar['date'] = df_bar['date'].apply(lambda x: x.strftime('%Y-%m'))
    df_bar.set_index('date', inplace=True)
    
    months = np.array(['January','February','March','April','May','June',
                        'July','August','September', 'October','November','December'])
    df_bar = df.copy()
    df_bar['year'] = df.index.year
    df_bar['Months'] = df.index.month
    df_bar = df_bar.rename(columns={'value':'page views'})

    df_bar = pd.pivot_table(
      df_bar,
      values='page views',
      index='year',
      columns='Months',
      aggfunc=np.mean
    )

    month_map = {i+1:month for i, month in enumerate(months)}
    df_bar = df_bar.rename(columns=month_map)

    # Draw bar plot
    ax = df_bar.plot(kind = 'bar')
    fig = ax.get_figure()
    fig.set_size_inches(8,7)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    fig, axs = plt.subplots(1,2, figsize=(28,10))
    sns.boxplot(x='year', y='value',data=df_box, ax = axs[0])
    axs[0].set_title('Year-wise Box Plot (Trend)')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')
    sns.boxplot(x='month', y='value',data=df_box, ax = axs[1], order=months)
    axs[1].set_title('Month-wise Box Plot (Seasonality)')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
