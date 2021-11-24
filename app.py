
from modules import menuFunctions as mf

if __name__ == '__main__':
    while True:
        choice = mf.intro()
        if choice == '1': mf.allTargets()            
        elif choice == '2': mf.searchTargetName()
        elif choice == '3': mf.oneTarget()
        elif choice == '4': mf.addTarget()
        elif choice == '5': mf.addPosition()
        elif choice == '6': mf.updateStatus()
        elif choice == '7': mf.listJobBoards()
        else:
            print('Thanks, come again.\n\n')
            exit(0)