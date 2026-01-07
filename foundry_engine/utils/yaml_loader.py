"""YAML loading and validation utilities for Foundry Engine."""

import logging
from pathlib import Path
from typing import Any, TypeVar

import yaml
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def load_yaml_file(file_path: Path) -> dict[str, Any]:
    """Load and parse a YAML file."""
    if not file_path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
            return data or {}
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML file {file_path}: {e}")
            raise


def load_and_validate_yaml(file_path: Path, model: type[T]) -> T:
    """Load a YAML file and validate it against a Pydantic model."""
    data = load_yaml_file(file_path)

    try:
        return model.model_validate(data)
    except ValidationError as e:
        logger.error(f"Validation error in {file_path}:")
        for error in e.errors():
            logger.error(f"  {error['loc']}: {error['msg']}")
        raise
