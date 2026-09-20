from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from calendar_rules.models import Country
from tickets.models import PAUSED_STATUS, ClockEvent, Ticket

IN_PROGRESS = "In Progress"
TO_DO = "To Do"

# title, priority, country, created days ago, due in days (negative is past), status
DEMO_TICKETS = [
    ("Warehouse scan guns offline in Mississauga", "P1", "CA", 3, -2, IN_PROGRESS),
    ("Customs document template outdated", "P2", "DE", 10, -7, TO_DO),
    ("Order allocation stuck for Pune plant", "P1", "IN", 35, -33, IN_PROGRESS),
    ("Monthly capacity report wrong units", "P3", "IN", 6, -1, TO_DO),
    ("Dock scheduling page times out", "P2", "CA", 5, 0.5, IN_PROGRESS),
    ("Duplicate shipments after ERP sync", "P1", "DE", 9, 1, IN_PROGRESS),
    ("Route optimizer ignores toll roads", "P2", "IN", 20, 2, TO_DO),
    ("Slotting export missing pallet height", "P3", "CA", 30, 3, IN_PROGRESS),
    ("Carrier rate import rejects CSV", "P2", "CA", 1, 3, TO_DO),
    ("Barcode labels print blurry", "P3", "IN", 2, 7, TO_DO),
    ("Forecast dashboard slow on Monday morning", "P3", "DE", 1, 14, IN_PROGRESS),
    ("Add French labels to picking screen", "P4", "CA", 2, 21, TO_DO),
    ("Timezone wrong on shift planning screen", "P2", "IN", 1, 28, TO_DO),
    ("Add KPI for truck fill rate", "P3", "DE", 3, 30, TO_DO),
    ("Onboard vendor to supplier portal", "P4", "IN", 1, 35, TO_DO),
    ("Rename cost center in transport model", "P4", "DE", 2, 365, TO_DO),
    ("Inventory count report shows negative stock", "P3", "CA", 4, 6, PAUSED_STATUS),
    ("WMS interface down at Hamburg site", "P1", "DE", 2, 1, PAUSED_STATUS),
    ("Request read access for new analyst", "P4", "CA", 8, 4, PAUSED_STATUS),
    ("Login page shows wrong logo", "P4", "DE", 12, 9, PAUSED_STATUS),
]


class Command(BaseCommand):
    help = "Create local demo tickets with hand picked due dates. Replaces its own tickets. --clear also deletes the Jira ones."

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true")

    def handle(self, *args, **options):
        if options["clear"]:
            Ticket.objects.all().delete()
        else:
            Ticket.objects.filter(jira_key=None).delete()
        now = timezone.now()
        for title, priority, code, created_days_ago, due_in_days, status in DEMO_TICKETS:
            ticket = Ticket.objects.create(
                title=title,
                priority=priority,
                status=status,
                country=Country.objects.get(code=code),
                created_at=now - timedelta(days=created_days_ago),
                due_at=now + timedelta(days=due_in_days),
            )
            if status == PAUSED_STATUS:
                ClockEvent.objects.create(ticket=ticket, status_from=IN_PROGRESS, status_to=status, at=now - timedelta(days=1))
            self.stdout.write(f"{ticket.id} {priority} {code} due in {due_in_days} days {title}")
        self.stdout.write(f"{len(DEMO_TICKETS)} demo tickets created")
