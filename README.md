# Task

Topic 2: ArgMax in Sliding-Window Aggregation

Group: Harnisch, Philipp; Herrmann, Richard; Muders, Julian

Paper: http://www.vldb.org/pvldb/vol8/p702-tangwongsan.pdf

Task: Develop a simple streaming aggregator in your favourite programming language based on the Reactive Aggregator (RA) framework presented in the paper. Limit yourself to the ArgMax operator over a sliding time-based window (some hard-coding of the operator is fine, no parsing of a query specification, etc, is required).  Implement the computation of the operator according to the lift/combine/lower functions, but keep the implementation to the bare essentials (neglect the optimizations mentioned in the paper). Run the implementation for a stream of synthetic data and explore the behaviour of the operator when changing the window size.

# TODO
1. develop aggregator, windowingLibrary and FlatFat (Done)
1. Create FlatFat and Reactive aggregator with static size (Done)
1. adapt RA for using fixed size windows (discarding timestamps) and sliding/update size  (Done)
1. Implement timing for RA (per tuple times and tuple/sec measurements) (Julian)
1. Run tests on synthetic data
    1. Create Synthetic streams (Done)
        * Read section 6.1 and try to build synthetic data based on information on streams used in the paper (if possible)
        * create stream all ordered (only insert, evict) (each arg is unique)
        * create stream with non FIFO data (timestamps out of order)
        * create two streams with medium and large amounts of trigger calls

    1. run these sets on different window sizes (1, 2, 4, 8, 10, 16, 25, 32, 50, 64, 75, 100, (continue in 100*x and 2^x) until at least 1024) - in events in window, not time
1. Analyze test results (until 30.06.)
1. Write report (30.06. - 07.07)

# Deadlines

https://moodle.hu-berlin.de/pluginfile.php/3859195/mod_resource/content/3/0_project_work.pdf

Until June 9, 2021

– Form groups (if not done yet) and submit topic preferences

June 10, 2021

– Topic assignments

Until July 7, 2021

– Work on the project

– No lectures / exercises on June 17, June 24, July 1

– Questions -> Moodle-Forum

On July 7, 2021 (AoE)

– Submission of the project report


# Submission

By the deadline, submit a PDF report per group with your results in Moodle

Use the VLDB template to prepare your report (Latex or Word):

https://www.vldb.org/pvldb/format.html

Using this template, I would expect the report to have a length of around 4 pages, incl. figures (e.g. the experimental pipeline), plots, etc.

Make sure to include names of all group members

Suggested structure for the report:

– Goal and scope

– Applied method

– Obtained results

– Discussion/Conclusion
