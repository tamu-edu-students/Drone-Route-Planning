# Drone Route Planning

> A web app for planning routes using polygon bounds on a map to generate kml files.
> Note: App currently not deployed, running locally is only option for use.

|               | Drone Route Planner             |
|---------------|---------------------------------|
| Organization: | Texas A&M University            |
| Sponsor:      | Dr. Robin Murphy                |
| Dev Team:     | [See the Team](#dev-team)       |


### Installation
##### Requirements
- [python](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)
- [git](https://git-scm.com/downloads)

##### Running Locally
- ```git clone git@github.com:tamu-edu-students/Drone-Route-Planning.git```
 or
- ```git clone https://github.com/tamu-edu-students/Drone-Route-Planning.git```
- ```cd Drone-Route-Planning```
- ```pip install -r requirements.txt```
- ```python main.py```
- visit ```localhost:5000``` in your browser

### Using the app

##### Main Screen
Map will attempt to use users location, if not found will center on TAMU's campus.

###### Buttons
- Draw Bounding Box
  - Allows you to draw box around area you want to extract the route from
- Extract Route
  - Active after bounding box is drawn, will use the roads bounded by the box to construct a route.

##### Route Render Screen
Map will focus the point from the bounding box and draw the route on the map

###### Buttons
- Draw Again
  - Takes you back to the main screen
- Download
  - Takes the rendered route and extracts the nodes to create a kml file based on the gps coordinates
  - Prompts user to enter desired file name before downloading as kml


### Dev Team

- [Dalton Avery](https://github.com/dalton-avery) - dalton.avery@tamu.edu
- [Jubey Garza](https://github.com/gJubey) - jubey.s.garza@tamu.edu
- [Yu-Hsi (Alvin) Lin](https://github.com/yxl3784) - yxl0899@tamu.edu