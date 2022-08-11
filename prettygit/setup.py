from pathlib import Path
import shutil as sh
import platform
import sys
import os

proj_path = Path(__file__).parent.resolve()
icon_ico_source = f'{proj_path}/icon.ico'


def main():
    if platform.system() == 'Linux':
        linux()
    elif platform.system() == 'Windows':
        windows()


def linux():
    home = Path.home()
    share = f'{home}/.local/share'

    dotdesktop_path = Path(f'{home}/.local/share/applications/PrettyGit.desktop')
    if not dotdesktop_path.exists():
        dotdesktop_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        with open(
            dotdesktop_path,
            'w',
        ) as dotdesktop:
            dotdesktop.write(
'''\
[Desktop Entry]
Comment=very simple and user friendly interface for git
Type=Application
Icon=PrettyGit
Name=PrettyGit
Terminal=true
TerminalOptions=\\s--noclose
Hidden=false
Keywords=pretty;git
Exec=/bin/python -m prettygit
'''
            )

    icon_path = Path(f'{share}/icons/PrettyGit.svg')
    if not icon_path.exists():
        icon_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        sh.copy(
            f'{proj_path}/icon.svg',
            f'{share}/icons/PrettyGit.svg',
        )


def windows():
    shortcut = Path(
        f'{proj_path.parent.resolve()}/{proj_path.name}.lnk'
    )

    if shortcut.exists():
        return

    icon = Path(
        f'{Path(__file__).parent.resolve()}/icon.ico'
    )

    home = os.environ["USERPROFILE"]

    desktop = Path(
        f'{home}/desktop/{shortcut.name}'
    )

    start_menu = Path(
        f"{home}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/gmanka/{shortcut.name}"
    )

    start_menu.parent.mkdir(
        parents = True,
        exist_ok = True,
    )

    shortcut_creator_path = f'{proj_path}/shortcut_creator.vbs'
    with open(
        shortcut_creator_path,
        'w'
    ) as shortcut_creator:
        shortcut_creator.write(
f'''\
set WshShell = WScript.CreateObject("WScript.Shell")
set Shortcut = WshShell.CreateShortcut("{shortcut}")
Shortcut.TargetPath = "{sys.executable}"
Shortcut.Arguments = "{proj_path}"
Shortcut.IconLocation = "{icon}"
Shortcut.Save
'''
        )
    shortcut_creator.close()
    os.system(shortcut_creator_path)
    os.remove(shortcut_creator_path)
    sh.copyfile(shortcut, desktop)
    sh.copyfile(shortcut, start_menu)
    # try:
    #     sh.copyfile(shortcut, desktop)
    # except PermissionError:
    #     pass
    # try:
    # except PermissionError:
    #     pass


main()

# sys.exit()
