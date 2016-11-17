# coding: utf-8
from __future__ import unicode_literals

import pytest
from mixer.backend.django import mixer

from ..videos.models import Video
from .models import BadgeAward


@pytest.fixture
def user():
    return mixer.blend('accounts.User')


@pytest.mark.parametrize('quantity,slug,level', [
    (10, 'assistiu-videos', 0),
    (25, 'assistiu-videos', 1),
])
@pytest.mark.django_db
def test_video_listener(user, quantity, slug, level):
    videos = mixer.cycle(quantity+1).blend(Video, title="Video {0}")
    assert user.badges_earned.count() == 0

    for idx, video in enumerate(videos):
        if idx >= quantity:
            break
        video.track_access(user)

    assert BadgeAward.objects.filter(user=user, slug=slug, level=level).exists()
