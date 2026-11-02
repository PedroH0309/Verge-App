# Verge: Library, Live TV and Playback Roadmap

## Existing library: preserve the Nuvio experience

Verge Mobile and Verge Desktop include the original Nuvio GPLv3 library implementation.

The existing library supports:

- Per-profile saved films, series and supported metadata types
- Horizontal category shelves or vertical layouts
- Filtering and sorting within the library
- Poster cards, metadata, saved lists and custom collections
- Watched/progress tracking and optional account synchronization
- Tracking integrations (Trakt, Simkl, MDBList), where their APIs and terms permit
- Optional media-server and cloud-library views

**The library is not a catalog of movies licensed to Verge.** The app may display metadata and user-selected sources, but copying Nuvio's code does not confer media playback or redistribution rights.

### User experience principles

1. Local library and profile information should display without waiting for external networking.
2. Keep layout, filter selection and last selected profile stable as the user navigates.
3. Make image requests asynchronous, use lazy scroll containers and avoid unnecessary continuous animations.
4. Avoid blocking navigation on failed avatar or metadata RPC requests.
5. Show helpful empty states and an explicit retry action when an online service is unavailable.
6. Preserve the existing Nuvio collections, watch-progress and library data models during rebranding.

## Live TV feasibility

Verge could support a dedicated **Live TV** area with a program guide and channels that the publisher or user is entitled to access. No copyrighted broadcast streams are bundled in this repository.

### Proposed architecture

- `LiveChannel`: immutable channel identifier, name, region, genre, poster, optional provider ID and permitted stream descriptors.
- `LiveProgram`: EPG data (start/end, timezone, title, description and age rating).
- `LiveChannelRepository`: licensed catalog, local favorites and recent channels; no indiscriminate scraping of channels.
- `LiveStreamResolver`: provider-authorized HLS/DASH stream resolution, session expiry handling and playback errors.
- `LiveGuideScreen`: lazy channel grid, current-program status, favorites, search and program details.
- `LivePlayerScreen`: adaptive playback, subtitle/audio selection and an explicit availability message.
- `AuthorizedProviderAdapter`: official integration using documented APIs, contracts and credentials; only use embedded playback where explicitly allowed.
- `UserOwnedSourceAdapter`: optional personal sources that the user has rights to access; validate URLs, do not bypass DRM, do not ship piracy playlists.

Recommended rollout: first add a test channel controlled by Verge (or a licensed public demo feed), then add an EPG fixture, favorites, and authorized provider integrations one at a time.

### Requested broadcasters

| Provider | Public viewing route | Direct in-app retransmission |
| --- | --- | --- |
| Band (Brazil) | Official Band ao vivo / Bandplay | Requires appropriate streaming rights and technical permission |
| Record (Brazil) | Official RecordPlus (formerly PlayPlus) | Requires agreement or authorized embedding/SDK |
| Premiere (Brazil) | Paid subscription through Premiere/Globoplay | Requires explicit distribution license, subscription entitlement and DRM compatibility |
| SBS (Australia) | Official SBS On Demand | Restricted to viewers within Australia; territory and broadcast rights must be respected |

Official reference pages:

- Band: https://www.band.com.br/ao-vivo
- RecordPlus: https://descubra.recordplus.com/
- Premiere: https://premiere.globo.com/
- SBS: https://help.sbs.com.au/hc/en-au/articles/360002023135-Information-on-Live-Streaming-SBS-and-the-SBS-On-Demand-Guide

**Important:** A channel being free to watch on a broadcaster's website does not mean it can be captured, embedded, resold or retransmitted by Verge. Do not bypass geographic restrictions, DRM, paywalls or access policies.

## Current implementation milestone

- Original Nuvio library is preserved, rather than replacing it with an empty prototype.
- Eight local Verge profile avatars allow immediate selection without the upstream RPC.
- GIF avatars animate on hover instead of continuously on the desktop.
- A full live-TV catalog, rights-managed EPG and channel player are not implemented yet; the above is a design proposal, not a claim that Band, Record, SBS or Premiere currently play inside Verge.
