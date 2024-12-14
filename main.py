# Gerekli kütüphanelerin import edilmesi
import tkinter as tk  # GUI için
from tkinter import filedialog  # Dosya seçme penceresi
import subprocess  # Komut satırı işlemlerini çalıştırmak için
import matplotlib.pyplot as plt  # Veri görselleştirme
import pandas as pd  # Veri analizi
import matplotlib.image as mpimg  # Resim okuma ve görselleştirme
import os  # Dosya ve dizin işlemleri
import cv2  # Video oynatma
import datetime  # Zaman damgası oluşturma
from dtw import read_and_plot_csv  # DTW (Dynamic Time Warping) dosya okuma ve çizim fonksiyonu
from awstools import *  # AWS dosya yükleme araçları
from network_tools import sse_clients, find_ip_by_mac  # Ağ araçları
import time  # Zaman işlemleri

# Zaman damgası oluşturma (Gün-Ay-Yıl Saat-Dakika-Saniye formatında)
timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")


# Kullanıcıdan isim alma ve dizin oluşturma fonksiyonu
def get_name():
    global username  # Global değişken olan 'username' tanımlanır
    username = name_entry.get()  # Kullanıcıdan alınan isim, 'name_entry' giriş kutusundan alınır

    # Eğer kullanıcı ismini girdiyse
    if username:
        # Hoş geldin mesajını güncelleyerek kullanıcı ismini gösterir
        welcome_label.config(text=f"Merhaba, {username}!")
        
        # 2 saniye bekledikten sonra ana pencereyi kapatır
        root.after(2000, root.destroy)
    else:
        # Kullanıcı ismi girilmediyse hata mesajı gösterir
        error_label.config(text="Lütfen bir isim girin!")

    # Kullanıcının verilerini depolamak için zaman damgası ile birlikte yeni bir klasör oluşturur
    os.mkdir(f"data/output/{username}_{timestamp}")


# Pencereyi kapatma fonksiyonu
def on_closing():
    root.destroy()

# CSV verilerini grafiğe dökme fonksiyonu
def plot_data(filename):
    data = pd.read_csv(filename)  # CSV dosyasını okuma
    movement = detect_movement_from_filename(filename)  # Dosya isminden hareket tipini bulma
    base_filename = os.path.basename(filename)  # Dosya ismi
    username = filename.split('_')[0]  # Dosyadan kullanıcı ismini alma
    
    # Hareket türüne göre ilgili CSV dosyasını okuma ve grafik çizimi
    if movement == "Hareket1":
        read_and_plot_csv(r"data\input\movement_1.csv", filename, username, movement, timestamp, showGraphs=True)
    elif movement == "Hareket2":
        read_and_plot_csv(r"data\input\movement_2.csv", filename, username, movement, timestamp, showGraphs=True)
    else:
        read_and_plot_csv(r"data\input\movement_3.csv", filename, username, movement, timestamp, showGraphs=True)

    # Hareketle ilgili resmin yüklenmesi ve grafikle birlikte gösterilmesi
    imagename = f"{movement}.jpeg"
    plt.ion()  # Etkileşimli mod
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8))  # 2 satırlı grafik oluşturma
    
    # Zaman ve açı verilerini çizme
    time = data.iloc[:, 0]  # İlk sütun: zaman
    ax2.plot(time, data.iloc[:, 1])
    ax2.plot(time, data.iloc[:, 2])
    ax2.plot(time, data.iloc[:, 3])
    ax2.plot(time, data.iloc[:, 4])
    ax2.set_xlabel('Time (sec)')
    ax2.set_ylabel('Angle (degrees)')
    ax2.legend(['Left Elbow', 'Left Shoulder', 'Right Elbow', 'Right Shoulder'])

    # Resim gösterimi
    img = mpimg.imread(imagename)
    ax1.imshow(img)
    ax1.axis('off')  # Resim eksenlerini gizle

    plt.tight_layout()
    plt.show()
    plt.pause(0.01)

# Video oynatma fonksiyonu
def play_video(video_path):
    cap = cv2.VideoCapture(video_path)  # Video dosyasını açma
    fps = 30  # Frame hızı
    
    while cap.isOpened():
        cap.set(cv2.CAP_PROP_FPS, fps)  # Frame hızı ayarlama
        ret, frame = cap.read()  # Her kareyi okuma
        
        if not ret:
            break
        
        cv2.imshow('Video Playback', frame)  # Frame gösterimi
        
        if cv2.waitKey(fps) & 0xFF == ord('q'):  # 'q' tuşuna basılınca çıkış
            break

# Analiz başlatma fonksiyonu
def start_analysis():
    global dtwfilename

    # Hareket seçim ekranı oluşturma
    movement_selection_window = tk.Toplevel(root)
    movement_selection_window.title("Hareket Seçimi")
    frame1 = tk.Frame(movement_selection_window)
    frame1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Pencere boyutlandırma
    window_width1 = 600
    window_height1 = 400
    screen_width1 = root.winfo_screenwidth()
    screen_height1 = root.winfo_screenheight()
    x_coordinate1 = (screen_width1 / 2) - (window_width1 / 2)
    y_coordinate1 = (screen_height1 / 2) - (window_height1 / 2)
    movement_selection_window.geometry("%dx%d+%d+%d" % (window_width1, window_height1, x_coordinate1, y_coordinate1))

    # Hareket seçildiğinde çalışacak fonksiyon
    def run_mediapipe(movement):
        movement_selection_window.after(1000, movement_selection_window.destroy)  # Pencereyi kapatma
        subprocess.Popen(["python", "Hareket1_mediapipe.py", username, movement, timestamp])  # Mediapipe çalıştırma

        f_name = f"data/output/{username}_{timestamp}/sensor_data_mp_{username}_{movement}_{timestamp}.csv"
        esp32_mac = "D0:eF:76:49:36:DC"  # ESP32 cihazının MAC adresi
        ip_address = find_ip_by_mac(esp32_mac)  # IP adresi bulma

        if ip_address:
            url = f"http://{ip_address}/events"
            sse_clients(url, f_name, 15)  # SSE istemcisi ile veri alma

            # AWS'ye dosya yükleme
            key_path = "awskey.pem"
            hostname = "15.188.53.33"
            username_aws = "ubuntu"

            remote_path = f'project/data/dtw_{username}_{movement}_{timestamp}.txt'
            local_path = f"data/output/{username}_{timestamp}/dtw_{username}_{movement}_{timestamp}.txt"
            upload_file_to_ec2(local_path, remote_path, key_path, hostname, username_aws)

            remote_path = f'project/data/sensor_data_mp_{username}_{movement}_{timestamp}.csv'
            local_path = f"data/output/{username}_{timestamp}/sensor_data_mp_{username}_{movement}_{timestamp}.csv"
            upload_file_to_ec2(local_path, remote_path, key_path, hostname, username_aws)
        else:
            print("ERROR FOR ESP32!!!")  # ESP32 hatası

    # Hareket seçim butonları
    tk.Label(movement_selection_window, text="Bir hareket seçin:").pack(pady=10)
    movements = ["Hareket1", "Hareket2", "Hareket3"]
    
    for movement in movements:
        button = tk.Button(frame1, text=movement, command=lambda m=movement: run_mediapipe(m), width=20, height=3)
        button.pack(pady=30)

# Dosya isminden hareket türünü tespit etme fonksiyonu
def detect_movement_from_filename(filename):
    if "Hareket1" in filename.lower():
        return "Hareket_1"
    elif "Hareket2" in filename.lower():
        return "Hareket_2"
    elif "Hareket3" in filename.lower():
        return "Hareket_3"
    else:
        return "Hareket_1"

# MATLAB fonksiyonlarını çalıştırma
def run_matlab():
    initialdir = r"\data\output"
    filename = filedialog.askopenfilename(initialdir=initialdir, title="Select a CSV file",
                                          filetypes=[("CSV files", "*.csv")])
    base_filename = os.path.basename(filename)
    video_filename = "mp_" + base_filename.replace('.csv', '.mp4')
    filename_video = os.path.join(os.path.dirname(filename), video_filename)

    if filename:
        plot_data(filename)  # CSV dosyasını grafiğe dökme
        print(filename)
        play_video(filename_video)  # İlgili videoyu oynatma

# Ana pencereyi oluşturma (kullanıcı ismi girişi)
root = tk.Tk()
root.title("Kullanıcı İsmi Girin")
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Hoş geldin mesajı için etiket
welcome_label = tk.Label(frame, text="Lütfen kullanıcı isminizi girin!")
welcome_label.pack(pady=10)

# Kullanıcı ismi giriş alanı
name_entry = tk.Entry(frame)
name_entry.pack(pady=10)

# Kullanıcı ismi onay butonu
name_button = tk.Button(frame, text="İsim gir", command=get_name)
name_button.pack(pady=10)
root.bind("<Return>", lambda event: name_button.invoke())  # 'Enter' tuşu ile tetikleme

# Hata mesajı etiketi
error_label = tk.Label(root, text="", fg="red")
error_label.pack()
root.protocol("WM_DELETE_WINDOW", on_closing)

# Pencere boyutlandırma
window_width = 600
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

root.mainloop()  # Pencereyi göstermek için mainloop

# Hareket analiz arayüzü oluşturma
root = tk.Tk()
root.title("Hareket analiz arayüzü")
frame1 = tk.Frame(root)
frame1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Hareket analizini başlatma butonu
button1 = tk.Button(frame1, text="Hareket analizini başlat", command=start_analysis, width=30, height=4)
button1.pack(pady=20)

# Mediapipe'den alınan hareket analizini görüntüleme butonu
button2 = tk.Button(frame1, text="Hareket analizini görüntüle", command=run_matlab, width=30, height=4)
button2.pack(pady=20)

# Pencere boyutlandırma
window_width = 1000
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

root.mainloop()  # Hareket analiz arayüzünü göstermek için mainloop
