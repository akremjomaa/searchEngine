from Document import RedditDocument, ArxivDocument


class DocumentFactory:
    @staticmethod
    def create_document(doc_type, *args, **kwargs):
        if doc_type == "Reddit":
            return RedditDocument(*args, **kwargs)
        elif doc_type == "Arxiv":
            return ArxivDocument(*args, **kwargs)
        else:
            raise ValueError("Type de document non pris en charge")
