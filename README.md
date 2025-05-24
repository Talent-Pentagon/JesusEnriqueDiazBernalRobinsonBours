# JesusEnriqueDiazBernalRobinsonBours
C3


## Evaluation
### Functional Correctness
#### Pass@ak
*The LLM generates k candidate solutions
for a given problem (e.g., a buggy snippet and its description). If at least one of these k
solutions passes a predefined set of unit tests, the problem is considered solved by the
LLM.*
 - For each programming problem/bug, have the LLM generate k different code solutions (e.g., by using a high "temperature" or top-p sampling).
 - Execute each of the k generated code samples against a set of unit tests specific to that problem.
 - If any of the k samples pass all unit tests, the problem is marked as "passed."
 - Pass@k is the total number of problems that "passed" divided by the total number
of problems.