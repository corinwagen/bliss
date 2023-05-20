import numpy as np

class SpeechBallot:
    def __init__(self, room_id, judge_id, student_ids, rankings):
        self.room_id = room_id
        self.judge_id = judge_id

        self.student_ids = np.array(student_ids)

        # make sure we got the right numbers
        assert len(student_ids) == len(rankings)
        assert set(rankings) == set(range(1, len(rankings) + 1))

        self.rankings = np.array(rankings)

class DebateBallot:
    def __init__(self, room_id, judge_id, team_ids, student_ids, rankings, speaker_points):
        self.room_id = room_id
        self.judge_id = judge_id

        self.team_ids = team_ids
        self.student_ids = np.array(student_ids)

        assert len(rankings) == 2
        self.rankings = rankings

        # make sure we got the right numbers
        assert len(student_ids) == len(speaker_points)
        self.speaker_points = np.array(speaker_points)
