from connectToPSQL import connectToPSQL
import prettyPrints as pp

if __name__ == '__main__':
    while True:
        choice = pp.intro()
        if choice == '1':
            for row in connectToPSQL("""SELECT * FROM targets ORDER BY target_id"""):
                print(f"{row[0]:>4} - {row[1]}")
        elif choice == '2':
            target = int(input('Enter id of target company: '))
            results = connectToPSQL(f"SELECT * FROM targets WHERE target_id = {target}")
            for row in results:
                pp.printTarget(row)
            results = connectToPSQL(f"SELECT * FROM positions WHERE target_id = {target}")
            for row in results:
                pp.printPosition(row, 5)
                
        else:
            print('Thanks, come again.\n\n')
            exit(0)