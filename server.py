import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class Watcher:
    DIRECTORY_TO_WATCH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        
        print(f"Watching directory: {self.DIRECTORY_TO_WATCH}")
        print(f"Starting main.py ...")
        
        subprocess.Popen([sys.executable, 'main.py'])
        
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'modified':
            print(f"Received modified event - {event.src_path}")
            restart_script()
            
            
def restart_script():
    if hasattr(restart_script, 'process') and restart_script.process.poll() is None:
        restart_script.process.terminate()
        restart_script.process.wait()
    
    restart_script.process = subprocess.Popen([sys.executable, 'main.py'])

if __name__ == '__main__':
    w = Watcher()
    w.run()
