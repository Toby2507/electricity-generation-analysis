import re

import pandas as pd


class NewFormatExtractor:
    '''
    Extracts data from the markdown text of the new format of the electricity generation data.
    Attributes:
        grid_markdown (str): The markdown text for the grid data to extract from.
        plant_markdown (str): The markdown text for the plant data to extract from.
        source_id (str): The source ID of the data.
        reporting_month (str): The reporting month of the data. Format: YYYY-MM
    '''

    # Initialization and public interface

    def __init__(self, source_id, reporting_month, grid_markdown=None, plant_markdown=None):
        self.source_id = source_id
        self.reporting_month = reporting_month
        self.grid_markdown = grid_markdown
        self.plant_markdown = plant_markdown
        self.unmatched_lines = set()

    def extract(self):
        '''
        Extracts data from the markdown text of the new format of the electricity generation data.
        Returns:
            tuple: A tuple containing two pandas DataFrames:
                - grid_df: A DataFrame containing the extracted grid data.
                - plant_df: A DataFrame containing the extracted plant data.
        '''
        grid_df = self._extract_grid_data()
        plant_df = self._extract_plant_data()

        return grid_df, plant_df

    # Data extraction

    def _extract_grid_data(self) -> pd.DataFrame:
        if (self.grid_markdown is None):
            return None

        data = {}

        volt_pattern = r'average lower grid voltage \((?P<lower_voltage>\d+\.\d+kV)\) and average upper grid voltage \((?P<upper_voltage>\d+\.\d+kV)\)'
        freq_pattern = r'average lower grid frequency \((?P<lower_frequency>\d+\.\d+Hz)\) and average upper grid frequency \((?P<upper_frequency>\d+\.\d+Hz)\)'

        for line in self.grid_markdown.splitlines():
            volt_match = re.search(volt_pattern, line)
            freq_match = re.search(freq_pattern, line)
            if volt_match:
                data = {**data, **volt_match.groupdict()}
            elif freq_match:
                data = {**data, **freq_match.groupdict()}

        return pd.DataFrame([{
            'source_id': self.source_id,
            'reporting_month': self.reporting_month,
            **data
        }])

    def _extract_plant_data(self) -> pd.DataFrame:
        if (self.plant_markdown is None):
            return None

        top_10_line_indicator = r'^Largest Energy Producers'
        top_10_pattern = (
            r'(?P<availability_factor>\d+%)\s*\('
            r'(?P<available_capacity>\d+)/'
            r'(?P<installed_capacity>\d+MW)\)\s+'
            r'(?P<plant_name>\S+)\s+'
            r'(?P<load_factor>\d+%)\s+\('
            r'(?P<average_generation>\d+MWh/h)\)'
        )
        other_plant_pattern = (
            r'\|(?P<plant_name>[^|]*)\|'
            r'(?P<installed_capacity>[\d,]+)\|'
            r'(?P<available_capacity>[\d,]+)\|'
            r'(?P<availability_factor>[^|]+)\|'
            r'(?P<average_generation>[\d,]+)\|'
            r'(?P<load_factor>[^|]+)\|'
        )

        rows = []

        for line_number, line in enumerate(self.plant_markdown.splitlines()):
            top_10_line = re.search(top_10_line_indicator, line)
            other_plant_line = re.search(other_plant_pattern, line)
            if top_10_line:
                top_10_plants = line.split('<br>')
                for top_10_plant in top_10_plants:
                    line_match = re.search(top_10_pattern, top_10_plant)
                    if line_match:
                        rows.append({
                            'source_id': self.source_id,
                            'line_number': line_number,
                            'reporting_month': self.reporting_month,
                            **line_match.groupdict()
                        })
            elif other_plant_line:
                rows.append({
                    'source_id': self.source_id,
                    'line_number': line_number,
                    'reporting_month': self.reporting_month,
                    **other_plant_line.groupdict()
                })
            else:
                self.unmatched_lines.add(line_number)

        return pd.DataFrame(rows)
