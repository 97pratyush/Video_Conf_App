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
WS_URL = "ws://6.tcp.ngrok.io:13939"

# API URL
URL = "https://0254-2601-642-4c05-56b2-ebe4-97a9-2807-917d.ngrok-free.app"

# Socket Constants - Meeting Participants
PARTICIPANTS_TOPIC = 'subscribeToParticipantList'
PARTICIPANTS_MESSAGE = 'participantListUpdated'

# Socket Constants - Chat Messages
CHAT_TOPIC = 'getChatMessages'
CHAT_HISTORY_TOPIC = 'chatMessageHistory'
CHAT_SEND_MESSAGE = 'sendChatMessage'
CHAT_NEW_MESSAGE = 'newChatMessage'