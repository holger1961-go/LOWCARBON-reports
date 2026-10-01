
import datetime
import inspect
import os


@staticmethod
def _date_full():
    return datetime.datetime.now()
@staticmethod
def _date_short():
    return datetime.datetime.now().strftime("%Y-%m-%d")
@staticmethod
def _time_short():
    return datetime.datetime.now().strftime("%H:%M:%S")
@staticmethod
def _date_time_short():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
@staticmethod
def _date_time_file():
    return datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S")
@staticmethod
def _date_year():
    return datetime.datetime.now().strftime("%Y")
@staticmethod
def _date_week():
    return datetime.datetime.now().strftime("%V")
@staticmethod
def _date_weekday():
    return datetime.datetime.now().weekday() + 1


@staticmethod
def __log_print(message, log_type: str = "info", def_name: str ="", line_number_in: int = None):
    match log_type:
        case "error":
            print(f"█ ERROR ██████████████████████████ [# {line_number_in}] ERROR: {message}")
        case "todo":
            print(f"{" " * 5}█ [# {line_number_in}] TODO: {message}")
        case "title":
            if message == "":
                print(f"{" " * 3}●●● [# {line_number_in}] TITLE / NAME:\n{" " * 20}'{def_name}'")
            else:
                print(f"{" " * 3}●●● [# {line_number_in}] TITLE / NAME:\n{" " * 20}'{def_name}'\n{" " * 21}{message}")
        case "loop":
            print(f"{" " * 5}● [# {line_number_in}] LOOP: ● ●  ●   ●     ● {message} ●     ●   ●   ● ●")
        case "mark":
            print(f"{" " * 3}█ MARK █\n{" " * 3}███ {_date_time_short()}\n{" " * 3}███ [# {line_number_in}] MARK: {message}")
        case "end":
            print(f"{" " * 5}● [# {line_number_in}] INFO: {message}\r", end = "")
        case "line":
            print(f"{" " * 3}●●●●●●●●\n{" " * 3}●●●●●●●●●●●●●●●●●●●●●●●● {message} ●●●●●●●●●●●●●●●●●●●●●●●●\n{" " * 3}●●●●●●●●{" " * 5}{_date_time_short()}")
        case "debug":
            print(f"{" " * 5}● [# {line_number_in}] DEBUG: {message}")
        case "info":
            print(f"{" " * 5}● [# {line_number_in}] INFO: {message}")

@staticmethod
def error(message):
    caller_frame = inspect.currentframe().f_back
    line_number = caller_frame.f_lineno
    __log_print(message, log_type="error", line_number_in=line_number)

@staticmethod
def todo(message):
    caller_frame = inspect.currentframe().f_back
    line_number = caller_frame.f_lineno
    __log_print(message, log_type="todo", line_number_in=line_number)

@staticmethod
def title(message = ""):
    caller_frame = inspect.currentframe().f_back
    def_name = caller_frame.f_code.co_name
    line_number = caller_frame.f_lineno
    __log_print(message, log_type="title", def_name = def_name, line_number_in=line_number)

@staticmethod
def loop(message):
    caller_frame = inspect.currentframe().f_back
    line_number = caller_frame.f_lineno
    __log_print(message, log_type="loop", line_number_in=line_number)

@staticmethod
def mark(message):
    caller_frame = inspect.currentframe().f_back
    line_number = caller_frame.f_lineno
    __log_print(message, log_type="mark", line_number_in=line_number)

@staticmethod
def line(message):
    caller_frame = inspect.currentframe().f_back
    line_number = caller_frame.f_lineno
    __log_print(message, log_type="line", line_number_in=line_number)    


@staticmethod
def info(message, typ = "info", debug_level: int = 0):
    caller_frame = inspect.currentframe().f_back
    line_number = caller_frame.f_lineno
    if typ == "info":
        __log_print(message, log_type="info", line_number_in=line_number)
    elif typ == "end":
        __log_print(message, log_type="end", line_number_in=line_number)
    elif typ == "debug":
        __log_print(message, log_type="debug", line_number_in=line_number)
    else:
        pass



@staticmethod
def _txtlog_file_open(file_name: str) -> None:
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    file = open(log_file_path, 'w', encoding='utf-8')
    file.write(f"Start: {_date_time_short()}\n")
    file.close()
    return None

@staticmethod
def _txtlog_write_clean(text: str, file_name: str) -> None:
    try:
        log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        mode = 'a' if os.path.exists(log_file_path) else 'w'
        with open(log_file_path, mode, encoding='utf-8') as file:
            file.write(text + '\n')
    except Exception as e:
        error(f"Fehler beim Schreiben in die Datei {file_name}: {e}")


if __name__ == "__main__":
    title(f"started")
    info(f"info")
    info(f"debuging: ",  typ="debug")
    line("Aufruf über MAIN gestartet")
    input("press ENTER")
