class BaseLLM:
    def invoke(self,messages)->str:
        raise NotImplementedError