from connectToPSQL import connectToPSQL

def intro():
    print('\n\n')
    print('Hello, welcome to the job tracking application. Here are the options:')
    print('1 - Display Target Companies')
    print('2 - Look at specific jobs at a particular company')
    print('3 - Add a new target company')
    print('4 - add a new position')
    print('5 - update status of an existing position')
    print('***** enter anything else to exit the program')
    return input('Enter option: ')

def printTarget(target, num_spaces=0):
    l = ' ' * num_spaces # calculate the leading space
    print(
        f"\n"
        f"{l}Target ID# {target[0]:>4}\n"
        f"{l}Name: {target[1]}\n"
        f"{l}Link: {target[2]}\n"
        f"{l}Description: {target[3]}\n"
        f"{l}Location: {target[4]}"
        )

def printPosition(position, num_spaces=0):
    l = ' ' * num_spaces # calculate the leading space
    print(
        f"\n"
        f"{l}Position ID# {position[0]:>4}\n"
        f"{l}Name: {position[2]}\n"
        f"{l}Link: {position[4]}\n"
        f"{l}Tier: {position[3]}\n"
        f"{l}Notes: {position[5]}"
    )
    statusLog = connectToPSQL(f"SELECT * FROM status_log WHERE position_id = {position[0]}")
    for row in statusLog:
        printStatus(row, num_spaces+4)

def printStatus(status, num_spaces = 0):
    l = ' ' * num_spaces # calculate the leading space
    print(l, status)
    # print(
    #     f"\n"
    #     f"{l}Position ID# {position[0]:>4}\n"
    #     f"{l}Name: {position[2]}\n"
    #     f"{l}Link: {position[4]}\n"
    #     f"{l}Tier: {position[3]}\n"
    #     f"{l}Notes: {position[5]}"
    # )