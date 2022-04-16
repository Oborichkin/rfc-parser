class Chapter:
    def __init__(self, title, paragraphs):
        self.title = title
        self.paragraphs = paragraphs

    def __len__(self):
        return len(self.paragraphs)
