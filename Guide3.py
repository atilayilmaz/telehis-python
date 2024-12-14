import tkinter as tk
from tkinter import filedialog
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.image as mpimg
import os
import cv2
import datetime
from dtw import read_and_plot_csv
from awstools import *
from network_tools import sse_clients,find_ip_by_mac
import time



timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

if __name__ == '__main__':
    sample_interval = 0.5
    def get_name():
        global username
        username = name_entry.get()
        if username:
            welcome_label.config(text=f"Merhaba, {username}!")
            root.after(2000, root.destroy)
        else:
            error_label.config(text="Lütfen bir isim girin!")
            # welcome_label.config(text="İsim girişi yapılmadı.")


    def on_closing():  # Pencere kapatıldığında programın sonlandırılması
        root.destroy()


    # Ana pencere oluşturulması
    root = tk.Tk()
    root.title("Kullanıcı İsmi Girin")
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    # Hoş geldin mesajı için etiket
    welcome_label = tk.Label(frame, text="Lütfen kullanıcı isminizi girin.!")
    welcome_label.pack(pady=10)
    name_entry = tk.Entry(frame)
    name_entry.pack(pady=10)

    name_button = tk.Button(frame, text="İsim gir", command=get_name)
    name_button.pack(pady=10)
    root.bind("<Return>", lambda event: name_button.invoke())

    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    window_width = 600
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    root.mainloop()  # Pencereyi göstermek için mainloop


    def plot_data(filename):

        data = pd.read_csv(filename)
        movement = detect_movement_from_filename(filename)
        base_filename = os.path.basename(filename)
        username = filename.split('_')[0]
        if movement == "Hareket1":
            read_and_plot_csv(r"Veriler\azizideal_Hareket1_20240823_1033.csv", filename,username,movement,timestamp, showGraphs=True)
        elif movement == "Hareket2":
            read_and_plot_csv(r"Veriler\azizideal_Hareket2_20240823_1033.csv", filename,username,movement,timestamp, showGraphs=True)
        else:
            read_and_plot_csv(r"Veriler\azizideal_Hareket3_20240823_1033.csv", filename,username,movement,timestamp, showGraphs=True)

        imagename = f"{movement}.jpeg"
        plt.ion()
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8))
        # plt.figure(figsize=(12, 8))
        # fig = plt.subplots()
        # fig.canvas.manager.window.move(800, 0)
        time = data.iloc[:, 0]
        ax2.plot(time, data.iloc[:, 1])
        ax2.plot(time, data.iloc[:, 2])
        ax2.plot(time, data.iloc[:, 3])
        ax2.plot(time, data.iloc[:, 4])
        ax2.set_xlabel('Time (sec)')
        ax2.set_ylabel('Angle (degrees)')
        ax2.legend(['Left Elbow', 'Left Shoulder', 'Right Elbow', 'Right Shoulder'])

        img = mpimg.imread(imagename)
        ax1.imshow(img)
        ax1.axis('off')  # Resim eksenlerini gizle
        # ax1.set_aspect(aspect=16 / 9)

        plt.tight_layout()
        plt.show()
        plt.pause(0.01)


    def play_video(video_path):
        # os.startfile(video_path)
        # subprocess.Popen(['start', video_path], shell=True)

        cap = cv2.VideoCapture(video_path)
        fps = 30
        while cap.isOpened():
            cap.set(cv2.CAP_PROP_FPS, fps)
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Video Playback', frame)
            if cv2.waitKey(fps) & 0xFF == ord('q'):
                break


    def start_analysis():
        global dtwfilename
        # Hareket seçim ekranı
        movement_selection_window = tk.Toplevel(root)
        movement_selection_window.title("Hareket Seçimi")
        frame1 = tk.Frame(movement_selection_window)
        frame1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        window_width1 = 600
        window_height1 = 400
        screen_width1 = root.winfo_screenwidth()
        screen_height1 = root.winfo_screenheight()
        x_coordinate1 = (screen_width1 / 2) - (window_width1 / 2)
        y_coordinate1 = (screen_height1 / 2) - (window_height1 / 2)
        movement_selection_window.geometry(
            "%dx%d+%d+%d" % (window_width1, window_height1, x_coordinate1, y_coordinate1))

        def run_mediapipe(movement):
            movement_selection_window.after(1000, movement_selection_window.destroy)
            subprocess.Popen(["python", "Hareket1_mediapipe.py", username, movement,timestamp])
            # start_collection(0.5, f"Veriler/sensor_data_{username}_{movement}_{timestamp}.csv")
            # ftp = FTPClient('172.20.10.2', 21, 'user', 'password')
            # ftp.connect()
            # ftp.getDataFromSSE("http://172.20.10.2/events",f"sensor_data_{username}_{movement}_{timestamp}.csv")

            f_name = f"Veriler/sensor_data_mp_{username}_{movement}_{timestamp}.csv"
            # Define ESP32 MAC Address we used
            esp32_mac = "D0:eF:76:49:36:DC"
            # Find and print the IP address
            ip_address = find_ip_by_mac(esp32_mac)
            if ip_address:
                url = f"http://{ip_address}/events"
                sse_clients(url, f_name, 15)
            else:
                print("ERROR FOR ESP32!!!")

            key_path = "C:\\Users\\hacet\\Downloads\\awskey.pem"
            hostname = "15.188.53.33"
            username_aws = "ubuntu"

            remote_path = f'project/data/dtw_{username}_{movement}_{timestamp}.txt'
            local_path = f"Veriler/dtw_{username}_{movement}_{timestamp}.txt"
            upload_file_to_ec2(local_path, remote_path, key_path, hostname, username_aws)

            remote_path = f'project/data/sensor_data_mp_{username}_{movement}_{timestamp}.csv'
            local_path = f"Veriler/sensor_data_mp_{username}_{movement}_{timestamp}.csv"
            upload_file_to_ec2(local_path, remote_path, key_path, hostname, username_aws)




            # subprocess.Popen(["python", "EMG_uart_data.py", username])

        tk.Label(movement_selection_window, text="Bir hareket seçin:").pack(pady=10)
        movements = ["Hareket1", "Hareket2", "Hareket3"]
        global m
        for movement in movements:
            button = tk.Button(frame1, text=movement, command=lambda m=movement: run_mediapipe(m), width=20, height=3)
            button.pack(pady=30)


    def detect_movement_from_filename(filename):
        if "Hareket1" in filename.lower():
            # read_and_plot_csv(r"Veriler\azizideal_Hareket1_20240823_1032.csv", fr"Veriler\{filename}")
            return "Hareket_1"
        elif "Hareket2" in filename.lower():
            # read_and_plot_csv(r"Veriler\azizideal_Hareket2_20240823_1033.csv", fr"Veriler\{filename}")
            return "Hareket_2"
        elif "Hareket3" in filename.lower():
            # read_and_plot_csv(r"Veriler\azizideal_Hareket3_20240823_1033.csv", fr"Veriler\{filename}")
            return "Hareket_3"
        else:
            return "Hareket_1"


    def run_matlab():
        initialdir = r"C:\C:\Users\hacet\PycharmProjects\IMUaug_4_2024\IMU\Veriler"
        filename = filedialog.askopenfilename(initialdir=initialdir, title="Select a CSV file",
                                              filetypes=[("CSV files", "*.csv")])
        base_filename = os.path.basename(filename)
        video_filename = "mp_" + base_filename.replace('.csv', '.mp4')
        filename_video = os.path.join(os.path.dirname(filename), video_filename)


        if filename:
            plot_data(filename)
            print(filename)
            play_video(filename_video)

    """
    def run_matlab_txt():
        initialdir = "C:/Users/hacet/OneDrive/Masaüstü/Veriler/EMG verileri"
        filename = filedialog.askopenfilename(initialdir = initialdir, title="Select a TXT file", filetypes=[("TXT files", "*.txt")])
        if filename:
            subprocess.Popen(["matlab", "-r", f"plot_data_txt('{filename}')"])
    """

    # Arayüz oluşturma
    root = tk.Tk()
    root.title("Hareket analiz arayüzü")
    frame1 = tk.Frame(root)
    frame1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Hareket analizini başlat
    button1 = tk.Button(frame1, text="Hareket analizini başlat", command=start_analysis, width=30, height=4)
    button1.pack(pady=20)

    # Mediapipe'dan alınan hareket analizini görüntüle
    button2 = tk.Button(frame1, text="Hareket analizini görüntüle", command=run_matlab, width=30, height=4)
    button2.pack(pady=20)
    """
    button3 = tk.Button(frame1, text="EMG Hareket analizini görüntüle", command=run_matlab_txt, width=30, height=4)
    button3.pack(pady=10)
    """
    window_width = 1000
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    root.mainloop()
