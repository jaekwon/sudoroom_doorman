# measures input audio for a loud squarewave tone.

import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
MEASURE_SECONDS = 5
MEASURE_SAMPLES = MEASURE_SECONDS * RATE

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

while True:
  data = stream.read(CHUNK)
  samples = wave.struct.unpack("%dh"%(len(data)/2), data)
  for sample in samples:
    sampleCount += 1
    sampleAbsSum += abs(sample)
  if sampleCount >= MEASURE_SAMPLES:
    print sampleCount, sampleAbsSum
    sampleAvgish = sampleAbsSum / float(sampleCount)
    sampleCount = 0
    sampleAbsSum = 0.0
    if sampleAvgish > 20000 and state is "OFF":
      print "ON"
      state = "ON"
    elif sampleAvgish < 10000 and state is "ON":
      print "OFF"
      state = "OFF"

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()
