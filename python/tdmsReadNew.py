import matplotlib.pyplot as plt
from nptdms import TdmsFile
import tkinter as tk
from tkinter.filedialog import askopenfilename
import numpy as np
from scipy.signal import butter, filtfilt
from scipy.interpolate import splev, splrep
import pandas as pd
import similaritymeasures

# Initialize Tkinter and hide the main window
root = tk.Tk()
root.withdraw()

# Open the simulated pressure file
digital_twin_pressure = pd.read_csv('C:/Users/10521/Documents/GitHub/Aquaman/lily-pad-master/LilyPad/testDataSave/pressure_map_test.csv', header=None)
digital_twin_pressure_REF = pd.read_csv('C:/Users/10521/Documents/GitHub/Aquaman/lily-pad-master/LilyPad/testDataSave/old/pressure_map_test_REF.csv', header=None)

# Open the file dialog to choose a file and get the file path
chemin_fichier = 'C:/Users/10521/Documents/GitHub/Aquaman/lily-pad-master/LilyPad/testDataSave/old/T3_Fish3_270923.tdms'

# Check if a file was selected
if chemin_fichier:
    # Read the TDMS file
    tdms_file = TdmsFile.read(chemin_fichier)

    # Set the cutoff frequency for the low-pass filter to 50Hz
    fc = 50.0

    # Assume a fixed sampling frequency for all channels
    fe = 500  # Sampling frequency in Hz, adjust according to your data

    # Count the total number of channels to size the subplot grid
    nombre_canaux = sum(len(group.channels()) for group in tdms_file.groups())
    nrows = int(np.ceil(np.sqrt(nombre_canaux)))
    ncols = nrows

    fig, axs = plt.subplots(nrows, ncols, figsize=(15, 15))
    axs = axs.flatten()  # Flatten the axes array for easier access
    channel_idx = 0

    # Iterate over all groups and channels in the TDMS file
    for group in tdms_file.groups():
        for channel in group.channels():
            if channel.name in ['S2', 'S4', 'S7']:
                data = channel.data
                if channel.name == 'S4':
                    dt_data = [digital_twin_pressure[i][210*128+39] for i in digital_twin_pressure.columns]
                    dt_data_REF = [digital_twin_pressure_REF[i][210*128+39] for i in digital_twin_pressure_REF.columns]
                if channel.name == 'S2':
                    dt_data = [digital_twin_pressure[i][164*128+127-39] for i in digital_twin_pressure.columns]
                    dt_data_REF = [digital_twin_pressure_REF[i][164*128+127-39] for i in digital_twin_pressure_REF.columns]
                if channel.name == 'S7':
                    dt_data = [-digital_twin_pressure[i][105*128+39] for i in digital_twin_pressure.columns]
                    dt_data_REF = [-digital_twin_pressure_REF[i][105*128+39] for i in digital_twin_pressure_REF.columns]

                # Generate a time sequence if possible
                if hasattr(channel, 'time_track'):
                    time = channel.time_track()
                else:
                    time = [i / fe for i in range(len(data))]
                dt_time = np.linspace(19.5, 21.75, len(dt_data))
                dt_time_REF = np.linspace(19.5, 21.75, len(dt_data_REF))

                time = time[int(19.5*500):int(21.75*500)]

                # Create a low-pass filter
                order = 2  # Filter order
                nyquist = 0.5 * fe
                normal_frequency = fc / nyquist
                b, a = butter(order, normal_frequency, btype='low', analog=False)

                # Apply the filter
                filtered_data = filtfilt(b, a, data)
                filtered_data = filtered_data[int(19.5*500):int(21.75*500)]
                mean_filtered_data = np.mean(filtered_data)

                # Configure the plot
                axs[channel_idx].plot(time, filtered_data - mean_filtered_data)
                axs[channel_idx].plot(dt_time, [k * 1025 * 0.0275 * 0.0275 for k in dt_data])
                axs[channel_idx].plot(dt_time_REF, [k * 1025 * 0.0275 * 0.0275 for k in dt_data_REF])
                axs[channel_idx].set_title(f'{channel.name}')
                axs[channel_idx].set_xlabel('Time (s)')
                axs[channel_idx].set_ylabel('Pressure (Pa)')
                axs[channel_idx].grid(True)

                # Calculate the discrete Fréchet distance
                exp_data = np.zeros((len(time), 2))
                exp_data[:, 0] = filtered_data - mean_filtered_data
                exp_data[:, 1] = time
                num_data = np.zeros((len(dt_time), 2))
                num_data[:, 0] = [k * 1025 * 0.0275 * 0.0275 for k in dt_data]
                num_data[:, 1] = dt_time
                num_data_REF = np.zeros((len(dt_time_REF), 2))
                num_data_REF[:, 0] = [k * 1025 * 0.0275 * 0.0275 for k in dt_data_REF]
                num_data_REF[:, 1] = dt_time_REF

                dist = similaritymeasures.frechet_dist(exp_data, num_data)
                dist_REF = similaritymeasures.frechet_dist(exp_data, num_data_REF)
                print("Discrete Fréchet distance between sensor curve and HAACHAMA curve: ", dist)
                print("Discrete Fréchet distance between sensor curve and perfect DT curve: ", dist_REF)

                channel_idx += 1

    # Hide unused axes if the number of channels is not a perfect square
    for idx in range(channel_idx, len(axs)):
        axs[idx].set_visible(False)

    plt.tight_layout()
    plt.show()
else:
    print("No file selected.")
