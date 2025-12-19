import sys
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from FileAlchemy.Windows.regedit import  CurrentUser
CurUser = CurrentUser()
AutoRunOnce = CurUser.AutoRunOnce
AutoRunOnce.pop("sddh")
print(CurUser.AutoRunOnce)