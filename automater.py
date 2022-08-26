import sys
import time
import logging
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

downloads_dir = ''
dest_dir_sfx = ''
dest_dir_music = ''
dest_dir_video = ''
dest_dir_image = ''
dest_dir_documents = ''

# supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

# supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

# supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

# supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]


def make_unique(dest, name):
  filename, extension = splitext(name)
  couter = 1
  while exists(f'{dest}/{name}'):
    name = f'{filename}-{str(counter)}{extension}'
    counter += 1

  return name


def move_file(dest, entry, name):
  if exists(f'{dest}/{name}'):
    unique_name = make_unique(dest, name)
    oldName = join(dest, name)
    newName = join(dest, unique_name)
    rename(oldName, newName)

  move(entry, dest)

class MoveHandler(FileSystemHandler):
  def on_modified(self, event):
    with os.scandir(downloads_dir) as entries:
      for entry in entries:
        name = entry.name
        filetype = name.spit('.')][-1].lower()
        self.check_audio(entry, name, filetype)
        self.check_document(entry, name, filetype)
        self.check_image(entry, name, filetype)
        self.check_video(entry, name, filetype)

  def check_audio(self, entry, name, filetype):
    if filetype in audio_extensions:
      if entry.stat().st_size < 10_1000_100:
        dest = dest_dir_sfx
      else:
        dest = dest_dir_music

      move_file(dest, entry, name)
      logging.info(f'Moved audio file: {name}')
  
  def check_video(self, entry, name, filetype):
    if filetype in video_extensions:
      move_file(dest_dir_video, entry, name)
      logging.info(f'Moved video file: {name}')

  def check_image(self, entry, name, filetype):
    if filetype in image_extensions:
      move_file(dest_dir_image, entry, name)
      logging.info(f'Moved image file: {name}')

  def check_document(self, entry, name):
    if filetype in document_extensions:
      move_file(dest_dir_documents, entry, name)
      logging.info(f'Moved document file: {name}')


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s - %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')

  path = downloads_dir
  event_handler = MoveHandler()
  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()

  try:
      while True:
          time.sleep(1)
  except KeyboardInterrupt:
      observer.stop()
  observer.join()