# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest

import django
django.setup()

from django.core.urlresolvers import reverse

from deck_builder.views import DeckBuilderView

from rest_framework.test import APITestCase

@pytest.mark.django_db()
class HearthstoneCardBuilderAPITest(APITestCase):

    fixtures = ['test_fixture.json',]

    def setUp(self):
        super().setUp()

    def test_get_400_no_player_class(self):
        self.url = reverse('get_cards')
        resp = self.client.get(self.url)
        assert resp.status_code == 400

    def test_get_400_invalid_player_class(self):
        self.url = reverse('get_cards') + '?player_class=BADCLASS'
        resp = self.client.get(self.url)
        assert resp.status_code == 400

    def test_get_200_verify_rules_kept(self):
        self.url = reverse('get_cards') + '?player_class=Priest'
        resp = self.client.get(self.url)
        assert resp.status_code == 200

        data = resp.json()

        card_id_count = {}

        assert len(data) == DeckBuilderView.DECK_SIZE

        for item in data:
            assert item['playerClass'] == 'Priest' or item['playerClass'] == 'Neutral'
            try:
                card_id_count[item['id']] += 1
            except KeyError:
                card_id_count[item['id']] = 1

        for id_count in card_id_count.values():
            assert id_count <= DeckBuilderView.CARD_MAX_PER_TYPE



