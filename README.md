# take-home-01
Public repository made for a take home problem

# Purpose
This code represents an Ad agency, this agency manages multiple brands and for each brand it runs multiple campaigns.
But all brands have a maximum daily budget and a maximum monthly budget, that should turn off all campaigns if reached or exceeeded.
Some campaigns should run only on defined hours a day.

# How to run this code

## Main scenario
This code doesn't need any external lib, just python installed. It was built using Python 3.12.3 but should run in any 3xx version.
Just go to the root folder and run python main.py (or python3 main.py on linux, recommended.)
You will be prompted a menu with the following options:

1. All brands
2. All Campaigns
3. Time now
4. Change time
5. Change time step
6. Pause/Start time
7. Exit

At this moment, the event loop will be running, and you will be able to read any update on logs.log, every iteration it will print the string representing the actual time.

If you type 1 and enter. You will be able to see all the brands registered.
If you type 2 and enter. You will be able to see all campaigns registered.
If you type 3 and enter. You will be able to see the string representing actual time.
If you type 4 and enter. You will be prompted again to choose a differente date with the format mm/dd/yyyy HH:mm.
If you type 5 and enter. You will be prompted again to choose a new time step in seconds, I will explain further about this step.
If you type 6 and enter. Time will toggle between stopping and activating.
If you type 7 and enter. The program will close.

About step 5, the purpose is beeing able to run this code from any time, to any time and with any speed.
So, if you type 2 -> Time will run twice as fast, and if you type 3600, type will pass as 1hour/second.

So, to validate I recommend changing the time_step to 1800 (every 30 minutes) and watch the file logs.log. You can type 6 and enter any time to stop the event_loop and analyze all brands and campaigns.

## Test cases

I Designed a batch of test cases to validate this code, they are all on the tests folder under the file run_tests.py
but you can also start it from the test.py file on the main folder test.py

All results will be displayed on the log, including a complete test that goes from 01/01/2025 to 02/01/2025

This test will not use data from dummy_data, instead, it will use data from test_data.json, settings some constants to always present the same result.

And will run only for one brand with one campaign, feel free to add more.

# The data structures

## Model description

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

## The main resources

### Main Event
Is the initial object that holds all logic in place.
When the MainEvent is initialized, it loads the dummy_data.json object and define the initial parameters as brands, campaigns and constants defined here.

### Event loop
I created an event loop to describe the passage of time that starts in a separated thread when code starts.
On the event loop, every second, it updates the passage of time and run all scheduled tasks (run_minute_task, run_hour_task)
Any delay calculated during the tasks will be added to the next time step as time dilatation
On this event loop, you can simulate any passage of time by any amount of seconds, just changing the TIME_STEP variable with the prompt number (5)

Later if desired, the event loop can be deprecated and changed by any task manager like celery or apscheduler, just calling the same functions (run_minute_task, run_hour_task).

### Minute Task
Is a task that represents a marketing campaign beeing run, more specifically, clients clicking on the Ad and contabilizing spend values.

### Hour Task
Is a task that will serve to initiate/stop the campaigns and also resetting the campaigns at the start of each day and month accordingly.

### Control
Is just a helper to navigate through the data and manipulate values across the Main Event

### Tests
The tests realized to assert that everything will work fine.

# The flow of the program

* After the event loop starts, every second, the time will be incremented by a determined amount (that you can change any time you want)
* Every time an hour change is detected, first we detect if a day changed, and if the day changed, if the next day is 1, representing a month change
* If a month changes, we will run the brand's function reset_all_campaigns which sets all brands daily_budget and monthly_budget to 0 and all campaign's active_daily and active_monthly flags to True
* If a day changes, we will run the brand's function reset_daily_campaigns which sets all brands daily_budget to 0 and all campaign's active_daily flag to True
* Then, all campaign will be verified with the checks as follows:
* If active_monthly is true, if active_daily is true, if dayparting is None OR if dayparting is not None but contains the corresponding new hour
* If all checks are true, this campaign will change to be "running" represented by a property on the object.
* If the campaign value was False and changed to True, the property base_cost will be automatically added using the Brand's spend function
* Every time a minute change is detected, all campaigns that are running will receive an amount of budget using the spend function represented by: SOMATORY[(campaign click_cost) * (random value between constants min_number_of_clicks and max_number_of_clicks)] per amount of minutes changed. So, if 2 minutes passed on a single tick, we will calculate (campaign click_cost) * (random value between constants min_number_of_clicks and max_number_of_clicks) twice
* The spend function adds the same number to both daily_budget and monthly_budget and then verifies if the max_monthly_budget or max_daily_budget reached or exceeded.
* If any of these values are reached (max_monthly_budget or max_daily_budget), all campaigns from the brand will be closed using the brand's model function stop_all_campaigns, and passing as argument if it was monthly or daily. It iterates all campaigns from the brand and changes the active_daily or active_monthly flag to off and also changes the running flag to off, so these campaigns will not register any more budgets again till the reset.

With this, we covered the required steps:
1. Checking and updating daily/monthly spends
2. Turning campaigns on/off when budgets are hit/exceeded
3. Resetting the budgets and reactivating campaigns at the start of each new day/month
4. Respecting dayparting schedules


# Assumptions and simplifications
1. Every minute, for each campaign, the amount of clicks will always be between min_number_of_clicks and max_number_of_clicks representing a running campaign.
2. dayparting will not use a granular control to be kept simple, so, it will always be checked on full hours and be presented by integers like: 1,2,3, ... 23.
3. No data will be persisted, so the code starts at the moment that its turned on with all default values set. And if you close and re-open, everything will be reset.
4. All starting values will be declared on dummy_data.json.
5. Brand names should be unique.
6. Campaign names should be unique per brand.
7. All values are integers, but their true value should be divided by 100 -> 100 means $1, then 150 means $1.50 and 100000 means $1000.
8. Time is relative on this test, the default value is 1 but for testing purposes we can change the time increment, and any delay will be added as time dilatation on the event_loop
9. Time in UTC
10. I Avoided some type annotations to keep it working in any python version