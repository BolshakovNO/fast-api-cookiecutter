from fastapi.responses import StreamingResponse


class OctetStream(StreamingResponse):
    media_type = 'application/octet-stream'
