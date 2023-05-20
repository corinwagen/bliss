import numpy as np

class Ballot:
    def __init__(self, room_id, judge_id, student_ids, rankings, speaker_points=None):
        self.room_id = room_id
        self.judge_id = judge_id

        self.student_ids = np.array(student_ids)

        # make sure we got the right numbers
        assert len(student_ids) == len(rankings)
        assert set(rankings) == set(range(1, len(rankings) + 1))

        if speaker_points is not None:
            assert len(speaker_points) == len(rankings)

        self.rankings = np.array(rankings)
        self.speaker_points = np.array(speaker_points)

