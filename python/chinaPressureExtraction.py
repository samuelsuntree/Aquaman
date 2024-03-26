import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

input_folder = "C:/Users/blagn771/Documents/Aquaman/Aquaman/lily-pad-master/LilyPad/chinaBenchmark/pressureMotion.txt"
output = []

with open(input_folder, 'r') as pressure:
    for line in pressure:
        output.append(line)

X = output[1][12:-3].split()
for i in range(len(X)):
    X[i] = float(X[i])
X = np.array(X)
index_min = np.where(X == X.min())

X_ordered = np.roll(X, shift=index_min[0], axis=0)
sensor = np.round(np.linspace(0,99,17)).astype(np.int16)
sensor = sensor[:-1]
X_sensor = X_ordered[sensor]

data = output[4:]
wall, cylinder, time = [], [], []
for i in range(len(data)):
    to_add = data[i].split()
    if to_add[-1] == ';':
        to_add.pop()
    to_add = np.array(to_add)
    to_add = to_add.astype(np.float32)
    if i % 2 == 0:
        time.append(to_add[0])
        to_add_ordered = np.roll(to_add[1:], shift=index_min[0], axis=0)
        to_add_sensor = to_add_ordered[sensor]
        cylinder.append(to_add_sensor)
    else:
        wall.append(to_add)

cylinder_dataframe = pd.DataFrame(cylinder)
wall_dataframe = pd.DataFrame(wall)

fig = plt.figure()
ax1 = fig.add_subplot(4,4,1)
ax1 = plt.plot(time[4:],cylinder_dataframe[0][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=π")
plt.ylim(-2.25,1.5)
ax2 = fig.add_subplot(4,4,2)
ax2 = plt.plot(time[4:],cylinder_dataframe[1][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=π+π/8")
plt.ylim(-2.25,1.5)
ax3 = fig.add_subplot(4,4,3)
ax3 = plt.plot(time[4:],cylinder_dataframe[2][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=π+2π/8")
plt.ylim(-2.25,1.5)
ax4 = fig.add_subplot(4,4,4)
ax4 = plt.plot(time[4:],cylinder_dataframe[3][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=π+3π/8")
plt.ylim(-2.25,1.5)
ax5 = fig.add_subplot(4,4,5)
ax5 = plt.plot(time[4:],cylinder_dataframe[4][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=π+4π/8")
plt.ylim(-2.25,1.5)
ax6 = fig.add_subplot(4,4,6)
ax6 = plt.plot(time[4:],cylinder_dataframe[5][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=π+5π/8")
plt.ylim(-2.25,1.5)
ax7 = fig.add_subplot(4,4,7)
ax7 = plt.plot(time[4:],cylinder_dataframe[6][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=π+6π/8")
plt.ylim(-2.25,1.5)
ax8 = fig.add_subplot(4,4,8)
ax8 = plt.plot(time[4:],cylinder_dataframe[7][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=π+7π/8")
plt.ylim(-2.25,1.5)
ax9 = fig.add_subplot(4,4,9)
ax9 = plt.plot(time[4:],cylinder_dataframe[8][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=0")
plt.ylim(-2.25,1.5)
ax10 = fig.add_subplot(4,4,10)
ax10 = plt.plot(time[4:],cylinder_dataframe[9][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=π/8")
plt.ylim(-2.25,1.5)
ax11 = fig.add_subplot(4,4,11)
ax11 = plt.plot(time[4:],cylinder_dataframe[10][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=2π/8")
plt.ylim(-2.25,1.5)
ax12 = fig.add_subplot(4,4,12)
ax12 = plt.plot(time[4:],cylinder_dataframe[11][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=3π/8")
plt.ylim(-2.25,1.5)
ax13 = fig.add_subplot(4,4,13)
ax13 = plt.plot(time[4:],cylinder_dataframe[12][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=4π/8")
plt.ylim(-2.25,1.5)
ax14 = fig.add_subplot(4,4,14)
ax14 = plt.plot(time[4:],cylinder_dataframe[13][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=5π/8")
plt.ylim(-2.25,1.5)
ax15 = fig.add_subplot(4,4,15)
ax15 = plt.plot(time[4:],cylinder_dataframe[14][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=6π/8")
plt.ylim(-2.25,1.5)
ax16 = fig.add_subplot(4,4,16)
ax16 = plt.plot(time[4:],cylinder_dataframe[15][4:])
plt.grid()
plt.title("Cp on the cylinder at θ=7π/8")
plt.ylim(-2.25,1.5)

fig.suptitle("Evolution of Cp with time at different position on the cylinder")
plt.show()

fig3 = plt.figure()
theta = np.linspace(180,540,17)
meanCp = [np.mean(cylinder_dataframe[i][4:]) for i in range(len(cylinder_dataframe.columns))]
meanCp.append(np.mean(cylinder_dataframe[0][4:]))
plt.grid()
plt.title("Mean Cp variation around the cylinder")
plt.xlabel("Theta (in deg)")
plt.ylabel("mean Cp")
plt.plot(theta, meanCp)
plt.ylim(-0.85,0.6)
plt.show()

fig2 = plt.figure()
ax1 = fig2.add_subplot(4,6,1)
ax1 = plt.plot(time[4:],wall_dataframe[0][4:])
plt.grid()
plt.title("Cp on the wall at n")
plt.ylim(-1,0.4)
ax2 = fig2.add_subplot(4,6,2)
ax2 = plt.plot(time[4:],wall_dataframe[1][4:])
plt.grid()
plt.title("Cp on the wall at n+L")
plt.ylim(-1,0.4)
ax3 = fig2.add_subplot(4,6,3)
ax3 = plt.plot(time[4:],wall_dataframe[2][4:])
plt.grid()
plt.title("Cp on the wall at n+2L")
plt.ylim(-1,0.4)
ax4 = fig2.add_subplot(4,6,4)
ax4 = plt.plot(time[4:],wall_dataframe[3][4:])
plt.grid()
plt.title("Cp on the wall at n+3L")
plt.ylim(-1,0.4)
ax5 = fig2.add_subplot(4,6,5)
ax5 = plt.plot(time[4:],wall_dataframe[4][4:])
plt.grid()
plt.title("Cp on the wall at n+4L")
plt.ylim(-1,0.4)
ax6 = fig2.add_subplot(4,6,6)
ax6 = plt.plot(time[4:],wall_dataframe[5][4:])
plt.grid()
plt.title("Cp on the wall at n+5L")
plt.ylim(-1,0.4)
ax7 = fig2.add_subplot(4,6,7)
ax7 = plt.plot(time[4:],wall_dataframe[6][4:])
plt.grid()
plt.title("Cp on the wall at n+6L")
plt.ylim(-1,0.4)
ax8 = fig2.add_subplot(4,6,8)
ax8 = plt.plot(time[4:],wall_dataframe[7][4:])
plt.grid()
plt.title("Cp on the wall at n+7L")
plt.ylim(-1,0.4)
ax9 = fig2.add_subplot(4,6,9)
ax9 = plt.plot(time[4:],wall_dataframe[8][4:])
plt.grid()
plt.title("Cp on the wall at n+8L")
plt.ylim(-1,0.4)
ax10 = fig2.add_subplot(4,6,10)
ax10 = plt.plot(time[4:],wall_dataframe[9][4:])
plt.grid()
plt.title("Cp on the wall at n+9L")
plt.ylim(-1,0.4)
ax11 = fig2.add_subplot(4,6,11)
ax11 = plt.plot(time[4:],wall_dataframe[10][4:])
plt.grid()
plt.title("Cp on the wall at n+10L")
plt.ylim(-1,0.4)
ax12 = fig2.add_subplot(4,6,12)
ax12 = plt.plot(time[4:],wall_dataframe[11][4:])
plt.grid()
plt.title("Cp on the wall at n+11L")
plt.ylim(-1,0.4)
ax13 = fig2.add_subplot(4,6,13)
ax13 = plt.plot(time[4:],wall_dataframe[12][4:])
plt.grid()
plt.title("Cp on the wall at n+12L")
plt.ylim(-1,0.4)
ax14 = fig2.add_subplot(4,6,14)
ax14 = plt.plot(time[4:],wall_dataframe[13][4:])
plt.grid()
plt.title("Cp on the wall at n+13L")
plt.ylim(-1,0.4)
ax15 = fig2.add_subplot(4,6,15)
ax15 = plt.plot(time[4:],wall_dataframe[14][4:])
plt.grid()
plt.title("Cp on the wall at n+14L")
plt.ylim(-1,0.4)
ax16 = fig2.add_subplot(4,6,16)
ax16 = plt.plot(time[4:],wall_dataframe[15][4:])
plt.grid()
plt.title("Cp on the wall at n+15L")
plt.ylim(-1,0.4)
ax17 = fig2.add_subplot(4,6,17)
ax17 = plt.plot(time[4:],wall_dataframe[16][4:])
plt.grid()
plt.title("Cp on the wall at n+16L")
plt.ylim(-1,0.4)
ax18 = fig2.add_subplot(4,6,18)
ax18 = plt.plot(time[4:],wall_dataframe[17][4:])
plt.grid()
plt.title("Cp on the wall at n+17L")
plt.ylim(-1,0.4)
ax19 = fig2.add_subplot(4,6,19)
ax19 = plt.plot(time[4:],wall_dataframe[18][4:])
plt.grid()
plt.title("Cp on the wall at n+18L")
plt.ylim(-1,0.4)
ax20 = fig2.add_subplot(4,6,20)
ax20 = plt.plot(time[4:],wall_dataframe[19][4:])
plt.grid()
plt.title("Cp on the wall at n+19L")
plt.ylim(-1,0.4)
ax21 = fig2.add_subplot(4,6,21)
ax21 = plt.plot(time[4:],wall_dataframe[20][4:])
plt.grid()
plt.title("Cp on the wall at n+20L")
plt.ylim(-1,0.4)

fig2.suptitle("Evolution of Cp with time at different position on the wall")
plt.show()

concat_wall = pd.concat([wall_dataframe[i][4:] for i in range(len(wall_dataframe.columns))], ignore_index=True)
N = len(concat_wall)
T = np.mean([time[i+1]-time[i] for i in range(len(time)-1)])
print(T)
wall_f = fft(np.array(concat_wall))
xf = fftfreq(N,T)[:N//2]
fig4 = plt.figure()
plt.plot(xf, 2.0/N * np.abs(wall_f[0:N//2]))
plt.grid()
plt.ylim(-0.0025,0.0325)
plt.show()