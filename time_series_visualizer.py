import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

df = pd.read_csv('fcc-forum-pageviews.csv', sep=',', header='infer',
                 index_col='date', parse_dates=True, date_format="%Y-%m-%d")

n = round((2.5 / 100) * df.shape[0])
df_nlargest = df.nlargest(n, columns='value', keep='all')
df_nsmallest = df.nsmallest(n, columns='value', keep='all')
df = df[(df['value'] < df_nlargest['value'].iloc[df_nlargest.shape[0] - 1])
        & (df['value'] > df_nsmallest['value'].iloc[df_nsmallest.shape[0] - 1])]


def draw_line_plot():

    fig, ax = plt.subplots(figsize=(18, 5.5))
    ax.plot(df, color='#B9490D', label=None)

    ax.set_title(
        'Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize=14)
    ax.set_xlabel('Date', fontsize=11)
    ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(),
                  rotation='horizontal', fontsize=11)
    ax.set_ylabel('Page Views', fontsize=11)
    ax.set_yticks(ax.get_yticks(), ax.get_yticklabels(),
                  rotation='horizontal', fontsize=11)
    ax.set_ylim(ymin=10000, ymax=185000)

    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    df_bar = df.copy()

    df_bar = df_bar.groupby(by=df_bar.index.strftime("%Y-%m")).mean()
    df_bar.index = pd.to_datetime(
        df_bar.index, format="%Y-%m").strftime('%Y-%m').astype('datetime64[ns]')

    average_per_month = pd.DataFrame()

    for idx, value in df_bar['value'].items():
        year = idx.year
        month = idx.month

        average_per_month.at[year, month] = value

    average_per_month = average_per_month[sorted(average_per_month.columns)]

    average_per_month.rename(columns={
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }, inplace=True)

    fig, ax = plt.subplots(figsize=(10, 10))

    average_per_month.plot(kind='bar', ax=ax)

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.set_xticks(range(len(average_per_month.index)))
    ax.set_xticklabels(average_per_month.index, rotation=90)

    ax.legend(title="Months", loc='upper left')

    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    fig, ax = plt.subplots(1, 2, figsize=(25.8, 10.8))

    sns.boxplot(x=df_box['year'], y=df_box['value'], hue=df_box['year'], ax=ax[0],
                palette=sns.color_palette(n_colors=df_box['year'].value_counts().shape[0]), legend=False,
                flierprops={"marker": "d",
                            "markersize": "4",
                            "markerfacecolor": "black"})

    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")
    ax[0].set_yticks([x for x in range(0, 200001, 20000)])

    sns.boxplot(x=df_box['month'], y=df_box['value'], hue=df_box['month'],
                order=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], ax=ax[1],
                palette=sns.color_palette("Set2", n_colors=df_box['month'].value_counts().shape[0]), legend=False,
                flierprops={"marker": "d",
                            "markersize": "4",
                            "markerfacecolor": "black"})

    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")
    ax[1].set_yticks([x for x in range(0, 200001, 20000)])

    fig.savefig('box_plot.png')
    return fig

