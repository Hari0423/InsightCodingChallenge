# Insight Data Engineering Coding Challenge
Coding challenge for Insight Data Engineering
### Challenge and Summary:
This [challenge](https://github.com/InsightDataScience/coding-challenge/blob/master/README.md#testing-your-directory-structure-and-output-format) requires  to:
* Use Venmo payments that stream in to build a graph of users and their relationship with one another.
* Calculate the median degree of a vertex in a graph and update this each time a new Venmo payment appears. The median degree across a 60-second sliding window is calculated.

The vertices on the graph represent Venmo users and whenever one user pays another user, an edge is formed between the two users.
The graph and its associated median degree is updated each time a new payment is processed. The graph only consists of payments with timestamps that are 60 seconds or less from the maximum timestamp that has been processed.

As new payments come in, edges that were formed between users with payments older than 60 seconds from the maximum timestamp are evicted


### Repo Structure:
```
├── README.md 
├── run.sh
├── src
│     └── median_degree.java
├── venmo_input
│   └── venmo-trans.txt
├── venmo_output
│   └── output.txt
└── insight_testsuite
       ├── run_tests.sh
       └── tests
            └── test-1-venmo-trans
            │   ├── venmo_input
            │   │   └── venmo-trans.txt
            │   └── venmo_output
            │       └── output.txt
            └── your-own-test
                 ├── venmo_input
                 │      └── venmo-trans.txt
                 └── venmo_output
                      └── output.txt
```
### Programming Language and version:
Python 2.7.9
### Default libraries:
1. sys
2. time
3. json
### Run Program:
To execute the main program:
```bash
bash ./run.sh
```
### Run Tests:
There are 3 test cases are in separate folder, insight_testsuite. So to execute them:
```bash
cd insight_testsuite
bash ./run_tests.sh
```
