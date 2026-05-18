# Beeper Patterns

The beeper uses simple on/off timing, so each pattern is distinguished by count,
duration, and cadence rather than pitch.

| Scenario | Pattern | Automatic use |
| --- | --- | --- |
| Acknowledge | One very short tap | Reserved for future local button or UI acknowledgement |
| Startup OK | Short, then longer tap | On boot after status LEDs start |
| Valve activity | Two quick equal taps | Reserved for future valve transition feedback |
| Sensor fault | Four fast taps | Any moisture sensor is missing, NaN, too low, or too high |
| Wi-Fi problem | Three medium taps | Wi-Fi signal has no state after startup, checked every 10 seconds |
| Dry warning | Two slower medium-long taps | Moisture is dry but not yet critical |
| Critical dry | Long, short, long | Moisture is below the critical threshold |

Preview buttons are exposed as web/API entities named:

```text
Beeper Preview - Acknowledge (single short tap)
Beeper Preview - Startup OK (short then long)
Beeper Preview - Valve Activity (two quick taps)
Beeper Preview - Sensor Fault (four fast taps)
Beeper Preview - WiFi Problem (three medium taps)
Beeper Preview - Dry Warning (two slow taps)
Beeper Preview - Critical Dry (long short long)
```

Preview buttons intentionally play the pattern directly. Automatic recurring
alerts respect `Beeper - Enabled` and `Beeper - Night Mute`.
