# up_in_time
It is a django-powered web app which can create reminders or alarms just by a single click.

![ScreenShot](https://raw.github.com/RJ722/up_in_time/master/static/screenshots/overview.png)

## Installation
* Make sure you have Python installed (if possible, use 2.x so that you wouldn't have to alter print statements written here and there)
* Start a new virtual enviroment for this project.
* Install required python libraries giving in the requirements.txt file
    ```
    pip install -r requirements.txt
    ```
* Start the develpoment server by running ```./manage.py runserver```
* Visit [here](http://127.0.0.1:8000/alarm/) (If you haven't changed the default port - 8000)

##Strategy:
* When user opens the home page - the index.html it is handled by alarm view that creates a database entry with mapping of id to alarm_time,thus making a POST request and then redirects to success.html
* Now, success.html is mapped to create_alarm view and in turn it checks for the alarm_time written for the current IP address and it then displays the current time on the page and at the same time javascript can check for the alarm time and we can play the music.

##Still To-Do:

* ~~Do something with the timezone, it is getting really getting conusing.~~
* ~~Add a level of validation for IP and time.~~
* Add an alert message when user tries to close the alarm tab.
* ~~Add a message input and display it on tha alarm screen for reminding purposes.~~
* Embed music in pop up so that there is actually an alarm
* ~~Seperate the Javascript and HTML in pop-up.~~
* ~~Make and add a favicon~~
* Add contact us, about_us page.
	
## What can be possible potential?
* Add the facility for the users to add custom Youtube videos or uploaded Audios or audio links to be served as alarm.
* Add functionality like sending automatic emails and messages(look up twillio) at the given time.
* A simple browser plugin from where user can set an alarm without even leaving window.
* Sync across all devices - still don't have any ideas HOW - would love to listen to :) - (HEAD IN THE CLOUD AND FEET ON THE FLOOR) 
* Setting an alarm for others - requires highly secure enviroment
