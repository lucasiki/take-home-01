from random import randrange

def run_minute_task(from_date, to_date, object, test=False):
    """
    First check the difference in minutes from to_date and from_date,
    then, for each running campaign, generate and add the spend value.
    Deactivate campaigns if limits reached
    """
    difference = int((to_date - from_date).total_seconds() // 60)
        
    if from_date.minute != to_date.minute and difference == 0:
        difference += 1
        
    if test:
        return difference
    
    if difference > 0:
        generate_spend_values(difference, object)
        

    

def generate_spend_values(difference, object, test=False):
    for campaign in object.CAMPAIGNS.values():
        if campaign.running:
            spend_value = sum([campaign.click_cost * randrange(object.min_number_of_clicks, 
                                                           object.max_number_of_clicks) 
                           for _ in range(difference)])
            campaign.last_spend_value = spend_value
            if not test:
                campaign.spend(spend_value, time=object.DATETIME)  

                