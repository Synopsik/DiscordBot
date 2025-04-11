import asyncpg


async def init_db_tables(db_pool: asyncpg.Pool) -> None:
    """
    Initializes or migrates necessary tables in the database.
    """
    async with db_pool.acquire() as conn:
        # Example: Create a 'users' table if it doesn't exist
        create_users_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id         SERIAL PRIMARY KEY,
                discord_id BIGINT UNIQUE NOT NULL,
                username   TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """
        await conn.execute(create_users_table_query)

        # Example: Create a 'logs' table if it doesn't exist
        create_logs_table_query = """
            CREATE TABLE IF NOT EXISTS logs (
                log_id     SERIAL PRIMARY KEY,
                user_id    BIGINT NOT NULL,
                command    TEXT,
                timestamp  TIMESTAMP DEFAULT NOW()
            );
        """
        await conn.execute(create_logs_table_query)

        print("[DB] Tables verified or created successfully.")


async def list_tables_and_columns(db_pool: asyncpg.Pool) -> None:
    """
    Lists tables and their columns in the connected database, and prints up to
    the first 10 entries from each table.
    """
    async with db_pool.acquire() as conn:
        # Fetch table names
        get_tables_query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """
        tables = await conn.fetch(get_tables_query)
        if not tables:
            print("[DB] No tables found in the database.")
            return

        for table in tables:
            table_name = table["table_name"]
            print(f"\n-- Table: {table_name} --")

            # Fetch columns for each table
            get_columns_query = """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = $1
                ORDER BY ordinal_position;
            """
            columns = await conn.fetch(get_columns_query, table_name)
            for col in columns:
                print(f"  Column: {col['column_name']} | Type: {col['data_type']}")

            # Fetch first 10 rows for a quick preview
            fetch_limited_rows_query = f"SELECT * FROM {table_name} LIMIT 10;"
            rows = await conn.fetch(fetch_limited_rows_query)
            if not rows:
                print("  (No entries in this table.)")
            else:
                print("  First 10 entries:")
                for row in rows:
                    print(f"    {row}")


async def bulk_update_users(db_pool: asyncpg.Pool, user_data: list) -> None:
    """
    Performs a bulk update or insert of user data.
    'user_data' should be a list of dictionaries or tuples with the necessary fields.

    Example structure of user_data (list of dict):
        [
            {"discord_id": 123456789, "username": "ExampleUser1"},
            {"discord_id": 987654321, "username": "ExampleUser2"},
            ...
        ]
    """
    async with db_pool.acquire() as conn:
        # Example upsert operation to handle existing & new users
        upsert_query = """
            INSERT INTO users (discord_id, username)
            VALUES ($1, $2)
            ON CONFLICT (discord_id) 
            DO UPDATE SET username = EXCLUDED.username
        """
        async with conn.transaction():
            for record in user_data:
                await conn.execute(
                    upsert_query,
                    record["discord_id"],
                    record["username"]
                )
    print("[DB] Bulk user update completed.")


async def update_single_user(db_pool: asyncpg.Pool, discord_id: int, username: str) -> None:
    """
    Updates a single user's record (or inserts if not present).
    """
    async with db_pool.acquire() as conn:
        upsert_query = """
            INSERT INTO users (discord_id, username)
            VALUES ($1, $2)
            ON CONFLICT (discord_id) 
            DO UPDATE SET username = EXCLUDED.username
        """
        await conn.execute(upsert_query, discord_id, username)
    print(f"[DB] User {discord_id} updated/inserted successfully.")


async def fetch_one(db_pool: asyncpg.Pool, query: str, *args):
    """
    Fetches a single row from the database.
    """
    async with db_pool.acquire() as conn:
        return await conn.fetchrow(query, *args)


async def fetch_all(db_pool: asyncpg.Pool, query: str, *args):
    """
    Fetches all rows matching the query.
    """
    async with db_pool.acquire() as conn:
        return await conn.fetch(query, *args)


async def fetch_val(db_pool: asyncpg.Pool, query: str, *args):
    """
    Fetches a single value (the first column of the first row) from the database.
    """
    async with db_pool.acquire() as conn:
        return await conn.fetchval(query, *args)


async def execute(db_pool: asyncpg.Pool, query: str, *args) -> None:
    """
    Executes a generic statement in the database (INSERT, UPDATE, DELETE, etc.).
    """
    async with db_pool.acquire() as conn:
        await conn.execute(query, *args)
