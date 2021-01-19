#Parse GridDynamics Blog with Scrapy and visualize it
## Introduction
   In this project a parser will be created for GridDynamics blog together with a report that will show us:
      
    - Top-5 Authors,
    - Top-5 New Articles,
    - Plot with articles counter of 7 most popular tags
## Technologies
    - Python 3.9
    - Scrapy
    - matplotlib
    - pandas
    - os
    - yaml
## Features
The aim of this project is to create a Web Crawler that will parse https://blog.griddynamics.com/,
obtain articles and author information from it.
Then generate a report with this information:

    - Top-5 Authors (based on articles counter)
    - Top-5 New Articles (based on publish data)
    - Plot with counts of 7 popular tags
## Sources 
    https://app.pluralsight.com/library/courses/scrapy-extracting-structured-data/table-of-contents
    https://app.pluralsight.com/library/courses/data-visualization-with-python-introduction/table-of-contents
    https://app.pluralsight.com/library/courses/python-fundamentals/table-of-contents

<img width="633" alt="Screenshot" src="https://user-images.githubusercontent.com/75839583/103350362-025ffd00-4aa0-11eb-8cce-d58d50f8110b.png">

## Environments setup and first run
First create a virtual environment
```
python3 -m venv scrapy_capstyone
```
Before to run your code be sure that the following libraries are present, otherwise run the following commands:
```
pip3 install -r requirements.txt
```
Add `report` folder to your PATH in order to make all custom module imports valid using
```
cd scrapy_capstone && export PATH=$PATH:$PWD/report && echo $PATH
```

Finally run the following instruction from the command line in order to execute the report generator
```
python3 report.py
```



