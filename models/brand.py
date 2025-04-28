import pprint
import logging

class Brand:
    name: str
    daily_budget: int = 0
    monthly_budget: int = 0
    max_daily_budget: int = 0
    max_monthly_budget: int = 0 
    campaign_list: list = []
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)
            
    
    def __repr__(self):
        return self.name
    
    def reset_all_campaigns(self, time=None, test=False):
        if not test:
            logging.info(f'Resetting monthly budget and campaigns for brand: {self.name} at {time}')
        self.daily_budget = 0
        self.monthly_budget = 0
        for campaign in self.campaign_list:
            campaign.active_daily = True
            campaign.active_monthly = True
            
    def reset_daily_campaigns(self, time=None, test=False):
        if not test:
            logging.info(f'Resetting daily budget and campaigns for brand: {self.name} at {time}')
        self.daily_budget = 0
        for campaign in self.campaign_list:
            campaign.active_daily = True
    
    def stop_all_campaigns(self, daily=False, monthly=False, time=None, test=False):
        for campaign in self.campaign_list:
            campaign.running = False
            
            if daily:
                campaign.active_daily = False
                if not test:
                    logging.info(f'stopping daily campaign: {campaign} for brand {campaign.brand} at {time}')
            elif monthly:
                campaign.active_monthly = False
                if not test:
                    logging.info(f'stopping monthly campaign: {campaign} for brand {campaign.brand} at {time}')
            else:
                if not test:
                    logging.info(f'stopping campaign: {campaign} for brand {campaign.brand} at {time}')