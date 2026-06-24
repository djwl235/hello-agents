class BaseEmbedding:
    def embed(self, text: str) -> list[float]:
        raise NotImplementedError