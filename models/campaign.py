
from .brand import Brand
import logging

class Campaign:
    name: str 
    base_cost: int = 0
    click_cost: int = 0
    dayparting: set[int] | None = None
    active_daily: bool = True
    active_monthly: bool = True
    running: bool = False
    brand: Brand 
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)
            
        self.active_daily = self.active_daily
        self.active_monthly = self.active_monthly
        self.running = self.running
            
    def __repr__(self):
        return self.name
    
    def spend(self, amount, time=None, test=False):
        self.brand.daily_budget += amount
        self.brand.monthly_budget += amount
        
        if self.brand.monthly_budget >= self.brand.max_monthly_budget:
            if not test:
                logging.info(f'Monthly budget reached for brand: {self.brand}, stopping campaigns from this brand at {time}.')
            self.brand.stop_all_campaigns(monthly=True, time=time, test=test)
        if self.brand.daily_budget >= self.brand.max_daily_budget:
            if not test:
                logging.info(f'Daily budget reached for brand: {self.brand}, stopping all campaigns from this brand at {time}, monthly budget: {self.brand.monthly_budget}')
            self.brand.stop_all_campaigns(daily=True, time=time, test=test)
            
            
    def verify(self, hour, time=None, test=False):
        last_state = self.running
        self.running = self.active_daily and self.active_monthly and \
                                        (self.dayparting is None or hour in self.dayparting)
        if not last_state and self.running:
            if not test:
                logging.info(f'starting campaign: {self.brand} {self} at {time}')
            self.spend(self.base_cost)
        elif last_state and not self.running:
            if not test:
                logging.info(f'stopping campaign: {self.brand} {self} at {time}')