import cv2
import mediapipe as mp
import time
import numpy as np
import datetime
import os               # Farklı bir klasöre kaydedebilmek için
import sys
import csv
from awstools import *
from dtw import read_and_plot_csv
from MovementMap import getMovementMap as movementMap


# ftp = FTPClient('172.20.10.5', 21, 'user', 'password')
# ftp.connect()



def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    if angle > 180.0:
        angle = 360 - angle

    return angle
def add_annotations(image, left_shoulder_elbow_angle, left_shoulder_angle, right_shoulder_elbow_angle, right_shoulder_angle, left_elbow, left_shoulder, right_elbow, right_shoulder):
    cv2.putText(image, f'Left elbow: {left_shoulder_elbow_angle:.0f}',
                tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(image, f'Left shoulder: {left_shoulder_angle:.0f}',
                tuple(np.multiply(left_shoulder, [640, 480]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(image, f'Right elbow: {right_shoulder_elbow_angle:.0f}',
                tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(image, f'Right shoulder: {right_shoulder_angle:.0f}',
                tuple(np.multiply(right_shoulder, [640, 480]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    return image

# Initialize Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

xs_time = []
ys = []

username = sys.argv[1]
movement = sys.argv[2]
timestamp = sys.argv[3]
save_folder = fr"data/output/{username}_{timestamp}"
file_name = f"{username}_{movement}_{timestamp}.csv"
file_name_video = f"mp_{username}_{movement}_{timestamp}.mp4"
file_name_video_black = f"landmarks_{username}_{movement}_{timestamp}.mp4"

save_file_path = os.path.join(save_folder, file_name)
save_file_path_video = os.path.join(save_folder, file_name_video)
save_file_path_video_black = os.path.join(save_folder, file_name_video_black)

# Start capturing video
cap = cv2.VideoCapture(0)  # görüntü girişinin seçildiği satır
# Save video
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc(*'H264')
video_out = cv2.VideoWriter(save_file_path_video, fourcc, 30, frame_size, isColor=False)


# Save video
fourcc1 = cv2.VideoWriter_fourcc(*'H264')
video_out_black = cv2.VideoWriter(save_file_path_video_black, fourcc1, 30, frame_size)

with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    start_time = time.time()

    with open(save_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Left_Shoulder_Elbow_Angle', 'Left_Shoulder_Angle',
                         'Right_Shoulder_Elbow_Angle', 'Right_Shoulder_Angle'])
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            try:
                left_landmarks = results.pose_landmarks.landmark
                left_shoulder = [left_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 left_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [left_landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              left_landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [left_landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              left_landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                left_hip = [left_landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                               left_landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_shoulder_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                left_shoulder_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
                                  #                     [left_shoulder[0], left_shoulder[1] + 0.1])
                cv2.putText(image, f'Left elbow: {left_shoulder_elbow_angle:.0f}',
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, f'Left shoulder: {left_shoulder_angle:.0f}',
                            tuple(np.multiply(left_shoulder, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                right_landmarks = results.pose_landmarks.landmark
                right_shoulder = [right_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  right_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [right_landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               right_landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [right_landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               right_landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                right_hip = [right_landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                               right_landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_shoulder_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                right_shoulder_angle = calculate_angle(right_elbow, right_shoulder, right_hip)
                                              #          [right_shoulder[0], right_shoulder[1] + 0.1])
                cv2.putText(image, f'Right elbow: {right_shoulder_elbow_angle:.0f}',
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, f'Right shoulder: {right_shoulder_angle:.0f}',
                            tuple(np.multiply(right_shoulder, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                current_time = time.time()                      # Şu anki zamanı al
                elapsed_time = current_time - start_time        # Geçen süreyi hesapla

                #current_time = datetime.datetime.now().strftime('%H.%M.%S.%f')
                writer.writerow([elapsed_time, left_shoulder_elbow_angle, left_shoulder_angle,
                             right_shoulder_elbow_angle, right_shoulder_angle])

            except:
                pass

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2) )

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            video_out.write(gray_image)


            black_image = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
            mp_drawing.draw_landmarks(black_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))

            black_image = add_annotations(black_image, left_shoulder_elbow_angle, left_shoulder_angle,
                                              right_shoulder_elbow_angle, right_shoulder_angle, left_elbow,
                                              left_shoulder, right_elbow, right_shoulder)

            video_out_black.write(black_image)


            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q') :

                break
            file.flush()
    cap.release()

video_out_black.release()
video_out.release()
cv2.destroyAllWindows()

dtwscore = read_and_plot_csv(f"data/input/movement_{movementMap().get(movement)}.csv",
                             f"data/output/{username}_{timestamp}/{username}_{movement}_{timestamp}.csv",username,movement,timestamp, showGraphs=False)
txt_file_path = os.path.join(f"data/output/{username}_{timestamp}", f"dtw_{username}_{movement}_{timestamp}.txt")
with open(txt_file_path, "w") as file:
    file.write(dtwscore)



# ftp.upload_file(save_file_path)
# ftp.upload_file(save_file_path_video)
#
# ftp.disconnect()

key_path = "awskey.pem"
hostname = "15.188.53.33"
username_aws = "ubuntu"

# remote_path = f'project/{file_name}'
# local_path = save_file_path
# upload_file_to_ec2(local_path, remote_path, key_path, hostname, username_aws)

remote_path = f'project/static/{file_name_video}'
local_path = save_file_path_video
upload_file_to_ec2(local_path, remote_path, key_path, hostname, username_aws)

remote_path = f'project/static/{file_name_video_black}'
local_path = save_file_path_video_black
upload_file_to_ec2(local_path, remote_path, key_path, hostname, username_aws)

remote_path = f'project/data/dtwfig_{username}_{movement}_{timestamp}.png'
local_path = f"data/output/{username}_{timestamp}/dtwfig_{username}_{movement}_{timestamp}.png"
upload_file_to_ec2(local_path, remote_path, key_path, hostname, username_aws)

