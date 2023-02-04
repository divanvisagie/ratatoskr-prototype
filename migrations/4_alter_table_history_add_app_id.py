from executor import Executor

ex = Executor()

ex.commit("""
ALTER TABLE history ADD COLUMN app_id INTEGER
""")

ex.release_resources()