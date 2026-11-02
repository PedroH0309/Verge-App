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


def patch_runtime_identity() -> None:
    """Correct user-facing native identity while preserving upstream code namespaces."""
    patches = (
        (
            DESKTOP / "composeApp/src/desktopMain/kotlin/com/nuvio/app/Main.kt",
            (
                ('title = if (smokePlayerUrl == null) "Nuvio" else "Nuvio Player Smoke"',
                 'title = if (smokePlayerUrl == null) "Verge" else "Verge Player Smoke"'),
            ),
        ),
        (
            DESKTOP / "composeApp/src/desktopMain/kotlin/com/nuvio/app/core/storage/DesktopStorage.kt",
            (
                ('Library/Application Support/Nuvio', 'Library/Application Support/Verge'),
                ('Library/Caches/Nuvio', 'Library/Caches/Verge'),
                ('resolve("Nuvio")', 'resolve("Verge")'),
                ('resolve("Nuvio/Cache")', 'resolve("Verge/Cache")'),
                ('resolve("nuvio")', 'resolve("verge")'),
                ('"Nuvio desktop preferences"', '"Verge desktop preferences"'),
            ),
        ),
        (
            DESKTOP / "composeApp/src/desktopMain/kotlin/com/nuvio/app/features/settings/AppIconPlatform.desktop.kt",
            (
                ('resolve("Nuvio.exe")', 'resolve("Verge.exe")'),
                ('"Nuvio Windows app restart"', '"Verge Windows app restart"'),
            ),
        ),
        (
            DESKTOP / "composeApp/src/desktopMain/kotlin/com/nuvio/app/features/settings/WindowsAppShortcutIconUpdater.kt",
            (
                ('"Nuvio/icons"', '"Verge/icons"'),
                ('"Nuvio.lnk"', '"Verge.lnk"'),
                ('"Nuvio/Nuvio.lnk"', '"Verge/Verge.lnk"'),
                ('"Microsoft/Internet Explorer/Quick Launch/User Pinned/TaskBar/Nuvio.lnk"',
                 '"Microsoft/Internet Explorer/Quick Launch/User Pinned/TaskBar/Verge.lnk"'),
                ('"Nuvio Windows app icon updater"', '"Verge Windows app icon updater"'),
            ),
        ),
        (
            DESKTOP / "composeApp/src/desktopMain/kotlin/com/nuvio/app/features/discordrpc/DiscordPresenceManager.kt",
            (
                ('details = "Browsing Nuvio"', 'details = "Browsing Verge"'),
            ),
        ),
        (
            DESKTOP / "composeApp/src/desktopMain/kotlin/com/nuvio/app/core/build/AppVersionPolicy.desktop.kt",
            (
                ('"NuvioDesktop"', '"VergeDesktop"'),
            ),
        ),
    )
    for file, changes in patches:
        content = file.read_text(encoding="utf-8")
        for before, after in changes:
            content = replace_once(content, before, after)
        file.write_text(content, encoding="utf-8")

    # Bump above previous 0.1.33-alpha Windows preview so an MSI upgrade is possible.
    version = DESKTOP / "composeApp/Configuration/DesktopVersion.properties"
    text = version.read_text(encoding="utf-8")
    text = replace_once(text, "VERSION_NAME=0.1.33-alpha", "VERSION_NAME=0.1.36-alpha")
    text = replace_once(text, "VERSION_CODE=33", "VERSION_CODE=36")
    version.write_text(text, encoding="utf-8")


def icons() -> None:
    """Replace both desktop launcher icons and actual in-app Compose wordmarks.

    The original MSI only replaced the native installer icon, which left the
    main application window, navigation and splash using Nuvio's images.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as error:
        raise RuntimeError("Pillow is required to create original Verge artwork.") from error

    colors = {
        "original": ((174, 124, 255), (95, 224, 247)),
        "arctic_blue": ((78, 172, 255), (122, 233, 255)),
        "emerald": ((59, 212, 153), (139, 243, 195)),
        "rose_gold": ((246, 141, 178), (255, 200, 160)),
        "copper": ((241, 151, 91), (255, 203, 135)),
        "graphite": ((168, 183, 206), (226, 235, 249)),
        "gold": ((240, 192, 93), (255, 226, 152)),
    }

    def icon(variant: str, background: bool = True):
        first, second = colors[variant]
        im = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        if background:
            draw.rounded_rectangle((16, 16, 496, 496), radius=115,
                                   fill=(9, 13, 26, 255),
                                   outline=(54, 65, 100, 255), width=3)
        draw.polygon([(113, 111), (177, 111), (269, 367), (243, 444)],
                     fill=(*first, 255))
        draw.polygon([(350, 111), (421, 111), (281, 444), (243, 444), (269, 367)],
                     fill=(*second, 255))
        return im

    def font(size: int):
        candidates = [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        ]
        for candidate in candidates:
            if Path(candidate).is_file():
                return ImageFont.truetype(candidate, size)
        return ImageFont.load_default()

    def wordmark(variant: str):
        result = Image.new("RGBA", (1220, 320), (0, 0, 0, 0))
        logo = icon(variant, background=False).resize((260, 260), Image.Resampling.LANCZOS)
        result.alpha_composite(logo, (2, 28))
        draw = ImageDraw.Draw(result)
        draw.text((285, 52), "VERGE", font=font(180), fill=(245, 247, 254, 255))
        return result

    icon_dir = RES / "icons"
    icon_dir.mkdir(parents=True, exist_ok=True)
    drawable_dir = UI_RES / "drawable"
    drawable_dir.mkdir(parents=True, exist_ok=True)

    def put_image(file: Path, image, fmt: str = "PNG"):
        image.save(file, format=fmt)

    for variant in ("original", "arctic_blue", "emerald",
                    "rose_gold", "copper", "graphite"):
        visible = icon(variant, background=True)
        transparent = icon(variant, background=False)
        # AppIconOption and AppBrandWordmark select these resources at runtime.
        put_image(drawable_dir / f"app_icon_{variant}.png", visible)
        put_image(drawable_dir / f"app_icon_{variant}_transparent.png", transparent)
        put_image(drawable_dir / f"app_logo_wordmark_{variant}.png", wordmark(variant))
        put_image(icon_dir / f"app-icon-{variant}-transparent.png", transparent)
        transparent.save(icon_dir / f"app-icon-{variant}-transparent.ico", format="ICO",
                         sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64),
                                (128, 128), (256, 256)])

    put_image(drawable_dir / "app_logo_wordmark.png", wordmark("original"))
    put_image(drawable_dir / "app_logo_wordmark_gold.png", wordmark("gold"))

    # Native Windows installer icon uses the same Verge mark as the app itself.
    put_image(icon_dir / "verge-app-icon-transparent.png",
              icon("original", background=False))
    icon("original", background=False).save(
        icon_dir / "verge-app-icon-transparent.ico", format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64),
               (128, 128), (256, 256)],
    )
    print("Generated Verge launcher icons, dynamic Compose icons and wordmarks.")


def main() -> None:
    patch_gradle()
    patch_runtime_identity()
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
