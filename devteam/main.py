#!/usr/bin/env python
import sys
import warnings
import yaml

from datetime import datetime

from devteam.crew import Devteam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # inputs = {
    #     'topic': 'AI LLMs',
    #     'current_year': str(datetime.now().year)
    # }
    
    # try:
    #     Devteam().crew().kickoff(inputs=inputs)
    # except Exception as e:
    #     raise Exception(f"An error occurred while running the crew: {e}")
    print("## Welcome to the Game Crew")
    print('-------------------------------')

    with open('src/devteam/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
        examples = yaml.safe_load(file)

    inputs = {
        'game' :  examples['example5_gestionhopital']
    }
    game= Devteam().crew().kickoff(inputs=inputs)
    # crew = Crew(output_log_file = crewai_logs.txt) 
    print("\n\n########################")
    print("## Here is the result")
    print("########################\n")
    print("final code for the game:")
    print(game)
    print(game.raw)
    # print(f"Raw Output: {crew_output.raw}")
    

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Devteam().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Devteam().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Devteam().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
