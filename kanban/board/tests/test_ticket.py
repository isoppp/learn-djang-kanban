import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from kanban.board.models import Ticket


class TicketTests(TestCase):
    def setup(self):
        self.client = APIClient()

    def test_post(self):
        url = reverse("ticket-list")
        payload = {
            "assignee": None,
            "name": "test ticket",
            "description": "This is a test ticket.",
            "status": 1,
            "start": "2018-06-01",
            "end": None,
        }

        response = self.client.post(url, json.dumps(payload), content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().name, "test ticket")
