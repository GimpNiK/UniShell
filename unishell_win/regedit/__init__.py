from .UserType import CurrentUser, User, Users
from PATH import PATH as stdPATH
from AutoRun import AutoRun as stdAutoRun
from AutoRunOnce import AutoRunOnce as stdAutoRunOnce

CurUser = CurrentUser()
PATH = stdPATH(CurUser)
AutoRun = stdAutoRun(CurUser)
AutoRunOnce = stdAutoRunOnce(CurUser)