import requests
from requests.auth import HTTPBasicAuth
import os


def find_supervisor_id(employees, supervisor_name):
    for employee in employees:
        if employee.get('displayName').lower() == supervisor_name.lower():
            return employee['id']
    return None

def fetch_subordinates(supervisor):
	employees = fetch_employee_directory()
	subordinates = [emp for emp in employees if emp.get('supervisor').lower() == supervisor.lower()]
	return subordinates


def fetch_employee_directory():
    headers = {'Accept': 'application/json'}
    response = requests.get(os.getenv('EMPLOYEE_DIRECTORY_ENDPOINT'), headers=headers, auth=HTTPBasicAuth(os.getenv('API_KEY'), 'x'))

    if response.status_code == 200:
        return response.json()['employees']
    else:
        print(f'Error fetching employee directory: {response.status_code}')
        return []