from app.models import Presentation


class PresentationDAO:
    def __init__(self) -> None:
        self._presentations = [
            Presentation(id=1, name="Tapa"),
            Presentation(id=2, name="Media ración"),
            Presentation(id=3, name="Ración"),
        ]

    def get_all(self) -> list[Presentation]:
        return self._presentations.copy()
