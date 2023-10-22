from date import datetime
from logging.config import listen
import speech_recognition as sr     # standard speech recognition library
import pyttsx3                      # text to speech library
import webbrowser                   # webbrowser library
import wikipedia
import wolframalpha

### IMPORTANT NOTES ### 
# need to pip install all of these requirements
# need to download Pyaudio for this to work! 


# Speech engine initialisation
engine = pyttsx3.init()                         # initializing the speech engine
voices = engine.getProperty('voices')           
engine.setProperty('voice', voices[0].id)       # options: 0 = male, 1 = female
activationWord = 'Christopher'                  # Single word activation   
                                                # listens for this word in order to trigger a command
 

# Configure browser
# Set the path for whichever browser you wish to use
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# method that allows the text to speech library to be useful
def speak(text, rate = 120):            # rate = how fast the AI voice speaks
    engine.setProperty('rate', rate)    
    engine.say(text)
    engine.runAndWait()                 


# method for the system to listen to commands and convert to text
def parseCommand():
    listener = sr.Recognizer()          # uses microphone and parses voice into text
    print('Listening for a command')
 
    with sr.Microphone() as source:
        listener.pause_threshold = 2               # the gap in your speech before it ends the listening
        input_speech = listener.listen(source)      
 
    try: 
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en_gb')       # language set to english
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')         # calls speak method to say this outloud
        print(exception)
        return 'None'
 
    return query



#############################################################################

# Main loop
if __name__ == '__main__':
    speak('Hello Sir. How can I help you?')
 
    while True:             # listen for commands until we jump out of it
        
        # Parse speech input as a list
        
        query = parseCommand().lower().split()      # gets a list of words
 

        if query[0] == activationWord:              # each command must start with the activation word
            query.pop(0)                            # remove activation word from query
 

            # List commands
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Hello')
                else: 
                    query.pop(0)                    # Remove 'say'
                    speech = ' '.join(query)
                    speak(speech)                   # echos what you say to it
 
            # Navigation to a website
            if query[0] == 'go' and query[1] == 'to':
                speak('Please wait a moment...')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)
                
 
            # Wikipedia 
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Querying the universal databank.')
                speak(search_wikipedia(query))