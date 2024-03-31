# A simple Sqlite3 CRUD manager class for Python 3.6+.

```python
import sqlite3


class SQLiteCRUD:
    """
    A class used to perform CRUD operations on a SQLite database.

    Attributes
    ----------
    conn : sqlite3.Connection
        A SQLite connection object to the database.
    cursor : sqlite3.Cursor
        A cursor object used to send SQL commands to a SQLite database.

    Methods
    -------
    create_table(table_name, fields)
        Creates a table with the given name and fields if it does not exist.

    insert(table_name, data)
        Inserts a new row into the specified table with the provided data.

    read(table_name, conditions=None)
        Reads and returns rows from the specified table that meet the conditions.

    update(table_name, data, conditions)
        Updates rows in the specified table based on the provided conditions.

    delete(table_name, conditions)
        Deletes rows from the specified table that meet the conditions.

    close()
        Closes the database connection.
    """

    def __init__(self, db_name):
        """
        Constructs all the necessary attributes for the SQLiteCRUD object.

        Parameters
        ----------
        db_name : str
            The name of the database file.
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, fields):
        """
        Creates a table with the given name and fields if it does not exist.

        Parameters
        ----------
        table_name : str
            The name of the table to create.
        fields : dict
            A dictionary of field names and their data types.
        """
        fields_str = ', '.join(f'{k} {v}' for k, v in fields.items())
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {table_name} ({fields_str})')
        self.conn.commit()

    def insert(self, table_name, data):
        """
        Inserts a new row into the specified table with the provided data.

        Parameters
        ----------
        table_name : str
            The name of the table to insert data into.
        data : dict
            A dictionary of field names and their values to insert.
        """
        placeholders = ', '.join('?' * len(data))
        fields = ', '.join(data.keys())
        try:
            self.cursor.execute(
                f'INSERT INTO {table_name} ({fields}) VALUES ({placeholders})', list(data.values()))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(
                f"Warning: ID already exists in {table_name}. Ignoring insert operation.")

    def read(self, table_name, conditions=None):
        """
        Reads and returns rows from the specified table that meet the conditions.

        Parameters
        ----------
        table_name : str
            The name of the table to read from.
        conditions : dict, optional
            A dictionary of field names and their values to filter results.

        Returns
        -------
        list
            A list of rows that meet the conditions.
        """
        query = f'SELECT * FROM {table_name}'
        if conditions:
            query += ' WHERE ' + \
                ' AND '.join(f'{k} = ?' for k in conditions.keys())
            self.cursor.execute(query, list(conditions.values()))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, table_name, data, conditions):
        """
        Updates rows in the specified table based on the provided conditions.

        Parameters
        ----------
        table_name : str
            The name of the table to update.
        data : dict
            A dictionary of field names and their new values.
        conditions : dict
            A dictionary of field names and their values to filter which rows to update.
        """
        query = f'UPDATE {table_name} SET ' + \
            ', '.join(f'{k} = ?' for k in data.keys())
        query += ' WHERE ' + \
            ' AND '.join(f'{k} = ?' for k in conditions.keys())
        self.cursor.execute(query, list(data.values()) +
                            list(conditions.values()))
        self.conn.commit()

    def delete(self, table_name, conditions):
        """
        Deletes rows from the specified table that meet the conditions.

        Parameters
        ----------
        table_name : str
            The name of the table to delete from.
        conditions : dict
            A dictionary of field names and their values to filter which rows to delete.
        """
        query = f'DELETE FROM {table_name} WHERE ' + \
            ' AND '.join(f'{k} = ?' for k in conditions.keys())
        self.cursor.execute(query, list(conditions.values()))
        self.conn.commit()

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()


if __name__ == '__main__':
    # Example usage:
    # Create an instance of SQLiteCRUD
    db = SQLiteCRUD('company.db')

    # Create the 'employees' table
    db.create_table('employees', {
        'id': 'INTEGER PRIMARY KEY',
        'first_name': 'TEXT',
        'last_name': 'TEXT',
        'email': 'TEXT',
        'department': 'TEXT'
    })

    # Insert a new employee
    db.insert('employees', {
        'id': 1,
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'department': 'Engineering'
    })

    # Read the 'employees' table
    print(db.read('employees'))

    # Update an employee's email
    db.update('employees', {'email': 'j.doe@example.com'}, {'id': 1})

    # Read the 'employees' table again
    print(db.read('employees'))

    # Delete an employee
    db.delete('employees', {'id': 1})

    # Read the 'employees' table one more time
    print(db.read('employees'))

    # Close the database connection
    db.close()
```
