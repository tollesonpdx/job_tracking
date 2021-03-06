from modules import connectToPSQL as psql

def intro():
    print(
        f"\n\n"
        f"---------------------------------------------------------------------\n"
        f"Hello, welcome to the job tracking application. Here are the options:\n"
        f"1 - Display Target Companies\n"
        f"2 - Search for a target using their name\n"
        f"3 - Look at specific jobs at a particular company\n"
        f"4 - Add a new target company\n"
        f"5 - Add a new position\n"
        f"6 - Update status of existing position\n"
        f"7 - List just the active job boards\n"
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

def printJobBoardsRecruiters(results):
    lenId, lenName = 0, 0
    lenDate = 25
    lenStatus = 17
    for row in results:
        lenId = max(lenId, len(str(row[0])))
        lenName = max(lenName, len(row[1] or ''))
    print(f"\n{'ID':>{lenId}} - {'Company Name':<{lenName}} - {'Last Date of Activity':<{lenDate}} - {'Status':<{lenStatus}} - {'Link'}")
    for row in results:
        print(f"{row[0]:>{lenId}} - {row[1] or '':<{lenName}} - {str(row[6]):<{lenDate}} - {row[5]:<{lenStatus}} - {row[4]}")

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
    print()
    if position[0]: print(f"{l}Position ID: {position[1]:>4}")
    print(
        f"{l}Name: {position[2]}\n"
        f"{l}Link: {position[3]}\n"
        f"{l}Tier: {position[4]}-{position[5]}\n"
        f"{l}Notes: {position[6]}"
    )
    if printStatusToo and position[1]:
        statusLog = psql.selectFromPSQL(f"SELECT * FROM vw_position_status_log WHERE position_id = {position[1]}")
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

def printStatuses():
    statuses = psql.selectFromPSQL(f"SELECT * FROM statuses ORDER BY status_id")
    for status in statuses: print(f"{status[0]:>3} - {status[1]}")

if __name__ == '__main__':
    print('printing intro')
    intro()
    
    print('\n\n\nprinting test position')
    printPosition((None, 1, 'aaa', 'www.nyt.com', 0, 'recruiter', 'aaa'))

    print('\n\n\n printing all position data for target 1')
  