import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class ParticipationAdoptionIndex:
    
    def __init__ (
            self,
            num_participants, 
            target_population,
            feedback_volume,
            w_pos,
            w_neg
    ):

        self.num_participants = num_participants
        self.target_population = target_population
        self.feedback_volume = feedback_volume
        self.w_pos = w_pos
        self.w_neg = w_neg

        self.components = {}

        # pcr, pci, spi_a, spi_b, spa, peg = 0.0

        # ---------- helper functions ---------- 
        
        def _compute_pci(self, participants_by_group):
            total = sum(participants_by_group.values())
            if total == 0:
                return 0.0

            shares = [
                count / total
                for count in participants_by_group.values()
            ]

            return sum(s ** 2 for s in shares)

        def _normalize_components(self, components):
            total = sum(abs(v) for v in components.values())

            if total == 0:
                return {k: 0.0 for k in components}

            return {
                k: v / total
                for k, v in components.items()
            }
        
        def _sort_components(self):
            return dict(
                sorted(
                    self.components.items(),
                    key=lambda item: abs(item[1]),
                    reverse=True
                )
            )
        
        # def _apply_threshold(self, components, threshold):
        #     if threshold is None:
        #         return components
            
        #     filtered_components = {} # dictionary of filtered components

        #     for component_name, value in components.items():
        #         if abs(value) >= threshold:
        #             filtered_components[component_name] = value

        #     return filtered_components
        
        # ---------- public API ----------

        def compute_pai(self, participants_by_group=None, threshold=0.2):
            # absolute counts
            spi_a_abs = target_population - num_participants
            spi_b_abs = target_population - spi_a_abs - feedback_volume
            peg_abs = num_participants - feedback_volume

            # ----- required PAI components -----
            pcr = num_participants / target_population
            spi_a = spi_a_abs / target_population
            spi_b = spi_b_abs / target_population
            spa = w_pos - w_neg
            peg = peg_abs / target_population
            
            if participants_by_group is not None:
                if not isinstance(participants_by_group, dict):
                    raise TypeError("participants_by_group must be a dict")
                else:
                    pci = self._compute_pci(participants_by_group)
            else:
                pci = None

            self.components = {
                "PCR": {"value": pcr, "description": "Participation Ratio"},
                "PCI": {"value": pci, "description": "Participation Concentration"},
                "SPI-A": {"value": spi_a, "description": "Silent Non-Adoption"},
                "SPI-B": {"value": spi_b, "description": "Silent Adoption"},
                "SPA": {"value": spa, "description": "Sentiment Asymmetry"},
                "PEG": {"value": peg, "description": "Participation-to-Expression Gap"}
            }

            self._normalize_components()

            sorted_components = self._sort_components()

            # filtered = self._apply_threshold(organized, threshold)

            return sorted_components