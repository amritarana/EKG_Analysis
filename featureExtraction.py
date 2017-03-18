import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pywt

def plotWave(y, title, xLab, folder = ""):
    # ignore time values, just use indices, get's iterated by 0.003 starting at 0
    plt.plot(y)
    plt.ylabel("mV")
    plt.xlabel(xLab)
    plt.title(title)
    if folder != "":
        plt.savefig(folder + title + ".png")
    plt.show()

EKG = pd.read_csv("../MIT-BIH_Arrhythmia/100.csv", header=None)

plotData = EKG[2:502]

x = np.asarray(plotData[0])
y = np.asarray(pd.to_numeric(plotData[1]))

# Wavelet transforms, using pywavelets

cA = y
plotWave(cA, "Original", "Index 1n * 0.003")
pointsNum = len(cA)

# level is the last index in list - 1
# currLevel of original ^^ is totalLevels + 1
# index kn * 0.003 k is (totalLevels - currLevel) + 2
# cDK K is (totalLevels - currLevel) + 1
# max pywavelets level is 4 for 200, 6 for 500, etc.
wavelet = 'sym4'
levels = 6
mode = 'constant'
coeffs = pywt.wavedecn(cA, wavelet, level=levels, mode=mode)
# np.set_printoptions(threshold=np.nan)

for i in range(1 + 2,levels + 1):
    index = i
    smallK = (levels - i) + 2
    bigK = (levels - i) + 1
    plotWave(coeffs[index]['d'], "cD" + str(bigK), "Index " + str(smallK) + "n * 0.003")

rebuilt = pywt.waverecn(coeffs, wavelet, mode=mode)
plotWave(rebuilt, "rebuilt1", "hopefully correct indices")

# Write automating function for coefficient omission
# Removing cA, cD1, cD2, and cD6
coeffs[-1] = {k: np.zeros_like(v) for k, v in coeffs[-1].items()}
coeffs[-2] = {k: np.zeros_like(v) for k, v in coeffs[-2].items()}
coeffs[-6] = {k: np.zeros_like(v) for k, v in coeffs[-6].items()}
coeffs[0] = np.zeros_like(coeffs[0])
rebuilt = pywt.waverecn(coeffs, wavelet, mode=mode)
plotWave(rebuilt, "rebuilt2", "hopefully correct indices")


# Imperatively grabbing features

# grab max and see if it matches with original signal
xMax = np.argmax(rebuilt)
print(xMax)
print(cA[xMax])
print(cA[np.argmax(cA)])

