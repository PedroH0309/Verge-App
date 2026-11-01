#!/usr/bin/env python3
"""Verge Android identity transformation for the Nuvio Mobile GPL-3.0 fork.

Verge retains Nuvio's internal source namespaces, third-party service URLs, and
all legal notices. Only user-facing identity and Android application IDs change.
Source: https://github.com/NuvioMedia/NuvioMobile (GNU GPLv3).
"""
from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
APP_ID = "com.verge.media"
DEBUG_ID = "com.verge.media.debug"
VERSIONS = ("original", "arctic_blue", "emerald", "rose_gold", "copper", "graphite")
COLORS = {
    "original": ((158, 112, 255), (100, 231, 255)),
    "arctic_blue": ((78, 172, 255), (122, 233, 255)),
    "emerald": ((59, 212, 153), (139, 243, 195)),
    "rose_gold": ((246, 141, 178), (255, 200, 160)),
    "copper": ((241, 151, 91), (255, 203, 135)),
    "graphite": ((168, 183, 206), (226, 235, 249)),
    "gold": ((240, 192, 93), (255, 226, 152)),
}
DENSITIES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
PROTECTED_LABELS = (
    "license", "attribution", "copyright", "support_nuvio", "supporters",
    "community_", "patreon", "donation", "server_", "tracking_nuvio_",
    "nuvio_library", "nuvio_progress", "trakt_", "simkl_", "imdb_", "tmdb_",
    "api_", "settings_licenses", "settings_about",
)
UI_STRING = re.compile(r'(<string\b[^>]*\bname="([^"]+)"[^>]*>)(.*?)(</string>)', re.DOTALL)


def replace_literal(path: Path, before: str, after: str) -> None:
    content = path.read_text(encoding="utf-8")
    if before in content:
        path.write_text(content.replace(before, after), encoding="utf-8")
    elif after not in content:
        raise RuntimeError(f"Upstream layout changed: {path} is missing {before!r}")


def patch_android() -> None:
    if not (ROOT / "androidApp/build.gradle.kts").is_file():
        raise RuntimeError("Missing original Nuvio Mobile sources; import must run first.")
    replace_literal(ROOT / "settings.gradle.kts",
                    'rootProject.name = "Nuvio"', 'rootProject.name = "Verge"')
    replace_literal(ROOT / "androidApp/build.gradle.kts",
                    'applicationId = "com.nuvio.app"', f'applicationId = "{APP_ID}"')
    replace_literal(ROOT / "androidApp/build.gradle.kts",
                    'variant.applicationId.set("com.nuviodebug.com")',
                    f'variant.applicationId.set("{DEBUG_ID}")')
    replace_literal(ROOT / "composeApp/src/androidMain/res/values/strings.xml",
                    '<string name="app_name">Nuvio</string>',
                    '<string name="app_name">Verge</string>')

    manifest = ROOT / "androidApp/src/main/AndroidManifest.xml"
    text = manifest.read_text(encoding="utf-8").replace(
        'android:scheme="nuvio"', 'android:scheme="verge"')
    pattern = re.compile(r'\s*<intent-filter\b[^>]*android:autoVerify="true"[^>]*>.*?</intent-filter>', re.S)
    text = pattern.sub(lambda match: "" if 'android:host="nuvio.tv"' in match.group(0)
                       else match.group(0), text)
    if 'android:host="nuvio.tv"' in text:
        raise RuntimeError("The app still claims ownership of the Nuvio domain.")
    manifest.write_text(text, encoding="utf-8")

    for folder in (ROOT / "androidApp/src", ROOT / "composeApp/src"):
        for path in folder.rglob("*.kt"):
            content = path.read_text(encoding="utf-8")
            updated = content.replace("nuvio://", "verge://")
            if updated != content:
                path.write_text(updated, encoding="utf-8")
    gradle = ROOT / "composeApp/build.gradle.kts"
    gradle.write_text(gradle.read_text(encoding="utf-8").replace(
        "nuvio://", "verge://"), encoding="utf-8")

    colors = ROOT / "composeApp/src/androidMain/res/values/colors.xml"
    replace_literal(colors, '<color name="app_icon_background">#000000</color>',
                    '<color name="app_icon_background">#0A0D17</color>')


def patch_strings() -> int:
    locations = [ROOT / "composeApp/src/androidMain/res",
                 ROOT / "composeApp/src/commonMain/composeResources"]
    count = 0
    for location in locations:
        for file in location.glob("values*/strings*.xml"):
            original = file.read_text(encoding="utf-8")
            def update(match):
                nonlocal count
                prefix, key, body, suffix = match.groups()
                if key == "app_name":
                    return prefix + "Verge" + suffix
                if any(part in key.lower() for part in PROTECTED_LABELS):
                    return match.group(0)
                # Keep third-party URLs and credit text untouched.
                if "https://" in body or "http://" in body or "GPL" in body or "copyright" in body.lower():
                    return match.group(0)
                replaced = re.sub(r'\bNuvio\b', 'Verge', body)
                if replaced != body:
                    count += 1
                return prefix + replaced + suffix
            updated = UI_STRING.sub(update, original)
            if updated != original:
                file.write_text(updated, encoding="utf-8")
    return count


def patch_version(version: str, version_code: int) -> None:
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,39}', version):
        raise ValueError("Version names must contain only letters, digits, dots, underscores, or hyphens.")
    if version_code < 1 or version_code > 2100000000:
        raise ValueError("Android versionCode is out of range.")
    path = ROOT / "iosApp/Configuration/Version.xcconfig"
    content = path.read_text(encoding="utf-8")
    for key, value in (("CURRENT_PROJECT_VERSION", str(version_code)),
                       ("MARKETING_VERSION", version)):
        content, hits = re.subn(rf'(?m)^{key}\s*=\s*.+$', f'{key}={value}', content)
        if hits != 1:
            raise RuntimeError(f"Cannot find a unique version definition for {key}.")
    path.write_text(content, encoding="utf-8")


def make_brand_art() -> int:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:
        raise RuntimeError("Pillow is required to build original Verge graphics.") from exc

    def icon(color="original", transparent=False, monochrome=False):
        size = 640
        bg = (0, 0, 0, 0) if transparent or monochrome else (10, 13, 23, 255)
        im = Image.new("RGBA", (size, size), bg)
        d = ImageDraw.Draw(im)
        first, second = COLORS[color]
        if monochrome:
            first = second = (255, 255, 255)
        if not transparent and not monochrome:
            d.rounded_rectangle((25, 25, 615, 615), radius=138, outline=(55, 75, 123))
        d.polygon([(140, 147), (218, 147), (329, 431), (294, 518)], fill=(*first, 255))
        d.polygon([(421, 147), (502, 147), (349, 518), (294, 518), (329, 431)], fill=(*second, 255))
        return im

    def wordmark(color):
        size = (1280, 300)
        im = Image.new("RGBA", size)
        symbol = icon(color, transparent=True).resize((280, 280))
        im.alpha_composite(symbol, (8, 8))
        drawer = ImageDraw.Draw(im)
        candidates = (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
        )
        font = None
        for path in candidates:
            if Path(path).is_file():
                font = ImageFont.truetype(path, 160)
                break
        font = font or ImageFont.load_default()
        drawer.text((315, 38), "VERGE", font=font, fill=(242, 246, 255, 255))
        return im

    replaced = 0
    resource_root = ROOT / "composeApp/src/androidMain/res"
    for density, pixels in DENSITIES.items():
        folder = resource_root / f"mipmap-{density}"
        for variant in VERSIONS:
            suffix = "" if variant == "original" else "_" + variant
            for filename, transparent in (("ic_launcher" + suffix, False),
                                          ("ic_launcher" + suffix + "_foreground", True)):
                destination = folder / (filename + ".webp")
                if destination.is_file():
                    icon(variant, transparent=transparent).resize((pixels, pixels)).save(
                        destination, "WEBP", quality=92)
                    replaced += 1
        for suffix, monochrome in (("round", False), ("monochrome", True)):
            destination = folder / f"ic_launcher_{suffix}.webp"
            if destination.is_file():
                icon(transparent=monochrome, monochrome=monochrome).resize(
                    (pixels, pixels)).save(destination, "WEBP", quality=92)
                replaced += 1
    splash_dir = resource_root / "drawable-nodpi"
    for variant in VERSIONS:
        suffix = "" if variant == "original" else "_" + variant
        path = splash_dir / f"ic_splash_logo{suffix}.webp"
        if path.is_file():
            icon(variant, transparent=True).resize((600, 600)).save(path, "WEBP", quality=94)
            replaced += 1
    compose = ROOT / "composeApp/src/commonMain/composeResources/drawable"
    for variant in VERSIONS:
        path = compose / f"app_icon_{variant}.png"
        if path.is_file():
            icon(variant).resize((512, 512)).save(path, "PNG")
            replaced += 1
        path = compose / f"app_logo_wordmark_{variant}.png"
        if path.is_file():
            wordmark(variant).save(path, "PNG")
            replaced += 1
    for filename, variant in (("app_logo_wordmark.png", "original"),
                              ("app_logo_wordmark_gold.png", "gold")):
        path = compose / filename
        if path.is_file():
            wordmark(variant).save(path, "PNG")
            replaced += 1
    if replaced < 50:
        raise RuntimeError(f"Only {replaced} graphic resources replaced; expected upstream launcher assets.")
    return replaced


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--version-code", default="1", type=int)
    args = parser.parse_args()
    patch_android()
    patch_version(args.version, args.version_code)
    changed = patch_strings()
    assets = make_brand_art()
    print(f"VERGE REBRAND: {changed} translated strings and {assets} original graphics updated.")
    print(f"Android app IDs: {APP_ID} (release) and {DEBUG_ID} (debug).")
    print("Original Nuvio copyright and GNU GPLv3 attribution are retained.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError) as error:
        sys.exit(f"Verge identity step failed: {error}")
