# Phase 3 Project: Hospital Management System (Back End)

## Project Description

This is my Phase 3 Project, where I get to develop a back end CLI application for Tiba Bora Hospital, an application that helps the hospital to store records of information about doctors, nurses, patients and wards. The Powerpoint slides can be found [here](./img/Tiba%20Bora%20Project.pdf)

## Requirements and Specifications

* Python v 3.10.*
* alembic
* sqlalchemy
* ipdb
* faker
* click

## Setup Instructions

To set up this project on your local machine:

1. Run `git clone git@github.com:joelnyongesa/Phase-3-Week-3-Code-Challenge.git`

2. Navigate into the project directory via terminal, and create a virtual environment and install the dependencies  `pipenv install && pipenv shell`

3. Once everything is done, navigate into the `lib/` directory. Make the `models.py` file executable using the command `chmod a+x models.py`. Then run the `models.py` script using `./models.py`

## How to Use

Once the project is set up, you should see the menu below:
<img src="./img/Screeenshot 1.png" alt="Main Menu"/>

From the menu provided, you can:

1. See all information about doctors -- View Nurses assigned to a specific doctor, as well as patients assigned to a specific doctor. Similarly, you can view the information about a specific doctor.

2. See the information about nurses -- View which doctor a particular nurse reports to, view the patients assigned to a specific nurse, and view the details of a specific nurse.

3. See information about patients -- View the doctor and nurses who are tasked with serving the patient, view details of a specific patient as well as the ward where the patient was admitted to.

4. See information about wards -- View details of a specific ward, also view the number of patients admitted in a specific ward at any given time.

5. Once you are done, you may press `Q` or `q` to exit the application

## Author

Made by `Joel Nyongesa`

## Contacts

Feel free to reach out via [this email]('mailto:joelnyongesa148@gmail.com) or [this email](mailto:joelnyongesa.students@moringaschool.com)

## Licence

[![License:MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Copyright (c) 2023 **Joel Nyongesa**