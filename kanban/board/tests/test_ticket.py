import json
import random

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from faker import Faker

from .factories import TicketFactory
from ..constants import TicketStatus
from ..models import Ticket


class TicketTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fake = Faker()

    def test_post(self):
        url = reverse("ticket-list")
        payload = {
            "assignee": None,
            "name": self.fake.word(),
            "description": self.fake.text(),
            "status": random.choice([x.value for x in TicketStatus]),
            "start": str(self.fake.date_object()),
            "end": None,
        }

        response = self.client.post(url, json.dumps(payload), content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().name, payload["name"])

    def test_validate_opposite_dates(self):
        url = reverse("ticket-list")
        payload = {
            "assignee": None,
            "name": self.fake.word(),
            "description": self.fake.text(),
            "status": random.choice([x.value for x in TicketStatus]),
            "start": str(self.fake.future_date()),
            "end": str(self.fake.past_date()),
        }

        response = self.client.post(url, json.dumps(payload), content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Ticket.objects.count(), 0)
        self.assertEqual(response.data, {"non_field_errors": ["'end' value must set after 'start' day"]})

    def test_validate_same_dates(self):
        url = reverse("ticket-list")
        date = str(self.fake.date_object())
        payload = {
            "assignee": None,
            "name": self.fake.word(),
            "description": self.fake.text(),
            "status": random.choice([x.value for x in TicketStatus]),
            "start": date,
            "end": date,
        }

        response = self.client.post(url, json.dumps(payload), content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().name, payload["name"])

    def test_get(self):
        ticket = TicketFactory()
        url = reverse("ticket-detail", kwargs={"pk": ticket.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": ticket.id,
                "assignee": ticket.assignee.username,
                "status_display": ticket.get_status_display(),
                "name": ticket.name,
                "description": ticket.description,
                "status": ticket.status,
                "start": ticket.start,
                "end": ticket.end,
            },
        )
