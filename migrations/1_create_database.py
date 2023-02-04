from migrations.executor import Executor

ex = Executor()

ex.commit("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    telegram_username TEXT NOT NULL,
    allowed BOOLEAN NOT NULL
)
""")

# Add some data to the table
ex.commit("INSERT INTO users (telegram_username, allowed) VALUES (?,?)", ("DivanVisagie", True))
ex.commit("INSERT INTO users (telegram_username, allowed) VALUES (?,?)", ("DaisyTheDeadWeed", True))
ex.commit("INSERT INTO users (telegram_username, allowed) VALUES (?,?)", ("danielwebb", True))
ex.commit("INSERT INTO users (telegram_username, allowed) VALUES (?,?)", ("temporalix", True))

ex.release_resources()