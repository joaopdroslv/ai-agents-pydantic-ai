import sqlite3
from typing import Any, Union

from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, RunContext

from main.models.local_qwen import local_qwen


class QueryError(Exception):
    pass


class DatabaseConn:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self._setup()

    def _setup(self):
        self.conn.execute(
            """
        CREATE TABLE users_logins (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            logged_in_at TEXT
        )
        """
        )
        self.conn.commit()

    async def execute(self, query: str) -> Any:
        try:
            return self.conn.execute(query).fetchall()
        except sqlite3.Error as e:
            raise QueryError(str(e))


class Success(BaseModel):
    sql_query: str


class InvalidRequest(BaseModel):
    error_message: str


Output = Union[Success, InvalidRequest]

agent: Agent[DatabaseConn, Output] = Agent(
    model=local_qwen,
    output_type=Output,
    deps_type=DatabaseConn,
    system_prompt=(
        "Generate SQLite3 flavored SQL queries based on user input."
        "Assume the following table exists:\n\n"
        "Table: users_logins\n"
        "- id: INTEGER PRIMARY KEY\n"
        "- user_id: INTEGER\n"
        "- name: TEXT\n"
        "- logged_in_at: TEXT (ISO datetime format)\n\n"
    ),
)


@agent.output_validator
async def validate_sql(ctx: RunContext[DatabaseConn], output: Output) -> Output:
    if isinstance(output, InvalidRequest):
        return output

    try:
        await ctx.deps.execute(f"EXPLAIN {output.sql_query}")
    except QueryError as e:
        raise ModelRetry(f"Invalid query: {e}") from e
    else:
        return output


question1 = "Get me the users who logged in yesterday. Today is 2025-05-27."
# > SELECT user_id, name FROM users_logins WHERE logged_in_at BETWEEN '2025-05-26T00:00:00' AND '2025-05-26T23:59:59'

question2 = "Get me the users that logged in at least 50 times last month. Current month is May of 2025."
# > SELECT user_id, COUNT(*) AS login_count FROM users_logins WHERE logged_in_at LIKE '2025-04-%' GROUP BY user_id HAVING COUNT(*) >= 50

result = agent.run_sync(question2, deps=DatabaseConn())

print(result.output)
