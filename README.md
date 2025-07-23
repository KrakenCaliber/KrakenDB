# KrakenDB Database Manager

A simple Database Manager using SQLModel and DuckDB.


## Dependencies

- [SQLModel](https://sqlmodel.tiangolo.com/)

    *Database ORM*

- [DuckDB](https://duckdb.org/)

    *Underlying Database*

- [Click](https://click.palletsprojects.com/)

    *OS Configuration*


## Usage

This package stores your data in a single file within your OS's configuration based on an application name.

For the following example, on macOS the file would be stored here: `~/Library/Application Support/KrakenDemo/Users.duckdb`.

### Example

```
from SQLModel import SQLModel, Field

from uuid import UUID, uuid4

from kraken_db import KrakenDB


class User(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=lambda: uuid4())
    name: str
    age: int


db = KrakenDB("KrakenDemo", "Users")

user = db.create(User(
    name="John Doe",
    age=30
))

print(user.id)
```
