import json
import pprint
from datetime import datetime, UTC
from models.brand import Brand
from models.campaign import Campaign
from tasks.event_loop import init_event_loop_thread
from control import control
import logging

with open("./logs.log", "w") as file:
    file.truncate(0)  # Clears the file

logging.basicConfig(
    filemode='a',
    filename='./logs.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d, %H:%M:%S',
)

class MainEvent:
    
    DATETIME = datetime.now(tz=UTC)
    
    BRANDS = dict()
    CAMPAIGNS = dict()
    
    min_number_of_clicks = 0
    max_number_of_clicks = 5
    
    TIME_STEP = 1
    
    PAUSE = False
    
    INITIAL_DATA = {}
    
    def __init__(self, initial_file='./dummy_data.json'):
        with open(initial_file, 'r') as f:
            self.INITIAL_DATA = json.loads(f.read())

        self.initialize()
        
        
    def initialize(self):
        for key, value in self.INITIAL_DATA['brands'].items():
            brand = Brand(name=key, **value)
            self.BRANDS[key] = brand
            new_campaign_list = []
            for campaign in brand.campaign_list:
                new_campaign = Campaign(brand=brand, **campaign)
                self.CAMPAIGNS[f"{key}_{new_campaign.name}"] = new_campaign
                new_campaign_list.append(new_campaign)
            brand.campaign_list = new_campaign_list
            
        self.DATETIME = datetime.now(tz=UTC).replace(second=0, microsecond=0)
        
        constants = self.INITIAL_DATA.get('constants', {})
        self.TIME_STEP = constants.get('time_step', 1)
        self.min_number_of_clicks = constants.get('min_number_of_clicks', 0)
        self.max_number_of_clicks = constants.get('max_number_of_clicks', 5)
                  
    def start_tasks(self):
        init_event_loop_thread(self)    
            
if __name__ == '__main__':
    mainevent = MainEvent()
    mainevent.initialize()
    mainevent.start_tasks()
    control(mainevent)