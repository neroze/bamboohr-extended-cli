# fetch_leave_records.py

import requests
import os
from requests.auth import HTTPBasicAuth
from utils import find_supervisor_id, fetch_subordinates, fetch_employee_directory
from colorama import Fore, Back, Style
from datetime import datetime, timedelta


# fetch_leave_history.py


def fetch_leave_requests(employee_id, start_date, end_date):
    headers = {'Accept': 'application/json'}
    params = {'start': start_date, 'end': end_date}
    all_leave_requests = []
    page = 1

    while True:
        response = requests.get(
            os.getenv('LEAVE_REQUESTS_ENDPOINT'),
            headers=headers,
            params={**params, 'page': page},
            auth=HTTPBasicAuth(os.getenv('API_KEY'), 'x')
        )

        if response.status_code == 200:
            leave_requests = response.json()
            employee_leave_requests = [
                request for request in leave_requests if request['employeeId'] == employee_id
            ]
            all_leave_requests.extend(employee_leave_requests)

            # Check if there are more pages
            if 'morePages' in response.json() and response.json()['morePages']:
                page += 1
            else:
                break
        else:
            print(f'Error fetching leave requests: {response.status_code} - {response.text}')
            break

    return all_leave_requests

def employeeLeave(employee_id, employee_name, start_date, end_date):
    end_date =  today = datetime.today().strftime('%Y-%m-%d')
    leave_requests = fetch_leave_requests(employee_id, start_date, end_date)
    if leave_requests:
        # print(f"Employee: {employee_name}")
        leave_types = {
            'Work From Home': [],
            'Annual Leave': [],
            'Sick Leave': [],
            'Substitute Leave': []
        }
        total_leave = 0

        for request in leave_requests:
            reason = request['type']['name']
            allStatus = request['status']

            leave_details = {
                'status': allStatus.get('status'),
                'start': request['start'],
                'end': request['end'],
                'approved': allStatus.get('lastChanged')
            }
            leave_types[reason].append(leave_details)  

        print(f' \n {Back.CYAN} -----------------{Fore.WHITE}{employee_name}---------------------- {Style.RESET_ALL}\n')
        total_leave = printLeave(leave_types, total_leave)
        print(f'{Back.WHITE} total_leave : {Fore.MAGENTA}{total_leave} {Style.RESET_ALL}')
        total_leave = 0

    else:
        print(f"Employee: {employee_name}, No leave requests found for the specified period.")

def printLeave(leaves, total_leave):
    for leave_type, leave_values in leaves.items():
        leave_count = len(leave_values)
        total_leave += leave_count
        print(f'type:{Fore.MAGENTA} {leave_type} {Style.RESET_ALL} - {Fore.RED}({leave_count}){Style.RESET_ALL}')
        for detail in leave_values:
            print(f"Approved Date: {detail.get('approved')}, Start: {detail.get('start')}, End: {detail.get('end')} Status: {detail.get('status')}")
    return total_leave

def all_leaves(supervisor):
    
    employees = fetch_employee_directory()
 
    if not employees:
        print('No employees found.')
        return

    subordinates = fetch_subordinates(supervisor)

    if not subordinates:
        print('No subordinates found.')
        return

    # Define the period for leave history, e.g., last month
    today = datetime.today()
    first_day_of_month = today.replace(day=1)
    last_month = first_day_of_month - timedelta(days=1)
    start_date = last_month.replace(day=1).strftime('%Y-%m-%d')
    end_date = last_month.strftime('%Y-%m-%d')

    print(f"Leave history from {start_date} to {end_date}:")
    subordinate = subordinates[0]
    employee_id = subordinate['id']
    employee_name = subordinate['displayName']

    for subordinate in subordinates:
        employee_id = subordinate['id']
        employee_name = subordinate['displayName']
        employeeLeave(employee_id, employee_name, start_date, end_date)

