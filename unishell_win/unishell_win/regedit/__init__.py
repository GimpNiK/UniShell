from .core.UserType import CurrentUser, User, Users
from .core.PATH import PATH as stdPATH
from .core.AutoRun import AutoRun as stdAutoRun
from .core.AutoRunOnce import AutoRunOnce as stdAutoRunOnce

CurUser = CurrentUser()
PATH = stdPATH(CurUser)
AutoRun = stdAutoRun(CurUser)
AutoRunOnce = stdAutoRunOnce(CurUser)