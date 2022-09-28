import logging
from enum import Enum
from typing import Any

from rich.console import Console
from rich.logging import RichHandler
from rich.prompt import Confirm


class Verbosity(str, Enum):
    verbose = "verbose"
    success = "success"
    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    exception = "exception"
    critical = "critical"


class Logger(logging.getLoggerClass()):
    VERBOSE = 15
    SUCCESS = 25
    DEBUG = 10

    @staticmethod
    def set_verbosity(verbose: str, quiet: bool = False):
        if quiet:
            logger.setLevel(logging.CRITICAL)
        elif verbose in ["VERBOSE", "SUCCESS"]:
            logger.setLevel(getattr(Logger, verbose))
        else:
            logger.setLevel(getattr(logging, verbose))

    def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        super(Logger, self).debug(f"[yellow3][D]{msg} [/yellow3]", *args, **kwargs)

    def debug_json(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(Logger.DEBUG):
            console.print("[yellow3][D]JSON data :[/yellow3]")
            console.print_json(data=msg)

    def verbose(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(Logger.VERBOSE):
            self._log(Logger.VERBOSE,
                      "{}[V]{} {}".format("[blue]", "[/blue]", msg), args, **kwargs)

    def verbose_json(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(Logger.VERBOSE):
            console.print("[blue][V]JSON data :[/blue]")
            console.print_json(data=msg)

    def raw(self, msg: Any, level=VERBOSE) -> None:
        if self.isEnabledFor(level):
            if type(msg) is bytes:
                msg = msg.decode('utf-8', errors="ignore")
            # Raw message are print directly to the console bypassing logging system and auto formatting
            console.print(msg, end='', markup=False, highlight=False)

    def info(self, msg: Any, tab=0, *args: Any, **kwargs: Any) -> None:
        super(Logger, self).info(f"{'   '*tab}[bold blue][*][/bold blue] {msg}", *args, **kwargs)

    def warning(self, msg: Any, tab=0, *args: Any, **kwargs: Any) -> None:
        super(Logger, self).warning(f"{'   '*tab}[bold orange3][!][/bold orange3] {msg}", *args, **kwargs)

    def error(self, msg: Any, tab=0, *args: Any, **kwargs: Any) -> None:
        super(Logger, self).error(f"{'   '*tab}[bold red][-][/bold red] {msg}", *args, **kwargs)

    def exception(self, msg: Any, tab=0, *args: Any, **kwargs: Any) -> None:
        super(Logger, self).exception(f"{'   '*tab}[red3][x][/red3] {msg}", *args, **kwargs)

    def critical(self, msg: Any, tab=0, *args: Any, **kwargs: Any) -> None:
        super(Logger, self).critical(f"{'   '*tab}[bold dark_red][X][/bold dark_red] {msg}", *args, **kwargs)

    def success(self, msg: Any, tab=0, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(Logger.SUCCESS):
            self._log(Logger.SUCCESS,
                      f"{'   '*tab}[bold green][+][/bold green] {msg}", args, **kwargs)

    @staticmethod
    def ask(msg: Any, *args: Any, **kwargs: Any) -> bool:
        return Confirm.ask("{}[?]{} {}".format("[bold orange3]", "[/bold orange3]", msg), *args, **kwargs)


logging.setLoggerClass(Logger)

logging.addLevelName(Logger.VERBOSE, "VERBOSE")
logging.addLevelName(Logger.SUCCESS, "SUCCESS")
logging.basicConfig(
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False, markup=True, show_level=False, show_path=False)]
)

logger: Logger = logging.getLogger("main")
# Default log level
logger.setLevel(logging.DEBUG)

console = Console()
