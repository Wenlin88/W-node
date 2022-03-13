import ulogger

def default_handlers():
    handlers = (
        ulogger.Handler(
            level=ulogger.DEBUG,
            colorful=True,
            fmt="&(time)% : &(level)%\t&(name)%\t&(msg)%",
            direction=ulogger.TO_TERM,
        ),
        ulogger.Handler(
            level=ulogger.WARN,
            fmt="&(time)% : &(level)%\t&(name)%\t&(msg)%",
            direction=ulogger.TO_FILE,
            file_name="logging.log",
            max_file_size=1024 # max for 1k
        )
    )
    return handlers