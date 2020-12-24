from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Date, and_
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Session = sessionmaker(bind=engine)

ACTIONS = {"1": "Today's tasks",
           "2": "Week's tasks",
           "3": "All tasks",
           "4": "Missed tasks",
           "5": "Add task",
           "6": "Delete task",
           "0": "Exit"}


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"id: {self.id}, title: {self.task}, deadline:{self.deadline}"

    def __str__(self):
        return self.task


class TaskManager:

    def __init__(self):
        # create table
        Base.metadata.create_all(engine)
        # create session
        self.session = Session()

    def fetch_tasks_from_DB(self, date: datetime.date, end_date=None):
        if end_date:
            return self.session.query(Task).filter(and_(Task.deadline >= date, Task.deadline <= end_date))
        else:
            return self.session.query(Task).filter(Task.deadline == date).all()

    def fetch_all_from_DB(self):
        return self.session.query(Task).order_by(Task.deadline).all()

    def print_all_tasks(self):
        tasks = self.fetch_all_from_DB()
        print("All tasks:")
        if tasks:
            counter = 1
            for task in tasks:
                print(f"{counter}. {task}. {task.deadline.strftime('%d %b')}")
                counter += 1
        else:
            print("Nothing to do!")
        return tasks

    def print_tasks(self, date, end_date=None):
        if end_date:
            tasks = self.fetch_tasks_from_DB(date, end_date)
            delta = end_date - date
            for i in range(delta.days + 1):
                current_day = date + timedelta(days=i)
                counter = 0
                print(current_day.strftime("%A %d %b:"))
                for task in tasks:
                    if task.deadline == current_day:
                        print(f"{counter + 1}. {task}")
                        counter += 1
                if counter == 0:
                    print("Nothing to do!")
                print()
        else:
            tasks = self.fetch_tasks_from_DB(date)
            print(date.strftime('%A %d %b:'))
            if tasks:
                counter = 1
                for task in tasks:
                    print(f"{counter}. {task}")
                    counter += 1
            else:
                print("Nothing to do!")
        return tasks

    def add_task(self):
        title = input("Enter task: ")
        deadline = [int(x) for x in input("Enter deadline (YYYY-MM-DD): ").split('-')]
        new_task = Task(task=title, deadline=datetime(*deadline))
        self.session.add(new_task)
        self.session.commit()

    def print_missed_tasks(self):
        tasks = self.fetch_tasks_from_DB(datetime.min.date(), datetime.today().date())
        print("Missed tasks:")
        if tasks:
            counter = 1
            for task in tasks:
                print(f"{counter}. {task}. {task.deadline.strftime('%d %b')}")
                counter += 1
        else:
            print("Nothing is missed!")
        return tasks

    def delete_task(self):
        tasks = self.print_all_tasks()
        choice = int(input("Choose the number of the task you want to delete: "))
        self.session.delete(tasks[choice - 1])
        self.session.commit()

    @staticmethod
    def get_user_input():
        for key, value in ACTIONS.items():
            print(f"{key}) {value}")
        return input()

    def menu(self):
        while True:
            user_input = self.get_user_input()

            if user_input in ACTIONS:
                today = datetime.today().date()

                if user_input == "1":
                    self.print_tasks(today)
                elif user_input == "2":
                    self.print_tasks(today, today + timedelta(7))
                elif user_input == "3":
                    self.print_all_tasks()
                elif user_input == "4":
                    self.print_missed_tasks()
                elif user_input == "5":
                    self.add_task()
                elif user_input == "6":
                    self.delete_task()
                elif user_input == "0":
                    print("Bye!")
                    quit()
                print()
            else:
                print("Wrong entering. Please try again")


manager = TaskManager()
manager.menu()
