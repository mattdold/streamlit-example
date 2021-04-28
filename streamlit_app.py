"""

Inputting 2010 & Skyscrapers yields best results :)
http://localhost:8501/





Matt Dold - Section 5
This code runs streamlit and allows a user to select a year, as well as type of building
The data is then visualized on the map and in a bar chart, as well as listed below by the parameters

Some key highlights
1. I added emojis to the title
2. I changed the color of the Scatterpoints on the map
3. I added a dataframe showing highlights of inputted user data

"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk

def read_data(filename):
    df = pd.read_csv(filename)
    lst = []

    columns = ["Name", "Year", "Type", "Feet", "Country", "City", "Lon", "Lat"]

    for index, row in df.iterrows():
        sub = []
        for col in columns:
            index_no = df.columns.get_loc(col)
            sub.append(row[index_no])
        lst.append(sub)
    return lst

print(read_data("skyscrapers.csv"))

def type_list(data):
    types = []

    for i in range(len(data)):
        if data[i][2] not in types:
            types.append(data[i][2])

    return types

print(type_list(read_data("skyscrapers.csv")))

def freq_data(data, types, year):
    freq_dict = {}

    for type in types:
        freq = 0
        for i in range(len(data)):
            if data[i][2] == type and year == data[i][1]:
                freq += 1

        freq_dict[type] = freq

    return freq_dict

#print(freq_data(read_data("skyscrapers.csv"),type_list(read_data("skyscrapers.csv")), 2010 ))

def bar_chart(freq_dict):
    x = freq_dict.keys()
    y = freq_dict.values()

    plt.bar(x,y, color="pink")
    plt.xticks(rotation = 45)
    plt.xlabel("Building Type")
    plt.ylabel("Frequency of type")

    title = "Number of"
    for key in freq_dict.keys():
        title += " " + key + "s"
    plt.title(title)

    return plt

def display_map(data, types, year):
    loc = []
    for i in range(len(data)):
        if data[i][2] in types and year == data[i][1]:
            loc.append([data[i][0], data[i][7], data[i][6]])

    map_df = pd.DataFrame(loc, columns = ["Type", "Lat", "Lon"])
    #print(map_df)

    view_state = pdk.ViewState(latitude=map_df["Lat"].mean(), longitude=map_df["Lon"].mean(), zoom=0, pitch=0, radius_scale=1,)

    layer = pdk.Layer("ScatterplotLayer", data = map_df, get_position= "[Lon, Lat]", get_radius=100000, get_color=[253, 128, 93], pickable=True )
    tool_tip = {"html": "<br>Name:<br/>{Type}", "style": {"backgroundColor": "black", "color": "white"}}

    map = pdk.Deck(map_style="mapbox://styles/mapbox/light-v9", initial_view_state=view_state, layers=[layer], tooltip=tool_tip)

    st.pydeck_chart(map)

def main():
    data = read_data("skyscrapers.csv")

    st.title("🏰 Buildings Web Application 🏗️") # I think this is cool that I added emojis into Python code!!
    st.write("Welcome")
    year = st.sidebar.number_input("Enter a year", format="%0f")
    types = st.sidebar.multiselect("Select a Type of Building", type_list(data))


   # yearset = st.sidebar.slider("Select a year", 1967, 2020, 1)

    if len(types) > 0:
        st.write("Map of skyscrapers:")
        display_map(data, types, year)
        st.write("Some More Info:")
        df = pd.DataFrame(data, columns= ["Name", "Year", "Type", "Feet", "Country", "City", "Lat", "Lon"])
        df = df[df["Year"] == year]
        df = df[df["Type"].isin(types)]
        st.dataframe(df)   #This was difficult for me to build this dataframe returning info that user selects
        st.write("\nCount of Buildings")
        st.pyplot(bar_chart(freq_data(data, types, year)))

main()
