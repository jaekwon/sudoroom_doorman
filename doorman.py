# measures input audio for a loud squarewave tone.

import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1          # Make sure the audio input goes into the right channel (left/right)
RATE = 44100          # This is some factor more than our theoretical baudrate. We should also look into telephony software to accept dial tones for easy digial binary transfer.
MEASURE_SECONDS = .05   # Change this to make the script more or less sensitive to temporary pulses
MEASURE_SAMPLES = MEASURE_SECONDS * RATE

# Note: We just get the abs(sample) value, which is fine for square waves, but may not be for sinusoidal waves.
ON_THRESHOLD =  1000.0  # Note that the sample format is a signed 16bit int. If the sample amplitudes are higher than this, switch to 'on' state.
OFF_THRESHOLD = 800.0 # If the sample amplitudes are lower than this, switch to 'off' state.

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* listening *")

state = "OFF"
sampleCount = 0
sampleAbsSum = 0.0

def distanceBetweenClaps(clapOne, clapTwo)
  """Reports the positive definite amount of time between clapOne and ClapTwo)"""
  distance = 0
  return distance

def recognizePattern(clapList)
  #TODO
  return False

clapList = []

while True:
  data = stream.read(CHUNK) #get a CHUNK's worth of data, which is CHUNK number of samples
  samples = wave.struct.unpack("%dh"%(len(data)/2), data) #destructure a binary sting into a list of sample integers
  for sample in samples:
    sampleCount += 1 
    sampleAbsSum += abs(sample) #remove negativity
  #enter this next condition once MEASURE_SAMPLEs has elapsed
  if sampleCount >= MEASURE_SAMPLES:
    sampleAvgish = sampleAbsSum / float(sampleCount) #calculate the average "amplitude" (postive definite metric)
    #print sampleCount, sampleAvgish, (sampleAvgish > ON_THRESHOLD),  (sampleAvgish < OFF_THRESHOLD)
    if sampleAvgish > ON_THRESHOLD and state is "OFF":
      print "Clapped"
      clapList.append(datetime.datetime.now()) #add a clap event date to our list
      if len(clapList) > 100: #see if it's full
        clapList.pop(0) #remove the first object since it's full now
        if recognizePattern(clapList):
          print 'Would open door'
    sampleCount = 0 #reset
    sampleAbsSum = 0.0 #rest


print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()
