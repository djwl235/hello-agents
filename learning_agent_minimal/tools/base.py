class BaseTool:
    name:str
    description:str
    def run(self,tool_input:str):
        raise NotImplementedError