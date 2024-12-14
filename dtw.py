import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dtaidistance import dtw


def normalize(series):
    """Normalize a Pandas Series to the range [0, 1]."""
    return (series - series.min()) / (series.max() - series.min())


def scale_and_interpolate(time, data, common_time):
    """Scale and interpolate data to match the common time axis."""
    # Calculate the scaling factor
    scale_factor = len(common_time) / len(time)

    # Resample the time and data to match the length of common_time
    resampled_time = np.linspace(time.min(), time.max(), num=len(common_time))

    # Interpolate data to the resampled time axis
    interpolated_data = np.interp(resampled_time, time, data, left=np.nan, right=np.nan)

    # Handle NaNs by filling forward and backward
    interpolated_data = pd.Series(interpolated_data).ffill().bfill().values

    return interpolated_data


def read_and_plot_csv(file_path1, file_path2,username,movement,timestamp,showGraphs=False):
    # Read the CSV files into DataFrames
    df1 = pd.read_csv(file_path1)
    df2 = pd.read_csv(file_path2)

    # Ensure the required columns are present
    required_columns = ['Time', 'Left_Shoulder_Elbow_Angle', 'Left_Shoulder_Angle']
    if not all(col in df1.columns for col in required_columns):
        raise ValueError(f"Missing columns in file: {file_path1}")
    if not all(col in df2.columns for col in required_columns):
        raise ValueError(f"Missing columns in file: {file_path2}")

    # Extract the relevant columns
    time1 = df1['Time']
    data1_left_shoulder_elbow = df1['Left_Shoulder_Elbow_Angle']
    data1_left_shoulder = df1['Left_Shoulder_Angle']

    time2 = df2['Time']
    data2_left_shoulder_elbow = df2['Left_Shoulder_Elbow_Angle']
    data2_left_shoulder = df2['Left_Shoulder_Angle']

    # Determine the common time range
    max_time = max(time1.max(), time2.max())
    min_time = min(time1.min(), time2.min())
    common_time = np.linspace(min_time, max_time, num=max(len(time1), len(time2)))

    # Interpolate both data sets to the common time axis
    data1_left_shoulder_elbow_interpolated = scale_and_interpolate(time1, data1_left_shoulder_elbow, common_time)
    data2_left_shoulder_elbow_interpolated = scale_and_interpolate(time2, data2_left_shoulder_elbow, common_time)

    data1_left_shoulder_interpolated = scale_and_interpolate(time1, data1_left_shoulder, common_time)
    data2_left_shoulder_interpolated = scale_and_interpolate(time2, data2_left_shoulder, common_time)

    # Normalize the interpolated data
    data1_left_shoulder_elbow_normalized = normalize(pd.Series(data1_left_shoulder_elbow_interpolated))
    data2_left_shoulder_elbow_normalized = normalize(pd.Series(data2_left_shoulder_elbow_interpolated))

    data1_left_shoulder_normalized = normalize(pd.Series(data1_left_shoulder_interpolated))
    data2_left_shoulder_normalized = normalize(pd.Series(data2_left_shoulder_interpolated))

    # Compute DTW distances
    dtw_distance_elbow = dtw.distance(data1_left_shoulder_elbow_normalized, data2_left_shoulder_elbow_normalized)
    dtw_distance_shoulder = dtw.distance(data1_left_shoulder_normalized, data2_left_shoulder_normalized)
    dtwavg = (dtw_distance_shoulder + dtw_distance_elbow) / 2
    print("DTW Distance for Left_Shoulder_Elbow_Angle:", dtw_distance_elbow)
    print("DTW Distance for Left_Shoulder_Angle:", dtw_distance_shoulder)
    print("Avg Distance:", dtwavg)

    if 0 <= dtwavg < 1.3:
        print("The movement was done well !")
    elif 1.3 <= dtwavg <= 1.7:
        print("The movement was done okay !")
    else:
        print("The movement wasn't done well")


    # Plot Time vs Normalized Data
    plt.figure(figsize=(14, 6))

    # Plot Left_Shoulder_Elbow_Angle
    plt.subplot(1, 2, 1)
    plt.plot(common_time, data1_left_shoulder_elbow_normalized, label='Left_Shoulder_Elbow_Angle (File 1)',
                 color='blue')
    plt.plot(common_time, data2_left_shoulder_elbow_normalized, label='Left_Shoulder_Elbow_Angle (File 2)',
                 color='orange')
    plt.xlabel('Time')
    plt.ylabel('Normalized Left_Shoulder_Elbow_Angle')
    plt.title('Time vs Normalized Left_Shoulder_Elbow_Angle')
    plt.legend()

    # Plot Left_Shoulder_Angle
    plt.subplot(1, 2, 2)
    plt.plot(common_time, data1_left_shoulder_normalized, label='Left_Shoulder_Angle (File 1)', color='green')
    plt.plot(common_time, data2_left_shoulder_normalized, label='Left_Shoulder_Angle (File 2)', color='red')
    plt.xlabel('Time')
    plt.ylabel('Normalized Left_Shoulder_Angle')
    plt.title('Time vs Normalized Left_Shoulder_Angle')
    plt.legend()

    # Show plots
    plt.tight_layout()

    if showGraphs==False:
        img_path = f"data/output/{username}_{timestamp}/dtwfig_{username}_{movement}_{timestamp}"
        plt.savefig(img_path)
        result = f"{dtw_distance_elbow:.3f} {dtw_distance_shoulder:.3f} {dtwavg:.3f}"
        return result

    else:
        plt.show()



## File paths for the two CSV files
#file_path1 = r'Veriler\azizideal_Hareket1_20240823_1033.csv'
#file_path2 = r'Veriler\azizok1_Hareket1_20240809_1841.csv'
## Read, normalize, interpolate, plot, and show data from both CSV files
#a=read_and_plot_csv(file_path1, file_path2,"azizok1","Hareket1","20240809_1841",showGraphs=True)
#print(f"DTW png was saved!!")
#print(a)