
import pprint
from datetime import datetime

def control(object):
    while True:
        func = input('Options: \n1. All brands\n2. All Campaigns\n3. Time now\n4. Change time\n5. Change time step\n6. Pause/Start time\n7. Exit\n')
        try: 
            func = int(func)
            if func == 1:
                for key, brand in object.BRANDS.items():
                    print('\n', key, ':')
                    pprint.pprint(brand.__dict__)
            elif func == 2:
                for key, campaign in object.CAMPAIGNS.items():
                    print('\n', key, ':')
                    pprint.pprint(campaign.__dict__)
            elif func == 3:
                print(object.DATETIME.strftime('%m/%d/%Y %H:%M:%S'))
            elif func == 4:
                date = input('Choose the actual date, example: mm/dd/yyyy HH:mm\n')
                object.DATETIME = datetime.strptime(date, "%m/%d/%Y %H:%M")
            elif func == 5:
                timestep = int(input('Choose the number for the time step, integers only\n'))
                object.TIME_STEP = timestep
            elif func==6:
                object.PAUSE = not object.PAUSE
            elif func == 7:
                quit()
        except Exception as Err:
            print('Invalid option, try again.\n', Err)