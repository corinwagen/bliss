# bliss
*a lightweight python package for speech-and-debate tournament tabulation*

## About
This is a side project to replace [Joy of Tournaments](https://www.joyoftournaments.com/) for speech-and-debate tabulation.
Bliss aims to provide a lightweight, object-oriented interface that gives tab directors maximum speed and flexibility, 
preventing the common issues that come with inflexible workflows.

Bliss provides mainly a Python library/API, with no immediate plans to develop a front-end interface. 
Jupyter Notebook is the recommended way to run things, with frequent use of *pickle* to save state.

## Todo
- Autogenerate blank ballot ``.yaml``  files with speaker IDs.
- Add code to autogenerate rankings.
- Track AFF/NEG for debate, making sure one team doesn't do all AFF or all NEG.
- Prevent repeat hits in debate - automatically assign pairings to prevent this. Manual makes this hard.
- Some way to break ties based on room difficulty for speech events.
- Debate breaks are awkward later - manually passing pairing indices is counterintuitive.
- print final results
- how to handle same-day add–drop
- finals rounds scoring independently. overall ranks are composite in out-rounds, previous rounds shouldn't affect anything.

## Corin Notes
- we need a spreadsheet!
- like, just a good spreadsheet that outputs all the info we want and need.
- code takes in spreadsheet - spreadsheet is the state!
- and we can manually look at all the data and assess its correctness.
- todo:
  - repeat hits, bad.
  - aff/neg bad
  - room difficulty? break ties.
  - debate breaks
  - FINAL ROUND SCORING

*Corin Wagen, 2023*
