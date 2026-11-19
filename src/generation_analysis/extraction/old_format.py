import re

import pandas as pd


class OldFormatExtractor:
    '''
    Extracts data from the markdown text of the old format of the electricity generation data.

    Attributes:
        markdown (str): The markdown text to extract data from.
        source_id (str): The source ID of the data.
        reporting_month (str): The reporting month of the data. Format: YYYY-MM
    '''

    # Initialization and public interface

    def __init__(self, markdown, source_id, reporting_month):
        self.markdown = markdown
        self.source_id = source_id
        self.reporting_month = reporting_month
        self.unmatched_lines = set()

    def extract(self):
        '''
        Extracts data from the markdown text of the old format of the electricity generation data.
        Returns:
            tuple: A tuple containing two pandas DataFrames:
                - grid_df: A DataFrame containing the extracted grid data.
                - plant_df: A DataFrame containing the extracted plant data.
        '''
        grid_section = self._isolate_grid_section()
        plant_section = self._isolate_plant_section()

        grid_data = self._extract_grid_section(grid_section)
        plant_data = self._extract_plant_section(
            plant_section['top_10'], plant_section['other_plant'])

        return grid_data, plant_data

    # Section isolation and preprocessing

    def _isolate_grid_section(self) -> list[str]:
        grid_values = []

        grid_data_lines = self.markdown.splitlines()[3:9]
        for data_line in grid_data_lines:
            grid_data = data_line.split('|')[1:6]
            grid_values.append(grid_data[-1].strip())

        return grid_values

    def _isolate_plant_section(self) -> dict[str, list[str]]:
        watermark_pattern = r'100%<br>80<br>60<br>40<br>20<br><br>|40<br>60<br>80<br>100%<br>|0<br>0<br>|<br>'

        other_plant_data = []
        plant_data_lines = self.markdown.splitlines()[4:20]
        for data_line in plant_data_lines:
            cells = data_line.split('|')[6:12]
            other_plant_data.append('|'.join(cells))

        top_10_data = []
        top_10_lines = self.markdown.splitlines()[11:21]
        for data_line in top_10_lines:
            cells = data_line.split('|')[1:6]
            relevant_cells = [cells[0], cells[1],
                              f'{cells[3].strip()}{cells[4].lstrip()}']
            cleaned_cells = [re.sub(watermark_pattern, '', cell).strip()
                             for cell in relevant_cells]
            for i in range(len(cleaned_cells) - 1):
                if cleaned_cells[i].endswith('MW') and cleaned_cells[i + 1].startswith(')'):
                    cleaned_cells[i] += ')'
                    cleaned_cells[i + 1] = cleaned_cells[i + 1].lstrip()[1:]
            top_10_data.append('|'.join(cleaned_cells))

        return {'top_10': top_10_data, 'other_plant': other_plant_data}

    # Data extraction

    def _extract_grid_section(self, grid_values: list[str]) -> pd.DataFrame:
        data = {}

        freq_pattern = (
            r'(?P<upper_frequency>\d+\.*\d+Hz)\S+\>'
            r'(?P<lower_frequency>\d+\.*\d+Hz)'
        )
        volt_pattern = r'(?P<volt>\d+\.*\d+kV)\S+'

        for idx, value in enumerate(grid_values):
            if idx == 1:
                freq_match = re.search(freq_pattern, value)
                if freq_match:
                    data = {**data, **freq_match.groupdict()}
            elif idx in [3, 5]:
                volt_match = re.search(volt_pattern, value)
                if volt_match:
                    if idx == 5:
                        data['lower_voltage'] = volt_match.group('volt')
                    else:
                        data['upper_voltage'] = volt_match.group('volt')

        return pd.DataFrame([{
            'source_id': self.source_id,
            'reporting_month': self.reporting_month,
            **data
        }])

    def _extract_plant_section(self, top_10_data: list[str], other_plant_data: list[str]) -> pd.DataFrame:
        rows = []

        top_10_pattern = (
            r'(?P<availability_factor>\d+%)\s*\('
            r'(?P<available_capacity>\d+)/'
            r'(?P<installed_capacity>\d+MW)\)\s*\|'
            r'(?P<plant_name>[^|]*)\|'
            r'(?P<load_factor>\d+%)\s*\('
            r'(?P<total_generation>\d+GWh)\)'
        )
        for line_number, line in enumerate(top_10_data, start=11):
            line_match = re.search(top_10_pattern, line)
            if line_match:
                rows.append({
                    'source_id': self.source_id,
                    'line_number': line_number,
                    'reporting_month': self.reporting_month,
                    **line_match.groupdict()
                })
            else:
                self.unmatched_lines.add(line_number)

        other_plant_pattern = (
            r'(?P<plant_name>[^|]*)\|'
            r'(?P<installed_capacity>[^|]*)\|'
            r'(?P<available_capacity>[^|]*)\|'
            r'(?P<availability_factor>[^|]*)\|'
            r'(?P<total_generation>[^|]*)\|'
            r'(?P<load_factor>[^|]*)'
        )
        for line_number, line in enumerate(other_plant_data, start=4):
            line_match = re.search(other_plant_pattern, line)
            split_rows = []
            if line_match:
                for key, val in line_match.groupdict().items():
                    val_split = list(
                        filter(lambda x: bool(x.strip()), val.split('<br>')))
                    for idx, value in enumerate(val_split):
                        clean_value = re.sub(r'<[^>]*>', '', value.strip())
                        if idx >= len(split_rows):
                            split_rows.append({
                                'source_id': self.source_id,
                                'line_number': line_number,
                                'reporting_month': self.reporting_month,
                                key: clean_value
                            })
                        else:
                            split_rows[idx][key] = clean_value
                rows.extend(split_rows)
            else:
                self.unmatched_lines.add(line_number)

        return pd.DataFrame(rows)
