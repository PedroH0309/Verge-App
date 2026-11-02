# Verge desktop profile avatar integration

The Windows/desktop profile experience includes eight offline Verge portraits in `composeApp/src/commonMain/composeResources/drawable/verge_avatar_*.svg`.

The corresponding shared Kotlin `VergeAvatarPresets.kt` handles mapping illustrations to color-backed profiles. The picker and profile switcher render these local SVG portraits before any remote request. Fallback initials remain visible if an online portrait cannot be downloaded.

This fixes the original dependency on a remote avatar-catalog RPC for basic profile customization. Windows settings and resources remain in the Verge-specific user directory created by the build transformation script.

The Nuvio-style library architecture, saved lists and synchronization adapters are preserved. As a GPLv3 derivative, the application retains all original source copyright and third-party notices.
