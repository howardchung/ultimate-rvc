"""
Module which defines functions and other definitions that facilitate
RVC-based TTS generation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pathlib import Path

import anyio

from ultimate_rvc.common import lazy_import
from ultimate_rvc.core.common import (
    OUTPUT_AUDIO_DIR,
    TTS_AUDIO_BASE_DIR,
    copy_file_safe,
    display_progress,
    json_dump,
)
from ultimate_rvc.core.exceptions import Entity, NotProvidedError, UIMessage
from ultimate_rvc.core.generate.common import (
    convert,
    get_unique_base_path,
    mix_audio,
    validate_exists,
)
from ultimate_rvc.core.generate.typing_extra import EdgeTTSAudioMetaData, MixedAudioType
from ultimate_rvc.typing_extra import (
    AudioExt,
    EmbedderModel,
    F0Method,
    RVCContentType,
    StrPath,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    import gradio as gr

    import edge_tts

else:
    edge_tts = lazy_import("edge_tts")


async def run_edge_tts(
    source: str,
    voice: str = "en-US-ChristopherNeural",
    pitch_shift: int = 0,
    speed_change: int = 0,
    volume_change: int = 0,
    progress_bar: gr.Progress | None = None,
    percentage: float = 0.5,
) -> Path:
    """
    Convert text to speech using edge TTS.

    Parameters
    ----------
    source : str
        A string or path to a file containing the text to be converted.

    voice : str, default="en-US-ChristopherNeural"
        The short name of the Edge TTS voice which should speak the
        provided text.

    pitch_shift : int, default=0
        The number of hertz to shift the pitch of the Edge TTS voice
        speaking the provided text.

    speed_change : int, default=0
        The absolute change to the speed of the Edge TTS voice speaking
        the provided text.

    volume_change : int, default=0
        The absolute change to the volume of the Edge TTS voice speaking
        the provided text.

    progress_bar : gr.Progress, optional
        Gradio progress bar to update.
    percentage : float, default=0.5
        Percentage to display in the progress bar.

    Returns
    -------
    Path
        The path to an audio track containing the spoken text.

    Raises
    ------
    NotProvidedError
        If no source is provided.

    """
    if not source:
        raise NotProvidedError(entity=Entity.SOURCE, ui_msg=UIMessage.NO_TTS_SOURCE)

    source_path = Path(source)
    source_is_file = source_path.is_file()
    if source_is_file:
        async with await anyio.open_file(source_path, "r", encoding="utf-8") as file:
            text = await file.read()
    else:
        text = source

    args_dict = EdgeTTSAudioMetaData(
        text=text,
        voice=voice,
        pitch_shift=pitch_shift,
        speed_change=speed_change,
        volume_change=volume_change,
    ).model_dump()
    TTS_AUDIO_BASE_DIR.mkdir(parents=True, exist_ok=True)
    paths = [
        get_unique_base_path(
            TTS_AUDIO_BASE_DIR,
            "1_EdgeTTS_Audio",
            args_dict,
        ).with_suffix(suffix)
        for suffix in [".wav", ".json"]
    ]

    converted_audio_path, converted_audio_json_path = paths

    if not all(path.exists() for path in paths):
        display_progress(
            "[~] Converting text using Edge TTS...",
            percentage,
            progress_bar,
        )

        pitch_shift_str = f"{pitch_shift:+}Hz"
        speed_change_str = f"{speed_change:+}%"
        volume_change_str = f"{volume_change:+}%"

        communicate = edge_tts.Communicate(
            text,
            voice,
            pitch=pitch_shift_str,
            rate=speed_change_str,
            volume=volume_change_str,
        )

        await communicate.save(str(converted_audio_path))

        json_dump(args_dict, converted_audio_json_path)

    return converted_audio_path


def run_pipeline(
    source: str,
    model_name: str,
    tts_voice: str = "en-US-ChristopherNeural",
    tts_pitch_shift: int = 0,
    tts_speed_change: int = 0,
    tts_volume_change: int = 0,
    n_octaves: int = 0,
    n_semitones: int = 0,
    f0_methods: Sequence[F0Method] | None = None,
    index_rate: float = 0.5,
    filter_radius: int = 3,
    rms_mix_rate: float = 0.25,
    protect_rate: float = 0.33,
    hop_length: int = 128,
    split_speech: bool = False,
    autotune_voice: bool = False,
    autotune_strength: float = 1,
    clean_voice: bool = False,
    clean_strength: float = 0.7,
    embedder_model: EmbedderModel = EmbedderModel.CONTENTVEC,
    embedder_model_custom: StrPath | None = None,
    sid: int = 0,
    output_gain: int = 0,
    output_sr: int = 44100,
    output_format: AudioExt = AudioExt.MP3,
    output_name: str | None = None,
    progress_bar: gr.Progress | None = None,
) -> tuple[Path, ...]:
    """
    Convert text to speech using a cascaded pipeline combining Edge TTS
    and RVC.

    The text is first converted to speech using Edge TTS, and then that
    speech is converted to a different voice using RVC.

    Parameters
    ----------
    source : str
        A string or path to a file containing the text to be converted
        to speech.

    model_name : str
        The name of the model to use for voice conversion.

    tts_voice : str, default="en-US-ChristopherNeural"
        The short name of the Edge TTS voice to use for text-to-speech
        conversion.

    tts_pitch_shift : int, default=0
        The number of hertz to shift the pitch of the speech generated
        by Edge TTS.

    tts_speed_change : int, default=0
        The absolute change to the speed of the speech generated by
        Edge TTS.

    tts_volume_change : int, default=0
        The absolute change to the volume of the speech generated by
        Edge TTS.

    n_octaves : int, default=0
        The number of octaves to shift the pitch of the voice converted
        using RVC.

    n_semitones : int, default=0
        The number of semitones to shift the pitch of the voice
        converted using RVC.

    f0_methods : list[F0Method], optional
        The methods to use for pitch extraction during RVC.

    index_rate : float, default=0.5
        The influence of the index file used during RVC.

    filter_radius : int, default=3
        The filter radius used during RVC.

    rms_mix_rate : float, default=0.25
        The blending rate of the volume envelope of the voice converted
        using RVC.

    protect_rate : float, default=0.33
        The protection rate for consonants and breathing sounds used
        during RVC.

    hop_length : int, default=128
        The hop length for CREPE-based pitch extraction used during RVC.

    split_speech : bool, default=False
        Whether to split the Edge TTS speech into smaller segments
        before converting it using RVC.

    autotune_voice : bool, default=False
        Whether to autotune the voice converted using RVC.

    autotune_strength : float, default=1
        The strength of the autotune applied to the converted voice.

    clean_voice : bool, default=False
        Whether to clean the voice converted using RVC.

    clean_strength : float, default=0.7
        The intensity of the cleaning applied to the converted voice.

    embedder_model : EmbedderModel, default=EmbedderModel.CONTENTVEC
        The model to use for generating speaker embeddings during RVC.

    embedder_model_custom : str | Path, optional
        The path to a custom model to use for generating speaker
        embeddings during RVC.

    sid : int, default=0
        The id of the speaker to use for multi-speaker RVC models.

    output_gain: int, default=0
        The gain to apply to the mixed audio track containing the
        converted voice.

    output_sr : int, default=44100
        The sample rate of the mixed audio track containing the
        converted voice.

    output_format : AudioExt, default=AudioExt.MP3
        The format of the mixed audio track containing the converted
        voice.

    output_name : str, optional
        The name of the mixed audio track containing the converted voice.

    progress_bar : gr.Progress, optional
        Gradio progress bar to update.

    Returns
    -------
    tuple[Path, ...]
        The path to a mixed audio track containing the converted voice
        and the paths to any intermediate audio tracks that were
        generated along the way.

    """
    validate_exists(model_name, Entity.MODEL_NAME)
    display_progress("[~] Starting RVC TTS pipeline...", 0, progress_bar)
    speech_track = anyio.run(
        run_edge_tts,
        source,
        tts_voice,
        tts_pitch_shift,
        tts_speed_change,
        tts_volume_change,
        progress_bar,
        0.0,
    )
    converted_voice_track = convert(
        audio_track=speech_track,
        directory=TTS_AUDIO_BASE_DIR,
        model_name=model_name,
        n_octaves=n_octaves,
        n_semitones=n_semitones,
        f0_methods=f0_methods,
        index_rate=index_rate,
        filter_radius=filter_radius,
        rms_mix_rate=rms_mix_rate,
        protect_rate=protect_rate,
        hop_length=hop_length,
        split_audio=split_speech,
        autotune_audio=autotune_voice,
        autotune_strength=autotune_strength,
        clean_audio=clean_voice,
        clean_strength=clean_strength,
        embedder_model=embedder_model,
        embedder_model_custom=embedder_model_custom,
        sid=sid,
        content_type=RVCContentType.VOICE,
        progress_bar=progress_bar,
        percentage=0.33,
    )

    mixed_voice_track = mix_audio(
        audio_track_gain_pairs=[(converted_voice_track, output_gain)],
        directory=TTS_AUDIO_BASE_DIR,
        output_sr=output_sr,
        output_format=output_format,
        content_type=MixedAudioType.VOICE,
        progress_bar=progress_bar,
        percentage=0.66,
    )

    if output_name is None:
        source_path = Path(source)
        song_name = source_path.stem if source_path.is_file() else "Text"
        output_name = f"{song_name} (Spoken by {model_name})"

    audio_path = OUTPUT_AUDIO_DIR / f"{output_name}.{output_format}"
    output_audio_track = copy_file_safe(mixed_voice_track, audio_path)

    return output_audio_track, speech_track, converted_voice_track