# -*- encoding: utf-8 -*-
import sys, shelve

def store_person(db):
    """
    Query user for data and store it in the shelf object
    :param db:
    :return:
    """
    # maybe, can check the valid of input data
    pid = raw_input("input uniq ID number:")
    person = {}
    person['name'] = raw_input("input person name:")
    person['age'] = raw_input("input person age:")
    person['phone'] = raw_input("input phone:")

    db[pid] = person


def lookup_person(db):
    """
    lookup person info from shelve by pid
    :param db:
    :return:
    """
    pid = raw_input("input person ID:")
    field = raw_input("What would you like to know? (name, age, phone): ")
    field = field.strip().lower() # 小写，所以可以随意用户输入大小写
    print field.capitalize() + ':', db[pid][field]


def print_help():
    """
    help message
    """
    print """The available commands are:
    store   :Stores information of a person
    lookup  :Looks a person by ID
    quit    :Saves changes and exit
    ?       :Print this message
    """


def enter_command():
    """
    get command from input
    :return:
    """
    cmd = raw_input("Enter command (? for help): ")
    cmd = cmd.strip().lower()
    return cmd


def main():
    """
    the main function
    :return:
    """
    database = shelve.open('F:\happy code\myGit\myPython\practise_pycharm\spider\DB.dbpy')
    try:
        while True:
            cmd = enter_command()
            if cmd == 'store':
                store_person(database)
            elif cmd == 'lookup':
                lookup_person(database)
            elif cmd == 'quit':
                return
            elif cmd == '?':
                print_help()
            else:
                print "wrong command, try again"
    finally:
        database.close()


class PersonInfo:
    """store person info """

    def __init__(self, name, age, phone):
        self.name = name
        self.age = age
        self.phone = phone

    def setName(self, name):
        self.name = name

    def setAge(self, age):
        self.age = age

    def setPhone(self, phone):
        self.phone = phone

    def getName(self):
        return self.name

    def getAge(self):
        return self.age

    def getPhone(self):
        return self.phone

if __name__ == '__main__':
    main()