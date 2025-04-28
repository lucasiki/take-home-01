import logging
from datetime import datetime
from datetime import timedelta
from models.brand import Brand
from models.campaign import Campaign
from tasks.event_loop import event_loop_body
from tasks.hour_task import run_hour_task
from tasks.minute_task import run_minute_task
from tasks.minute_task import generate_spend_values
from time import sleep

def verify_constants(object):
    
    """Verify if all constants belong to the adequate values."""
    
    logging.info("[test] [verify_constants] [start]")

    assert type(object.BRANDS) == dict, 'BRANDS is not a dict'
    assert type(object.CAMPAIGNS) == dict, 'CAMPAIGNS is not a dict'
    assert type(object.TIME_STEP) == int, 'TIME_STEP is not an int'
    assert object.TIME_STEP > 0, 'TIME_STEP should be greater than 0'
    assert type(object.min_number_of_clicks) == int, 'TIME_STEP  is not an int'
    assert type(object.max_number_of_clicks) == int, 'TIME_STEP  is not an int'
    assert object.min_number_of_clicks >= 0, 'min_number_of_clicks should be greater than 0'
    assert object.max_number_of_clicks > 0, 'max_number_of_clicks should be greater than 0'
    assert object.max_number_of_clicks >= object.min_number_of_clicks, 'max_number_of_clicks should be greater than min_number_of_clicks'
    
    logging.info("[test] [verify_constants] [completed]")

def verify_brands(brands):
    
    """Verify if all brands have the adequate properties."""
    
    logging.info("[test] [verify_brands] [start]")
    
    for brand in brands.values():
        
        assert type(brand) == Brand, f"Brand {brand} should be of type Brand"
        
        assert type(brand.name) == str, f"Brand {brand} name should be a string"
        assert type(brand.daily_budget) == int, f"Brand {brand} daily_budget should be an int"
        assert type(brand.monthly_budget) == int, f"Brand {brand} monthly_budget should be an int"
        assert type(brand.max_daily_budget) == int, f"Brand {brand} max_daily_budget should be an int"
        assert type(brand.max_monthly_budget) == int, f"Brand {brand} max_monthly_budget should be an int"
        assert type(brand.campaign_list) == list, f"Brand {brand} campaign_list should be a list"
        
        assert brand.daily_budget >= 0, f"Brand {brand} daily_budget be greater or equal 0"
        assert brand.monthly_budget >= 0, f"Brand {brand} monthly_budget be greater or equal 0"
        assert brand.max_daily_budget >= 0, f"Brand {brand} max_daily_budget be greater or equal 0"
        assert brand.max_monthly_budget >= 0, f"Brand {brand} max_monthly_budget be greater or equal 0"
        
        for campaign in brand.campaign_list:
            assert type(campaign) == Campaign, f"Brand {brand}, campaign {campaign} should be of type Campaign"
        
    logging.info("[test] [verify_brands] [completed]")

def verify_campaigns(campaigns):
    
    """Verify if all campaigns have the adequate properties."""
    
    logging.info("[test] [verify_campaigns] [start]")
    
    for campaign in campaigns.values():
        assert type(campaign) == Campaign, f"Campaign {campaign} should be of type Campaign"
        assert type(campaign.brand) == Brand, f"Campaign {campaign} brand should be of type Brand"
        
        assert type(campaign.name) == str, f"Campaign {campaign} name should be a string"
        assert type(campaign.base_cost) == int, f"Campaign {campaign} base_cost should be an int"
        assert type(campaign.click_cost) == int, f"Campaign {campaign} click_cost should be an int"
        assert type(campaign.active_daily) == bool, f"Campaign {campaign} active_daily should be True or False"
        assert type(campaign.active_monthly) == bool, f"Campaign {campaign} active_monthly should be True or False"
        assert type(campaign.running) == bool, f"Campaign {campaign} running should be True or False"
        assert (type(campaign.dayparting) == type(None) or type(campaign.dayparting) == list), f"Campaign {campaign} dayparting should be None or a list"
        
        if campaign.dayparting is not None:
            for each in campaign.dayparting:
                assert type(each) == int, f"Campaign {campaign} dayparting value should be an int"
                assert each >= 0 and each < 24, f"Campaign {campaign} dayparting value should be greater or equal 0 and lower than 24"
        
        assert campaign.base_cost >= 0, f"Campaign {campaign} base_cost should be greater or equal 0"
        assert campaign.click_cost >= 0, f"Campaign {campaign} click_cost greater or equal 0"


    logging.info("[test] [verify_campaigns] [completed]")

def verify_event_loop(object):
    
    """Verify if the eventloop is running properly."""
    
    logging.info("[test] [verify_event_loop] [start]")
    object.DATETIME = datetime.strptime("01/01/2025 00:00", "%m/%d/%Y %H:%M")
    for _ in range(0, 3600):
        time_before = object.DATETIME
        event_loop_body(object, 3600, test=True)
        assert object.DATETIME == (time_before + timedelta(seconds=3600))
    logging.info("[test] [verify_event_loop] [completed]")

def verify_hour_task(object):
    
    """Verify if the hour task is running properly."""
    
    logging.info("[test] [verify_hour_task] [start]")
    
    first_date = datetime.strptime("01/01/2025 00:00", "%m/%d/%Y %H:%M")
    object.DATETIME = datetime.strptime("01/01/2025 01:00", "%m/%d/%Y %H:%M")
    
    _, hour_changed, _ = run_hour_task(first_date, object.DATETIME, object, test=True)
    
    assert hour_changed == True, "Hour didn't change"
    
    first_date = datetime.strptime("01/01/2025 00:59", "%m/%d/%Y %H:%M")
    object.DATETIME = datetime.strptime("01/01/2025 01:00", "%m/%d/%Y %H:%M")
    
    _, hour_changed, _ = run_hour_task(first_date, object.DATETIME, object, test=True)
    
    assert hour_changed == True, "Hour didn't change"
    
    object.DATETIME = datetime.strptime("01/02/2025 00:00", "%m/%d/%Y %H:%M")
    
    day_changed, hour_changed, _ = run_hour_task(first_date, object.DATETIME, object, test=True)
    
    assert hour_changed == True, "Hour didn't change"
    assert day_changed == True, "Day didn't change"
    
    object.DATETIME = datetime.strptime("02/01/2025 00:00", "%m/%d/%Y %H:%M")
    
    day_changed, hour_changed, month_changed = run_hour_task(first_date, object.DATETIME, object, test=True)
    
    assert month_changed == True, "Month didn't change"
    assert hour_changed == True, "Hour didn't change"
    assert day_changed == True, "Day didn't change"
    
    object.DATETIME = datetime.strptime("01/01/2026 00:00", "%m/%d/%Y %H:%M")
    
    day_changed, hour_changed, month_changed = run_hour_task(first_date, object.DATETIME, object, test=True)
    
    assert month_changed == True, "Month didn't change"
    assert hour_changed == True, "Hour didn't change"
    assert day_changed == True, "Day didn't change"
    
    logging.info("[test] [verify_hour_task] [completed]")

def verify_minute_task(object):
    
    """Verify if the minute task is running properly."""
    
    logging.info("[test] [verify_minute_task] [start]")
    
    first_date = datetime.strptime("01/01/2025 00:00:00", "%m/%d/%Y %H:%M:%S")
    object.DATETIME = datetime.strptime("01/01/2025 00:00:30", "%m/%d/%Y %H:%M:%S")
    
    difference = run_minute_task(first_date, object.DATETIME, object, test=True)
    
    assert difference == 0, f'difference should be 0 and is {difference}'
    
    first_date = datetime.strptime("01/01/2025 00:00:59", "%m/%d/%Y %H:%M:%S")
    object.DATETIME = datetime.strptime("01/01/2025 00:01:00", "%m/%d/%Y %H:%M:%S")
    
    difference = run_minute_task(first_date, object.DATETIME, object, test=True)
    
    assert difference == 1,  f'difference should be 1 and is {difference}'
    
    first_date = datetime.strptime("01/01/2025 00:00:00", "%m/%d/%Y %H:%M:%S")
    object.DATETIME = datetime.strptime("01/01/2025 01:00:00", "%m/%d/%Y %H:%M:%S")
    
    difference = run_minute_task(first_date, object.DATETIME, object, test=True)
    
    assert difference == 60,  f'difference should be 60 and is {difference}'
    
    logging.info("[test] [verify_minute_task] [completed]")

def verify_generate_spend_values(object):
    
    """Verify if the generate_spend_values function is properly adding values."""
    
    logging.info("[test] [generate_spend_values] [start]")
    
    object.min_number_of_clicks = 1
    object.max_number_of_clicks = 2
    
    for campaign in object.CAMPAIGNS.values():
        campaign.running = True
        campaign.click_cost = 1
    
    difference = 60
    generate_spend_values(difference, object, test=True)
    
    for campaign in object.CAMPAIGNS.values():
        assert campaign.last_spend_value == difference, f"The last spend value should be {difference} and is: {campaign.last_spend_value}"

    logging.info("[test] [generate_spend_values] [completed]")

def verify_reset_all_campaigns(brands):
    
    """Verify if the reset_all_campaigns function from brand object is running properly."""
    
    logging.info("[test] [verify_reset_all_campaigns] [start]")
    
    for brand in brands.values():
        brand.daily_budget = 1000
        brand.monthly_budget = 1000
        for campaign in brand.campaign_list:
            campaign.active_daily = False
            campaign.active_monthly = False
            
        brand.reset_all_campaigns(test=True)

        assert brand.daily_budget == 0, f"Brand: {brand} daily budget is not 0 after reset."
        assert brand.monthly_budget == 0, f"Brand: {brand} monthly budget is not 0 after reset."
        for campaign in brand.campaign_list:
            assert campaign.active_daily == True, f"Brand: {brand} Campaign: {campaign} active_daily is not True after reset."
            assert campaign.active_monthly == True, f"Brand: {brand} Campaign: {campaign} active_monthly is not True after reset."
        
    logging.info("[test] [verify_reset_all_campaigns] [completed]")

def verify_reset_daily_campaigns(brands):
    
    """Verify if the reset_daily_campaigns function from brand object is running properly."""
    
    logging.info("[test] [verify_reset_daily_campaigns] [start]")
    
    for brand in brands.values():
        brand.daily_budget = 1000
        for campaign in brand.campaign_list:
            campaign.active_daily = False
            
        brand.reset_daily_campaigns(test=True)

        assert brand.daily_budget == 0, f"Brand: {brand} daily budget is not 0 after reset."
        for campaign in brand.campaign_list:
            assert campaign.active_daily == True, f"Brand: {brand} Campaign: {campaign} active_daily is not True after reset."
        
    logging.info("[test] [verify_reset_daily_campaigns] [completed]")

def verify_stop_all_campaigns(brands):
    
    """Verify if the reset_daily_campaigns function from brand object is running properly."""
    
    logging.info("[test] [verify_stop_all_campaigns] [start]")
    
    for brand in brands.values():
        for campaign in brand.campaign_list:
            campaign.running = True
            campaign.active_daily = True
            campaign.active_monthly = True
            
        brand.stop_all_campaigns(daily=True, test=True)
        
        for campaign in brand.campaign_list:
            assert campaign.running == False, f'Campaign {campaign} was not turned off properly from stop_all_campaigns'
            assert campaign.active_daily == False, f'Campaign {campaign} active_daily was not turned off properly from stop_all_campaigns'
            
            campaign.running = True
            campaign.active_daily = True
            campaign.active_monthly = True
            
        brand.stop_all_campaigns(monthly=True, test=True)
        
        for campaign in brand.campaign_list:
            assert campaign.running == False, f'Campaign {campaign} was not turned off properly from stop_all_campaigns'
            assert campaign.active_monthly == False, f'Campaign {campaign} active_monthly was not turned off properly from stop_all_campaigns'
    
    logging.info("[test] [verify_stop_all_campaigns] [completed]")

def verify_campaign_verify(campaigns):
    
    """Verify if the campaign_verify function from campaign object is running properly."""
    
    logging.info("[test] [verify_campaign_verify] [start]")
    
    for campaign in campaigns.values():
        campaign.running = False
        campaign.active_daily = True
        campaign.active_monthly = True
        campaign.dayparting = None
        
        campaign.verify(0, test=True)
        
        assert campaign.running == True, 'Campaign was not turned on properly.'
        
        campaign.active_daily = False
        
        campaign.verify(0, test=True)
        
        assert campaign.running == False, 'Campaign was not turned off properly.'
        
        campaign.active_daily = True
        
        campaign.verify(0, test=True)
        
        assert campaign.running == True, 'Campaign was not turned on properly.'
        
        campaign.active_monthly = False
        
        campaign.verify(0, test=True)
        
        assert campaign.running == False, 'Campaign was not turned off properly.'
        
        campaign.active_monthly = True
        campaign.dayparting = [0]
        
        campaign.verify(0, test=True)
        
        assert campaign.running == True, 'Campaign was not turned on properly with dayparting.'
        
        campaign.dayparting = [1,2,3]
        
        campaign.verify(0, test=True)
        
        assert campaign.running == False, 'Campaign was not turned off properly with dayparting.'
        
        campaign.dayparting = [10,11,12]
        
        campaign.verify(10, test=True)
        
        assert campaign.running == True, 'Campaign was not turned on properly with dayparting.'
        
    
    logging.info("[test] [verify_campaign_verify] [completed]")

def verify_campaign_spend(brands):
    
    """Verify if the campaign_spend function from campaign object is running properly."""
    
    logging.info("[test] [verify_campaign_spend] [start]")
    
    spend_increment = 100
    
    for brand in brands.values():
        brand.daily_budget = 0
        brand.monthly_budget = 0
        
        brand.max_daily_budget = 100
        brand.max_monthly_budget = 200
        
        for campaign in brand.campaign_list:
            campaign.spend(spend_increment, test=True)
            
        assert brand.daily_budget == len(brand.campaign_list) * spend_increment, f'Daily budget not incremented correctly on {brand}'
        
        daily_exceeded = brand.daily_budget >= brand.max_daily_budget
        monthly_exceeded = brand.monthly_budget >= brand.max_monthly_budget
        
        for campaign in brand.campaign_list:
            
            if monthly_exceeded:
                assert (campaign.active_monthly) == False, f'Campaign {campaign} active_monthly from brand {brand} was not deactivated correctly'
            if daily_exceeded:
                assert (campaign.active_daily) == False, f'Campaign {campaign} active_daily from brand {brand} was not deactivated correctly'
    
    
    
    logging.info("[test] [verify_campaign_spend] [completed]")
    
def complete_test(object):
    
    """This is a complete test that will replicate the campaigns working from 01/01/2025 to 02/02/2025
    with controlled values"""
    
    logging.info("[test] [complete_test] [start]")
            
    object.initialize()
    
    object.DATETIME = datetime.strptime("01/01/2025 00:00:00", "%m/%d/%Y %H:%M:%S")
        
    for _ in range(3600*24*32):
        event_loop_body(object, 1)
            
    logging.info("[test] [complete_test] [completed]")

def run_tests(object):

    verify_constants(object)
    verify_brands(object.BRANDS)
    verify_campaigns(object.CAMPAIGNS)
    verify_event_loop(object)
    verify_hour_task(object)
    verify_minute_task(object)
    verify_generate_spend_values(object)
    verify_reset_all_campaigns(object.BRANDS)
    verify_reset_daily_campaigns(object.BRANDS)
    verify_stop_all_campaigns(object.BRANDS)
    verify_campaign_verify(object.CAMPAIGNS)
    verify_campaign_spend(object.BRANDS)
    complete_test(object)
