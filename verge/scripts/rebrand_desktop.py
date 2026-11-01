#!/usr/bin/env python3
"""Prepare the independent Verge Desktop identity from the imported Nuvio Desktop GPLv3 sources.

This is a reproducible build transformation. It does not erase upstream author credits,
Nuvio service names, attribution text, or third-party license terms.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
DESKTOP = ROOT / "platforms" / "desktop"
GRADLE = DESKTOP / "composeApp" / "build.gradle.kts"
RES = DESKTOP / "composeApp" / "src" / "desktopMain" / "resources"
UI_RES = DESKTOP / "composeApp" / "src" / "commonMain" / "composeResources"
MSI_UUID = "72de31c8-43d3-42bb-9f82-3c7bcb48b27d"

PROTECTED_NAMES = (
    "license", "attribution", "copyright", "support_nuvio", "supporters",
    "community_", "patreon", "donation", "server_", "tracking_nuvio_",
    "nuvio_library", "nuvio_progress", "trakt_", "simkl_", "imdb_",
    "tmdb_", "api_", "settings_licenses", "settings_about",
)
STRING = re.compile(r'(<string\b[^>]*\bname="([^"]+)"[^>]*>)(.*?)(</string>)', re.S)


def replace_once(text: str, before: str, after: str) -> str:
    if before in text:
        return text.replace(before, after)
    if after in text:
        return text
    raise ValueError("Upstream packaging configuration changed: " + before)


def patch_gradle() -> None:
    if not GRADLE.exists():
        raise FileNotFoundError("Missing imported Nuvio Desktop Gradle sources.")
    text = GRADLE.read_text(encoding="utf-8")
    for old, new in (
        ('packageName = "Nuvio"', 'packageName = "Verge"'),
        ('vendor = "Nuvio Media"', 'vendor = "Verge Media"'),
        ('menuGroup = "Nuvio"', 'menuGroup = "Verge"'),
        ('val windowsMsiUpgradeUuid = "395990ee-9b8a-3548-922c-e7a23a495b8d"',
         'val windowsMsiUpgradeUuid = "' + MSI_UUID + '"'),
        ('"Nuvio-Windows-$windowsPlayerBridgeArch-$desktopReleaseVersionName.msi"',
         '"Verge-Windows-$windowsPlayerBridgeArch-$desktopReleaseVersionName.msi"'),
        ('"Nuvio-$desktopReleasePackageVersion.msi"', '"Verge-$desktopReleasePackageVersion.msi"'),
        ('src/desktopMain/resources/icons/nuvio-app-icon-transparent.ico',
         'src/desktopMain/resources/icons/verge-app-icon-transparent.ico'),
        ('src/desktopMain/resources/icons/nuvio-app-icon-transparent.png',
         'src/desktopMain/resources/icons/verge-app-icon-transparent.png'),
        ('bundleID = "com.nuvio.media.desktop"', 'bundleID = "com.verge.media.desktop"'),
        ('<string>com.nuvio.media.desktop</string>', '<string>com.verge.media.desktop</string>'),
    ):
        text = replace_once(text, old, new)
    GRADLE.write_text(text, encoding="utf-8")

    # Keep "Nuvio" as Gradle's internal root project name and Kotlin namespace
    # so existing Compose-generated Res imports do not break.
    settings = (DESKTOP / "settings.gradle.kts").read_text(encoding="utf-8")
    if 'rootProject.name = "Nuvio"' not in settings:
        raise ValueError("Unexpected desktop root project namespace: review generated Res imports.")


def patch_ui() -> int:
    modified = 0
    resource_paths = [
        DESKTOP / "composeApp/src/androidMain/res",
        UI_RES,
    ]
    for directory in resource_paths:
        if not directory.exists():
            continue
        for path in directory.glob("values*/strings*.xml"):
            text = path.read_text(encoding="utf-8")
            def update(match):
                nonlocal modified
                prefix, key, value, suffix = match.groups()
                if any(protected in key.lower() for protected in PROTECTED_NAMES):
                    return match.group(0)
                if "https://" in value or "http://" in value or "GPL" in value:
                    return match.group(0)
                replaced = re.sub(r'\bNuvio\b', 'Verge', value)
                if replaced != value:
                    modified += 1
                return prefix + replaced + suffix
            updated = STRING.sub(update, text)
            if updated != text:
                path.write_text(updated, encoding="utf-8")
    return modified


def icons() -> None:
    try:
        from PIL import Image, ImageDraw
    except ImportError as error:
        raise RuntimeError("Pillow is required to create original Verge desktop icons.") from error

    image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((20, 20, 492, 492), radius=112, fill="#090D1A")
    draw.polygon([(116, 117), (184, 117), (273, 370), (245, 444)],
                 fill=(174, 124, 255, 255))
    draw.polygon([(350, 117), (420, 117), (285, 444), (245, 444), (273, 370)],
                 fill=(95, 224, 247, 255))
    folder = RES / "icons"
    folder.mkdir(parents=True, exist_ok=True)
    image.save(folder / "verge-app-icon-transparent.png", format="PNG")
    image.save(folder / "verge-app-icon-transparent.ico", format="ICO",
               sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64),
                      (128, 128), (256, 256)])


def main() -> None:
    patch_gradle()
    count = patch_ui()
    icons()
    print("Verge Desktop branding applied.")
    print("Windows MSI has a unique upgrade UUID; original Nuvio may coexist.")
    print(f"Updated {count} user-facing resource strings; legal notices preserved.")
    print("Desktop application code remains under the Nuvio upstream GPLv3 license.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError) as error:
        sys.exit("Verge desktop preparation failed: " + str(error))
