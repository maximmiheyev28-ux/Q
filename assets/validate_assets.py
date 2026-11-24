from pathlib import Path
import struct
import sys

EXPECTED = {
    "city_stage.png": (1200, 240),
    "player_idle.png": (960, 96),
    "player_run.png": (1536, 96),
    "player_attack_1.png": (672, 96),
    "player_attack_2.png": (672, 96),
    "player_attack_3.png": (576, 96),
    "player_air_attack.png": (960, 96),
    "player_jump_start.png": (288, 96),
    "player_jump_fall.png": (96, 96),
    "player_dash.png": (672, 96),
    "player_hurt.png": (288, 96),
    "player_death.png": (480, 96),
    "player_throw.png": (672, 96),
    "player_shuriken.png": (8, 8),
    "boss_idle.png": (768, 108),
    "boss_run.png": (1024, 108),
    "boss_attack_1.png": (896, 108),
    "boss_attack_2.png": (768, 108),
    "boss_hurt.png": (512, 108),
    "boss_death.png": (3328, 108),
    "enemy_punk_idle.png": (384, 63),
    "enemy_punk_walk.png": (384, 63),
    "enemy_punk_punch.png": (288, 63),
    "enemy_punk_hurt.png": (256, 63),
    "enemy_brawler_idle.png": (384, 63),
    "enemy_brawler_walk.png": (960, 63),
    "enemy_brawler_kick.png": (480, 63),
    "enemy_brawler_hurt.png": (192, 63),
}

PNG_MAGIC = b"\\x89PNG\\r\\n\\x1a\\n"
errors = []
for name, expected in EXPECTED.items():
    path = Path("assets") / name
    if not path.is_file():
        errors.append(f"Missing PNG: {path}")
        continue
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != PNG_MAGIC:
        errors.append(f"Invalid PNG header: {path}")
        continue
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != expected:
        errors.append(f"{path}: expected {expected}, got {(width, height)}")
    else:
        print(f"OK {path}: {width}x{height}")

for name in ("player_asset_license.txt", "boss_asset_license.txt", "ART_CREDITS.md"):
    if not (Path("assets") / name).is_file():
        errors.append(f"Missing asset documentation: assets/{name}")

if Path("assets/generate_assets.py").exists():
    errors.append("Procedural art generator must not be present in the project.")

if errors:
    print("\\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"Validated {len(EXPECTED)} committed game PNG files. No image generation is performed.")
