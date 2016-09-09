# up_in_time
It is a django-powered web app which can create reminders or alarms just by a single click.

## Installation
* Just clone the git repo.
* OPen the terminal and cd into the folder 
* Run ```./manage.py runserver```
* Visit [here](http://127.0.0.1:8000/alarm/) (If you haven't changed the default port - 8000)

##Strategy:
* When user opens the home page - the index.html it is handled by alarm view that creates a database entry with mapping of id to alarm_time,thus making a POST request and then redirects to success.html
* Now, success.html is mapped to create_alarm view and in turn it checks for the alarm_time written for the current IP address and it then displays the current time on the page and at the same time javascript can check for the alarm time and we can play the music.

##Still To-Do:

* Correct the way it gives error report.
* Add a placeholder on time input so the user knows the format.
* Give user the choice for entering in either the 24 hr system or 12 hr system.
* ~~Do something with the timezone, it is getting really getting conusing.~~
* Obviously, give it some *better* looks.
* ~~Add a level of validation for IP and time.~~
* Add an alert message when user tries to close the alarm tab, perhaps a modal popup.
* Add a message input and display it on tha alarm screen for reminding purposes.
* optimize the code - Use django's template system
* Design GUI and choose colors.
* ~~Embed music in pop up so that there is actually an alarm~~
* ~~Seperate the Javascript and HTML in pop-up.~~
* Add customization to alarm screen.
* ~~Make and add a favicon~~
* Add contact us, about_us page.
	
### Far away:
* Add functionality like sending automatic emails and messages(look up twillio) at the given time.
* Make the website responsive.
* Add the facility for the users to add custom Youtube videos or uploaded Audios or audio links to be served as alarm.

## Dependencies

* python
* django v1.9.8
* Make sure that pop ups are allowed in your browser.

