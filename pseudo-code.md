# Model description

Brand:
    name: str -> Brand's Name
    daily_budget: int -> Actual daily spend
    monthly_budget: int -> Actual monthly spend
    max_daily_budget: int -> Max daily budget
    max_monthly_budget: int -> Max monthly budget
    campaign_list: List[Campaign] -> All Brand's campaigns

Campaign:
    name: str -> Campaign's name
    base_cost: int -> Base cost of every campaign
    click_cost: int -> Per click's cost
    dayparting: Set[int] or None -> Dayparting list containing numbers from 0 to 23 or None
    active_daily: bool -> If the campaign can run on the current day
    active_monthly: bool -> If the campaign can run on the current month
    running: bool -> If the campaign is active now
    brand: Brand -> This campaign brand

## Constants
    min_number_of_clicks: int -> Minimum amount of clicks to be randomly generated
    max_number_of_clicks: int -> Maximum amount of clicks to be randomly generated

## Global variables to represent the database which will not be implemented on this test.

### Object containing all brands
BRANDS = {
    name: Brand,
    ...
}

### Object containing all campaigns
CAMPAIGNS = {
    name_brand: Campaign,
    ...
}

# Steps, using event loop

## Event loop

1. Every hour, will be checked for each campaign if the flags active_monthly and active_daily are True, and if they have the dayparting has any value or it does have a value which represents the actual hour.
2. If all checks are True, we will change the campaign running flag to True, representing the marketing advertisement.

### Running campaigns

1. Every minute, on each running campaign, we will generate the campaign cost, represented by: base_cost + (amount of clicks * click_cost).
2. The amount of clicks will be randomly generated between the constants min_number_of_clicks and max_number_of_clicks.
3. The total cost will be added to Brand's daily_budget and monthly_budget.
4. After every generation of clicks, will be verified if the monthly_budget reached the max_monthly_budget and then, if the daily_budget reached the max_daily_budget.

### Turning campaigns Off
1. If the monthly budget is reached, for each campaign in the brand, both flags running and active_monthly will change to False, meaning that the AD stopped beeing served.
2. If the daily budget is reached, for each campaign in the brand, both flags running and active_daily will change to False, meaning that the AD stopped beeing served.
3. In the campaign thread, if the running flag is False, the thread will close, stopping the campaign.


### Turning campaigns ON
1. At the start of every month (when day changes and day is equal 1), before the main code of the event loop, we will change all active_monthly and active_daily flags to True and monthly_budget and daily_budget to 0, it will allow each campaign to be processed on the event loop.
2. At the start of every day (when the day changes), before the main code of the event loop, we will change all active_daily to True and daily_budget to 0, it will allow each campaign to be processed on the event loop if the active_monthly flag is True.


# Assumptions
1. Every minute, for each campaign, the amount of clicks will always be between min_number_of_clicks and max_number_of_clicks.
2. dayparting will not use a granular control to be kept simple, so, it will always be checked on full hours and be presented by integers like: 1,2,3, ... 23.
3. No data will be persisted, so the code starts at the moment that its turned on with all default values set. And if you close and re-open, everything will be reset.
4. All starting values will be declared on dummy_data.json.
5. Brand names should be unique.
6. Campaign names should be unique per brand.
7. All values are integers, but their true value should be divided by 100 -> 100 means $1, then 150 means $1.50 and 100000 means $1000.
8. Time is relative on this test, the default value is 1 but for testing purposes we can change the time increment, and any delay will be added as time dilatation on the event_loop
9. Time in UTC

