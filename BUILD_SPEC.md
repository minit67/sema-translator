# Build Spec — Parallel AI Voice Translator (Zoiko Sema, LiveKit)

**Goal:** In a live Zoiko Sema meeting, each participant speaks their own language and each listener hears + reads the meeting in the language they picked. One speaker → many listeners, each in their own language.

**This document is written to be fed to Claude Code / OpenCode as the build plan.** Follow the phases in order. Do not skip to later phases before the acceptance criteria of the current one pass. Build the smallest thing that passes each phase, then move on.

---

## 0. How to use this doc

- Zoiko Sema already runs on **LiveKit**, so the meeting, rooms, tokens, and audio transport already exist. **Do not rebuild any of that.** This feature is a *layer on top*: one new server-side Agent + small client changes.
- The core trick: the Agent publishes **one translated audio track per language**; each client subscribes only to the track for its chosen language. You route per *language*, not per person.
- **Important accuracy note for the coding agent:** LiveKit's Agents API evolves quickly and may have changed since this spec was written. Before writing agent code, fetch the current LiveKit Agents docs (docs.livekit.io) and match the current API. Treat the code blocks below as structure/intent, not exact signatures.

---

## 1. Scope — build this, not that

### BUILD (v1)
1. A server-side **LiveKit Agent** that joins each meeting room, listens to each human speaker, and does STT → translate → TTS.
2. The Agent publishes **one translated audio track per target language** back into the room.
3. **Live captions** per language, sent over LiveKit's data channel.
4. A **per-participant language picker** in the client, and **selective subscription** so each client hears only its language and mutes the raw speaker audio.

### DO NOT BUILD (v1) — explicitly out of scope
- ❌ **Voice/tone/emotion preservation or voice cloning.** Use a good natural voice per language. This is the single biggest time sink and the highest risk of sounding broken. Park it.
- ❌ Admin console, policies, consent flows, terminology glossaries, audit logs, analytics, post-meeting transcripts, public marketing page. (These exist in the larger product spec; none are needed to make the feature *work*.)
- ❌ New meeting infrastructure, custom SFU, WebRTC plumbing. LiveKit already does this.
- ❌ Mobile-specific work until desktop web works end to end.

If a task feels like it belongs in "DO NOT BUILD," stop and confirm before doing it.

---

## 2. Architecture

```
  Human A (Telugu mic)     Human B          Human C          Human D
        │                    │                │                │
        ▼ (audio track)      ▼                ▼                ▼
  ┌──────────────────────── LiveKit room ────────────────────────┐
  │                                                                │
  │   Translator Agent (server-side, identity = "translator")     │
  │     • subscribes to each HUMAN speaker track                   │
  │     • STT (with source-language detect)                        │
  │     • translate → each configured target language              │
  │     • TTS per language                                         │
  │     • publishes tracks: translation-en, translation-hi, ...    │
  │     • publishes captions over data channel                     │
  │                                                                │
  └───────────┬───────────────┬───────────────┬──────────────────┘
              │ translation-en │ translation-hi│ translation-es
              ▼                ▼                ▼
        B hears "en"      C hears "hi"     D hears "es"
     (subscribes en,   (subscribes hi,  (subscribes es,
      mutes raw mics)   mutes raw mics)  mutes raw mics)
```

**One-paragraph summary:** An invisible Agent participant joins the room. It reads each human's mic track, transcribes and translates, and publishes a separate audio track for each language plus caption data. Every client subscribes only to the translation track matching its chosen listening language and unsubscribes/mutes the original human mics. That produces the proposal's exact example (A speaks Telugu; B/C/D each hear English/Hindi/Spanish).

---

## 3. Decisions (LOCKED — build to these)

These are confirmed against the repo. Build to exactly this.

- **Agent language: Python.** The Zoiko backend is **FastAPI (Python)**, so use the mature **`livekit-agents` Python SDK** for the translator agent. It runs as a separate worker process; it does not need to import the FastAPI app.
- **✅ LiveKit media layer: CONFIRMED.** The client is fully on LiveKit — `MeetLobby.jsx` states *"LiveKit is the only media plane now — the legacy WebRTC mesh room has been removed."* Meeting audio flows through the self-hosted SFU rooms, so the agent plan applies directly. No migration needed.
- **LiveKit hosting: SELF-HOSTED (not Cloud).** The agent connects to your own SFU at `LIVEKIT_PUBLIC_WS_URL` / `VITE_LIVEKIT_WS_URL` using the shared `LIVEKIT_API_KEY` / `LIVEKIT_API_SECRET` (same secret the SFU, egress, and FastAPI already use).
- **Reuse existing server LiveKit infra — do NOT rebuild it.** Token minting already exists (server `/media-token` endpoint + `server/app/connect/media_service/livekit_provider.py`); webhooks exist (`server/app/api/webhooks.py`). The agent reuses these credentials and the app's room-naming (`meetingRoomPath(code)`), not its own auth.
- **Client: React 19 + Vite + React Router v6, plain JavaScript (`.jsx`), plain CSS.** NOT Next.js, NOT TypeScript. The live meeting room is `client/src/features/meeting/MeetRoomLivekit.jsx` (NOT `pages/MeetRoom.jsx` — that file is gone). Caption + language-picker changes go there. New client files should be `.jsx`.
- **AI provider: OpenAI for all three steps.** STT, translation, and TTS via OpenAI, using LiveKit's official OpenAI plugin(s). One `OPENAI_API_KEY`.
- **Target languages (v1): `["te", "en", "hi", "es"]`** — Telugu, English, Hindi, Spanish.

---

## Phase 0 — RESOLVED ✅

The client is fully on LiveKit (`MeetLobby.jsx`: *"LiveKit is the only media plane now — the legacy WebRTC mesh room has been removed"*). Meeting audio is in the self-hosted SFU rooms. **Proceed to Phase 1.**

Before writing agent code, read these to learn the exact room-naming and token flow the agent must match:
- `client/src/features/meeting/MeetRoomLivekit.jsx` — how the client connects to the room (room name, token fetch).
- The server `/media-token` route + `server/app/connect/media_service/livekit_provider.py` — how tokens are minted and rooms named (`auto_create=false`, so join an existing room; name derives from the meeting code via `meetingRoomPath(code)`).

---

## 4. Repo layout (add, don't restructure)

```
/agent/                         # NEW — the translator agent (Python, livekit-agents)
  translator_agent.py           # worker entrypoint + pipeline
  config.py                     # target languages, voice map
  requirements.txt
  .env.example

/client/src/                    # EXISTING (React 19 + Vite, plain .jsx) — small additions
  components/LanguagePicker.jsx           # NEW — pick listening + spoken language
  hooks/useTranslationTracks.js           # NEW — selective subscribe + mute originals
  components/Captions.jsx                 # NEW — render per-language captions
  features/meeting/MeetRoomLivekit.jsx    # MODIFY — mount the three above (this is the live room)
```

---

## 5. Data contracts (agree on these before coding — they are the glue)

### Language codes
Use ISO-639-1 two-letter codes everywhere (`en`, `hi`, `es`, `te`, ...). One shared constant map: code → { display name, STT locale, TTS voice id }.

### Published track naming
Each translation track is published by the Agent with a **track name**:
```
translation-<langCode>      e.g. "translation-en", "translation-hi"
```
Clients decide subscription by matching this name. (If the SDK version prefers track metadata/attributes over name, use that — but keep one consistent scheme.)

### Participant attributes (so Agent + clients know who wants what)
Each client sets, on join and on change:
```json
{ "listeningLang": "hi", "spokenLang": "te" }
```
via `localParticipant.setAttributes(...)`. The Agent reads these to know which languages are actually needed (v1 may just produce the fixed configured set; deriving from attributes is a fast-follow optimization).

### Caption data-channel message (JSON, published by Agent)
```json
{
  "type": "caption",
  "speakerIdentity": "user_A",
  "sourceLang": "te",
  "targetLang": "hi",
  "text": "हम शुक्रवार तक समीक्षा पूरी कर सकते हैं।",
  "final": true,
  "ts": 1730000000000
}
```
Clients render only messages where `targetLang === my listeningLang`. Send interim (`final:false`) updates too if latency allows; otherwise final-only is fine for v1.

### Agent identity
The Agent joins with a fixed identity, e.g. `translator-agent`. **Everything keys off this identity** for echo prevention (see §10).

---

## 6. Phase plan (build in this order)

### Phase 1 — Agent joins and transcribes  ·  target ~1 week
Stand up a LiveKit Agent worker that connects to a room, subscribes to one human speaker's audio, and logs live transcription to the console.

**Tasks**
- [ ] Scaffold agent from the current LiveKit Agents starter/template.
- [ ] Connect worker to `LIVEKIT_URL` with API key/secret; auto-dispatch to rooms (or explicit dispatch — match current LiveKit docs).
- [ ] Subscribe to remote audio tracks from human participants only (skip self).
- [ ] Pipe one speaker's track through streaming STT; log interim + final transcripts with detected source language.

**Acceptance:** Join a real Zoiko meeting, speak, and see accurate live transcripts + detected language in the agent logs. No audio is published yet.

---

### Phase 2 — Translate + speak back, ONE language  ·  target ~1 week
Prove the end-to-end loop for a single listener.

**Tasks**
- [ ] On each final STT segment, translate text into one hard-coded target language (e.g. `en`).
- [ ] Send translated text to TTS; capture audio frames.
- [ ] Create one `AudioSource` + `LocalAudioTrack` named `translation-en`; publish it to the room; push TTS frames into it.
- [ ] In the client, temporarily hard-code: subscribe to `translation-en`, and mute/unsubscribe the original human mic tracks.

**Acceptance:** In a real meeting, Person A speaks Telugu and Person B hears an English translation through the actual Zoiko call, with original audio muted for B. **This is the core "it works" milestone.**

---

### Phase 3 — Fan out to all languages + captions + picker  ·  target ~1 week
Turn the single track into the real parallel feature.

**Tasks**
- [ ] Loop over the configured target languages; for each `lang != sourceLang`, translate + TTS + publish `translation-<lang>`. Reuse one AudioSource per language for the whole session.
- [ ] Publish captions over the data channel per the schema in §5 (send one message per target language).
- [ ] Build `LanguagePicker` client component: sets `listeningLang` / `spokenLang` via participant attributes.
- [ ] Build `useTranslationTracks` hook: on track published / picker change, subscribe to `translation-<listeningLang>`, unsubscribe the rest, and mute original human tracks. Use manual subscription (`autoSubscribe: false` or per-track `setSubscribed`).
- [ ] Build `Captions` component: render data-channel messages where `targetLang === listeningLang`, labeled with speaker name.

**Acceptance:** Four participants in one real meeting; A speaks Telugu; B/C/D each pick English/Hindi/Spanish and each independently hears + reads their language; changing the picker mid-meeting re-routes audio without rejoining.

---

### Phase 4 — Make it hold up  ·  target ~1 week (ongoing)
Handle the things that break live audio.

**Tasks**
- [ ] **Echo prevention** (critical — see §10): the Agent must never transcribe its own published tracks or other agents.
- [ ] Serialize TTS per language so translated utterances don't overlap into garble (simple queue per language track).
- [ ] Active-speaker / overlap handling: if two humans talk at once, don't cross-attribute captions; label uncertain segments "Multiple speakers."
- [ ] Reconnect handling: agent rejoins if dropped; client re-establishes subscriptions on reconnect.
- [ ] Latency pass: measure end-of-speech → heard-translation. Expect **~2–4s** with chained STT→translate→TTS; tune by using streaming STT finals early and starting TTS on sentence boundaries.

**Acceptance:** A 10-minute real meeting runs without feedback loops, without the agent translating itself, and with translations that are usable (not overlapping) at ~2–4s latency.

---

## 7. Agent pipeline (reference skeleton — verify against current LiveKit API)

> The agent is **Python** using the `livekit-agents` SDK + OpenAI plugin(s). The block below is **structural pseudocode** — match real imports/signatures to the current `livekit-agents` docs.

```python
# translator_agent.py  (structure/intent only — verify against current docs)

TARGET_LANGS = ["en", "hi", "es", "te"]
AGENT_IDENTITY = "translator-agent"

async def entrypoint(ctx):
    await ctx.connect()  # join the room

    sources = {}  # lang -> AudioSource, created once per session
    for lang in TARGET_LANGS:
        src = create_audio_source()
        track = create_local_audio_track(f"translation-{lang}", src)
        await ctx.room.local_participant.publish_track(track)
        sources[lang] = src

    async def handle_speaker(participant, audio_track):
        if is_agent(participant):        # ECHO GUARD (see §10)
            return
        stt = start_streaming_stt(audio_track)   # detect source lang
        async for segment in stt:
            if not segment.final:
                continue
            src_lang = segment.language
            for lang in TARGET_LANGS:
                if lang == src_lang:
                    continue
                text = await translate(segment.text, src_lang, lang)
                publish_caption(ctx, participant, src_lang, lang, text)
                audio = await tts(text, lang)          # natural voice per lang
                await enqueue_and_push(sources[lang], audio)  # serialized

    on_track_subscribed(ctx.room, handle_speaker)  # only human tracks

def is_agent(participant):
    return participant.identity == AGENT_IDENTITY or participant.identity.startswith("translator")
```

Key point: **create each language's `AudioSource`/track once**, then keep pushing frames into it. Don't create a new track per utterance.

---

## 8. Client changes (reference skeleton)

```ts
// useTranslationTracks.ts (structure only)
// On join: room connects with autoSubscribe = false.
// Subscribe to translation-<listeningLang>; mute original human mics.

function useTranslationTracks(room, listeningLang) {
  useEffect(() => {
    const apply = () => {
      for (const p of room.remoteParticipants.values()) {
        for (const pub of p.trackPublications.values()) {
          const isTranslation = pub.trackName?.startsWith("translation-");
          if (isTranslation) {
            pub.setSubscribed(pub.trackName === `translation-${listeningLang}`);
          } else if (pub.kind === "audio") {
            pub.setSubscribed(false); // mute raw human mic while translating
          }
        }
      }
    };
    apply();
    room.on("trackPublished", apply);
    return () => room.off("trackPublished", apply);
  }, [room, listeningLang]);
}
```

`LanguagePicker` just calls `room.localParticipant.setAttributes({ listeningLang, spokenLang })` and updates local state that feeds the hook. `Captions` subscribes to `room.on("dataReceived")`, parses the JSON, and renders messages matching `listeningLang`.

---

## 9. Environment variables (server-side Agent only — never in the client)

```
LIVEKIT_URL=            # self-hosted SFU ws url = LIVEKIT_PUBLIC_WS_URL / VITE_LIVEKIT_WS_URL
LIVEKIT_API_KEY=        # SAME shared secret the SFU, egress, and FastAPI already use
LIVEKIT_API_SECRET=
OPENAI_API_KEY=         # used for STT, translation, and TTS
```

Reuse the existing LiveKit credentials from the server config — do not create a new key pair. Rooms use `auto_create=false`, so the agent joins rooms the app has already created; use the same room name the meeting uses.

The client keeps using Zoiko's **existing** token endpoint to join rooms. No AI keys ever reach the browser.

---

## 10. Gotchas / must-not-break rules

1. **Echo / self-transcription (the #1 bug).** The Agent publishes audio into the same room it listens to. If it transcribes its own `translation-*` tracks, it will translate its own output forever. **Guard by participant identity**: only run STT on tracks whose publisher is a human (not `translator-agent`, not any agent). Verify this in Phase 4 explicitly.
2. **Keys stay server-side.** All STT/translate/TTS calls happen in the Agent. The browser never sees an AI key.
3. **One track per language, created once.** Don't spawn tracks per utterance; reuse the per-language `AudioSource`.
4. **Serialize TTS per language.** Two overlapping translations on one track = garble. Queue per language.
5. **Latency expectation.** Chained STT→translate→TTS is realistically ~2–4s. That is usable and demoable; it is not sub-second. Say this to stakeholders up front.
6. **Selective subscription must also mute originals.** Subscribing to the translation track isn't enough — you must unsubscribe/mute the raw human mics, or listeners hear both.
7. **No emotion/voice cloning in v1.** If you find yourself wiring a voice-clone provider, stop — it's out of scope.

---

## 11. Minimum-time path (if the clock is tight, cut in this order)

To reach a working, honest version fastest:
1. Ship **Phases 1–2 first** (one speaker → one listener hears translation in the real meeting). That alone proves the feature in the product.
2. Then Phase 3 **captions-only** before wiring all TTS voices, if audio fan-out is fiddly — captions per language demonstrate the parallel idea with far less risk.
3. Add remaining TTS languages one at a time.
4. Phase 4 hardening last, but do the **echo guard (§10.1) as soon as any audio is published** — it's not optional even in a rough build.

**Realistic total: ~3–5 weeks solo with Claude Code, on the existing LiveKit stack.** The engine you already prototyped (STT→translate→TTS) is reused inside the Agent; the new work is the LiveKit routing, which the Agents framework carries most of.

---

### Definition of done (v1)
In a real Zoiko Sema meeting, four people join; one speaks Telugu; the other three each select English, Hindi, and Spanish; each independently hears a natural translated voice and reads live captions in their language; changing language mid-meeting re-routes without rejoining; no feedback loop; latency ~2–4s. Emotion preservation, admin/governance, and post-meeting features are explicitly deferred.
