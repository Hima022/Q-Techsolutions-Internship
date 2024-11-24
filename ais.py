import datetime
from collections import defaultdict

class Scheduler:
    def __init__(self):
        self.availability = defaultdict(list)  # {person: [(start_time, end_time)]}
        self.schedule = []  # [(interviewer, candidate, start_time, end_time)]

    def add_availability(self, person, start_time, end_time):
        """Add availability for a person."""
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M")
        if start_time >= end_time:
            raise ValueError("Start time must be before end time.")
        self.availability[person].append((start_time, end_time))

    def schedule_interview(self, interviewer, candidate, start_time, end_time):
        """Schedule an interview if both parties are available."""
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M")

        if self._is_available(interviewer, start_time, end_time) and self._is_available(candidate, start_time, end_time):
            self.schedule.append((interviewer, candidate, start_time, end_time))
            print(f"Interview scheduled: {interviewer} with {candidate} from {start_time} to {end_time}")
        else:
            print(f"Cannot schedule: Conflict detected for {interviewer} or {candidate}.")

    def _is_available(self, person, start_time, end_time):
        """Check if a person is available during the given time."""
        for available_start, available_end in self.availability[person]:
            if available_start <= start_time and available_end >= end_time:
                return True
        return False

    def view_schedule(self):
        """Print the scheduled interviews."""
        print("\nScheduled Interviews:")
        for interview in self.schedule:
            interviewer, candidate, start_time, end_time = interview
            print(f"- {interviewer} with {candidate} from {start_time} to {end_time}")

    def export_schedule(self, file_name="schedule.txt"):
        """Export the schedule to a text file."""
        with open(file_name, "w") as file:
            for interview in self.schedule:
                interviewer, candidate, start_time, end_time = interview
                file.write(f"{interviewer} with {candidate} from {start_time} to {end_time}\n")
        print(f"Schedule exported to {file_name}")

# Example Usage
if __name__ == "__main__":
    scheduler = Scheduler()

    # Add availability
    scheduler.add_availability("Interviewer1", "2024-11-24 09:00", "2024-11-24 12:00")
    scheduler.add_availability("Candidate1", "2024-11-24 10:00", "2024-11-24 11:00")

    # Schedule interviews
    scheduler.schedule_interview("Interviewer1", "Candidate1", "2024-11-24 10:00", "2024-11-24 10:30")

    # View and export schedule
    scheduler.view_schedule()
    scheduler.export_schedule("interview_schedule.txt")
