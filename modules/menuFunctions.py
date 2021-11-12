from modules import connectToPSQL as psql
from modules import prettyPrints as pp

def intro(defaultEntry = None):
    pp.intro()
    return defaultEntry or input("Enter option: ")

def allTargets():
    results = psql.selectFromPSQL("""SELECT * FROM vw_target_latest_status""")
    lenId, lenName = 0, 0
    for row in results:
        lenId = max(lenId, len(str(row[0])))
        lenName = max(lenName, len(row[1] or ''))
    print(f"{'ID':>{lenId}} - {'Company Name':<{lenName}} - {'Last Date of Activity'}")
    for row in results:
        print(f"{row[0]:>{lenId}} - {row[1] or '':<{lenName}} - {row[2] or ''}")

def oneTarget(target=None):
    if not target: target = int(input('Enter id of target company: '))
    results = psql.selectFromPSQL(f"SELECT * FROM targets WHERE target_id = {target}")
    for row in results:
        pp.printTarget(row)
    results = psql.selectFromPSQL(f"SELECT * FROM vw_position_info WHERE target_id = {target}")
    for row in results:
        pp.printPosition(row, True, 4)

def addTarget():
    confirm = False
    while confirm != 'y':
        targetName = input("Enter target name: ")
        targetLink = input("Enter link to target website or information: ")
        targetDesc = input("Enter a brief description of the target: ")
        targetLoc = input("Enter location of target: ")
        target = (None, targetName, targetLink, targetDesc, targetLoc)
        pp.printTarget(target)
        confirm = input("Enter y to confirm target information is correct, enter x to exit, anything else to re-enter target info: ")
        if confirm == 'x': return 0
        if confirm == 'y':
            added = psql.selectFromPSQL(f"SELECT * FROM vw_position_info WHERE target_id = {target}")

if __name__ == '__main__':
    intro(1)
    allTargets()
    oneTarget(126)