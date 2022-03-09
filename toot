#!/usr/bin/env python3
#
# Usage:
#     ./toot.py <toot text file> <attachment file>

from mastodon import Mastodon
import sys

mastodon = Mastodon(
    access_token="token.secret",
    api_base_url="https://botsin.space",
)
text = open(sys.argv[1]).read()
media = mastodon.media_post(sys.argv[2], focus=(-1, -1))
mastodon.status_post(text, media_ids=[media])
