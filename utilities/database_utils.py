import asyncpg


async def init_db_tables(db_pool):
    """
    Initializes all necessary DB tables if they do not already exist,
    using a dedicated schema (bot_schema). Make sure the database user
    has privileges to create and use this schema.
    """
    create_schema_query = """
        CREATE SCHEMA IF NOT EXISTS bot_schema;
    """

    create_table_queries = [
        """
        CREATE TABLE IF NOT EXISTS bot_schema.guilds (
            guild_id BIGINT PRIMARY KEY,
            guild_name TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS bot_schema.users (
            user_id BIGINT NOT NULL,
            guild_id BIGINT NOT NULL,
            user_name TEXT,
            PRIMARY KEY (user_id, guild_id),
            FOREIGN KEY (guild_id)
                REFERENCES bot_schema.guilds (guild_id)
                ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS bot_schema.messages (
            message_id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            guild_id BIGINT NOT NULL,
            content TEXT,
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            FOREIGN KEY (guild_id, user_id)
                REFERENCES bot_schema.users (guild_id, user_id)
                ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS bot_schema.logs (
            log_id BIGSERIAL PRIMARY KEY,
            guild_id BIGINT NOT NULL,
            user_id BIGINT,
            event_type TEXT,
            event_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            FOREIGN KEY (guild_id, user_id)
                REFERENCES bot_schema.users (guild_id, user_id)
                ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS bot_schema.mentors (
            mentor_id BIGSERIAL PRIMARY KEY,
            guild_id BIGINT,
            user_id BIGINT,
            skill TEXT,
            contact TEXT,
            FOREIGN KEY (guild_id, user_id)
                REFERENCES bot_schema.users (guild_id, user_id)
                ON DELETE CASCADE
        );
        """
    ]
    async with db_pool.acquire() as conn:
        # Create the new schema if not present
        await conn.execute(create_schema_query)
        # Now create the tables within our dedicated schema
        for query in create_table_queries:
            await conn.execute(query)


async def list_tables_and_columns(bot):
    """
    Lists the tables and their columns exclusively within 'bot_schema'.
    """
    query_tables = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'bot_schema';
    """
    query_columns = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'bot_schema'
          AND table_name = $1;
    """
    async with bot.acquire() as conn:
        table_records = await conn.fetch(query_tables)
        tables_and_columns = {}
        for record in table_records:
            table_name = record["table_name"]
            column_records = await conn.fetch(query_columns, table_name)
            columns = [row["column_name"] for row in column_records]
            tables_and_columns[table_name] = columns
    print(f"Current tables and columns in 'bot_schema':\n[Guilds]{tables_and_columns["guilds"]}\n"
                                                        f"[Users]{tables_and_columns["users"]}")
    return tables_and_columns


async def fetch_one(bot, query: str, *params):
    async with bot.acquire() as connection:
        record = await connection.fetchrow(query, *params)
    return record


async def fetch_all(bot, query: str, *params):
    async with bot.acquire() as connection:
        records = await connection.fetch(query, *params)
    return records


async def execute(bot, query: str, *params):
    async with bot.acquire() as connection:
        result = await connection.execute(query, *params)
    return result


async def fetch_val(bot, query: str, *params):
    async with bot.acquire() as connection:
        value = await connection.fetchval(query, *params)
    return value
