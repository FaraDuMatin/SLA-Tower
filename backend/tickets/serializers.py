from django.conf import settings
from rest_framework import serializers

from .models import Ticket
from .sla import bucket


class TicketSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source="country.code")
    timezone = serializers.CharField(source="country.timezone")
    bucket = serializers.SerializerMethodField()
    jira_url = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "jira_key",
            "jira_url",
            "title",
            "priority",
            "status",
            "country",
            "timezone",
            "created_at",
            "due_at",
            "paused_minutes",
            "bucket",
        ]

    def get_bucket(self, ticket):
        return bucket(ticket)

    def get_jira_url(self, ticket):
        if ticket.jira_key is None:
            return None
        return settings.JIRA_BASE_URL + "/browse/" + ticket.jira_key
