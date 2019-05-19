import json
import random

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from faker import Faker

from kanban.board.constants import TicketStatus
from kanban.board.models import Ticket


class TicketTests(TestCase):
    def setup(self):
        self.client = APIClient()

    def test_post(self):
        fake = Faker()
        url = reverse("ticket-list")
        payload = {
            "assignee": None,
            "name": fake.word(),
            "description": fake.text(),
            "status": random.choice([x.value for x in TicketStatus]),
            "start": str(fake.date_object()),
            "end": None,
        }

        response = self.client.post(url, json.dumps(payload), content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().name, payload["name"])
