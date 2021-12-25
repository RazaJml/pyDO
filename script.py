import requests
import json
import datetime
import schedule
import time

def creatingDroplets():
    droplet_url = 'https://api.digitalocean.com/v2/droplets'
    token = 'e93c9340e7de74d3eaf9b5b0c003d08c6fc810829dff1f1e149c4f4c7a69b122'

    droplet_res = requests.get(droplet_url, headers={'Authorization': f'Bearer {token}'})
    droplet_res_data = droplet_res.json()
    counter = len(droplet_res_data['droplets'])

    load_balancer_url = "https://api.digitalocean.com/v2/load_balancers"

    load_balancer_req = requests.get(load_balancer_url, headers={'Authorization': f'Bearer {token}'})
    load_balancer_data = load_balancer_req.json()

    droplet_ids = load_balancer_data['load_balancers'][0]['droplet_ids']

    print(f'soe {droplet_ids}')

    one_drop_url = f'https://api.digitalocean.com/v2/droplets/{droplet_ids[0]}/'

    get_one_drop_req = requests.get(one_drop_url, headers={'Authorization': f'Bearer {token}'})
    one_drop_data = get_one_drop_req.json()
   
    snapshot = one_drop_data['droplet']['snapshot_ids'][0]

    data = {
        "name":f'mydroplet{counter+1}',
        "region":"nyc1",
        "size":"s-1vcpu-1gb",
        "image": snapshot,
        "password":'Qwerty,123raza',
        "tags":["testing"],
    }

    res = requests.post(droplet_url, data, headers={'Authorization': f'Bearer {token}'})
    print(res.json())

# creatingDroplets()

def removingDroplets():
    token = 'e93c9340e7de74d3eaf9b5b0c003d08c6fc810829dff1f1e149c4f4c7a69b122'
    load_balancer_url = "https://api.digitalocean.com/v2/load_balancers"

    load_balancer_req = requests.get(load_balancer_url, headers={'Authorization': f'Bearer {token}'})
    load_balancer_data = load_balancer_req.json()

    droplet_ids = load_balancer_data['load_balancers'][0]['droplet_ids']

    if len(droplet_ids) > 0:
        remove_droplet_url = f'https://api.digitalocean.com/v2/droplets/{droplet_ids[-1]}'
        res = requests.delete(remove_droplet_url, headers={'Authorization': f'Bearer {token}'})


# removingDroplets()

def autoBalancer():
    # Basic URLS
    droplet_url = "https://api.digitalocean.com/v2/droplets" 
    load_balancer_url = "https://api.digitalocean.com/v2/load_balancers"
    token = 'e93c9340e7de74d3eaf9b5b0c003d08c6fc810829dff1f1e149c4f4c7a69b122'


    droplet_res = requests.get(droplet_url, headers={'Authorization': f'Bearer {token}'})
    droplet_res_data = droplet_res.json()
    droplet_image_id = droplet_res_data['droplets'][0]['image']['id']

    print(droplet_image_id)

    # ssh_key_url = "https://api.digitalocean.com/v2/account/keys"
    # ssh_key_res = requests.get(ssh_key_url, headers={'Authorization': f'Bearer {token}'})
    # ssh_key = ssh_key_res.json()

    # print(ssh_key)

    load_balancer_req = requests.get(load_balancer_url, headers={'Authorization': f'Bearer {token}'})
    load_balancer_data = load_balancer_req.json()

    droplet_ids = load_balancer_data['load_balancers'][0]['droplet_ids']

    print(droplet_ids)

    # snapshots




    # Geting Stats usung droplet ids

    load1_stats = []
    load5_stats = []
    cpu_stats = []

    # Timestamp in epoch format

    datetime_object1 = datetime.datetime.now()
    datetime_object2 = datetime.datetime.now()

    seconds_since_epoch = datetime_object1.timestamp()
    seconds_end_epoch = datetime_object2.timestamp()

    for i in range(len(droplet_ids)):

        load1 = requests.get(
            f"https://api.digitalocean.com/v2/monitoring/metrics/droplet/load_5?host_id={droplet_ids[i]}&start={seconds_since_epoch}&end={seconds_end_epoch}",
            headers={
                'Authorization': f'Bearer {token}'
            }
        )

        load5 = requests.get(
            f"https://api.digitalocean.com/v2/monitoring/metrics/droplet/load_5?host_id={droplet_ids[i]}&start={seconds_since_epoch}&end={seconds_end_epoch}",
            headers={
                'Authorization': f'Bearer {token}'
            }
        )

        cpuS = requests.get(
            f"https://api.digitalocean.com/v2/monitoring/metrics/droplet/cpu?host_id={droplet_ids[i]}&start={seconds_since_epoch}&end={seconds_end_epoch}",
            headers={
                'Authorization': f'Bearer {token}'
            }
        )

        load1_data = load1.json()
        load1_stats.append(load1_data)      
     
        load5_data = load1.json()
        load5_stats.append(load5_data)

        cpu_data = cpuS.json()
        cpu_stats.append(cpu_data)

    # Getting Values of CPU, Load 1, Load 5 stats

    load1_stats_values = []
    load5_stats_values = []
    cpu_stats_values = []

    # load 1 values

    load1_stats_results = []

    for load1_res in load1_stats:
        load1_stats_results.append(load1_res['data']['result'])
    
    for val in load1_stats_results[0]:
        load1_stats_values.append(val['values'])
    
    print(load1_stats_values)

    # Load 5 values

    load5_stats_results = []

    for load5_res in load5_stats:
        load5_stats_results.append(load5_res['data']['result'])
    
    for val in load5_stats_results[0]:
        load5_stats_values.append(val['values'])
    
    print(load5_stats_values)

    # CPU Values

    cpu_stats_results = []

    for cpu_res in cpu_stats:
        cpu_stats_results.append(cpu_res['data']['result'])
    
    for val in cpu_stats_results[0]:
        cpu_stats_values.append(val['values'])
    
    print(cpu_stats_values)

    # Average Value

    total_values = []

    for i in range(len(cpu_stats_values)):
        total_values.append(int(float(cpu_stats_values[i][0][1])))    

    for i in range(len(load1_stats_values)):
        total_values.append(int(float(load1_stats_values[i][0][1])))    

    for i in range(len(load5_stats_values)):
        total_values.append(int(float(load5_stats_values[i][0][1]))) 

    average_value = sum(total_values) / len(total_values)

    print(average_value)
    
    # Khud sy kuch b set kar deya ha abi ky leye
    threshold = 10000 
  
    # conditions

    if average_value > threshold:
        creatingDroplets()
    elif average_value < threshold:
        removingDroplets()

autoBalancer()

schedule.every(5).minutes.do(autoBalancer)

# fortesting run in seconds
# schedule.every(10).seconds.do(autoBalancer)

while True:
    schedule.run_pending()
    time.sleep(1)