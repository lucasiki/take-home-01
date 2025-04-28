
def run_hour_task(from_date, to_date, object, test=False):
    """
    First check the difference in hours from to_date and from_date,
    if changed, should verify every campaign to set the running flag accordingly
    Check if day == 1 and day changed to consider the start of a new month or a day change
    """
    
    difference = int((to_date - from_date).total_seconds() // 3600)

    hour_changed = difference > 0 or to_date.hour != from_date.hour

    day_changed = (to_date.day != from_date.day) or difference > 24
    
    month_changed = (day_changed and to_date.day == 1)
    
    if test:
        return day_changed, hour_changed, month_changed
        
    if month_changed:
        reset_all_monthly_campaigns(object, time=object.DATETIME)
    elif day_changed:
        reset_all_daily_campaigns(object, time=object.DATETIME)
    
    if hour_changed:
        verify_all_campaigns(to_date.hour, object, time=object.DATETIME)
        
    
    
def reset_all_monthly_campaigns(object, time=None):
    for brand in object.BRANDS.values():
        brand.reset_all_campaigns(time=time)
        
def reset_all_daily_campaigns(object, time=None):
    for brand in object.BRANDS.values():
        brand.reset_daily_campaigns(time=time)
        
def verify_all_campaigns(hour, object, time=None):
    
    for campaign in object.CAMPAIGNS.values():
        campaign.verify(hour, time=time)
        