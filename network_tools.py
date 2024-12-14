import subprocess
import re
import matplotlib.pyplot as plt
import pandas as pd
import requests
import os
import csv
import time
import keyboard

def find_ip_by_mac(mac_address):
    # Normalize the MAC address format
    mac_address = mac_address.lower().replace(':', '-')

    # Run the 'arp -a' command and capture the output
    result = subprocess.run(['arp', '-a'], capture_output=True, text=True)

    # Check the output line by line
    for line in result.stdout.splitlines():
        # Use a regular expression to find IP and MAC addresses
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([-A-Fa-f0-9:]+)", line)
        if match:
            ip = match.group(1)
            mac = match.group(2).lower()

            # If the MAC address matches the specified address, return the IP address
            if mac == mac_address:
                return ip
    return None

# ---------------------------------------------------------------------------------------------

def sse_clients(url, csv_filename, timeout=15):
    if os.path.exists(csv_filename):     # If the CSV file exists, delete it
        os.remove(csv_filename)
    headers = {'Accept': 'text/event-stream'}
    try:
        response = requests.get(url, stream=True, headers=headers, timeout=timeout)
        if response.status_code != 200:
            raise Exception(f"Connection failed: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"Connection could not be completed within {timeout} seconds.")
        return
    client = response.iter_lines()
    start_time = time.time()
    with open(csv_filename, 'a', newline='') as csvfile:     # Open the CSV file and initialize the DictWriter
        fieldnames = ['time_elapsed', 'ax1', 'ay1', 'az1', 'gx1', 'gy1', 'gz1',
            'mx1', 'my1', 'mz1', 'ax2', 'ay2', 'az2', 'gx2', 'gy2',
            'gz2', 'mx2', 'my2', 'mz2', 'emg1', 'emg2', 'fsr1', 'fsr2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()         # If the file is newly created, write the headers
        try:
            for line in client:
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data:"):
                        data = decoded_line[5:].strip()
                        parts = data.split()
                        float_list = list(map(float, parts))
                        print(float_list)
                        current_time = time.time() # Start time elapsed
                        time_elapsed = current_time - start_time
                        writer.writerow({
                            'time_elapsed': time_elapsed,
                            'ax1': float_list[0],'ay1': float_list[1],'az1': float_list[2],
                            'gx1': float_list[3],'gy1': float_list[4],'gz1': float_list[5],
                            'mx1': float_list[6],'my1': float_list[7],'mz1': float_list[8],
                            'ax2': float_list[9],'ay2': float_list[10],'az2': float_list[11],
                            'gx2': float_list[12],'gy2': float_list[13],'gz2': float_list[14],
                            'mx2': float_list[15],'my2': float_list[16],'mz2': float_list[17],
                            'emg1': float_list[18],'emg2': float_list[19],
                            'fsr1': float_list[20],'fsr2': float_list[21] })
                    if keyboard.is_pressed('q'):
                        print("Stopping collection...")
                        break
        except KeyboardInterrupt:
            print("Connection interrupted.")
        finally:
            response.close()
            data = pd.read_csv(csv_filename)
            plt.figure()
            plt.subplot(3,1,1)
            plt.plot(data['time_elapsed'],data['fsr1'])
            plt.subplot(3,1,2)
            plt.plot(data['time_elapsed'],data['fsr2'])
            plt.subplot(3,1,3)
            plt.plot(data['time_elapsed'],data['emg1'])
            plt.show()

if __name__ == '__main__':
    # Target MAC address (ESP32's MAC address)
    esp32_mac = "D0:eF:76:49:36:DC"
    # Find and print the IP address
    ip_address = find_ip_by_mac(esp32_mac)
    if ip_address:
        print(f"The IP address of the ESP32 is: {ip_address}")
    else:
        print("The device with the specified MAC address was not found.")
    url = f"http://{ip_address}/events"
    sse_clients(url,'sensor_data.csv',15)
