from pydantic import BaseModel, ValidationError, validator


class SlackResponseMetaData(BaseModel):
    next_cursor: str


class SlackFile(BaseModel):
    permalink: str | None


class SlackMessage(BaseModel):
    text: str
    ts: str
    reply_count: int | None
    files: list[SlackFile] | None


class SlackResponse(BaseModel):
    ok: bool

    @validator("ok")
    def ok_must_true(cls, ok):
        if not ok:
            raise ValidationError("Request to Slack failed in some reason")
        return ok


class ConversationsHistory(SlackResponse):
    """slack.com/api/conversations.history"""

    ok: bool
    messages: list[SlackMessage]
    response_metadata: SlackResponseMetaData | None


class ConversationsReplies(SlackResponse):
    """slack.com/api/conversations.replies"""

    ok: bool
    messages: list[SlackMessage]
