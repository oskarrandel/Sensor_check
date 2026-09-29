import pandas as pd
import yaml

def main() -> None:
    """Run the pipeline: read config, join data, and export overdue sensors."""

    max_days, output_file = read_config("config.yml")
    sensors = read_join("sensors.xlsx", "calibrations.csv")
    filter_export(sensors, max_days, output_file)

def read_config(configuration_file: str) -> tuple[int, str]:
    """Read config file and return max_days_since_calibration and output_file."""
    with open(configuration_file) as f:
        config = yaml.safe_load(f)

    return config["max_days_since_calibration"], config["output_file"]

def read_join(sensor_file: str, calibration_file:str) -> pd.DataFrame:
    sensor = pd.read_excel(sensor_file)
    calibration = pd.read_csv(calibration_file)

    return sensor.merge(calibration, on="sensor_id")

def filter_export(sensors: pd.DataFrame, max_days: int, output_file: str) -> None:
  """Filter sensors exceeding max_days_since_calibration and export to JSON."""
  
  overdue_sensors = sensors[sensors["days_since_calibration"] > max_days]

  # Convert the DataFrame to a list of records (dicts)
  data_to_export = overdue_sensors.to_dict(orient="records")

  # Write as formatted JSON array with indent=2
  with open(output_file, "w") as f:
    json.dump(data_to_export, f, indent=2)


if __name__ == "__main__":
  main()
