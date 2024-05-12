# assignment-cardano


## first ideas:

for this usecase, what I'm thinking to do is to build an api/script to do the processing and the teams would be able to use them. For the api approach, a negative point would be hosting it, but it can make it easier if differents teams are using it and the solution can become more robust in the future. For the script, one of the negatives points would be being python dependent, but given the team that will be using it, running the script probably wouldn't be to difficult.

Both enrichment operations can probably run assynchronously so the whole process is faster.

At the end, we could either add the data to a database of sorts, or return a new csv. A database may be a good solution so we don't query the same data twice, among other things, but I'm deciding to return a simple csv file back so it would be easier to work with for the end users (they are already using a csv file as an input).
