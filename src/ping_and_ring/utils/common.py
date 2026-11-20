import json
import sys
from pathlib import Path

import pandas as pd
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations

from ping_and_ring.utils.exception import CustomException
from ping_and_ring.utils.logger import get_logger


class CommonUtils:
    def __init__(self):
        self.logger = get_logger(name="utils.common")

    @ensure_annotations
    def read_file(self, file_path: Path) -> ConfigBox | pd.DataFrame:
        """
        Read a JSON, YAML, or CSV file.

        Args:
            file_path: path to the input file

        Raises:
            ValueError: if the file format is unsupported or the file is empty
            CustomException: if there is an error reading or parsing the file

        Returns:
            ConfigBox for JSON/YAML mappings or a DataFrame for CSV rows
        """
        file_path = Path(file_path)
        file_type = file_path.suffix.lower()
        if file_type not in {".json", ".yaml", ".yml", ".csv"}:
            raise ValueError(f"Unsupported file format '{file_path.suffix}'. Expected .json, .yaml, .yml, or .csv.")

        try:
            if file_type == ".csv":
                content = pd.read_csv(file_path)
                if content.empty:
                    raise ValueError(f"{file_path.name} is empty")
                return content

            with file_path.open(encoding="utf-8", newline="") as input_file:
                if file_type == ".json":
                    content = json.load(input_file)
                else:
                    content = yaml.safe_load(input_file)

                if content is None or content == []:
                    raise ValueError(f"{file_path.name} is empty")

                return ConfigBox(content)

        except BoxValueError:
            raise ValueError(f"{file_path.name} is empty") from None
        except ValueError:
            raise
        except Exception as e:
            self.logger.error(f"Error reading file: {file_path}")
            raise CustomException(e, sys) from e
