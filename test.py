project_root = r"C:\Users\ПК\Desktop\UniShell\unishell"
import sys
sys.path.insert(0, project_root)
project_root = r"C:\Users\ПК\Desktop\UniShell\unishell_win"
sys.path.insert(0, project_root)

from unishell.regedit import Environment

print(Environment.json())
