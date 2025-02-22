from .. import db
from .frame import frame
from multiprocessing import Process
from ..detecUtil.function_counter import detector

class video(db.Model):
    __tablename__ = 'Video'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    area_id = db.Column(db.Integer, db.ForeignKey('Area.id'))
    source = db.Column(db.String)

    def __init__(self, area_id, source):
        self.area_id = area_id
        self.source = source
        print("Start Process to detect")
        Process(target=self.start_detect, args={self}).start()

    def start_detect(self, video):
        for detect_result in detector(video):
            new_frame = frame(video.area_id, detect_result)
            db.session.add(new_frame)
            db.session.commit()
        print("End of detect for area:" + str(video.area_id))
