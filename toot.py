from mastodon import Mastodon

mastodon = Mastodon(
    access_token="token.secret",
    api_base_url="https://botsin.space",
)

media = mastodon.media_post("../plot.png")
mastodon.status_post(
    """Ausbau erneuerbarer Energien von 2022-03-02 bis 2022-03-09:
- Solar: 61.17 GW (+0.41 GW) registriert, laut Plan sollten es 61.37 GW sein.
- Wind an Land: 56.14 GW (+0.02 GW) registriert, laut Plan sollten es 56.48 GW sein.
- Wind auf See: 7.79 GW (+0.00 GW) registriert, laut Plan sollten es 7.88 GW sein.""",
    media_ids=[media],
)
