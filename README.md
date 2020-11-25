# database-query-visualizer

Repo for course project work CX4031 DATABASE SYSTEM PRINCIPLES from NTU.

## Raw Data

Raw csv data is too large to be checked into VCS. Download the data from here using your NTU office account. https://entuedu-my.sharepoint.com/:f:/g/personal/nlee016_e_ntu_edu_sg/Eu9asRzO8kVGkEYXAaafDbsBUCi4eUeKqyXawFfPnFoiog?e=O6jxY1

## Quick start
The easiest way to do development on this repo is to use docker

Set up the project and the database
~~~
docker-compose build && docker-compose up
~~~
Afterwards head to [url](http://localhost:5000/) 

## Local development
This project uses pipenv to manage the dependencies. To install:
~~~
pipenv install
pipenv shell
~~~

Installing pre-commit hooks (Suggested)
~~~
pre-commit install
~~~