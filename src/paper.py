class Paper:
    def __init__(self, title, summary, score, paper_id, link):
        self.title = title
        self.summary = summary
        self.score = score
        self.paper_id = paper_id
        self.link = link

    def __str__(self):
        return f"{self.paper_id}, {self.title}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.paper_id == other.paper_id

    def __hash__(self):
        return hash(self.paper_id)

    def to_dict(self):
        return {"title": self.title,
                "summary": self.summary,
                "score": self.score,
                "paper_id": self.paper_id,
                "link": self.link}

    def to_list_elem(self):
        return {"paper_id": self.paper_id,
                "score": self.score}

