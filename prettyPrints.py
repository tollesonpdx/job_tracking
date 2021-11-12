from connectToPSQL import connectToPSQL

def intro():
    print(
        f"\n\n"
        f"Hello, welcome to the job tracking application. Here are the options:'\n"
        f"1 - Display Target Companies\n"
        f"2 - Look at specific jobs at a particular company\n"
        f"3 - Add a new target company\n"
        f"4 - add a new position\n"
        f"5 - update status of an existing position\n"
        f"***** enter anything else to exit the program"
    )

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

def printPosition(position, printStatusToo = False, num_spaces=0):
    l = ' ' * num_spaces # calculate the leading space
    print(
        f"\n"
        f"{l}Position ID# {position[0]:>4}\n"
        f"{l}Name: {position[2]}\n"
        f"{l}Link: {position[4]}\n"
        f"{l}Tier: {position[3]}\n"
        f"{l}Notes: {position[5]}"
    )
    if printStatusToo:
        statusLog = connectToPSQL(f"SELECT * FROM vw_position_status_log WHERE position_id = {position[0]}")
        for row in statusLog:
            printStatus(row, num_spaces+4)

def printStatus(status, num_spaces = 0):
    l = ' ' * num_spaces # calculate the leading space
    print(f"{l}{status[3]} - {status[1]:<18} - {status[2]}")