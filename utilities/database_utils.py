# database_utils.py

import asyncpg


async def fetch_one(bot, query: str, *params):
    """
    Fetch a single record from the database.

    :param bot: The instance of your bot that has `db_pool`.
    :param query: The SQL query to execute.
    :param params: Any parameters to pass into the SQL query.
    :return: A single database record or None if no result found.
    """
    async with bot.db_pool.acquire() as connection:
        record = await connection.fetchrow(query, *params)
    return record


async def fetch_all(bot, query: str, *params):
    """
    Fetch all records matching the query.

    :param bot: The instance of your bot that has `db_pool`.
    :param query: The SQL query to execute.
    :param params: Any parameters to pass into the SQL query.
    :return: A list of records, each a dictionary-like object.
    """
    async with bot.db_pool.acquire() as connection:
        records = await connection.fetch(query, *params)
    return records


async def execute(bot, query: str, *params):
    """
    Execute a query that doesn't return rows (e.g., INSERT/UPDATE/DELETE).

    :param bot: The instance of your bot that has `db_pool`.
    :param query: The SQL query to execute.
    :param params: Any parameters to pass into the SQL query.
    :return: The status of the last command (e.g., "INSERT 0 1").
    """
    async with bot.db_pool.acquire() as connection:
        result = await connection.execute(query, *params)
    return result


async def fetch_val(bot, query: str, *params):
    """
    Fetch a single scalar value from the database.

    :param bot: The instance of your bot that has `db_pool`.
    :param query: The SQL query to execute.
    :param params: Any parameters to pass into the SQL query.
    :return: A single value (e.g., INTEGER, TEXT), or None if not found.
    """
    async with bot.db_pool.acquire() as connection:
        value = await connection.fetchval(query, *params)
    return value