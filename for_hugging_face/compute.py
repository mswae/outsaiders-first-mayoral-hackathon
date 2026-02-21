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
                
        # ---------- public API ----------
        def compute_pai(self, participants_by_group=None):
            # absolute counts
            spi_a_abs = self.target_population - self.num_participants
            spi_b_abs = self.target_population - spi_a_abs - self.feedback_volume
            peg_abs = self.num_participants - self.feedback_volume

            # ----- required PAI components -----
            pcr = self.num_participants / self.target_population
            spi_a = spi_a_abs / self.target_population
            spi_b = spi_b_abs / self.target_population
            spa = self.w_pos - self.w_neg
            peg = peg_abs / self.target_population
            
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

            return sorted_components