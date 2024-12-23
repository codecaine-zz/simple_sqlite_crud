# SQLite CRUD Example

This repository contains a simple example of how to perform CRUD (Create, Read, Update, Delete) operations using SQLite and SQLAlchemy in Python.

## File Overview

### `sqlite_example.py`

This script demonstrates how to use SQLAlchemy to interact with an SQLite database. It defines an `Employee` model and a `SQLiteCRUD` class to handle database operations.

### Key Components

- **Employee Model**: Defines the structure of the `employees` table.
- **SQLiteCRUD Class**: Provides methods to perform CRUD operations on the `employees` table.

### Usage

1. **Initialization**: Create an instance of `SQLiteCRUD` with the database name.
    ```python
    db = SQLiteCRUD('company.db')
    ```

2. **Insert**: Add new employees to the database.
    ```python
    db.insert(Employee(id=1, first_name='John', last_name='Doe', email='john.doe@example.com', department='Engineering'))
    ```

3. **Read**: Retrieve employees based on conditions.
    ```python
    employees = db.read({'department': 'Engineering'})
    ```

4. **Update**: Update employee details.
    ```python
    db.update({'id': 1}, {'email': 'j.doe@example.com'})
    ```

5. **Delete**: Remove employees from the database.
    ```python
    db.delete({'id': 1})
    ```

6. **Close**: Close the database connection.
    ```python
    db.close()
    ```

### Example Usage

The script includes an example usage section that demonstrates how to perform various operations:

- Insert new employees
- Read employees based on different conditions
- Update an employee's email
- Delete an employee
- Use advanced filters like `gt`, `lt`, `contains`, `in_`, and `regex`

#### Advanced Filters

- **Greater Than (`gt`)**: Retrieve employees with IDs greater than 1.
    ```python
    employees = db.read({'id': {'gt': 1}})
    ```

- **Less Than (`lt`)**: Retrieve employees with IDs less than 5.
    ```python
    employees = db.read({'id': {'lt': 5}})
    ```

- **Contains (`contains`)**: Retrieve employees whose department contains 'Eng'.
    ```python
    employees = db.read({'department': {'contains': 'Eng'}})
    ```

- **In List (`in_`)**: Retrieve employees whose IDs are in the list [1, 2, 3].
    ```python
    employees = db.read({'id': {'in_': [1, 2, 3]}})
    ```

- **Regular Expression (`regex`)**: Retrieve employees whose email matches the regex pattern.
    ```python
    employees = db.read({'email': {'regex': r'@example\.com$'}})
    ```

### Running the Script

To run the script, simply execute it with Python:
```sh
python sqlite_example.py
```

This will perform the example operations and print the results to the console.

### Dependencies

- SQLAlchemy
- SQLite (included with Python)

Install SQLAlchemy using pip:
```sh
pip install sqlalchemy
```

### License

This project is licensed under the MIT License.