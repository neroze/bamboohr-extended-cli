import os
import argparse
from dotenv import load_dotenv
# from __future__ import print_function, unicode_literals
from PyInquirer import prompt 
from colorama import init
from all_leaves import all_leaves

# Initialize colorama on Windows
init()

def load_environment(mode):
    # Load .env file in development or testing mode
    if mode in ['development', 'testing']:
        load_dotenv()

    # For production mode, environment variables are expected to be set directly in the server environment

def promptName():
    questions = [
        {
            'type': 'input',
            'name': 'supervisor',
            'message': 'Enter Supervisor Name',
        }
    ]

    answers = prompt(questions)
    return answers.get('supervisor')

def main():
    
    # supervisor = promptName();
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run the application in different modes.")
    parser.add_argument(
        '-m', '--mode',
        default='development',
        choices=['development', 'production', 'testing'],
        help='Set the mode for the application'
    )

    parser.add_argument(
        '-n', '--name',
        help='Enter Supervisor Name'
    )

    # Parse command-line arguments
    args = parser.parse_args()
    mode = args.mode
    supervisor = args.name
    print(args)

    if not supervisor:
        supervisor = promptName()

    # Load environment variables based on mode
    load_environment(mode)

    # Get the value of an environment variable
    api_key = os.getenv('API_KEY')
    aa = os.getenv('EMPLOYEE_DIRECTORY_ENDPOINT')

    # Use the environment variable values in your code
    print("Mode:", mode)
    print("EMPLOYEE_DIRECTORY_ENDPOINT:", aa)
    print("Answer:", supervisor)
    all_leaves(supervisor)

if __name__ == "__main__":
    main()
