from pathlib import Path
import venv


def KF_kornyezet_letrehoz():
    cel = Path(__file__).parent / ".venv"
    venv.create(cel, with_pip=False)
    print(f"A virtuális környezet elkészült: {cel}")
    print("Mac/Linux: .venv/bin/python main.py")
    print(r"Windows: .venv\Scripts\python.exe main.py")


if __name__ == "__main__":
    KF_kornyezet_letrehoz()
