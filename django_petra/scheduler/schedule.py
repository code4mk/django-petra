import inspect
from .schedule_cron import ScheduleCron

class ScheduleConverter:
    def __init__(self, schedules):
        self.schedules = schedules
        self.result = {}

    def convert(self):
        for schedule in self.schedules:
            task_method =  schedule.task_data.get('task')
            name = schedule.name_data
            last_part = schedule.schedule_cron
            task_method_name = task_method.__name__
            module_name = inspect.getmodule(task_method).__name__
            
            self.result[name] = {
                'task': f'{module_name}.{task_method_name}',
                'schedule': last_part,
            }

        return self.result

class Schedule(ScheduleCron):
    def __init__(self):
        self.task_data = {}
        self.name_data = None
        self.schedule_cron = None

    def task(self, task):
        self.task_data['task'] = task
        return self

    def name(self, name):
        self.name_data = name
        return self


def bind_beat_schedule(schedules):
    data = ScheduleConverter(schedules).convert()
    return data