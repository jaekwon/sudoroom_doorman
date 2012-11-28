# measures input audio for a loud squarewave tone.

import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1          # Make sure the audio input goes into the right channel (left/right)
RATE = 44100          # This is some factor more than our theoretical baudrate. We should also look into telephony software to accept dial tones for easy digial binary transfer.
MEASURE_SECONDS = 5   # Change this to make the script more or less sensitive to temporary pulses
MEASURE_SAMPLES = MEASURE_SECONDS * RATE

# Note: We just get the abs(sample) value, which is fine for square waves, but may not be for sinusoidal waves.
ON_THRESHOLD = 20000  # Note that the sample format is a signed 16bit int. If the sample amplitudes are higher than this, switch to 'on' state.
OFF_THRESHOLD = 10000 # If the sample amplitudes are lower than this, switch to 'off' state.

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
    if sampleAvgish > ON_THRESHOLD and state is "OFF":
      print "ON"
      state = "ON"
    elif sampleAvgish < OFF_THRESHOLD and state is "ON":
      print "OFF"
      state = "OFF"

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()
