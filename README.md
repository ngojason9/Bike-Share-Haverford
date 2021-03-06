# Bike Share Program
The Flask Web App streamlines the check-in/check-out process for Haverford Bike Share Program.

## Getting Started

### Introduction
The Blue Bike Share Program was offered by the Committee of Environmental Responsibility (CER) at Haverford College. The program aims to make bicycles accessible to students who might find them difficult to purchase or only need them for short-term use. It provides an environmentally friendly, fun, and convenient way for students to get around!

### Prerequisites
- `Python 3.6`
- `pip`
- `virtualenv`

### Installing
First, clone the repository to your local machine
```
$ git clone https://github.com/ngojason9/Bike-Share-Haverford/
```
Next, go to the directory and create a new Python 3 virtual enviroment `$ virtualenv -p python3 env`.

Then, activate the virtual environment. If you are on Linux/MacOS, use the command `$ source env/bin/activate`. If you are on Windows, use `$ env\Scripts\activate`.

Finally, install all dependencies via the command
```
$ pip install -r requirements.txt
```

### Usage
Now that you have installed all the dependencies, run the command `$ flask run` in the virtual environment to test the application.

![Home Page Screencast](screenshots/myimage.gif)

#### Email Feature
To fully test the email feature of the app, set the following variables in your config file:
```
MAIL_DEBUG = True
MAIL_SERVER = '<your-email-server'>
MAIL_PORT = <your-email-port>
MAIL_USE_TLS = <your-email-TLS-setting>
MAIL_USERNAME = <'your-email-address'>
MAIL_PASSWORD = <'your-email-password'>
```

## Deployment
The project is now live on bikeshare.jasonngo.net (initial deployment). More developing work is still needed.

## Acknowledgement

## Contact
Please email me at ngojason9@gmail.com with any questions or suggestions.