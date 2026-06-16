"""Tests for the ALSA microphone plugin.

These tests do not open a real ALSA capture device, so they are safe to run
on CI runners without a sound card. Instantiating ``AlsaMicrophone`` only
configures the dataclass; capture is started lazily by ``start()`` (which we
never call here).
"""
import inspect

from ovos_plugin_manager.templates.microphone import Microphone

from ovos_microphone_plugin_alsa import AlsaMicrophone


def test_subclasses_microphone_template():
    assert issubclass(AlsaMicrophone, Microphone)


def test_registered_entrypoint_class():
    # the opm.microphone entrypoint points at this class
    mic = AlsaMicrophone()
    assert isinstance(mic, Microphone)


def test_microphone_interface_methods():
    for name in ("start", "stop", "read_chunk"):
        assert callable(getattr(AlsaMicrophone, name)), f"missing method {name}"


def test_inherited_template_properties():
    mic = AlsaMicrophone()
    # properties provided by the Microphone template
    assert isinstance(type(mic).frames_per_chunk, property)
    assert isinstance(type(mic).seconds_per_chunk, property)
    assert mic.sample_rate == 16000
    assert mic.sample_width == 2
    assert mic.sample_channels == 1
    # derived values must be consistent with the configured chunk size
    assert mic.frames_per_chunk == mic.chunk_size // (
        mic.sample_width * mic.sample_channels
    )
    assert mic.seconds_per_chunk == mic.frames_per_chunk / mic.sample_rate


def test_alsa_specific_defaults():
    mic = AlsaMicrophone()
    assert mic.device == "default"
    assert mic.period_size == 1024
    assert mic.multiplier == 1.0
    # capture thread is not started until start() is called
    assert mic._thread is None
    assert mic._is_running is False


def test_read_chunk_requires_running():
    mic = AlsaMicrophone()
    # reading before start() must fail rather than touch hardware
    sig = inspect.signature(AlsaMicrophone.read_chunk)
    assert "self" in sig.parameters
    try:
        mic.read_chunk()
    except AssertionError as err:
        assert "Not running" in str(err)
    else:
        raise AssertionError("read_chunk should refuse when not running")
