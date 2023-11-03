# BNZ Calendar for Cycling Races
## Video Demo:  https://youtu.be/k-MZ4_URq_s
## Description:
Amateur cyclists can go (and usually go) to a lot of different amateur races. There are plenty of options out there, however, most of the times, there is one website for each race, a different way of registering to it, and it's quite difficult to mantain your own calendar without having a lot of work to do so, and still not achieving a very user-friendly way to see it\
In this project, my intention is to create a solid calendar, where people will have their user page, and will be able to apply to the races so each user can create their own calendar.\
Users will also be able to add races to the general calendar, but it has to be approved by an admin

## Development:
I used Flask, HTML+CSS, and a a little bit of JavaScript to create this project\
Most of the things were created from scratch, but I got from the internet a few things for the front-end, such as the card template that shows the races\
Also got the flash alert system from an online video from Tech with Tim\

## Files Structure
I tried to organize the project in different folders\
**Root folder:** where database and main file app will remains\
**Website:** Python scripts (auth.py for authentication functions such as login and logout -- models.py for the database models (not used yet) -- views.py for the general functions)\
**Website/templates:** All the HTML files\
**Website/static:** CSS file\
**Website/static/race_images:** files for the pictures that are uploaded when the races are created


## Future Implementations
Right now the front-end is quite ugly, because for me, it takes a lot of time.\
In the future, I want to improve it and make it nice\
Also want to implement a calendar view for the races, a**nd more filters to it.\
Change the hosting of the pictures from local folder to cloud (s3)\