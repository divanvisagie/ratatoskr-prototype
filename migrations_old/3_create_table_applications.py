from migrations.executor import Executor

ex = Executor()

# Create a table
ex.commit("""
CREATE TABLE IF NOT EXISTS app (
    id INTEGER PRIMARY KEY,
    app_name TEXT NOT NULL
)
""")

ex.release_resources()