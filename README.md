# Temporary Repo for ALS Hiring Exercise

## Background
Contains anonymized hiring exericise for Anne Lewis Strategies <br />
Role: Senior Data Analyst <br />
Date: May 24, 2021

## Overview
Repo contains: <br />
people.py: python script that reads in public AWS S3 files from ALS <br />
people.csv: file containing email, code, is_unsub, create_dt, and updated_dt <br />
acquisition_facts.csv: file containing aggregated stats (# constituents by acquisition_date) from people.csv

## Getting Started
To run the people.py: <br />
Install Python3 <br />
Install Pandas <br />
Run python file in terminal <br />

Other notes:<br />
people.py is set to automatically read in the public AWS S3 files indicated in the hiring exercise <br />
people.csv and acquisition_facts.csv will save to working directory for people.py <br />
on initial run, a new folder called als_hiring_exercise will be created in the working directory indicated above