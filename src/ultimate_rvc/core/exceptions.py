"""
Module which defines custom exception and enumerations used when
instiating and re-raising those exceptions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from enum import StrEnum

if TYPE_CHECKING:
    from ultimate_rvc.typing_extra import StrPath


class Entity(StrEnum):
    """Enumeration of entities that can be provided."""

    # General entities
    FILE = "file"
    FILES = "files"
    DIRECTORY = "directory"
    DIRECTORIES = "directories"

    # Model entities
    MODEL_NAME = "model name"
    MODEL_NAMES = "model names"
    VOICE_MODEL = "voice model"
    TRAINING_MODEL = "training model"
    CUSTOM_EMBEDDER_MODEL = "custom embedder model"
    CUSTOM_GENERATOR = "custom pretrained generator"
    CUSTOM_DISCRIMINATOR = "custom pretrained discriminator"
    MODEL_FILE = "model file"
    MODEL_BIN_FILE = "pytorch_model.bin file"
    CONFIG_JSON_FILE = "config.json file"

    # Audio entities
    AUDIO_TRACK = "audio track"
    AUDIO_TRACK_GAIN_PAIRS = "pairs of audio track and gain"
    VOICE_TRACK = "voice track"
    SPEECH_TRACK = "speech track"
    VOCALS_TRACK = "vocals track"
    SONG_DIR = "song directory"
    DATASET = "dataset"
    DATASETS = "datasets"
    DATASET_NAME = "dataset name"

    # Source entitiess
    SOURCE = "source"
    URL = "URL"


AudioFileEntity = Literal[
    Entity.AUDIO_TRACK,
    Entity.VOICE_TRACK,
    Entity.SPEECH_TRACK,
    Entity.VOCALS_TRACK,
    Entity.FILE,
]

AudioDirectoryEntity = Literal[Entity.SONG_DIR, Entity.DATASET, Entity.DIRECTORY]

ModelEntity = Literal[
    Entity.VOICE_MODEL,
    Entity.TRAINING_MODEL,
    Entity.CUSTOM_EMBEDDER_MODEL,
    Entity.CUSTOM_DISCRIMINATOR,
    Entity.CUSTOM_GENERATOR,
]


class Location(StrEnum):
    """Enumeration of locations where entities can be found."""

    # Audio locations
    INTERMEDIATE_AUDIO_ROOT = "the root of the intermediate audio base directory"
    SPEECH_AUDIO_ROOT = "the root of the speech audio directory"
    TRAINING_AUDIO_ROOT = "the root of the training audio directory"
    OUTPUT_AUDIO_ROOT = "the root of the output audio directory"

    # Model locations
    EXTRACTED_ZIP_FILE = "extracted zip file"


class UIMessage(StrEnum):
    """
    Enumeration of messages that can be displayed in the UI
    in place of core exception messages.
    """

    # General messages
    NO_UPLOADED_FILES = "No files selected."

    # Audio messages
    NO_AUDIO_TRACK = "No audio tracks provided."
    NO_SPEECH_AUDIO_FILES = (
        "No files selected. Please select one or more speech audio files to delete."
    )
    NO_OUTPUT_AUDIO_FILES = (
        "No files selected. Please select one or more output audio files to delete."
    )
    NO_SONG_DIR = "No song directory selected."
    NO_SONG_DIRS = (
        "No song directories selected. Please select one or more song directories"
        " containing intermediate audio files to delete."
    )
    NO_DATASETS = (
        "No datasets selected. Please select one or more datasets containing audio"
        " files to delete."
    )

    # Model messages
    NO_VOICE_MODEL = "No voice model selected."
    NO_VOICE_MODELS = "No voice models selected."
    NO_TRAINING_MODELS = "No training models selected."
    NO_CUSTOM_EMBEDDER_MODEL = "No custom embedder model selected."
    NO_CUSTOM_EMBEDDER_MODELS = "No custom embedder models selected."
    NO_CUSTOM_DISCRIMINATOR = "No custom pretrained discriminator selected."
    NO_CUSTOM_DISCRIMINATORS = "No custom pretrained discriminators selected."
    NO_CUSTOM_GENERATOR = "No custom pretrained generator selected."
    NO_CUSTOM_GENERATORS = "No custom pretrained generators selected."

    # Source messages
    NO_AUDIO_SOURCE = (
        "No source provided. Please provide a valid Youtube URL, local audio file"
        " or song directory."
    )
    NO_TEXT_SOURCE = (
        "No source provided. Please provide a valid text string or path to a text file."
    )


class NotProvidedError(ValueError):
    """Raised when an entity is not provided."""

    def __init__(self, entity: Entity, ui_msg: UIMessage | None = None) -> None:
        """
        Initialize a NotProvidedError instance.

        Exception message will be formatted as:

        "No `<entity>` provided."

        Parameters
        ----------
        entity : Entity
            The entity that was not provided.
        ui_msg : UIMessage, default=None
            Message which, if provided, is displayed in the UI
            instead of the default exception message.

        """
        super().__init__(f"No {entity} provided.")
        self.ui_msg = ui_msg


class NotFoundError(OSError):
    """Raised when an entity is not found."""

    def __init__(
        self,
        entity: Entity,
        location: StrPath | Location,
        is_path: bool = True,
    ) -> None:
        """
        Initialize a NotFoundError instance.

        Exception message will be formatted as:

        "`<entity>` not found `(`in `|` at:`)` `<location>`."

        Parameters
        ----------
        entity : Entity
            The entity that was not found.
        location : StrPath | Location
            The location where the entity was not found.
        is_path : bool, default=True
            Whether the location is a path to the entity.

        """
        proposition = "at:" if is_path else "in"
        entity_cap = entity.capitalize() if not entity.isupper() else entity
        super().__init__(
            f"{entity_cap} not found {proposition} {location}",
        )


class ModelNotFoundError(OSError):
    """Raised when an model with a given name is not found."""

    def __init__(self, entity: ModelEntity, name: str) -> None:
        r"""
        Initialize a ModelNotFoundError instance.

        Exception message will be formatted as:

        '`<entity>` with name "`<name>`" not found.'

        Parameters
        ----------
        entity : str
            The model entity that was not found.
        name : str
            The name of the model that was not found.

        """
        super().__init__(f"{entity.capitalize()} with name '{name}' not found.")


class PreprocessedAudioNotFoundError(OSError):
    """
    Raised when no preprocessed dataset audio files are associated
    with a model.
    """

    def __init__(self, name: str) -> None:
        r"""
        Initialize a PreprocessedAudioNotFoundError instance.

        Exception message will be formatted as:

        'No preprocessed dataset audio files associated with the model
        with name "`<name>`".'

        Parameters
        ----------
        name : str
            The name of the model with no associated preprocessed
            dataset audio files.

        """
        super().__init__(
            "No preprocessed dataset audio files associated with the model with name"
            f" '{name}'.",
        )


class DatasetFileListNotFoundError(OSError):
    """Raised when no dataset file list is associated with a model."""

    def __init__(self, name: str) -> None:
        r"""
        Initialize a DatasetFileListNotFoundError instance.

        Exception message will be formatted as:

        'No dataset file list associated with the model with name
        "`<name>`".'

        Parameters
        ----------
        name : str
            The name of the model with no associated dataset file list.

        """
        super().__init__(
            f"No dataset file list associated with the model with name '{name}'.",
        )


class ModelExistsError(OSError):
    """Raised when a model already exists."""

    def __init__(self, entity: ModelEntity, name: str) -> None:
        r"""
        Initialize a ModelExistsError instance.

        Exception message will be formatted as:

        '`<entity>` with name "`<name>`" already exists. Please provide
        a different name for your {entity}.'

        Parameters
        ----------
        entity : str
            The model entity that already exists.
        name : str
            The name of the model that already exists.

        """
        super().__init__(
            f"{entity.capitalize()} with name '{name}' already exists. Please provide a"
            f" different name for your {entity}.",
        )


class InvalidLocationError(OSError):
    """Raised when an entity is in a wrong location."""

    def __init__(self, entity: Entity, location: Location, path: StrPath) -> None:
        r"""
        Initialize an InvalidLocationError instance.

        Exception message will be formatted as:

        "`<entity>` should be located in `<location>` but found at:
        `<path>`"

        Parameters
        ----------
        entity : Entity
            The entity that is in a wrong location.
        location : Location
            The correct location for the entity.
        path : StrPath
            The path to the entity.

        """
        entity_cap = entity.capitalize() if not entity.isupper() else entity
        super().__init__(
            f"{entity_cap} should be located in {location} but found at: {path}",
        )


class HttpUrlError(OSError):
    """Raised when a HTTP-based URL is invalid."""

    def __init__(self, url: str) -> None:
        """
        Initialize a HttpUrlError instance.

        Exception message will be formatted as:

        "Invalid HTTP-based URL: `<url>`"

        Parameters
        ----------
        url : str
            The invalid HTTP-based URL.

        """
        super().__init__(
            f"Invalid HTTP-based URL: {url}",
        )


class YoutubeUrlError(OSError):
    """
    Raised when an URL does not point to a YouTube video or
    , potentially, a Youtube playlist.
    """

    def __init__(self, url: str, playlist: bool) -> None:
        """
        Initialize a YoutubeURlError instance.

        Exception message will be formatted as:

        "URL does not point to a YouTube video `[`or playlist`]`:
         `<url>`"

        Parameters
        ----------
        url : str
            The URL that does not point to a YouTube video or playlist.
        playlist : bool
            Whether the URL might point to a YouTube playlist.

        """
        suffix = "or playlist" if playlist else ""
        super().__init__(
            f"Not able to access Youtube video {suffix} at: {url}",
        )


class UploadLimitError(ValueError):
    """Raised when the upload limit for an entity is exceeded."""

    def __init__(self, entity: Entity, limit: str | float) -> None:
        """
        Initialize an UploadLimitError instance.

        Exception message will be formatted as:

        "At most `<limit>` `<entity>` can be uploaded."

        Parameters
        ----------
        entity : Entity
            The entity for which the upload limit was exceeded.
        limit : str
            The upload limit.

        """
        super().__init__(f"At most {limit} {entity} can be uploaded.")


class UploadTypeError(ValueError):
    """
    Raised when one or more uploaded entities have an invalid
    type.
    """

    def __init__(
        self,
        entity: Entity,
        valid_types: list[str],
        type_class: Literal["formats", "names"],
        multiple: bool,
    ) -> None:
        """
        Initialize an UploadTypeError instance.

        Exception message will be formatted as:

        "Only `<entity>` with the following `<type_class>` can be
        uploaded `(`by themselves | together`)`: `<types>`."

        Parameters
        ----------
        entity : Entity
            The entity with an invalid type that was uploaded.
        valid_types : list[str]
            The valid types for the entity that was uploaded.
        type_class : Literal["formats", "names"]
            The name for the class of valid types.
        multiple : bool
            Whether multiple instances of the entity were uploaded.

        """
        suffix = "by themselves" if not multiple else "together (at most one of each)"
        super().__init__(
            f"Only {entity} with the following {type_class} can be uploaded {suffix}:"
            f" {', '.join(valid_types)}.",
        )


class InvalidAudioFormatError(ValueError):
    """Raised when an audio file has an invalid format."""

    def __init__(self, path: StrPath, formats: list[str]) -> None:
        """
        Initialize an InvalidAudioFormatError instance.

        Exception message will be formatted as:

        "Invalid audio file format: `<path>`. Supported formats are:
        `<formats>`."

        Parameters
        ----------
        path : StrPath
            The path to the audio file with an invalid format.
        formats : list[str]
            Supported audio formats.

        """
        super().__init__(
            f"Invalid audio file format: {path}. Supported formats are:"
            f" {', '.join(formats)}.",
        )
