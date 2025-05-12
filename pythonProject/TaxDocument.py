from datetime import datetime, date

class TaxDocument:
    def __init__(self, form_name, due_date, pdf_link, irs_key, status, why, how_to, description):
        self.form_name = form_name
        self.due_date = due_date  # This will be a string
        self.pdf_link = pdf_link
        self.key = irs_key
        self.status = status
        self.why = why
        self.how_to = how_to
        self.description = description

    

    
    def check_due_date_status(self):
        """Calculate the remaining days until the next due date."""
        today = date.today()

        # Handle "As Needed" case
        if self.due_date.lower() == "as needed":
            return "No specific due date (As Needed)."

        # Split the due_date string into individual dates
        try:
            due_dates = [datetime.strptime(d.strip(), "%Y-%m-%d").date() for d in self.due_date.split(",")]
        except ValueError:
            return f"Invalid due date format: {self.due_date}"

        # Find the next due date
        upcoming_due_dates = [d for d in due_dates if d >= today]
        if not upcoming_due_dates:
            return "All due dates have passed."

        next_due_date = min(upcoming_due_dates)
        delta = (next_due_date - today).days

        if delta == 0:
            return "Due today!"
        elif delta == 1:
            return "Due tomorrow!"
        else:
            return f"{delta} days remaining until due date on {next_due_date.strftime('%B %d, %Y')}."
