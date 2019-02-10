
# World_map
###### The main aim
The application visualizes all the locations of the year you want on the world map.
## Appearance of the site
To show you how `index.html` looks you can follow this path `./examples` and you will see some pictures of the wed page.
## What map shows?
1. The world map
2. Colourful countries due to the number of th epopulation
3. Locations of each film of the chosen year with the names
4. Clusters with number of films
5. Small map to navigate
6. Layer controller
## Installation
To run world_map you have to have all libraries that are used in this project.
So run this line in your cmd: 
```
sudo pip install -r requirements.txt
```
## Usage
To start the application you have to have installed python 3+ version
```
python3 app.py
```
After that you will have a field:
```
Enter the year: <year>
```
You have to enter the year. After that you have to wait a littele bit.
If the browser will not be opened you have to open `./docs/index.html` with your browser.
## Possible errors
You can meet `geopy.exc.GeocoderQuotaExceeded: HTTP Error 429: Too Many Requests` or `geopy.exc.GeocoderTimedOut: Service timed out` problems. My advice change the wifi network or use VPN.
## Description of the HTML file
The main file that is in `./docs`

`<!DOCTYPE html>` - to define that the type of file is`HTML5`.

`<head>` - a tag to post inside the most important information

`<meta>` - a tag for metadata

`<script>` - a tag to hook the scripts to the HTML file

`<link>` - a tag to connect CSS files to the HTML file

`<style>` - to write CSS code inside HTML file

`<body>` - a tag that contain all the information that have to be on the web page

`<div>` - a tag that doing like a block that can have different styles and tags inside

`<script>` - a tag to write a JS code inside HTML file

## Conclusion
The program shows us a map with the locations where the films of the chosen year were filmed. 
Also you can make an investigation of the information:
 - where the majority of the films were filmed
 - which year was the most productive
 - which locations are the most popular
 - tend of the names and the locations
 
I hope this simple web page will be usefull for you. Wish you luck!
