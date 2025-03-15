from datetime import datetime, timedelta
import calendar

class SmartMeetingScheduler:
    def __init__(self):
        self.working_hours = (9, 17)  # 9 AM to 5 PM
        self.public_holidays = {  # Example holidays
            "2025-01-01", "2025-05-01", "2025-12-25"
        }
        self.schedule = {}

    def is_working_day(self, date):
        if date.weekday() >= 5 or date.strftime("%Y-%m-%d") in self.public_holidays:
            return False
        return True

    def get_available_slots(self, user, date):
        if not self.is_working_day(date):
            return []

        booked_slots = self.schedule.get(user, {}).get(date.strftime("%Y-%m-%d"), [])
        available_slots = []
        
        start_hour, end_hour = self.working_hours
        current_time = datetime(date.year, date.month, date.day, start_hour, 0)
        
        while current_time.hour < end_hour:
            next_time = current_time + timedelta(hours=1)
            if not any(s[0] < next_time and s[1] > current_time for s in booked_slots):
                available_slots.append((current_time.strftime('%I:%M %p'), next_time.strftime('%I:%M %p')))
            current_time = next_time
        
        if not available_slots:
            return "No available slots."
        
        formatted_slots = "\n".join([f"{start} - {end}" for start, end in available_slots])
        return f"Available slots:\n{formatted_slots}"

    def schedule_meeting(self, user, date, start_hour, end_hour):
        if not self.is_working_day(date):
            return "Cannot schedule on weekends or holidays."
        
        if start_hour < self.working_hours[0] or end_hour > self.working_hours[1]:
            return "Meeting must be within working hours."
        
        start_time = datetime(date.year, date.month, date.day, start_hour, 0)
        end_time = datetime(date.year, date.month, date.day, end_hour, 0)
        
        self.schedule.setdefault(user, {}).setdefault(date.strftime("%Y-%m-%d"), [])
        
        for s, e in self.schedule[user][date.strftime("%Y-%m-%d")]:
            if s < end_time and e > start_time:
                return "Meeting time overlaps with an existing meeting."
        
        self.schedule[user][date.strftime("%Y-%m-%d")].append((start_time, end_time))
        return "Meeting scheduled successfully."

    def view_meetings(self, user, date):
        meetings = self.schedule.get(user, {}).get(date.strftime("%Y-%m-%d"), [])
        if not meetings:
            return "No meetings scheduled."
        formatted_meetings = "\n".join([f"{s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}" for s, e in meetings])
        return f"Scheduled Meetings:\n{formatted_meetings}"

# Example Usage
scheduler = SmartMeetingScheduler()
date = datetime(2025, 3, 18)

print(scheduler.schedule_meeting("Alice", date, 10, 11))
print(scheduler.get_available_slots("Alice", date))
print(scheduler.view_meetings("Alice", date))
