<h1 align="center">

  ProjectSync
  <br>
</h1>

Problem Id: 1369

Title: Online integrated platform for projects taken up by the students of various universities/colleges
(Smart India Hackathon 2023) 

Team: Akhil Nagar, Ishika De, Hetvi Gudka, Yashvi Donga, Sanyukta Joshi, Avish Rodrigues

Proposed Solution:
1) There exists University profiles that will display all ongoing projects that the students are working on.
2) Using automation and AI, we can read the ReadMe file, create a summary of the project, and assign necessary domain tags to the project which will be displayed on the portal.
3) Using these tags, we create an ML recommendation system for students from other universities to browse similar projects.
4) In order to curb plagiarism, we will introduce a plagiarism check between codebases to ensure no two projects have the exact same code.
5) Students can search, filter, and query project ideas based on their domain interests. There will be an option for students to see/contact the team if they wish to contribute to the open-source project.
6) There will be a feed such that a student can subscribe to the project of their liking and keep up to date with the latest developments. They can leave feedback and comments too!
7) This project also serves as a breeding ground for startup innovation and people/organizations can fund/provide grants to specific projects based on scope/viability.
8) It'll help students learn and build over the current approaches that already exist.
9) The platform will allow collaboration inter-college hence creating a strong community of passionate coders.
10) A blog/communication platform for students to come together for ideation and networking opportunities.




# Pre-Requisites

> **Note**
>For Windows insallation only
<br>

To clone and run this application, you'll need [Git](https://git-scm.com) and python installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/AkhilNagar/Split-facewise.git


# Create a Virtual Env
$ virtualenv2 --no-site-packages env

# Activate the Environment
$ source env/bin/activate

# Install cmake
$ pip install cmake

# Install Dlib
$ pip install dlib
#Dlib package is present in the repository
$ pip install https://github.com/AkhilNagar/Split-facewise/blob/master/dlib-19.19.0-cp38-cp38-win_amd64.whl

# Install all other Requirements
$pip install requirements.txt



```

# Run Django

```bash
# Activate the Environment
$ source env/bin/activate

# Change Directory to Project folder
(env)$ cd Splitwise

#Run Django Server on localhost
(env)$ python manage.py runserver

Navigate to [localhost](http://127.0.0.1:8000/)
```


# User Interface

<h2>Home Page </h2>

![screenshot](https://github.com/AkhilNagar/Split-facewise/blob/master/Screenshots/homepage.png)

<h2>Profile Page </h2>

![screenshot](https://github.com/IshikaDe-2803/SIH-HexaByte/master/Screenshots/Profile.png)

<h2>Explore Page </h2>

![screenshot](https://github.com/AkhilNagar/Split-facewise/blob/master/Screenshots/Explore.png)

<h2>Personalised Automated Feed </h2>

![screenshot](https://github.com/IshikaDe-2803/SIH-HexaByte/master/Screenshots/Feed.png)

<h2>Upload Project </h2>

![screenshot](https://github.com/IshikaDe-2803/SIH-HexaByte/master/Screenshots/UploadProject.png)

