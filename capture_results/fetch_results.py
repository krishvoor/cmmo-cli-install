import requests
import csv
import urllib3
import argparse
from datetime import datetime
from elasticsearch import Elasticsearch

# Disable Warnings while interacting with https
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create the Parser Object
parser = argparse.ArgumentParser(description="Capture recommendations from console-dot")

# Define the argumets
parser.add_argument('--namespace',
                    help='Supply the Namespace/Project name')

parser.add_argument('--container_name',
                    help='Provide the Container name')

parser.add_argument('--workload_name',
                    help='Provide the Workload name')

parser.add_argument('--username', 
                    help='Provides console-dot username')

parser.add_argument('--password', 
                    help='Provides console-dot password')

parser.add_argument('--url',
                    help='Provide the required console-dot URL',
                    default="https://console.redhat.com/api/cost-management/v1/recommendations/openshift")

# Assign them as attributes
args = parser.parse_args()

namespace = f'{args.namespace}'
container_name = f'{args.container_name}'
workload_name = f'{args.workload_name}'
username = f'{args.username}' 
password = f'{args.password}'
login_url = f'{args.url}'

def index_metadata(uuid):
    # Connect to the Elasticsearch server with authentication
    es = Elasticsearch(
        hosts='https://search-perfscale-pro-wxrjvmobqs7gsyi3xvxkqmn7am.us-west-2.es.amazonaws.com:443',
        http_auth=('admin', 'nKNQ9=vw_bwaSy1')
    )
    # Define the index name
    index = 'hypershift-wrapper-timers'

    # Path to the CSV file
    csv_file_path = 'path/to/your/csv/file.csv'
    
    # Index UUID with kube-burner

    # Read the CSV file
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Push each row as a document to the Elasticsearch server
            response = es.index(index=index, body=row)

            # Check the response
            if response['result'] == 'created':
                print('Data pushed successfully.')
            else:
                print('Failed to push data:', response)

auth = requests.auth.HTTPBasicAuth(username, password)

queries = [
    {
        'query_name': 'etcd',
        'params': {
            'project': f'{namespace}',
            'container': 'etcd'
        }
    },
    {
        'query_name': 'kube_apiserver',
        'params': {
            'project': f'{namespace}',
            'workload': 'kube-apiserver',
            'container': 'kube-apiserver'
        }
    },
    {
        'query_name': 'northd',
        'params':{
            'project': f'{namespace}',
            'container': 'northd'
        }
    }
]

timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
output_filename = f'output_{timestamp}.csv'

with open(output_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Query Name', 'Limits', 'Requests'])

    for query in queries:
        query_name = query['query_name']
        params = query['params']

        response = requests.get(login_url, auth=auth, params=params)

        if response.status_code == 200:
            data = response.json()
            config = data['data'][0]['recommendations']['duration_based']['short_term']['config']
            
            writer.writerow([query_name, config, config])
        else:
            writer.writerow([query_name, 'Request Failed', ''])

        response.close()  # Close the connection after each query

print(f'Query outputs saved to {output_filename}')