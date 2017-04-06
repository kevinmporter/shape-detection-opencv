"""
Database document configuration for MongoDB.
"""
import mongoengine as me
import settings


me.connect(settings.MONGODB_DATABASE["name"],
           host=settings.MONGODB_DATABASE["host"],
           username=settings.MONGODB_DATABASE["username"],
           password=settings.MONGODB_DATABASE["password"]
           )


class Result(me.EmbeddedDocument):
    """
    An individual result inside a VideoRun. This "record" indicates a subject found
    in the attached frame. The x, y, w, and h values represent the coordinates of the
    rectangle that can be drawn around the attached image.
    """
    x = me.IntField()
    y = me.IntField()
    w = me.IntField()
    h = me.IntField()
    picture = me.FileField()


class VideoRun(me.Document):
    """
    An entire video run through the system. This would represent a stream or a
    larger recording event when used in realtime.
    """
    start = me.DateTimeField()
    end = me.DateTimeField()
    video = me.FileField()
    results = me.EmbeddedDocumentListField(Result)
