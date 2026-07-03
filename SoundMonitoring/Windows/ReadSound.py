import serial
import time
from pycaw.pycaw import AudioUtilities
from dashboard import startDash, updateSound

PORT = "COM3"
BAUD = 9600

base = 204
num_samples = 10

samples = [0] * num_samples
index = 0
total = 0

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

startDash()

print("Dashboard: http://127.0.0.1:5000")


def getSound():
    sound_value = ser.readline().decode().strip()
    updateSound(sound_value)
    return sound_value

def numOverX(number):
    if(int(getSound()) > number):
        return True

speakers = AudioUtilities.GetSpeakers()
volume = speakers.EndpointVolume
def lowerVolume(vol):

    vol = (vol - 1)/99
    current_scalar = volume.GetMasterVolumeLevelScalar()
    newVol = current_scalar - vol
    volume.SetMasterVolumeLevelScalar(newVol, None)
    print(f"Vol. set to: {newVol}")
    time.sleep(.2)



while True:
    numRn = getSound()
    if(numOverX(25)):
        lowerVolume(5)
