from modules import connectToPSQL as psql
from modules import prettyPrints as pp
import datetime

def intro(defaultEntry = None):
    pp.intro()
    return defaultEntry or input("Enter option: ")

def allTargets():
    results = psql.selectFromPSQL("""SELECT * FROM vw_target_latest_status""")
    pp.printAllTargets(results)

def oneTarget(target=None):
    if not target: target = int(input('\nEnter id of target company: '))
    results = psql.selectFromPSQL(f"SELECT * FROM targets WHERE target_id = {target}")
    for row in results:
        pp.printTarget(row)
    results = psql.selectFromPSQL(f"SELECT * FROM vw_position_info WHERE target_id = {target}")
    print(f'Positions: {len(results)}')
    for row in results:
        pp.printPosition(row, True, 4)

def addTarget():
    confirm = False
    while confirm != 'y':
        print("\nEnter details for new target company.")
        targetName = input("Enter target name: ")
        targetLink = input("Enter link to target website or information: ")
        targetDesc = input("Enter a brief description of the target: ")
        targetLoc = input("Enter location of target: ")
        target = (None, targetName, targetLink, targetDesc, targetLoc)
        pp.printTarget(target)
        confirm = input("Enter y to confirm target information is correct, enter x to return to the main menu, anything else to re-enter target info: ")
        if confirm.lower() == 'x': return 0
        if confirm.lower() == 'y':
            queryText = f"INSERT INTO targets (target_name, target_link, target_description, target_location) VALUES (%s, %s, %s, %s)"
            queryVars = target[1:]
            added = psql.crudPSQL(queryText, queryVars)
            pp.printAdded(added)

def addPosition():
    confirm = False
    while confirm != 'y':
        print("\nEnter detail for new position.")
        posTarget = None
        while isinstance(posTarget, int) == False:
            print("\nEnter the ID for the target company, or\nenter L to list target companies and their ID, or\nenter X to return to main menu", end='')
            posTarget = input(': ')
            if posTarget.lower() == 'l': allTargets()
            elif posTarget.lower() == 'x': return 0
            else:
                try:
                    posTarget = int(posTarget)
                except:
                    print("Target ID must be an integer, please try again.")
                    posTarget = None
                    continue
                try:
                    targetName = psql.selectFromPSQL(f"SELECT target_name FROM targets WHERE target_id = {posTarget}")
                    assert targetName and targetName != []
                    print(f'Target company {targetName} selected.')
                except Exception as err:
                    print("Given target id not found in the database.", err)
                    posTarget = None
        posName = input('Enter the position title/name: ')
        posTier = None
        while isinstance(posTier, int) == False:
            print("\nEnter the position priority / interest tier, or\nenter T to print a list of tiers, or\nenter X to return to the main menu", end='')
            posTier = input(": ")
            if posTier.lower() == 't': pp.printTiers()
            elif posTier.lower() == 'x': return 0
            else:
                try:
                    posTier = int(posTier)
                except:
                    print("Tier ID must be an integer, please try again.")
                    posTier = None
                    continue
                try:
                    tierName = psql.selectFromPSQL(f"SELECT tier_name FROM tiers WHERE tier_id = {posTier}")
                    assert tierName and tierName != []
                    print(f'Chosen tier description: {tierName}.')
                except Exception as err:
                    print("Given tier id not found in the database.", err)
                    posTier = None
        posLink = input('Enter a link to the position description or posting: ')
        posNotes = input('Enter any relevant notes about the position: ')
        pp.printPosition((None, posTarget, posName, posLink, posTier, tierName, posNotes))
        confirm = input("Enter Y to confirm position information is correct, enter X to return to the main menu, anything else to re-enter target info: ")
        if confirm.lower() == 'x': return 0
        if confirm.lower() == 'y':
            queryText = "INSERT INTO positions (target_id, position_name, position_link, position_tier, position_notes) VALUES (%s, %s, %s, %s, %s)"
            queryVars = ( posTarget, posName, posLink, posTier, posNotes )
            added = psql.crudPSQL(queryText, queryVars)
            pp.printAdded(added)

def updateStatus():
    confirm = False
    while confirm != 'y':
        print("\nEnter information for position update.")
        posTarget = None
        while isinstance(posTarget, int) == False:
            print("Enter the ID for the target company, or\nenter L to list target companies and their ID, or\nenter X to return to main menu", end='')
            posTarget = input(': ')
            if posTarget.lower() == 'l': allTargets()
            elif posTarget.lower() == 'x': return 0
            else:
                try:
                    posTarget = int(posTarget)
                except:
                    print("Target ID must be an integer, please try again.")
                    posTarget = None
                    continue
                try:
                    targetName = psql.selectFromPSQL(f"SELECT target_name FROM targets WHERE target_id = {posTarget}")
                    assert targetName and targetName != []
                    print(f'Target company {targetName} selected.')
                except Exception as err:
                    print("Given target id not found in the database.", err)
                    posTarget = None
        posId = None
        while isinstance(posId, int) == False:
            print("\nEnter the position id, or\nenter P to print a list of positions, or\nenter X to return to the main menu", end='')
            posId = input(": ")
            if posId.lower() == 'p': oneTarget(posTarget)
            elif posId.lower() == 'x': return 0
            else:
                try:
                    posId = int(posId)
                except:
                    print("Position ID must be an integer, please try again.")
                    posId = None
                    continue
                try:
                    posName = psql.selectFromPSQL(f"SELECT position_name FROM positions WHERE position_id = {posId}")
                    assert posName and posName != []
                    print(f'Selected position: {posName}.')
                except Exception as err:
                    print("Given position id not found in the database.", err)
                    posId = None
        statusId = None
        while isinstance(statusId, int) == False:
            print("\nEnter the status id, or\nenter S to print a list of statuses, or\nenter X to return to the main menu", end='')
            statusId = input(": ")
            if statusId.lower() == 's': pp.printStatuses()
            elif statusId.lower() == 'x': return 0
            else:
                try:
                    statusId = int(statusId)
                except:
                    print("Status ID must be an integer, please try again.")
                    statusId = None
                    continue
                try:
                    status = psql.selectFromPSQL(f'SELECT status FROM statuses WHERE status_id = {statusId}')
                    assert status and status != []
                    print(f'Selected statis: {status}.')
                except Exception as err:
                    print("Given status id not found in the database.", err)
                    statusId = None
        statusNote = input('Enter any relevant notes about the status update: ')
        statusDate = None
        while isinstance(statusDate, datetime.datetime) == False:
            statusDate = input("Enter the date of the status update, format YYYY-MM-DD, or\nleave the entry blank to use the current date and time:")
            if not statusDate:
                statusDate = datetime.datetime.now()
            else:
                try:
                    statusDate = datetime.datetime.strptime(statusDate, "%Y-%m-%d")
                except:
                    print('Incorrect date format, please try again.')
                    statusDate = None
        statusDate = statusDate.isoformat(sep = ' ', timespec='seconds')
        statusUpdate = (posId, statusDate, statusNote, statusId, status[0][0])
        print(statusUpdate)
        confirm = input("Enter Y to confirm that updated status is correct, enter X to return to the main menu, anything else to re-enter status update info: ")
        if confirm.lower() == 'x': return 0
        if confirm.lower() == 'y':
            queryText = "INSERT INTO status_log (position_id, status_date, status_id, status_note) VALUES (%s, %s, %s, %s)"
            queryVars = ( posId, statusDate, statusId, statusNote )
            added = psql.crudPSQL(queryText, queryVars)
            pp.printAdded(added)

if __name__ == '__main__':
    intro(1)
    allTargets()
    oneTarget(126)