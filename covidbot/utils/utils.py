import os
import base64
import json
import requests
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
sns.set(style="whitegrid")

def create_covid_distribution_plot():
    df = pd.read_csv(
        "https://api.covid19india.org/csv/latest/state_wise.csv").sort_values("Confirmed", ascending=False)
    df.drop([0, 36], inplace=True)

    # Initialize the matplotlib figure
    _, ax = plt.subplots(figsize=(15, 20))

    sns.barplot(x="Confirmed", y="State", data=df,
                label="Confirmed", color="blue")

    sns.barplot(x="Recovered", y="State", data=df,
                label="Recovered", color="green")

    sns.barplot(x="Active", y="State", data=df,
                label="Active", color="red")

    sns.barplot(x="Deaths", y="State", data=df,
                label="Deaths", color="black")

    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(ylabel="", xlabel="Covid-19 Cases Distribution")
    plt.xticks(np.arange(min(df['Confirmed']), max(df['Confirmed'])+1, 500000))
    plt.ticklabel_format(style='plain', axis='x')
    sns.despine(left=True, bottom=True)

    script_dir = os.path.dirname(__file__)
    img_dir = os.path.join(script_dir, 'images/')
    file_name = "covid_cases_distribution.png"

    if not os.path.isdir(img_dir):
        os.makedirs(img_dir)

    final_path = img_dir + file_name

    plt.savefig(final_path, bbox_inches='tight')

    return final_path


def create_covid_map_plot():
    fp = "IND_adm1.shp"
    map_df = gpd.read_file(fp)

    states_df = pd.read_csv(
        "https://api.covid19india.org/csv/latest/state_wise.csv").sort_values("Confirmed", ascending=False)
    states_df.drop([0, 36], inplace=True)
    states_df.sort_values(by=['State'], inplace=True)
    states_df.reset_index(inplace=True)
    states_df.drop(columns=['index'], inplace=True)
    map_df['State'] = states_df['State']
    map_df['Active'] = states_df['Active']

    # set the value column that will be visualised
    variable = 'Active'
    # set the range for the choropleth values
    vmin, vmax = min(map_df['Active']), max(map_df['Active'])
    # create figure and axes for Matplotlib
    fig, ax = plt.subplots(1, figsize=(10, 10))
    # remove the axis
    ax.axis('off')
    # add a title
    ax.set_title('# of Active Cases per State', fontdict={
                 'fontsize': '15', 'fontweight': '1'})
    sm = plt.cm.ScalarMappable(
        cmap='Oranges', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    # empty array for the data range
    sm.set_array([])
    # add the colorbar to the figure
    fig.colorbar(sm, fraction=0.046, pad=0.04)
    # create map
    map_df.plot(variable, cmap='Oranges',
                linewidth=0.8, ax=ax, edgecolor='0.8')

    script_dir = os.path.dirname(__file__)
    img_dir = os.path.join(script_dir, 'images/')
    file_name = "covid_cases_map.png"

    if not os.path.isdir(img_dir):
        os.makedirs(img_dir)

    final_path = img_dir + file_name

    plt.savefig(final_path, bboxes_inches='tight')

    return final_path


def upload_to_imgur(local_img_path):
    f = open(local_img_path, "rb")
    image_data = f.read()
    b64_image = base64.standard_b64encode(image_data)

    client_id = "5220f1a25616ff4"  # put your client ID here
    headers = {'Authorization': 'Client-ID ' + client_id}

    data = {'image': b64_image, 'title': 'test'}

    response = requests.put(
        url="https://api.imgur.com/3/upload.json", data=data, headers=headers).json()

    return response['data']['link']
