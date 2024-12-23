from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, func
from typing import Dict, Any, List, Optional

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    department = Column(String)

    def __repr__(self) -> str:
        return (f"<Employee(id={self.id}, first_name='{self.first_name}', "
                f"last_name='{self.last_name}', email='{self.email}', "
                f"department='{self.department}')>")

class SQLiteCRUD:
    def __init__(self, db_name: str) -> None:
        self.engine = create_engine(f'sqlite:///{db_name}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session: Session = self.Session()

    def insert(self, employee: Employee) -> None:
        try:
            self.session.add(employee)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            print(f"Warning: ID {employee.id} already exists. Ignoring insert operation.")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")

    def read(self, conditions: Optional[Dict[str, Any]] = None) -> List[Employee]:
        query = self.session.query(Employee)
        if conditions:
            for attr, condition in conditions.items():
                if isinstance(condition, dict):
                    for op, value in condition.items():
                        if op == 'lt':
                            query = query.filter(getattr(Employee, attr) < value)
                        elif op == 'gt':
                            query = query.filter(getattr(Employee, attr) > value)
                        elif op == 'lte':
                            query = query.filter(getattr(Employee, attr) <= value)
                        elif op == 'gte':
                            query = query.filter(getattr(Employee, attr) >= value)
                        elif op == 'neq':
                            query = query.filter(getattr(Employee, attr) != value)
                        elif op == 'contains':
                            query = query.filter(getattr(Employee, attr).contains(value))
                        elif op == 'in_':
                            query = query.filter(getattr(Employee, attr).in_(value))
                        elif op == 'regex':
                            query = query.filter(getattr(Employee, attr).op('REGEXP')(value))
                        # Add more operators as needed
                else:
                    query = query.filter(getattr(Employee, attr) == condition)
        return query.all()

    def update(self, conditions: Dict[str, Any], data: Dict[str, Any]) -> None:
        query = self.session.query(Employee)
        for attr, value in conditions.items():
            query = query.filter(getattr(Employee, attr) == value)
        query.update(data)
        self.session.commit()

    def delete(self, conditions: Dict[str, Any]) -> None:
        query = self.session.query(Employee)
        for attr, value in conditions.items():
            query = query.filter(getattr(Employee, attr) == value)
        query.delete()
        self.session.commit()

    def close(self) -> None:
        self.session.close()

if __name__ == '__main__':
    # Example usage:
    db = SQLiteCRUD('company.db')

    # Insert a new employee
    db.insert(Employee(id=1, first_name='John', last_name='Doe', email='john.doe@example.com', department='Engineering'))

    # Insert more employees
    db.insert(Employee(id=2, first_name='Jane', last_name='Smith', email='jane.smith@example.com', department='Marketing'))
    db.insert(Employee(id=3, first_name='Alice', last_name='Johnson', email='alice.johnson@example.com', department='Engineering'))

    # Read employees from the 'Engineering' department
    print("Engineering Department:", db.read({'department': 'Engineering'}))

    # Read employees with the last name 'Smith'
    print("Employees with last name Smith:", db.read({'last_name': 'Smith'}))

    # Read employees with the first name 'Alice' and department 'Engineering'
    print("Alice in Engineering:", db.read({'first_name': 'Alice', 'department': 'Engineering'}))

    # Read the 'employees' table
    print("All employees:", db.read())

    # Update an employee's email
    db.update({'id': 1}, {'email': 'j.doe@example.com'})

    # Verify the update operation
    print("Updated employee with id 1:", db.read({'id': 1}))

    # Read the 'employees' table again
    print("All employees after update:", db.read())

    # Delete an employee
    db.delete({'id': 1})

    # Read the 'employees' table one more time
    print("All employees after deletion:", db.read())

    # Example of using new filters
    print("Employees with id greater than 1:", db.read({'id': {'gt': 1}}))
    print("Employees with first name containing 'Jane':", db.read({'first_name': {'contains': 'Jane'}}))
    print("Employees with id less than or equal to 3:", db.read({'id': {'lte': 3}}))
    print("Employees with id not equal to 2:", db.read({'id': {'neq': 2}}))
    print("Employees with id in [1, 3]:", db.read({'id': {'in_': [1, 3]}}))
    print("Employees with email matching regex '.*@example.com':", db.read({'email': {'regex': '.*@example.com'}}))

    # Close the database connection
    db.close()
