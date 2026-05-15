from typing import TypedDict

class JobState(TypedDict):
    input: str
    raw_text: str
    summary: str
    stored_id: int
