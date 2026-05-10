from pathlib import Path

base = Path("fixedCode")

prefix_map = {
    "Atomicity Violation": "A",
    "Dead Lock": "D",
    "Live Lock": "L",
    "Locking Problem": "LP",
    "Order Violation": "O",
    "Race Condition": "R",
    "Starvation": "S",
}

def find_prefix(folder: Path):
    """
    현재 폴더의 상위 경로들 중 prefix_map에 있는 폴더명을 찾음
    """
    for parent in [folder, *folder.parents]:
        if parent.name in prefix_map:
            return prefix_map[parent.name]
    return None

for folder in base.rglob("*"):
    if not folder.is_dir():
        continue

    # 제일 하위 디렉토리만 처리
    if any(child.is_dir() for child in folder.iterdir()):
        continue

    prefix = find_prefix(folder)

    # 지정된 상위 폴더가 아니면 스킵
    if prefix is None:
        continue

    for file in folder.iterdir():
        if not file.is_file():
            continue

        name = file.stem
        ext = file.suffix

        # 파일명이 정확히 두 자리 숫자인 경우만 처리
        if len(name) == 2 and name.isdigit():
            a, b = name[0], name[1]

            if a == "0":
                new_name = f"{prefix}1{a}S{b}{ext}"
            else:
                new_name = f"{prefix}{a}S{b}{ext}"

            new_path = file.with_name(new_name)

            print(file, "->", new_path)
            file.rename(new_path)