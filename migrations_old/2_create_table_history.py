from migrations.executor import Executor
ex = Executor()

# Create a table
ex.commit("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
)
""")

ex.release_resources()