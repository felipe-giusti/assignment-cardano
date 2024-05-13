# assignment-cardano
I decided to create both a script and an api. The script is easy to use, but the api would allow for better growth / changes in the future.

##  How to run
> Note: My python installation is abreviated as `py`, you may need to use `python3` or another keyword to run python

Install the libraries

`pip install -r requirements.txt`

### To run the Script
Add csv files to input folder (./in).
> Note: I added the folder and a csv to GIT just to make it easier to run, in a real scenario, I would keep it in the .gitignore file.
  
run on default directory:

`py enrich_script.py`

The resulting csv will be saved in the output folder (./out)

### To run the API
run on default directory to start server:

 `uvicorn run:app  `

To query the data, you can use the following route:

```
POST localhost:8000/enrich

Body (form-data)
file: yourfile.csv
```


Curl example:

`curl -X POST -F "file=@input_dataset.csv" http://localhost:8000/enrich`



## API Overview
Just to clarify how I'm organizing the API modules

- models: business models / domain
- repo: data in/out or communication layer -> talk to apis or databases for example and structure the data
- routes: FastAPI routes. system entry point
- services: Decided to remove it in the end, but could hold business logic and the "enrich data" functions

## first ideas:

for this usecase, what I'm thinking to do is to build an api/script to do the processing and the teams would be able to use them. For the api approach, a negative point would be hosting it, but it can make it easier if differents teams are using it and the solution can become more robust in the future. For the script, one of the negatives points would be being python dependent, but given the team that will be using it, running the script probably wouldn't be to difficult.

Both enrichment operations can probably run assynchronously so the whole process is faster.

At the end, we could either add the data to a database of sorts, or return a new csv. A database may be a good solution so we don't query the same data twice, among other things, but I'm deciding to return a simple csv file back so it would be easier to work with for the end users (they are already using a csv file as an input).
