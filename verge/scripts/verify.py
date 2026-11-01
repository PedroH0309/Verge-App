#!/usr/bin/env python3
"""Read-only checks for the imported Verge Android fork."""
from pathlib import Path
import sys
import re

ROOT=Path(__file__).resolve().parents[2]

def main():
    required=[
      "LICENSE", "androidApp/build.gradle.kts", "composeApp/build.gradle.kts",
      "composeApp/src/androidMain/res/values/strings.xml",
      "androidApp/src/main/AndroidManifest.xml",
      "gradlew", "platforms/tv/LICENSE", "platforms/desktop/LICENSE",
      "docs/UPSTREAM.md", "DOWNLOADS.md"
    ]
    missing=[p for p in required if not (ROOT/p).is_file()]
    if missing: raise ValueError("Missing imported files: "+", ".join(missing))
    if "GNU GENERAL PUBLIC LICENSE" not in (ROOT/"LICENSE").read_text():
        raise ValueError("Mobile GPLv3 license is missing.")
    gradle=(ROOT/"androidApp/build.gradle.kts").read_text()
    if 'applicationId = "com.verge.media"' not in gradle:
        raise ValueError("Android application ID is not Verge.")
    if 'variant.applicationId.set("com.verge.media.debug")' not in gradle:
        raise ValueError("Debug application ID is not Verge.")
    strings=(ROOT/"composeApp/src/androidMain/res/values/strings.xml").read_text()
    if '<string name="app_name">Verge</string>' not in strings:
        raise ValueError("Android launcher label is not Verge.")
    manifest=(ROOT/"androidApp/src/main/AndroidManifest.xml").read_text()
    if 'android:scheme="verge"' not in manifest or 'android:host="nuvio.tv"' in manifest:
        raise ValueError("Legacy Nuvio deep link or domain ownership remains.")
    if 'rootProject.name = "Verge"' not in (ROOT/"settings.gradle.kts").read_text():
        raise ValueError("Gradle project was not rebranded.")
    for density in ("mdpi","hdpi","xhdpi","xxhdpi","xxxhdpi"):
        file=ROOT/f"composeApp/src/androidMain/res/mipmap-{density}/ic_launcher.webp"
        if not file.is_file() or file.stat().st_size < 100:
            raise ValueError("Missing Verge launcher image: "+str(file))
    print("Verge source structure and Android identity checks passed.")
    print("These checks do not demonstrate that Android compilation or playback is successful.")

if __name__=="__main__":
    try: main()
    except (OSError,ValueError) as error: sys.exit(str(error))
