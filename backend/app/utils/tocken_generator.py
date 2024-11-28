""" Dynamically generate access tockens for connecting LiveKit server
by granting permission to user, and then return tockens as a JWT
(JSON Web Tocken) for secure authentication and authorization"""

from livekit import AccessToken, VideoGrant
from app.config import settings

"""identity: A unique identifier for a specific user who will use the token. 
It could be a username, user ID, or session ID. (useful for multiple)"""
def create_access_tocken(identity: str):
	# create a grant with required premission
	grant = VideoGrant(room_join=True)

	# create an access tocken
	tocken = AccessToken(
		api_key = settings.LIVEKIT_API_KEY,
		api_secret_key = settings.LIVEKIT_SECRET_KEY,
		identity = identity
		)
	# add prev defined permission
	tocken.add_grant(grant)

	""" optionally set tocken expiery with TTL (time to live) 
	with how long the tocken is valid in seconds"""
	tocken.ttl = 3600

	# to return the tocken convert yo JWT
	return tocken.to_jwt()