"""BGM(mp3)を、そのままでは音声ファイルとして取り出せない形(bgm.dat)に変換する。

OpenTracks(旧DOVA-SYNDROME)の規約では、利用者が音源ファイルを
そのまま取り出せる状態で組み込むことが禁止されているため、
公開するのは変換後の assets/data/bgm.dat だけにする。
元の mp3(assets/bgm/bgm.mp3)は .gitignore で公開対象から外している。

使い方:  python tools/pack_bgm.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'assets' / 'bgm' / 'bgm.mp3'
DST = ROOT / 'assets' / 'data' / 'bgm.dat'
MAGIC = b'WRSI'
KEY = 'waraishi-aji-stone-run'.encode('utf-8')  # index.html の BGM_KEY と同じにすること


def main():
    raw = SRC.read_bytes()
    out = bytearray(len(raw))
    for i, b in enumerate(raw):
        out[i] = b ^ KEY[i % len(KEY)] ^ (i * 31 & 0xFF)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_bytes(MAGIC + bytes(out))
    print(f'{SRC.name} ({len(raw):,} bytes) -> {DST.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
