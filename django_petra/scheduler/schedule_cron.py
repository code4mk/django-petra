from celery.schedules import crontab, timedelta

class ScheduleCron:
    def __init__(self):
        self.schedule_cron = None

    def cron(self, cron_schedule):
        self.schedule_cron = crontab(cron_schedule)
        return self

    def everySecond(self):
        self.schedule_cron = timedelta(seconds=1)
        return self

    def everyTwoSeconds(self):
        self.schedule_cron = timedelta(seconds=2)
        return self

    def everyFiveSeconds(self):
        self.schedule_cron = timedelta(seconds=5)
        return self

    def everyTenSeconds(self):
        self.schedule_cron = timedelta(seconds=10)
        return self

    def everyFifteenSeconds(self):
        self.schedule_cron = timedelta(seconds=15)
        return self

    def everyTwentySeconds(self):
        self.schedule_cron = timedelta(seconds=20)
        return self

    def everyThirtySeconds(self):
        self.schedule_cron = timedelta(seconds=30)
        return self

    def everyMinute(self):
        self.schedule_cron = crontab(minute='*')
        return self

    def everyTwoMinutes(self):
        self.schedule_cron = crontab(minute='*/2')
        return self

    def everyThreeMinutes(self):
        self.schedule_cron = crontab(minute='*/3')
        return self

    def everyFourMinutes(self):
        self.schedule_cron = crontab(minute='*/4')
        return self

    def everyFiveMinutes(self):
        self.schedule_cron = crontab(minute='*/5')
        return self

    def everyTenMinutes(self):
        self.schedule_cron = crontab(minute='*/10')
        return self

    def everyFifteenMinutes(self):
        self.schedule_cron = crontab(minute='*/15')
        return self

    def everyThirtyMinutes(self):
        self.schedule_cron = crontab(minute='*/30')
        return self

    def hourly(self):
        self.schedule_cron = crontab(minute=0, hour='*')
        return self

    def hourlyAt(self, minute):
        self.schedule_cron = crontab(minute=minute, hour='*')
        return self

    def everyOddHour(self, minutes=0):
        self.schedule_cron = crontab(minute=minutes, hour='1-23/2')
        return self

    def everyTwoHours(self, minutes=0):
        self.schedule_cron = crontab(minute=minutes, hour='*/2')
        return self

    def everyThreeHours(self, minutes=0):
        self.schedule_cron = crontab(minute=minutes, hour='*/3')
        return self

    def everyFourHours(self, minutes=0):
        self.schedule_cron = crontab(minute=minutes, hour='*/4')
        return self

    def everySixHours(self, minutes=0):
        self.schedule_cron = crontab(minute=minutes, hour='*/6')
        return self

    def daily(self):
        self.schedule_cron = crontab(minute=0, hour=0)
        return self

    def dailyAt(self, time):
        hour, minute = map(int, time.split(':'))
        self.schedule_cron = crontab(minute=minute, hour=hour)
        return self

    def twiceDaily(self, first, second):
        self.schedule_cron = crontab(minute=0, hour=(first, second))
        return self

    def twiceDailyAt(self, first, second, minute):
        self.schedule_cron = crontab(minute=minute, hour=(first, second))
        return self

    def weekly(self):
        self.schedule_cron = crontab(minute=0, hour=0, day_of_week=0)
        return self

    def weeklyOn(self, day, time):
        hour, minute = map(int, time.split(':'))
        self.schedule_cron = crontab(minute=minute, hour=hour, day_of_week=day)
        return self

    def monthly(self):
        self.schedule_cron = crontab(minute=0, hour=0, day_of_month=1)
        return self

    def monthlyOn(self, day, time):
        hour, minute = map(int, time.split(':'))
        self.schedule_cron = crontab(minute=minute, hour=hour, day_of_month=day)
        return self

    def twiceMonthly(self, first, second, time):
        hour, minute = map(int, time.split(':'))
        self.schedule_cron = crontab(minute=minute, hour=hour, day_of_month=(first, second))
        return self

    def lastDayOfMonth(self, time):
        hour, minute = map(int, time.split(':'))
        self.schedule_cron = crontab(minute=minute, hour=hour, day_of_month=-1)
        return self

    def quarterly(self):
        self.schedule_cron = crontab(minute=0, hour=0, month_of_year=(1, 4, 7, 10), day_of_month=1)
        return self

    def quarterlyOn(self, month, time):
        hour, minute = map(int, time.split(':'))
        self.schedule_cron = crontab(minute=minute, hour=hour, month_of_year=month, day_of_month=1)
        return self

    def yearly(self):
        self.schedule_cron = crontab(minute=0, hour=0, day_of_month=1, month_of_year=1)
        return self

    def yearlyOn(self, month, day, time):
        hour, minute = map(int, time.split(':'))
        self.schedule_cron = crontab(minute=minute, hour=hour, day_of_month=day, month_of_year=month)
        return self
