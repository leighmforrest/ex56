# ex56

A project where TTB reports are generated from links scraped from a website and where video reports from data retrieved from a JSON api. All data retrieved from [Learn Code The Hard Way](https://learncodethehardway.com/).

---

## Up and Running

To run the code as intended, you need to add PYTHONPATH to .bashrc. Run this command: `nano ~/.bashrc`

Then you need to add the PYTHONPATH to the bashrc file: `export PYTHONPATH="."`, then exit.

To run the code, run `source ~/.bashrc`

Get into the project root to create the environment and install the dependencies: `conda create --name <env> --file requirements.txt` (let env be the name of the environment that you choose).

The program should run with this command when in the directory: `python ex56`