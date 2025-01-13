import json
import os
import datetime

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    print('1. add task')
    print('2. update task')
    print('3. delete task')
    print('4. change task status')
    print('5. show all tasks')
    print('6. show all DONE')
    print('7. show all IN PROGRESS')
    print('8. Exit')

def write_task():
    task_name = input('Task name: ')
    task_theme = input('Task theme HOME/WORK: ')
    if task_theme != 'HOME' or task_theme != 'WORK':
        task_theme = input('Task theme HOME/WORK: ')
    task_status = 'IN_PROGRESS'
    task_desc = input('Description: ')

    task_base = {
        "task_name":task_name,
        "theme":task_theme,
        "status":task_status,
        "start_date": datetime.datetime.now(),
        "end_date":'/',
        "task_desc":task_desc,
    }
    return task_base

def new_task(task_base):
    with open('task_manager.json','a') as file_json:
        json.dump(task_base, file_json,default=str)


def main():
    clearScreen()
    menu()
    input_number = input('Enter number: ')
    match input_number:
        case '1':
            task_base = write_task()
            # print(task_base)
            new_task(task_base)
        case '2':
            pass
        case '3':
            pass
        case '4':
            pass
        case '5':
            pass
        case '6':
            pass
        case '7':
            pass
        case '8':
            exit()
if __name__ == '__main__':
    main()