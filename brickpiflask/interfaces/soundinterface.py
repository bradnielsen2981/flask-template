import speake3
import pygame

class SoundInterface():
    
    def __init__(self):
        self.engine = speake3.Speake()
        self.engine.set('voice', 'en-scotish')
        self.engine.set('speed', '150')
        self.engine.set('pitch', '60')
        #load music player
        pygame.mixer.init()
        return
    
    def get_all_voices(self):
        #shows all the voices that could be selected
        voices = self.engine.get("voices")
        for voice in voices:
            print(voice)
        #shows all english voices
        voices_2 = self.engine.get("voices", "en")
        for voice in voices_2:
            print(voice)
        return
    
    def say(self, message):
        #gets robot to speak word or phrase
        self.engine.say(message)
        self.engine.talkback()
        return

    def load_mp3(self, song):
        pygame.mixer.music.load(song)
        #saves the song as something recongniseable
        return
    
    def play_music(self, times = -1):
        pygame.mixer.music.play(times)
        return
    
    def pause_music(self):
        pygame.mixer.music.pause()
        return
    
    def unpause_music(self):
        pygame.mixer.music.unpause()
        return

    def stop_music(self):
        pygame.mixer.music.stop()
        return

    def set_volume(self, v=0.8):
        pygame.mixer.music.set_volume(v)
        return


#---------------------------------------------
#only execute if this is the main file, good for testing code.
        
if __name__ == "__main__":
    SOUND = SoundInterface()
    SOUND.load_mp3("inspectorgadget.mp3")
    #letting the user know help is on the way
    SOUND.say("I am on a mission to mine martian ice.")
    print("finished")
    SOUND.play_music(1)
    SOUND.set_volume(0.6)
    reponse = input("Press Enter to stop")
    SOUND.stop_music()

    
    
    
    