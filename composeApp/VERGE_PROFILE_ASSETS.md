# Verge offline avatar integration

The mobile profile picker uses eight original SVG portrait resources in `src/commonMain/composeResources/drawable/verge_avatar_*.svg`.

`VergeAvatarPresets.kt` maps each preset to an illustration and a distinct profile accent color. The app displays these portraits immediately without waiting for the upstream Nuvio/Supabase avatar catalog.

For compatibility with the current profile synchronization API, selecting a Verge portrait stores its distinct color in `avatar_color_hex`, while `avatar_id` remains null. The same preset can be reconstructed from the profile color on another Verge device. External avatar URLs and IDs always take priority when explicitly provided.

The source includes unit tests for preset identity, selection, persistence and external-avatar precedence.

Avoid changing existing `ProfilePushPayload` fields or replacing the Nuvio library architecture during the rebrand. The original source copyright and GPLv3 attribution remain required.
