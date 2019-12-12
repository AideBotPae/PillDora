class SpeechSynth():
  def __init__(self, lang, name, text):
        self.lang = lang
        self.name = name
        self.text = text
  def Path(self):
        # Import the Gtts module for text to speech conversion 
        from gtts import gTTS 
        import pyaudio
        import os
        from pathlib import Path


        file = gTTS(text=self.text, lang=self.lang)
        file.save("/home/paesav/PAET2019/PillDora/server/Speech_Synth/audios/" + self.name + ".mp3") 

        #PLAY AUDIO
        #os.system("mpg321 --stereo /home/paesav/PAET2019/PillDora/server/Speech_Synth/audios/" + self.name + ".mp3")
        
        #os.remove(self.name + ".mp3")
        dir_path = os.path.dirname(os.path.realpath(self.name + ".mp3"))        
        return  dir_path