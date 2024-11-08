import os
import librosa
import sounddevice as sd
import keyboard

class TootBoard():
    
    _toots = []
    
    def __init__(self, file_paths):
        self._file_paths = file_paths
    
    def load_toots(self):
        if not self._file_paths: raise ValueError("No paths to the toots")
        if type(self._file_paths) != type([]): raise ValueError("file_paths must be a list")
        
        for path in self._file_paths:
            if os.path.isfile(path):
                self._toots.append(self._load_toot(path))
            elif os.path.isdir(path):
                print(f'Processing path {path}')
                self._process_toot_directory(path)
            else:
                raise ValueError("Path is not a valid file or directory name")
    
    def _load_toot(self, file_path):
        audio_data, sample_rate = librosa.load(file_path)
        print(f'{file_path}: Toot successfully loaded')
        return Toot(audio_data=audio_data, sample_rate=sample_rate, name=os.path.basename(file_path))
    
    def _process_toot_directory(self, directory_path):
        for filename in os.listdir(directory_path):
            # Create proper path for file
            full_path = os.path.join(directory_path, filename)
            if os.path.isfile(full_path) and os.path.splitext(full_path)[1] == ".wav":
                print(f'Loading {full_path}')
                self._toots.append(self._load_toot(full_path))
    
    def play_toot(self, index):
        
        # Bound the index
        index = max(min(index, len(self._toots) - 1), 0)
        
        print(f'Playing toot #{index}')
        
        sd.play(self._toots[index].get_audio_data(), self._toots[index].get_sample_rate())
        sd.wait()
        
        print('Toot successfully played!')
        

class Toot():
    
    __slots__ = ("_audio_data", "_sample_rate", "_name")
    
    def __init__(self, audio_data, sample_rate, name):
        self._audio_data = audio_data
        self._sample_rate = sample_rate
        self._name = name
        
    def get_audio_data(self):
        return self._audio_data
    
    def get_sample_rate(self):
        return self._sample_rate
    
    def get_name(self):
        return self._name
                
if __name__ == "__main__":
    toots = TootBoard(["./assets/sound/"])
    toots.load_toots()
    
    counter = 0
    while(True):
        if keyboard.is_pressed('space'):
            toots.play_toot(counter)
            counter += 1
    
    