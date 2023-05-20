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

*Corin Wagen, 2023*
