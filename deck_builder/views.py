# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import math
import random

from django.views import View

from django.http.response import HttpResponse, HttpResponseBadRequest

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HearthstoneCard
from .serializers import HearthstoneCardSerializer


# Create your views here.

class HttpResponse429(HttpResponse):
    status_code = 429


class ReloadDeckView(View):

    def post(self, request, *args, **kwargs):
        headers = {'X-Mashape-Key': 'ZTMJtzbYvXmshPTFEZI4ztIy3I68p1nPwgHjsnIGukKZeJxGcs'}

        resp = requests.get('https://omgvamp-hearthstone-v1.p.mashape.com/cards/sets/Rastakhan%27s%20Rumble',
                            headers=headers)

        if resp.status_code == 429:
            return HttpResponse429('Dude, you got throttled. Check who else is using the API key.')

        data = resp.json()
        cards_not_in_db = HearthstoneCard.objects.exclude(cardId__in=[card['cardId'] for card in data])
        cards_not_in_db.delete()

        for card in data:
            if HearthstoneCard.objects.filter(cardId=card['cardId']).exists():
                instance = HearthstoneCard.objects.get(cardId=card['cardId'])
                srz = HearthstoneCardSerializer(instance, data=card, partial=True)
                srz.save()
            else:
                srz = HearthstoneCardSerializer(data=card)
                if srz.is_valid():
                    srz.save()

        return HttpResponse('Card DB updated.', status=201)


'''
DECK BUILDER RULES:
    1. The deck must have 30 cards.
    2. The cards given back to the player must be either of the player_class or 'Neutral' type.
    3. There can only be a max of 2 of a kind in the deck.
'''


class DeckBuilderView(APIView):
    PLAYER_CLASS_LIST = ['Druid', 'Hunter', 'Mage',
                         'Paladin', 'Priest', 'Rogue',
                         'Shaman', 'Warlock', 'Warrior',
                         'Neutral']

    DECK_SIZE = 30
    CARD_MAX_PER_TYPE = 2
    MIN_CARD_IDS_IN_ROSTER = math.ceil(DECK_SIZE / CARD_MAX_PER_TYPE)

    def get_serializer(self, *args, **kwargs):
        return HearthstoneCardSerializer(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        # Simple validation to check for player class. No need for serializers yet I guess.

        if 'player_class' not in request.GET:
            return HttpResponseBadRequest('Please input your player_class as a query param.')
        elif not request.GET['player_class'] in self.PLAYER_CLASS_LIST:
            return HttpResponseBadRequest('Sorry, invalid player class.')

        player_class = request.GET['player_class']

        allowed_cards = HearthstoneCard.objects.filter(playerClass__in=[player_class, 'Neutral'])
        allowed_cards_pks = list(allowed_cards.values_list('pk', flat=True))

        # Rule 3 means we must have enough card types in the deck from the source.
        # If we don't have then it means something's wrong with the data.
        # Probably won't happen since it's Hearthstone, but just in case...
        if allowed_cards.count() < self.MIN_CARD_IDS_IN_ROSTER:
            return HttpResponse("There aren't enough card types to generate a full deck. "
                                "Maybe try a different player_class?")

        player_card_current_count_dict = {}
        player_card_data = []

        for i in range(self.DECK_SIZE):
            choice = random.choice(allowed_cards_pks)
            try:
                # Limit the number per type here.
                if player_card_current_count_dict[choice] < self.CARD_MAX_PER_TYPE:
                    srz = self.get_serializer(instance=HearthstoneCard.objects.get(pk=choice))
                    player_card_data.append(srz.data)
                    player_card_current_count_dict[choice] += 1
                else:
                    allowed_cards_pks.remove(choice)
            except KeyError:
                srz = self.get_serializer(instance=HearthstoneCard.objects.get(pk=choice))
                player_card_data.append(srz.data)
                player_card_current_count_dict[choice] = 1

        return Response(data=player_card_data, status=200)