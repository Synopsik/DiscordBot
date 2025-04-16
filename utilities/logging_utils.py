import logging
import asyncio
from datetime import datetime
from typing import Optional

import utilities.database_utils as database_utils

def setup_logging(
        db_pool,
        loop: asyncio.AbstractEventLoop,
        logger_name: Optional[str] = None,
        level: int = logging.INFO,
        table_name: str = "logs"):
    """
    Configures and returns a Python logger that uses the DatabaseLogHandler.
    - db_pool: The asyncpg Pool for database interactions.
    - loop: The event loop used for scheduling async DB calls.
    - logger_name: Optional name for the logger (defaults to root logger if None).
    - level: Logging level (DEBUG, INFO, etc.).
    - table_name: Which DB table to store logs in (default 'logs').
    """
    if logger_name:
        logger = logging.getLogger(logger_name)
    else:
        logger = logging.getLogger()

    # Set level of logs broadcasted (ex. logging.INFO in our level parameter)
    logger.setLevel(level)

    # Create and add our custom handler
    db_handler = DatabaseLogHandler(db_pool=db_pool, loop=loop, table_name=table_name)
    # You could also attach additional formatters here:
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # Set our formatter we made and attach it to our handler
    db_handler.setFormatter(formatter)
    # Add handler to our logger
    logger.addHandler(db_handler)

    return logger


class DatabaseLogHandler(logging.Handler):
    """
    A custom logging handler that stores log records in the database via database_utils.
    Since Python's logging is synchronous by default but our DB functions are async,
    we use run_coroutine_threadsafe to push work into the event loop.
    """

    def __init__(self, db_pool, loop: asyncio.AbstractEventLoop, table_name: str = "logs"):
        super().__init__()
        self.db_pool = db_pool
        self.loop = loop
        self.table_name = table_name # Unsure if I'll need this once db is configured, maybe just hardcode


    def emit(self, record: logging.LogRecord) -> None:
        """
        Called automatically when a log event occurs. Formats the log message
        and submits a database write through an async method.
        """

        print(self.format(record))

        """
        try:
            msg = self.format(record)
            # For consistent timestamps, we can convert the 'created' field (float) into a datetime
            log_time = datetime.fromtimestamp(record.created)
            # Schedule the async DB call on the provided event loop
            asyncio.run_coroutine_threadsafe(
                self._write_log_to_db(
                    log_time,
                    record.name,
                    record.levelname,
                    msg
                ),
                self.loop
            )
        except Exception:
            self.handleError(record)
        """


    async def _write_log_to_db(self, log_time: datetime, logger_name: str, level: str, message: str):
        """
        An async helper method for writing a single log entry to the database.
        """
        insert_query = f"""
            INSERT INTO {self.table_name} (timestamp, logger, level, message)
            VALUES ($1, $2, $3, $4)
        """
        await database_utils.execute(
            self.db_pool,
            insert_query,
            log_time.isoformat(),
            logger_name,
            level,
            message
        )