import mongoengine as me
import settings


me.connect(settings.MONGODB_DATABASE["name"],
           host=settings.MONGODB_DATABASE["host"],
           username=settings.MONGODB_DATABASE["username"],
           password=settings.MONGODB_DATABASE["password"]
           )


class Result(me.EmbeddedDocument):
    x = me.IntField()
    y = me.IntField()
    w = me.IntField()
    h = me.IntField()
    picture = me.FileField()


class VideoRun(me.Document):
    start = me.DateTimeField()
    end = me.DateTimeField()
    video = me.FileField()
    results = me.EmbeddedDocumentListField(Result)
