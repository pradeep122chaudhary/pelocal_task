# todo/init_db.py

from django.db import connection

from django.db import connection

def create_tasks_table():
    """
    Creates a professional-grade 'tasks' table in SQLite using raw SQL.
    Includes constraints, indexes, triggers, and full-text search.
    """
    with connection.cursor() as cursor:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL
                    CHECK(length(title) > 0 AND length(title) <= 200 AND trim(title) != ''),

                description TEXT DEFAULT '',

                due_date DATE,

                status TEXT NOT NULL DEFAULT 'pending'
                    CHECK(status IN ('pending', 'completed', 'archived')),

                priority TEXT DEFAULT 'medium'
                    CHECK(priority IN ('low', 'medium', 'high', 'urgent')),

                created_by INTEGER,

                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,

                is_deleted BOOLEAN NOT NULL DEFAULT 0
            );
        """)

        # Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status) WHERE is_deleted = 0;")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date) WHERE is_deleted = 0;")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority) WHERE is_deleted = 0;")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_created_by ON tasks(created_by) WHERE is_deleted = 0;")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at DESC);")

        # FTS table
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS tasks_fts USING fts5(
                title,
                description,
                content='tasks',
                content_rowid='id'
            );
        """)

        # Triggers
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS trigger_tasks_update_timestamp
            AFTER UPDATE ON tasks FOR EACH ROW
            BEGIN
                UPDATE tasks SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END;
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS trigger_tasks_set_completed
            AFTER UPDATE ON tasks FOR EACH ROW
            WHEN NEW.status = 'completed' AND OLD.status != 'completed'
            BEGIN
                UPDATE tasks SET completed_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END;
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS trigger_tasks_clear_completed
            AFTER UPDATE ON tasks FOR EACH ROW
            WHEN OLD.status = 'completed' AND NEW.status != 'completed'
            BEGIN
                UPDATE tasks SET completed_at = NULL WHERE id = OLD.id;
            END;
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS trigger_tasks_ai AFTER INSERT ON tasks
            BEGIN
                INSERT INTO tasks_fts(rowid, title, description)
                VALUES (new.id, new.title, new.description);
            END;
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS trigger_tasks_au AFTER UPDATE ON tasks
            BEGIN
                UPDATE tasks_fts
                SET title = new.title, description = new.description
                WHERE rowid = old.id;
            END;
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS trigger_tasks_ad AFTER DELETE ON tasks
            BEGIN
                DELETE FROM tasks_fts WHERE rowid = old.id;
            END;
        """)

    print("Tasks table created successfully")

def add_created_by_column():
    with connection.cursor() as cursor:
        cursor.execute("""
            ALTER TABLE tasks
            ADD COLUMN created_by INTEGER;
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_created_by
            ON tasks(created_by)
            WHERE is_deleted = 0;
        """)

    print("created_by column added successfully")

if __name__ == "__main__":
    create_tasks_table()


# todo/db_utils.py
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dictfetchone(cursor):
    row = cursor.fetchone()
    if not row:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))
