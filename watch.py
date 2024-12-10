from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

def watch_files(event_handler_func, path='.', regexes=None, ignore_regexes = None, ignore_directories = False, case_sensitive = True):
    my_event_handler = RegexMatchingEventHandler(regexes, ignore_regexes, ignore_directories, case_sensitive)
    my_event_handler.on_modified = event_handler_func

    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=True)

    return my_observer
