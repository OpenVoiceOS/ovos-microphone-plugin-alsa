## Description

This plugin captures audio from an ALSA device for OpenVoiceOS (OVOS). It
implements the `Microphone` interface from
[ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager) and
registers under the `opm.microphone` entry point as
`ovos-microphone-plugin-alsa`.

## Install

```bash
pip install ovos-microphone-plugin-alsa
```

## Configuration

Add this block to your `mycroft.conf`, or merge it with your existing
`listener` section.

```python
"listener": {
    "microphone": {
        "module": "ovos-microphone-plugin-alsa",
        "device": "pulse",                  # name/alias of the device; default = "default"
        "period_size": 1024,                # frames per period; default = 1024
        "timeout": 5.0,                     # blocks x seconds and raises the Empty exception if no item was available within that time; default = 5.0
        "multiplier": 1.0,                  # Increase/decrease loudness of audio; default = 1.0
        "audio_retries": 0,                 # Number of times to retry listening; default = 0
        "audio_retry_delay": 0.0            # Seconds to wait between retries; default = 0.0
    }
}
```

## Related projects

- [ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager) defines the `Microphone` template this plugin implements.
- [ovos-dinkum-listener](https://github.com/OpenVoiceOS/ovos-dinkum-listener) is the OVOS listener service that loads microphone plugins.

## License

Apache License 2.0. See [LICENSE](LICENSE).
