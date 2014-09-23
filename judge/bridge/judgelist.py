from operator import attrgetter
from random import choice


class JudgeList(list):
    __slots__ = 'queue', 'submission_map'

    def __init__(self, *args, **kwargs):
        super(JudgeList, self).__init__(*args, **kwargs)
        self.queue = []
        self.submission_map = {}

    def on_got_problems(self, judge):
        for elem in self.queue:
            id, problem, language, source = elem
            if problem in judge.problems:
                self.submission_map[id] = judge
                judge.submit(id, problem, language, source)
                break
        else:
            return
        self.queue.remove(elem)

    def on_judge_free(self, judge, submission):
        del self.submission_map[submission]
        if self.queue:
            id, problem, language, source = self.queue.pop(0)
            self.submission_map[id] = judge
            judge.submit(id, problem, language, source)

    def abort(self, submission):
        self.submission_map[submission].abort()

    def judge(self, id, problem, language, source):
        try:
            judge = min([judge for judge in self if problem in judge.problems and not judge.working],
                        key=attrgetter('load'))
        except ValueError:
            self.queue.append((id, problem, language, source))
        else:
            self.submission_map[id] = judge
            judge.submit(id, problem, language, source)
