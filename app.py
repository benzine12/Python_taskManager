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
    while True:
        task_theme = input('Task theme HOME/WORK : ')
        if task_theme == 'HOME' or task_theme == 'WORK':
            break
        else:
            print('Wrong answer, enter valid theme.')
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
    try:
        with open('task_manager.json','r+') as file_json:
            try:
                # load the data from the file
                file_json_data = json.load(file_json)
            # if file empty initialize it with the - []
            except json.JSONDecodeError:
                file_json_data = []
            
            # add to the current json data new task
            file_json_data.append(task_base)
            # move the file pointer to the beginning of the file
            file_json.seek(0)
            # write back to the file updated data
            json.dump(file_json_data, file_json,default=str, indent=4)
    except FileNotFoundError:
        with open('task_manager.json', 'w') as file_json:
            json.dump([task_base], file_json, default=str, indent=4)

def main():
    while True:
        clearScreen()
        menu()
        input_number = input('Enter number: ')
        match input_number:
            case '1':
                task_base = write_task()
                new_task(task_base)
                # clearScreen()
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