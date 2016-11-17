# coding: utf-8
from __future__ import unicode_literals

import pytest
from mixer.backend.django import mixer

from .templatetags.badges_tags import most_awarded_badges
from .models import BadgeAward


@pytest.mark.django_db
def test_most_awarded_badges():

    user = mixer.blend('accounts.User')  # each user has it's own client
    other_user = mixer.blend('accounts.User')
    mixer.cycle(10).blend(BadgeAward, slug='oi', level=0, user=user)
    mixer.cycle(7).blend(BadgeAward, slug='mobile', level=0, user=user)

    # will be rejected since it belongs to another client
    mixer.cycle(6).blend(BadgeAward, slug='downloader', level=0, user=other_user)

    mixer.cycle(6).blend(BadgeAward, slug='diario-atualizado', level=0, user=user)
    mixer.cycle(5).blend(BadgeAward, slug='journal-shared', level=0, user=user)
    mixer.cycle(5).blend(BadgeAward, slug='journal-shared', level=1, user=user)
    mixer.cycle(4).blend(BadgeAward, slug='journal-shared', level=2, user=user)
    mixer.cycle(3).blend(BadgeAward, slug='diario-atualizado', level=1, user=user)
    mixer.cycle(3).blend(BadgeAward, slug='diario-atualizado', level=2, user=user)

    expected = [
        {'count': 10, 'name': 'Oi!'},
        {'count': 7, 'name': 'Mobile'},
        {'count': 6, 'name': 'Meu querido diário'},
        {'count': 5, 'name': 'Social'},
        {'count': 5, 'name': 'Divulgador'},
    ]

    mab = most_awarded_badges(client_id=user.client_id)
    found = [dict(name=unicode(badge.name), count=badge.count) for badge in mab]

    assert expected == found
