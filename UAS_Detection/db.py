import mongoengine as me


me.connect('uas_detection_collection',
           host='localhost'
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