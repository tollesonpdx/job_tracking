from modules import connectToPSQL as psql

def intro():
    print(
        f"\n\n"
        f"---------------------------------------------------------------------\n"
        f"Hello, welcome to the job tracking application. Here are the options:\n"
        f"1 - Display Target Companies\n"
        f"2 - Look at specific jobs at a particular company\n"
        f"3 - Add a new target company\n"
        f"4 - Add a new position\n"
        f"5 - Update status of existing position\n"
        f"***** enter anything else to exit the program"
    )

def printAllTargets(results):
    lenId, lenName = 0, 0
    for row in results:
        lenId = max(lenId, len(str(row[0])))
        lenName = max(lenName, len(row[1] or ''))
    print(f"{'ID':>{lenId}} - {'Company Name':<{lenName}} - {'Last Date of Activity'}")
    for row in results:
        print(f"{row[0]:>{lenId}} - {row[1] or '':<{lenName}} - {row[2] or ''}")

def printTarget(target, num_spaces=0):
    l = ' ' * num_spaces # calculate the leading space
    print()
    if target[0]: print(f"{l}Target ID# {target[0]:>4}")
    print(
        f"{l}Name: {target[1]}\n"
        f"{l}Link: {target[2]}\n"
        f"{l}Description: {target[3]}\n"
        f"{l}Location: {target[4]}"
    )

def printPosition(position, printStatusToo = True, num_spaces=0):
    l = ' ' * num_spaces # calculate the leading space
    print(
        f"\n"
        f"{l}Position ID# {position[0]:>4}\n"
        f"{l}Name: {position[2]}\n"
        f"{l}Link: {position[3]}\n"
        f"{l}Tier: {position[4]}-{position[5]}\n"
        f"{l}Notes: {position[6]}"
    )
    if printStatusToo:
        statusLog = psql.selectFromPSQL(f"SELECT * FROM vw_position_status_log WHERE position_id = {position[0]}")
        for row in statusLog:
            printStatus(row, num_spaces+4)

def printStatus(status, num_spaces=0):
    l = ' ' * num_spaces # calculate the leading space
    print(f"{l}{status[1]} - {status[3]:>2}:{status[4]:<18} - {status[2]}")

def printAdded(added):
    print(f"{added} records added to the database")

def printTiers():
    tiers = psql.selectFromPSQL(f"SELECT * FROM tiers")
    for tier in tiers: print(f"{tier[0]} - {tier[1]}")
