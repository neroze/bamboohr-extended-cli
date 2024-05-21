import requests
import json
from requests.auth import HTTPBasicAuth
from utils import find_supervisor_id, fetch_subordinates, fetch_employee_directory
from config import BAMBOOHR_SUBDOMAIN, API_KEY, SUPERVISOR_NAME


# Replace with your BambooHR subdomain and API key
BAMBOOHR_SUBDOMAIN = 'logpoint'
API_KEY = '7c81917d059c56750520c005eae70cc0ada76c38'
SUPERVISOR_NAME = 'nmh@logpoint.com'  # Replace with the supervisor's name or email
SUPERVISOR = 'Niraj Maharjan'  # Replace with the supervisor's name or email

def fetch_leave_requests(employee_id, date):
	url = f'https://api.bamboohr.com/api/gateway.php/{BAMBOOHR_SUBDOMAIN}/v1/time_off/requests'
	params = {
		'start': date,
		'end': date
	}
	headers = {
		'Accept': 'application/json'
	}
	response = requests.get(url, headers=headers, params=params, auth=HTTPBasicAuth(API_KEY, 'x'))

	if response.status_code == 200:
		leave_requests = response.json()
		employee_leave_requests = [request for request in leave_requests if request['employeeId'] == employee_id]
		return employee_leave_requests
	else:
		print(f'Error fetching leave requests: {response.status_code}')
		return []

def main():
	employees = fetch_employee_directory()

	if not employees:
		print('No employees found.')
		return

	supervisor_id = find_supervisor_id(employees, SUPERVISOR_NAME)
	print(f'Supervisor ID : {supervisor_id}')

	if not supervisor_id:
		print(f'Supervisor named {SUPERVISOR_NAME} not found.')
		return

	leave_date = '2024-05-20'
	subordinates = fetch_subordinates(supervisor_id)

	if not subordinates:
		print('No subordinates found.')
		return

	print(f"Leave requests for {leave_date}:")
	for subordinate in subordinates:
		employee_id = subordinate['id']
		employee_name = subordinate['displayName']
		leave_requests = fetch_leave_requests(employee_id, leave_date)

		for request in leave_requests:
			reason = request['type']['name']
			start_date = request['start']
			end_date = request['end']
			print(f"Employee: {employee_name}, Reason: {reason}, Start Date: {start_date}, End Date: {end_date}")

if __name__ == "__main__":
	main()
