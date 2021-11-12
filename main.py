
from modules import menuFunctions as mf

if __name__ == '__main__':
    while True:
        choice = mf.intro()
        if choice == '1': mf.allTargets()            
        elif choice == '2': mf.oneTarget()
        elif choice == '3': mf.addTarget()      
        else:
            print('Thanks, come again.\n\n')
            exit(0)