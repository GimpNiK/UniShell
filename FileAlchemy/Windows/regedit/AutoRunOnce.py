from __future__ import annotations

from .AutoRun import AutoRun
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .UserType import CurrentUser, User, Users


class AutoRunOnce(AutoRun):
	def __init__(self, user: "CurrentUser|User|Users|str|None" = None) -> None:
		super().__init__(user)
		self.key_path = self.key_path.replace("\\Run", "\\RunOnce")
	
	def __repr__(self) -> str:
		return f"<AutoRunOnce: {self.all()}>"
		