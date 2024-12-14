import paramiko

def upload_file_to_ec2(local_path, remote_path, key_path, hostname, username):
    """
    Uploads a file to an EC2 instance via SFTP.

    :param local_path: Path to the local file to be uploaded
    :param remote_path: Destination path on the EC2 instance
    :param key_path: Path to the SSH private key file
    :param hostname: IP address or hostname of the EC2 instance
    :param username: SSH username for the EC2 instance
    """
    # Paramiko SSHClient nesnesini oluştur
    ssh = paramiko.SSHClient()

    # Otomatik olarak sunucunun anahtarını kabul et
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # SSH anahtarını kullanarak bağlantıyı kur
        ssh.connect(hostname, username=username, key_filename=key_path)

        # SFTP bağlantısını başlat
        sftp = ssh.open_sftp()

        # Dosyayı yükle
        sftp.put(local_path, remote_path)
        print(f"File uploaded to {remote_path}")

        # SFTP bağlantısını kapat
        sftp.close()

    finally:
        # SSH bağlantısını kapat
        ssh.close()

# Kullanım örneği
# key_path = "C:\\Users\\hacet\\Downloads\\AWS-test.pem"
# hostname = "15.237.138.254"
# username = "ubuntu"
# local_path = 'C:\\Users\\hacet\\Downloads\\402report.pdf'
# remote_path = 'project/402-interim1.pdf'
#
# upload_file_to_ec2(local_path, remote_path, key_path, hostname, username)
def download_file_from_ec2(remote_path, local_path, key_path, hostname, username):
    """
    Downloads a file from an EC2 instance via SFTP.

    :param remote_path: Path to the file on the EC2 instance
    :param local_path: Path where the file will be saved locally
    :param key_path: Path to the SSH private key file
    :param hostname: IP address or hostname of the EC2 instance
    :param username: SSH username for the EC2 instance
    """
    # Paramiko SSHClient nesnesini oluştur
    ssh = paramiko.SSHClient()

    # Otomatik olarak sunucunun anahtarını kabul et
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # SSH anahtarını kullanarak bağlantıyı kur
        ssh.connect(hostname, username=username, key_filename=key_path)

        # SFTP bağlantısını başlat
        sftp = ssh.open_sftp()

        # Dosyayı indir
        sftp.get(remote_path, local_path)
        print(f"File downloaded to {local_path}")

        # SFTP bağlantısını kapat
        sftp.close()

    finally:
        # SSH bağlantısını kapat
        ssh.close()

# Kullanım örneği
# key_path = "C:\\Users\\hacet\\Downloads\\AWS-test.pem"
# hostname = "15.237.138.254"
# username = "ubuntu"
# remote_path = 'project/402-interim.pdf'
# local_path = 'C:\\Users\\hacet\\Downloads\\deneme3.pdf'
#
# download_file_from_ec2(remote_path, local_path, key_path, hostname, username)
#

    def getDataFromSSE(self,url, csv_filename, timeout=15):
        # Eğer CSV dosyası varsa, sil
        if os.path.exists(csv_filename):
            os.remove(csv_filename)

        headers = {'Accept': 'text/event-stream'}

        try:
            response = requests.get(url, stream=True, headers=headers, timeout=timeout)

            if response.status_code != 200:
                raise Exception(f"Bağlantı başarısız oldu: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"Bağlantı {timeout} saniye içinde tamamlanamadı.")
            return

        client = response.iter_lines()
        start_time = time.time()

        # CSV dosyasını aç ve DictWriter'ı başlat
        with open(csv_filename, 'a', newline='') as csvfile:
            fieldnames = [
                'time_elapsed', 'ax1', 'ay1', 'az1', 'gx1', 'gy1', 'gz1',
                'mx1', 'my1', 'mz1', 'ax2', 'ay2', 'az2', 'gx2', 'gy2',
                'gz2', 'mx2', 'my2', 'mz2', 'emg1', 'emg2', 'fsr1', 'fsr2'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Dosya yeni oluşturulduysa, başlıkları yaz
            writer.writeheader()

            try:
                for line in client:
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data:"):
                            data = decoded_line[5:].strip()
                            parts = data.split()
                            float_list = list(map(float, parts))
                            print(float_list)

                            current_time = time.time()
                            time_elapsed = current_time - start_time

                            writer.writerow({
                                'time_elapsed': time_elapsed,
                                'ax1': float_list[0],
                                'ay1': float_list[1],
                                'az1': float_list[2],
                                'gx1': float_list[3],
                                'gy1': float_list[4],
                                'gz1': float_list[5],
                                'mx1': float_list[6],
                                'my1': float_list[7],
                                'mz1': float_list[8],
                                'ax2': float_list[9],
                                'ay2': float_list[10],
                                'az2': float_list[11],
                                'gx2': float_list[12],
                                'gy2': float_list[13],
                                'gz2': float_list[14],
                                'mx2': float_list[15],
                                'my2': float_list[16],
                                'mz2': float_list[17],
                                'emg1': float_list[18],
                                'emg2': float_list[19],
                                'fsr1': float_list[20],
                                'fsr2': float_list[21]
                            })
                        if keyboard.is_pressed('q'):
                            print("Stopping collection...")
                            break
            except KeyboardInterrupt:
                print("Bağlantı kesildi.")
            finally:
                response.close()
                ftp = FTPClient('172.20.10.5', 21, 'user', 'password')
                ftp.connect()
                ftp.upload_file(csv_filename)
                print('File successfully uploaded to the FTP server.')

