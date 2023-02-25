from executor import Executor

ex = Executor()

ex.commit("""
CREATE TABLE secrets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    app_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);
""")

ex.release_resources()