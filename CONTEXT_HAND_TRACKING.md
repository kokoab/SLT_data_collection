# Context: Hand Tracking Issues in SLT Data Collection

## Instructions for AI Assistants (Claude, etc.)

When helping with hand tracking or SLT data collection in this project:

1. **Prioritize practical fixes** — Suggest concrete, implementable changes (code, protocol, config) over theoretical options.
2. **Respect fundamental limits** — Do not suggest solutions for occlusion; acknowledge when a problem is inherent (e.g. overlapping hands).
3. **Stay in scope** — Collection → extraction → training. Recommend changes in the right phase (e.g. temporal interpolation belongs in extraction, not collection).
4. **Be concise** — Use short bullets and tables; avoid long explanations unless the user asks.
5. **When editing code** — Preserve existing structure and comments; change only what is needed.
6. **Mention trade-offs** — If a change has costs (e.g. lower thresholds → more false positives), state them briefly.

---

## Problem

When collecting sign language video data with MediaPipe HandLandmarker, hand landmarks disappear or fail under certain conditions:

1. **Hand overlap** — When one hand occludes another, the occluded hand’s landmarks disappear. The model cannot see the hidden hand.
2. **Fast motion** — When hands move quickly, tracking drops between frames because of motion blur or large displacement.
3. **Partial visibility** — Hands at edges or partially out of frame are often not detected or lose tracking.

## Current Mitigations (Collection Phase)

- **Lower thresholds**: `min_hand_detection_confidence=0.4`, `min_tracking_confidence=0.3` to keep detections longer.
- **VIDEO mode**: Use `RunningMode.VIDEO` with timestamps for temporal tracking instead of frame-independent IMAGE mode.
- **UI hints**: "Keep both hands in frame, facing camera", "Sign at moderate speed, avoid overlapping hands".
- **Retake suggestion**: After recording, if >25% of frames had 0 hands or >50% had 0–1 hands, suggest discarding and re-recording.

## Possible Solutions

### Collection

| Approach | Description |
|----------|-------------|
| Protocol | Instruct signers to sign at moderate speed, keep hands slightly apart when both visible, and retake clips where tracking is weak. |
| Camera | Use a higher FPS camera and good lighting to reduce blur and improve temporal sampling. |
| Resolution | Ensure sufficient resolution so hands are clearly visible. |

### Extraction (Post-Processing)

| Approach | Description |
|----------|-------------|
| Temporal interpolation | When landmarks are missing for 1–10 frames, interpolate from neighboring frames (linear or spline). |
| Multi-model fusion | Run MediaPipe Hands and another model (e.g. MediaPipe Holistic, MMPose) and merge or fallback on low-confidence frames. |
| Confidence filtering | Drop or down-weight frames below a confidence threshold instead of using bad landmarks. |

### Training

| Approach | Description |
|----------|-------------|
| Frame masking / dropout | Randomly mask or drop frames during training so the model learns to handle missing landmarks. |
| Noisy input | Add noise or jitter to landmark inputs for robustness. |

### Fundamental Limits

- **Occlusion**: Overlapping hands are inherently invisible; there is no way to recover landmarks from hidden hands.
- **Model capacity**: MediaPipe HandLandmarker has fixed performance; improvements come from protocol, extraction, and training robustness.
