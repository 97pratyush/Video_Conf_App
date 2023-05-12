# Define the dimensions of the video frames
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

# Define the IP address and port number of the server
SERVER_IP = '10.0.0.248'
SERVER_PORT = 4000

# Video Codec
VIDEO_CODEC = 'flv'

RTMP_URL = 'rtmp://10.0.0.248/live'

# Time in seconds
MAX_WAIT_TIME_FOR_SERVER = 10
MAX_WAIT_TIME_TO_SEND = 5

MAX_TRIES = 30

# Define the address and port to use for the socket connection
WS_URL = "ws://2.tcp.ngrok.io:14936"

# API URL
URL = "https://6f0c-2601-646-9d01-1da0-4a80-d63-becb-76c2.ngrok-free.app"

PARTICIPANTS_TOPIC = 'subscribeToParticipantList'
PARTICIPANTS_MESSAGE = 'participantListUpdated'

CHAT_TOPIC = 'getChatMessages'