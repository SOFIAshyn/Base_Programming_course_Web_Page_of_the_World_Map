import pandas
import re
import folium
import webbrowser
from geopy.geocoders import Bing
import numpy as np
import folium.plugins as plugins
import datetime


def check_point_name(point):
    """
    (str) -> str

    Returns name of location without bugs

    >>> check_point_name('{{SUSPENDED}}New Orleans Louisiana USA')
    'New Orleans Louisiana USA'

    >>> check_point_name('New Orleans Louisiana USA')
    'New Orleans Louisiana USA'
    """
    if "}}" in point:
        return point.split("}}")[1]
    else:
        return point


def add_markers(dictionary):
    """
    (dict) -> class 'folium.map.FeatureGroup'

    Returns loactions to add it to the map
    """
    fg = folium.FeatureGroup(name='Locations with names')
    for key in dictionary:
        points = dictionary[key]
        if fg:
            fg.add_child(
                folium.Marker(location=[points[0], points[1]], popup=key,
                              icon=folium.Icon()))
    return fg


def add_boundaries():
    """
    (None) -> class 'folium.map.FeatureGroup'

    Returns population mask to add it to the map
    """
    population_mask = folium.FeatureGroup(name="Population")
    population_mask.add_child(
        folium.GeoJson(data=open('./docs/world.json', 'r',
                                 encoding='utf-8-sig').read(),
                       style_function=lambda x: {'fillColor': '#EE2376'  # pink
                       if x['properties']['POP2005'] < 100000
                       else '#81DC1A' if 100000 <= x['properties'][
                           'POP2005'] < 200000  # green
                       else '#B6E80E' if 200000 <= x['properties'][
                           'POP2005'] < 1000000  # light green
                       else '#5503E5' if 1000000 <= x['properties'][
                           'POP2005'] < 2000000  # purple
                       else '#E57703' if 2000000 <= x['properties'][
                           'POP2005'] < 9000000  # orange
                       else '#0EE896' if 9000000 <= x['properties'][
                           'POP2005'] < 15000000  # blue
                       else '#E112B5' if 15000000 <= x['properties'][
                           'POP2005'] < 20000000  # pink
                       else '#3882EC'}))  # dark blue
    return population_mask


def add_clusters(dictionary):
    """
    (dict) -> class 'folium.map.FeatureGroup'

    Returns clusters to add it to the map
    """
    clusters = folium.FeatureGroup(name="Clusters by the area")
    first_loc = []
    second_loc = []
    for key in dictionary:
        points = dictionary[key]
        first_loc.append(points[0])
        second_loc.append(points[1])
    data = np.array(
        [
            np.array(first_loc),
            np.array(second_loc),
            range(len(dictionary))
        ]
    ).T
    plugins.MarkerCluster(data).add_to(clusters)
    return clusters


def create_map(dictionary):
    """
    (None) -> None

    Create a map with folium in HTML file
    Add: map, locations, clusters, population colour, mini map, layer control
    """
    map = folium.Map([45, 3], zoom_start=2)
    # ADD MARKERS
    fg = add_markers(dictionary)
    # ADD BOUNDARIES
    population_mask = add_boundaries()
    # ADD CLASTERS
    clusters = add_clusters(dictionary)
    # MINI MAP
    minimap = plugins.MiniMap()
    # ADD ALL CHILDS
    map.add_child(fg)
    map.add_child(population_mask)
    map.add_child(clusters)
    map.add_child(minimap)
    # to tick/untick the whole group put things
    # in LC and handle them as a single layer
    map.add_child(folium.LayerControl())
    map.save('./docs/index.html')
    webbrowser.open("./docs/index.html")


def convert_to_coordinates(dictionary):
    """
    (None) -> None

    Connects with API and returns dictionary with coordinates
    dictionary: name - coordinates in tuple

    >>> convert_to_coordinates({'Betrayal': 'New Orleans Louisiana USA'})
    {'Betrayal': (29.9536991119385, -90.077751159668)}
    """
    geolocator = Bing(
        "AomOhTUAKsV-5fu4bzeuBtVlx5VeMi_M86P4gODXuCd6f7S2dquidP7Aj2xtDoS0")
    dict_coordinates = {}
    for key in dictionary:
        point = dictionary[key]
        try:
            address, (latitude, longitude) = geolocator.geocode(point)
            dict_coordinates[key] = (latitude, longitude)
        except TypeError:
            continue
    return dict_coordinates


def create_year_dict(data_set, year):
    """
    (set, str) -> dict

    Creates dictionary of the films of year that we need
    dictionary: name - location
    """
    dict_films = {}
    for el in data_set:
        each_year = re.findall('\d\d\d\d', el[1])
        if each_year != [] and each_year[0] == year:
            if el[0] not in dict_films:
                dict_films[el[0]] = el[2]
    return dict_films


def check_no_data(lst):
    """
    (lst) -> bool

    Checks if every element of lst is readable

    >>> check_no_data(["NO DATA", "2016", "Santa Clarita California USA"])
    False
    >>> check_no_data(["Betrayal", "2016", "Santa Clarita California USA"])
    True
    """
    for el in lst:
        if type(el) == str and "NO DATA" in el:
            return False
    return True


def read_file(path):
    """
    (str) -> set

    Returns set of filtered and combined data -
    name of movie, year, location
    """
    data = pandas.read_csv(path, error_bad_lines=False)
    films = data["movie"]
    date = data["year"]
    locations = data["location"]
    data_set = set(zip(films, date, locations))
    data_set = set(
        filter(lambda sublst: check_no_data(sublst), data_set))
    return data_set


def user_interface():
    """
    (None) -> int

    Returns user input - year for searching
    """
    while True:
        year = input("Enter the year: ")
        if year.isdigit() and len(year) == 4:
            year_today = datetime.date.today().year
            if int(year) <= year_today:
                return year


def main():
    """
    (None) -> None

    Runs program functions
    """
    year = user_interface()
    data_set = read_file('./docs/locations.csv')
    film_places = create_year_dict(data_set, year)
    film_coord = convert_to_coordinates(film_places)
    create_map(film_coord)


if __name__ == "__main__":
    main()
    # import doctest
    #
    # print(doctest.testmod())
