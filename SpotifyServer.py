import time

class SpotifyServer:
    def __init__(self):
        self.available = True
        self.buffered_music = True  # Simula o armazenamento temporário da música

    def simulate_music_playback(self):
        if not self.available and not self.buffered_music:
            raise Exception("Falha no servidor e sem buffer disponível!")
        return True

    def restore_connection(self):
        time.sleep(2)  # Simula tempo de reconexão
        self.available = True