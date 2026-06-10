MOTORCYCLE_MODELS = {
    'R3 ABS 70th': '30176', 
    'FACTOR 150 UBS 2016 A 2024': '30093', 
    'FZ15 2023 A 2024': '30094', 
    'FAZER 250 2018 A 2024': '30095', 
    'CROSSER XTZ150 Z 2015 A 2024': '30097', 
    'CROSSER XTZ150 S 2015 A 2024': '30096', 
    'XMAX 2021 A 2024': '30098', 
    'NMAX CONNECTED 2023 A 2024': '30101', 
    'LANDER 250 2020 A 2024': '30105', 
    'FACTOR 125 i (UBS) 2017 A 2025': '30106', 
    'FAZER 150 UBS 2014 A 2025': '30107', 
    'FLUO ABS 2022 A 2025': '30108', 
    'NEO 125 2017 A 2024': '30115', 
    'MT03 ABS 2021 A 2025': '30121', 
    'NOVA NMAX CONNECTED 2025': '30127', 
    'XMAX CONNECTED 2025': '30123', 
    'LANDER 250 ABS CONNECTED 2025': '30126', 
    'CROSSER XTZ150 S 2025': '30125', 
    'CROSSER XTZ150 Z 2025': '30131', 
    'YZF-R3 ABS 2020 A 2025': '30109', 
    'FACTOR': '30129', 
    'NOVA FACTOR DX 2025': '30132', 
    'FLUO ABS HYBRID CONNECTED': '30171', 
    "NEO'S DUAL CONNECTED 2026": '30130', 
    'YZF R3 ABS CONNECTED 2026': '30140', 
    'NOVA MT-03 CONNECTED 2026': '30141', 
    'NOVA MT-07 CONNECTED 2026': '30142', 
    'NOVA XMAX 300 CONNECTED': '30147', 
    'TÉNÉRÉ 700': '30143', 
    'AEROX ABS CONNECTED': '30164', 
    'FAZER FZ15 ABS CONNECTED 2025 A 2026': '30160', 
    'R15 ABS 2024 A 2026': '30163', 
    'FZ25 CONNECTED DE 2025 A 2026': '30161', 
    'LANDER CONNECTED 2025 a 2026': '30167', 
    'NOVA NMAX ABS CONNECTED': '30168', 
    'FAZER FZ25 CONNECTED': '30173', 
    'YAMAHA ZR HYBRID CONNECTED': '30175', 
    'Nova Factor 2025 a 2026': '30174', 
    'NOVA FACTOR DX 2025 a 2026': '30172', 
    'CROSSER 150 Z ABS 2025 a 2026': '30170', 
    'CROSSER 150 S ABS 2025 a 2026': '30169'
}

_TRUTHY_VALUES = { '1', 's', 'sim', 't', 'true', 'v', 'verdade', 'verdadeiro', 'y', 'yes' }

def get_parameter(parameter, default=None):
    return default if parameter is None else str(parameter).strip().lower()

def get_cache_parameter(parameter, default=False):
    return get_parameter(parameter, default) in _TRUTHY_VALUES