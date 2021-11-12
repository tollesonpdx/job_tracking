from connectToPSQL import connectToPSQL
import prettyPrints as pp

def intro(defaultEntry = None):
    pp.intro()
    return defaultEntry or input("Enter option: ")

def allTargets():
    results = connectToPSQL("""SELECT * FROM vw_target_latest_status""")
    lenId, lenName = 0, 0
    for row in results:
        lenId = max(lenId, len(str(row[0])))
        lenName = max(lenName, len(row[1] or ''))
    print(f"{'ID':>{lenId}} - {'Company Name':<{lenName}} - {'Last Date of Activity'}")
    for row in results:
        print(f"{row[0]:>{lenId}} - {row[1] or '':<{lenName}} - {row[2] or ''}")

def oneTarget(target=None):
    if not target: target = int(input('Enter id of target company: '))
    results = connectToPSQL(f"SELECT * FROM targets WHERE target_id = {target}")
    for row in results:
        pp.printTarget(row)
    results = connectToPSQL(f"SELECT * FROM positions WHERE target_id = {target}")
    for row in results:
        pp.printPosition(row, True, 4)

if __name__ == '__main__':
    intro(1)
    allTargets()
    oneTarget(126)