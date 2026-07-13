# Live Language Agent — Naming & Meeting-Screen Implementation Specification

**Canonical decision: Sema Interpreter AI**
Business-first | Individual-accessible | ZoikoTime-integrated

| Control | Value |
|---|---|
| Document ID | ZS-AI-LANG-01 v1.0 |
| Status | Final implementation specification |
| Date | 13 July 2026 |
| Platform | Zoiko Sema |
| Primary consumers | Product, Meeting Client, AI Platform, Backend, UX/UI, QA, Accessibility, Security, Privacy, Compliance, Support |
| Decision authority | Founder/CTO product direction |
| Supersedes | Working label "translator-agent" and all unapproved public variants |
| Brand colors | Sema Navy #172A44; Action Violet #5A45D6; restrained teal for live-state confirmation |

Source file: `Zoiko_Sema_Live_Language_Agent_Naming_Implementation_Specification.docx` (received via WhatsApp, 2026-07-13).

## 0. Executive Decision

Naming decision is final at the product-specification level; legal trademark review remains a separate normal release control.

**Why "Interpreter" wins:** the service operates on spoken language in real time. Professional language convention distinguishes spoken interpreting from written translation. Enterprise precedent: Microsoft "Interpreter agent" (Teams), Zoom "Voice translator" / "Live AI Interpreter", Google "Speech Translation". Market permits "translator" but "interpreter" is the more exact identity for an agent represented inside a live meeting.

### Approved canonical public name

**Sema Interpreter** — displayed with a separate **AI** disclosure badge. "AI" must not be embedded into the product name itself.

| Candidate | Assessment | Decision |
|---|---|---|
| Sema Translator | Understandable, but implies document/chat/caption/file translation rather than spoken meeting service | Viable secondary wording; not selected |
| Sema Translator AI | Generic-feeling, duplicates disclosure badge | Do not use as canonical name |
| **Sema Interpreter** | Most precise, premium, scalable, enterprise-credible | **Approved** |
| Sema AI Interpreter | Clear but less elegant than separate AI badge | Reserved; do not use by default |
| Sema Live Interpreter | Accurate but "Live" belongs in operating state, not name | Do not use as canonical name |

| Layer | Canonical value | Primary use |
|---|---|---|
| Capability label | Live translation | Settings, menus, onboarding, help, entitlement descriptions |
| Agent identity | Sema Interpreter | Participant/service list, active service tile, activity feed, audit UI |
| Disclosure | AI badge | Always adjacent to name where agent is personified/listed as meeting entity |
| Current state | Interpreting live | Runtime status; state-specific copy when paused/reconnecting/blocked |
| Internal service key | `sema-interpreter-agent` | Service registry, logs, config, deployment, observability |
| Internal participant type | `AI_SERVICE` | Prevents accidental treatment as human participant or media endpoint |
| Feature key | `live_interpretation` | Entitlements, policy, billing, telemetry, analytics |

**Hard rule:** never expose internal slugs, deployment names, bot identifiers, model names, provider names, or hyphenated service tokens in the meeting UI. `translator-agent` is an implementation label, not product copy.

## 1. Critical Analysis of the Current Implementation

Current tile behaves like a failed human participant tile — product, accessibility, governance, and engineering ambiguity.

**Current-state defects:**
- `translator-agent` exposes an internal technical token.
- Lowercase, hyphenated label fails product-name and localization standards.
- "T" avatar resembles a human initial rather than an AI service identity.
- "Camera off" is semantically false — an interpreter service has no camera.
- Muted-microphone icon implies user-controlled audio capture rather than governed service processing.
- Tile can be counted/perceived as a human attendee unless participant model differentiated.
- No explicit AI disclosure adjacent to the name.
- No visible language pair, operating state, policy state, or user control context.

**Required correction doctrine:**

| Principle | Implementation requirement |
|---|---|
| Identity | Present as a named Zoiko Sema capability, not infrastructure |
| Transparency | Label AI wherever it appears as entity/participant/service actor |
| Semantic accuracy | No camera, microphone, hand raise, reaction, or human-presence controls on AI service tile |
| Count integrity | Exclude from human attendee counts; expose separate service/agent counts only where useful |
| Progressive disclosure | Calm default grid; full tile only when active/pinned/selected/required by policy |
| Policy awareness | UI reflects permission, recording/transcript behavior, retention, Confidential Mode restrictions |
| Localization | Canonical brand name stable; localize descriptive states/accessibility text |

## 2. Naming Evaluation Framework

Tested against 12 weighted criteria (spoken-language precision 15, five-second comprehension 12, enterprise credibility 10, product-brand ownership 9, AI transparency 8, UI compactness 8, localization resilience 8, scope clarity 8, future scalability 7, accessibility 6, technical mapping 5, marketing/search familiarity 4).

| Candidate | Score | Rank |
|---|---|---|
| Sema Interpreter | 93/100 | 1 |
| Sema Live Interpreter | 88/100 | 2 |
| Sema Translator | 84/100 | 3 |
| Sema AI Interpreter | 82/100 | 4 |
| Sema Translator AI | 76/100 | 5 |
| Sema Language Agent | 69/100 | 6 |
| Sema Translation Agent | 66/100 | 7 |

**Decision boundary:** use "translation" for the feature category and user action; use "Interpreter" for the AI service identity.

## 3. Canonical Meeting-Screen Experience

| Priority / surface | Role | Canonical display | Behavior |
|---|---|---|---|
| 1. Meeting toolbar / status chip | Default active-state surface | Interpreter on · AI | Visible when active; opens language/audio controls |
| 2. Participants panel | Persistent transparency surface | Sema Interpreter [AI] | Listed under "AI services", not mixed into people |
| 3. Gallery/service tile | Conditional surface | Sema Interpreter [AI] | Shown only when selected/pinned/actively speaking/policy-required |
| 4. Meeting details / activity | Audit-friendly surface | "Live interpretation started by {actor}" | Records activation, policy, language scope, state changes |
| 5. Recording/transcript indicators | Data-use surface | "Interpretation included / excluded" | Must reflect actual recording/transcript/retention behavior |

**Service-tile content anatomy:**

| Zone | Element | Copy | Rule |
|---|---|---|---|
| Top-left | AI disclosure badge | AI | Always visible when tile is visible |
| Center | Service icon | Approved interpreter/translation icon | No human initial, no invented second logo |
| Center state | Runtime status | Interpreting live | Update within 500ms of backend state confirmation |
| Center detail | Language context | English → Spanish | Only when single pair applies to viewer; else "2 languages active" |
| Bottom-left | Canonical name | Sema Interpreter | Never truncate to internal slug; compact fallback "Interpreter" |
| Bottom-left adjacent | AI badge | AI | Separate visual badge; accessible name "artificial intelligence service" |
| Bottom-right | Health / scope | Active · 2 languages | No camera-off or muted-mic iconography |

**Responsive display rules:**

| Viewport / mode | Required display |
|---|---|
| ≥ 1024 px | Sema Interpreter [AI] + state + viewer language pair |
| 600–1023 px | Sema Interpreter [AI] + state; language pair to tooltip/details |
| 360–599 px | Interpreter [AI] + active-state dot; full accessible name remains "Sema Interpreter, artificial intelligence service" |
| < 360 px / compact chip | Interpreter on; AI icon; no duplicate brand text |

Screen reader: "Sema Interpreter, artificial intelligence service, interpreting live from English to Spanish."

## 4. Canonical UI Copy and State Model

**Approved public labels:**

| Surface | Canonical copy |
|---|---|
| Feature menu | Live translation |
| Feature settings title | Live translation |
| Agent/service name | Sema Interpreter |
| Disclosure badge | AI |
| Enable action | Turn on interpretation |
| Disable action | Turn off interpretation |
| Language control | Choose the language you want to hear |
| Speaking language | My speaking language |
| Original audio option | Hear original audio |
| Translated audio option | Hear interpreted audio |
| Audio mix control | Original / interpreted audio balance |
| Participant grouping | AI services |
| Admin policy label | Live interpretation |

**Runtime state copy:**

| State | Primary message | Compact | Tone | Meaning |
|---|---|---|---|---|
| OFF | Not active | Interpreter off | Neutral | Service not running |
| STARTING | Starting interpretation… | Starting | Progress | Resources/policy/models/routes initializing |
| READY | Ready to interpret | Ready | Positive neutral | Initialized; waiting for speech |
| ACTIVE | Interpreting live | Active | Positive | Speech-to-speech operating |
| PAUSED_USER | Interpretation paused | Paused | Neutral | Paused by authorized user |
| PAUSED_POLICY | Paused by meeting policy | Managed | Policy | Policy engine suspended service |
| RECONNECTING | Reconnecting interpretation… | Reconnecting | Warning | Temporary service/media interruption |
| DEGRADED | Interpretation quality may be reduced | Limited | Warning | High latency/low confidence/unsupported terminology/audio issue |
| UNSUPPORTED_PAIR | This language pair is not available | Unavailable | Blocking | No approved model/route for pair |
| BLOCKED_CONFIDENTIAL | Unavailable in Confidential Mode | Unavailable | Blocking | Blocked by confidentiality policy |
| FAILED | Interpretation stopped | Stopped | Error | Failed; offer retry and original audio |

**Prohibited public copy:**
- "translator-agent", "translation-agent", "interpreter-agent" as a visible name
- "bot", "robot", "system user", "service account", or provider/model names
- "Camera off", "Mic muted", or "No video" on the service tile
- "100% accurate", "perfect translation", "human-level", or guaranteed-outcome claims
- "Recording" or "not recording" unless driven by actual recording/transcript policy state
- Language-pair claims that don't match the viewer-specific route

## 5. Engineering Identity, Data Contract, and Event Model

**Canonical identity contract:**

```json
{
  "entity_type": "AI_SERVICE",
  "service_kind": "INTERPRETER",
  "service_id": "sema-interpreter-agent",
  "display_name_key": "meeting.ai_service.interpreter.name",
  "display_name_fallback": "Sema Interpreter",
  "disclosure": "AI",
  "feature_key": "live_interpretation",
  "counts_as_human_participant": false,
  "has_camera_capability": false,
  "has_user_microphone_control": false,
  "is_recording_actor": false,
  "policy_managed": true,
  "viewer_language_context": true
}
```

**Required domain types:**

| Field | Canonical value | Implementation rule |
|---|---|---|
| entity_type | AI_SERVICE | Distinct from HUMAN, ROOM, PSTN, SIP, EXTERNAL_BOT, SYSTEM |
| service_kind | INTERPRETER | Extensible family: INTERPRETER, NOTE_TAKER, FACILITATOR, MODERATOR, SUPPORT |
| feature_key | live_interpretation | Stable entitlement/policy/billing key |
| runtime_state | InterpreterState enum | OFF, STARTING, READY, ACTIVE, PAUSED_USER, PAUSED_POLICY, RECONNECTING, DEGRADED, BLOCKED, FAILED |
| policy_state | ALLOW / DENY / MANAGED | Evaluated before activation and on policy change |
| confidentiality_mode | STANDARD_SECURE / CONFIDENTIAL | Default deny in Confidential Mode |
| audio_mode | ORIGINAL / INTERPRETED / MIXED | Viewer-specific, not global participant state |
| language_route | source_locale + target_locale | Viewer-specific route; auto-detect only where approved |

**Localization keys:**

```
meeting.ai_service.interpreter.name = "Sema Interpreter"
meeting.ai_service.interpreter.badge = "AI"
meeting.ai_service.interpreter.state.active = "Interpreting live"
meeting.ai_service.interpreter.state.ready = "Ready to interpret"
meeting.ai_service.interpreter.state.reconnecting = "Reconnecting interpretation…"
meeting.ai_service.interpreter.blocked.confidential = "Unavailable in Confidential Mode"
meeting.ai_service.interpreter.a11y.active = "Sema Interpreter, artificial intelligence service, interpreting live from {sourceLanguage} to {targetLanguage}."
meeting.live_translation.menu = "Live translation"
meeting.live_translation.enable = "Turn on interpretation"
meeting.live_translation.disable = "Turn off interpretation"
```

**Audit and telemetry events:**

| Event | Minimum payload |
|---|---|
| live_interpretation_activation_requested | meeting_id, tenant_id, actor_id, language_scope, policy_version, entitlement_result |
| live_interpretation_policy_evaluated | allow/deny, reason_code, confidentiality_mode, jurisdiction, admin_policy_id |
| interpreter_service_started | service_session_id, provider_route_id, model_route_version, source/target locales, started_at |
| interpreter_service_state_changed | from_state, to_state, reason_code, latency_ms, viewer_scope |
| interpreter_language_route_changed | actor_id, prior route, new route, effective_at |
| interpreter_quality_degraded | quality_reason, confidence band, audio condition, fallback applied |
| interpreter_service_stopped | initiator, reason_code, duration, usage units, retention disposition |
| interpreter_consent_notice_shown | viewer_id, notice_version, timestamp, acknowledgement state where required |

## 6. Governance, Privacy, Security, and Confidential Mode

**Policy evaluation order:** tenant entitlement/plan → org admin policy → meeting organizer policy/classification → Confidential Mode/E2EE gate → jurisdiction/residency/cross-border rules → language-pair availability/approved route → participant notice/consent → recording/transcript/retention/audit config → runtime safety/service-health gate.

**Default confidentiality rule:** Sema Interpreter is unavailable in Confidential Mode unless a future endpoint-only, cryptographically compatible architecture is separately approved. Current server-mediated path must fail closed.

**Required governance behaviors:**

| Control | Required behavior |
|---|---|
| Activation transparency | Notify participants AI live interpretation is active; identify what's processed/heard/retained |
| Participant choice | Each participant chooses original/interpreted/mixed audio; can disable for own output route |
| Host/admin control | Authorized hosts enable/disable supported routes; org policy can lock setting |
| Recording boundary | Do not infer recording from interpretation — separate capabilities, separate indicators |
| Data minimization | Process only audio/metadata required for active route; avoid retaining raw audio by default |
| Provider disclosure | Provider/model names stay internal unless legal/procurement requires disclosure in admin/trust surface |
| Auditability | Store activation/policy/route/state/stop events without exposing model internals in public UI |
| Failure safety | On failure, preserve original audio, announce interruption, never mute/delay original stream without explicit user selection |

**Participant-count doctrine:** service must not increase displayed human attendee count. Use separate label e.g. "24 people · 2 AI services". Participants panel may group AI services beneath people/rooms/dial-in, grouping must remain visible and keyboard accessible.

## 7. Accessibility, Localization, and Inclusive Design

- Use localized language names, not raw locale codes, in public UI.
- "English → Spanish" only when route is directional and viewer-specific.
- "English ↔ Spanish" only when service truly supports and has enabled both directions.
- For multilingual meetings, use viewer-specific copy ("Hear in Spanish") rather than a global pair that may be false for other participants.
- Never label automatic detection as exact until source language confirmed; use "Detecting spoken language…" during detection.
- Flag icons only as optional decorative aids, never the sole language indicator.
- Accessible name: "Sema Interpreter, artificial intelligence service" + state + viewer language pair when present.
- Polite live-region announcements for normal state changes; assertive only for failures that materially change audio comprehension.
- Color independence: AI/active/degraded/blocked states require text/icon labels, never color alone.
- Full keyboard operability; minimum 44×44 CSS px touch targets.
- Do not assume live captions are enabled — separate preference from interpretation.
- Default view: one state, one action; advanced controls in progressive disclosure.
- Keep "Sema Interpreter" as brand identity unless formal brand-localization strategy approves a localized equivalent.
- Test RTL languages, arrow direction, locale order, truncation, mirrored layouts; verify screen-reader pronunciation of "Sema".

## 8. Implementation and Migration Plan

**Phase 1 — Identity correction (release blocking)**
- Replace visible "translator-agent" strings with canonical i18n key and fallback "Sema Interpreter".
- Add AI disclosure badge and accessible service classification.
- Remove "Camera off", human initial avatar, and muted-microphone controls from the service tile.
- Exclude entity from human participant counts and attendance exports.
- Add service-specific runtime states and original-audio fallback behavior.

**Phase 2 — Governed live-translation controls**
- Implement viewer-specific language and audio routes.
- Add admin/host policy enforcement and participant notices.
- Add Confidential Mode fail-closed behavior.
- Add audit events, telemetry, support diagnostics.
- Add participants-panel grouping and compact toolbar chip.

**Phase 3 — Quality and scale**
- Quality confidence bands and degraded-state explanations.
- Approved terminology glossaries and tenant-specific vocabulary where licensed/governed.
- Language-route capacity management, quota/usage metering, entitlement enforcement.
- Expanded meetings/calls coverage with same canonical agent identity.
- Endpoint-safe interpretation research for possible future Confidential Mode compatibility.

**Backward compatibility / migration:**

| Artifact | Legacy value | Migration rule |
|---|---|---|
| Legacy display name | translator-agent | Map to "Sema Interpreter"; never preserve in UI |
| Legacy service ID | translator-agent | May remain temporarily as internal alias; canonical service ID becomes `sema-interpreter-agent` |
| Analytics dimensions | translator_agent | Migration mapping to live_interpretation / INTERPRETER; maintain historical query compatibility |
| Saved meeting policy | translator_enabled | Migrate to live_interpretation.policy_state with explicit ALLOW/DENY/MANAGED semantics |
| Attendance records | participant row | Reclassify as AI_SERVICE where technically safe; no retroactive rewrite of legal records without governance approval |

**Ownership:**

| Owner | Accountability |
|---|---|
| Product | Canonical copy, feature scope, entitlement rules, meeting UX behavior |
| Meeting Client | Toolbar, participant panel, service tile, responsive states, accessibility semantics |
| AI Platform | Speech route, model/provider abstraction, quality state, usage metrics |
| Backend / Realtime | AI_SERVICE entity model, runtime state, event delivery, counts |
| Security / Privacy / Compliance | Policy gates, notices, processing boundary, audit and retention |
| Design System | AI badge, service tile pattern, iconography, state tokens |
| Localization | Language names, state copy, RTL and truncation validation |
| QA | Functional, policy, accessibility, failure, device, language-route and regression testing |

## 9. Release Acceptance Criteria

| Gate | Pass standard | Severity |
|---|---|---|
| Naming | No user-visible "translator-agent," service slug, provider name, model name, or unapproved variant remains | Block |
| AI disclosure | Every personified/listed agent surface shows AI visually and exposes "artificial intelligence service" to assistive tech | Block |
| Semantic UI | No camera, human microphone, hand-raise, reaction, or presence controls rendered for AI_SERVICE | Block |
| Counts | Human attendee counts, attendance reports, licensing counts follow approved service-count rules | Block |
| State integrity | UI state driven by confirmed service state, not optimistic local state; failures preserve original audio | Block |
| Policy | Confidential Mode and denied policies fail closed; managed states explain why controls unavailable | Block |
| Privacy notice | Required participant notice shown and versioned before/at activation | Block |
| Accessibility | Keyboard, screen reader, contrast, live-region, focus, touch target, zoom tests pass | Block |
| Localization | Supported locales pass truncation, RTL, pluralization, language-name, pair-direction tests | Block |
| Performance | Agent-state updates render within 500ms of confirmed realtime event under normal conditions | Major |
| Observability | Activation, policy, route, degradation, failure, stop events traceable by meeting/service session | Block |
| Supportability | Support can identify service state/reason codes without access to meeting content | Major |
| Visual quality | Tile/chip feels native to Zoiko Sema, uses Sema Navy/Violet correctly, no human placeholder resemblance | Major |

**Minimum test matrix:**

| Dimension | Coverage |
|---|---|
| Modes | Standard Secure; Confidential Mode; guest meeting; webinar/large meeting where supported |
| Clients | Web; Windows; macOS; Android; iOS; room/device surfaces where supported |
| Roles | Organizer; co-host; member; guest; anonymous guest; admin-managed user |
| Language routes | One-way; bidirectional; unsupported pair; auto-detect; multilingual viewer-specific routes |
| States | All state enum values, rapid transitions, reconnect loops, backend timeout, provider failover |
| Audio | Original; interpreted; mixed; device change; low bandwidth; packet loss; Bluetooth switch |
| Accessibility | Screen readers; keyboard-only; 200% zoom; high contrast; reduced motion; RTL |
| Policy | Allow; deny; managed; entitlement exhausted; jurisdiction blocked; Confidential Mode |

**Final release decision:** implementation is not complete when the text label changes. Release requires the AI_SERVICE identity model, correct counts and controls, governed policy behavior, accessible semantics, and runtime state integrity described in this specification.

## Appendix A — Engineering Copy Matrix

| Purpose | Approved copy | Note |
|---|---|---|
| Service name | Sema Interpreter | Canonical; do not localize without brand approval |
| AI badge | AI | Visible and accessible |
| Active state | Interpreting live | Do not use "Translating…" for persistent active state |
| Ready state | Ready to interpret | Service initialized |
| Starting state | Starting interpretation… | Ellipsis only for active progress |
| Reconnecting | Reconnecting interpretation… | Original audio remains available |
| Degraded | Interpretation quality may be reduced | Link to reason/details when actionable |
| Stopped | Interpretation stopped | Include retry where authorized |
| Confidential block | Unavailable in Confidential Mode | Policy-managed explanation |
| Unsupported pair | This language pair is not available | Offer supported alternatives |
| Menu | Live translation | Plain-language category |
| Enable | Turn on interpretation | Verb matches spoken service |
| Disable | Turn off interpretation | Do not use "remove agent" for normal control |
| Hear target | Choose the language you want to hear | User-centered wording |
| Original audio | Hear original audio | Viewer preference |
| Interpreted audio | Hear interpreted audio | Viewer preference |
| Panel group | AI services | Separates services from people |
| Count summary | {peopleCount} people · {serviceCount} AI services | Only where service count adds value |

**Compact and accessibility variants:**

| Context | Copy |
|---|---|
| Compact tile name | Interpreter |
| Compact status chip | Interpreter on |
| Tooltip | Sema Interpreter is interpreting this meeting using AI. |
| Accessible inactive | Sema Interpreter, artificial intelligence service, not active. |
| Accessible active | Sema Interpreter, artificial intelligence service, interpreting live from {sourceLanguage} to {targetLanguage}. |
| Accessible managed | Sema Interpreter, artificial intelligence service. This setting is managed by {organizationName}. |
| Accessible blocked | Sema Interpreter is unavailable because this meeting is using Confidential Mode. |

## Appendix B — Standards and Competitive Reference Notes

References used for terminology/pattern analysis only; Zoiko Sema retains its own product architecture and brand.

1. American Translators Association — Translator vs. Interpreter: interpreters work with spoken language; translators work with written text.
2. Microsoft Support — Interpreter in Microsoft Teams meetings and calls: precedent for naming real-time speech-to-speech AI capability "Interpreter agent".
3. Microsoft Support — Use language interpretation in Microsoft Teams meetings.
4. Zoom Support — Voice translator for meetings: precedent for consumer-familiar "Voice translator" terminology.
5. Zoom Support — Zoom Contact Center Live AI Interpreter: precedent for "Live AI Interpreter" in speech-to-speech product.
6. Google Meet Help — Speech Translation: precedent for functional feature label rather than personifying the service as an agent.

**Reference conclusion:** the category has no single universal label. "Translation" is the most familiar feature term; "interpreter" is the most exact name for a spoken-language actor. The selected architecture uses both at their strongest layer: **Live translation** for the capability, **Sema Interpreter** for the AI service identity.

---

**Canonical lock line:** Public agent identity: **Sema Interpreter**. Disclosure: **AI badge**. Capability: **Live translation**. Internal service: `sema-interpreter-agent`.
