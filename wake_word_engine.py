import pvporcupine
import pyaudio
import struct
import webbrowser

ACCESS_KEY = "YOUR_PICOVOICE_KEY"
WAKE_WORD = "jarvis"   # or your trained "hey aris" model file

def start_wake_word():

    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keywords=[WAKE_WORD]
    )

    pa = pyaudio.PyAudio()

    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("🔥 Wake Word Engine Running...")

    while True:
        pcm = stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        result = porcupine.process(pcm)

        if result >= 0:
            print("✅ WAKE WORD DETECTED")
            print("🔥 WAKE ENGINE STARTED")

            # ACTION
            webbrowser.open("http://127.0.0.1:1490")