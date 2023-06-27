import requests
import csv
from datetime import datetime

url = 'https://console.redhat.com/api/cost-management/v1/recommendations/openshift'
username = 'krvoora-ocm'
password = 'PP820cik@08544'

auth = requests.auth.HTTPBasicAuth(username, password)

namespace = 'ocm-staging-24aent04pggtel21mlirb2fioej9ga3h-krz24-dpt-0001'

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

        response = requests.get(url, auth=auth, params=params)

        if response.status_code == 200:
            data = response.json()
            config = data['data'][0]['recommendations']['duration_based']['short_term']['config']
            
            limits = config.get('limits') or {}
            requests = config.get('requests') or {}
            
            formatted_limits = {key: f"{value['amount']} {value['format']}" for key, value in limits.items()}
            formatted_requests = {key: f"{value['amount']} {value['format']}" for key, value in requests.items()}
            
            writer.writerow([query_name, formatted_limits, formatted_requests])
        else:
            writer.writerow([query_name, 'Request Failed', ''])

print(f'Query outputs saved to {output_filename}')
