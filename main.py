import serial
import speech_recognition as sr
import pywhatkit as kit  # For Google search and YouTube play
import time 
import pyttsx3
import noisereduce as nr
import numpy as np

# Set up serial communication with Arduino (adjust COM port if needed)
arduino = serial.Serial("COM6", 9600, timeout=1)  # Adjust COM port as needed
recognizer = sr.Recognizer()
engine = pyttsx3.init()

robot_name = 'Rex'

def listen_for_command():
    """ Listen for a command using speech recognition when sound level exceeds threshold """
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)

        # Convert audio to numpy array for noise reduction
        audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
        
        # Apply noise reduction
        reduced_noise = nr.reduce_noise(y=audio_data, sr=audio.sample_rate)

        # Create a new AudioData instance with the reduced noise
        reduced_audio = sr.AudioData(reduced_noise.tobytes(), audio.sample_rate, audio.sample_width)

        try:
            command = recognizer.recognize_google(reduced_audio)
            print(f"Command received: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I could not understand the command.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def main():
    while True:


        # Read sound level from Arduino
        if arduino.in_waiting > 0:
            try:
                data = arduino.readline().decode().strip()  # Read and decode Arduino data
                if data.isdigit():  # Check if the data is numeric
                    sound_level = int(data)
                    print(f"Sound Level: {sound_level}")

                    # If sound level exceeds a threshold, trigger speech recognition
                    if sound_level > 40:  # Adjust the threshold based on your testing
                        print("Sound level high enough, listening for command...")
                        command = listen_for_command()
                        if command:
                            # Process the command (e.g., play YouTube, search Google, etc.)
                            arduino.write(command.encode())     
                            print(f'Sent command to arduino: {command}')

                            if "play" in command:
                                print("Playing content on YouTube...")
                                engine.say("Playing content on YouTube...")
                                engine.runAndWait()
                                query = command.split("play", 1)[1].strip()
                                kit.playonyt(query)  # Play video on YouTube

                            elif "search" in command:
                                print("Searching on Google...")
                                engine.say("Searching on Google...")
                                query = command.split("search", 1)[1].strip()
                                kit.search(query)  # Search on Google
                                engine.runAndWait()

                            elif "hello" in command:
                                print("Hello! How can I assist you?")
                                engine.say('Hello! How can I assist you?')
                                time.sleep(2)
                                engine.runAndWait()

                            elif 'dance' in command:
                                print("Dancing...")
                                engine.say('Dancing')
                                time.sleep(1)
                                engine.runAndWait()

                            elif 'what is your name' in command:
                                print(f"My name is {robot_name}")
                                engine.say(f"My name is {robot_name}")
                                engine.runAndWait()

                            elif 'how are you' in command:
                                print("I'm doing well, thanks for asking!")
                                engine.say("I'm doing well, thanks for asking!")
                                engine.runAndWait()

                            elif "goodbye" in command:
                                print("Goodbye!")
                                engine.say("Goodbye!")
                                engine.runAndWait()                    
                                break

                    else:
                        print("Sound level too low, not triggering command.")
                else:
                    print(f"Invalid data received: {data}")

            except ValueError as e:
                print(f"Error reading sound level: {e}")
                continue

if __name__ == "__main__":
    main()