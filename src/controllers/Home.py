from src.utils.controller.BaseController import BaseController
from src.utils.controller.RoutesUtils import get


class Home(BaseController):
    def __init__(self):
        super().__init__()

    @get("/")
    def root(self):
        return {"message": "Hello World"}