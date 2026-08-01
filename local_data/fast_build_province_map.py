import pandas as pd
import json
import os

# Comprehensive coordinate map for Italian provinces
PROVINCE_COORDS = {
    "AGRIGENTO": (37.3111, 13.5765), "ALESSANDRIA": (44.9123, 8.6148), "ANCONA": (43.6158, 13.5189),
    "AOSTA": (45.7370, 7.3197), "AREZZO": (43.4633, 11.8797), "ASCOLI PICENO": (42.8546, 13.5755),
    "ASTI": (44.9004, 8.2069), "AVELLINO": (40.9146, 14.7909), "BARI": (41.1171, 16.8719),
    "BARLETTA-ANDRIA-TRANI": (41.2294, 16.2906), "BELLUNO": (46.1388, 12.2166), "BENEVENTO": (41.1297, 14.7816),
    "BERGAMO": (45.6983, 9.6773), "BIELLA": (45.5630, 8.0583), "BOLOGNA": (44.4949, 11.3426),
    "BOLZANO": (46.4983, 11.3548), "BRESCIA": (45.5416, 10.2118), "BRINDISI": (40.6322, 17.9417),
    "CAGLIARI": (39.2238, 9.1217), "CALTANISSETTA": (37.4922, 14.0620), "CAMPOBASSO": (41.5604, 14.6598),
    "CASERTA": (41.0821, 14.3333), "CATANIA": (37.5079, 15.0830), "CATANZZARO": (38.9098, 16.5877),
    "CATANZARO": (38.9098, 16.5877), "CHIETI": (42.3510, 14.1675), "COMO": (45.8081, 9.0852),
    "COSENZA": (39.2983, 16.2537), "CREMONA": (45.1333, 10.0333), "CROTONE": (39.0807, 17.1272),
    "CUNEO": (44.3844, 7.5427), "ENNA": (37.5670, 14.2794), "FERMO": (43.1611, 13.7183),
    "FERRARA": (44.8381, 11.6198), "FIRENZE": (43.7696, 11.2558), "FOGGIA": (41.4622, 15.5447),
    "FORLI'-CESENA": (44.2227, 12.0407), "FROSINONE": (41.6402, 13.3514), "GENOVA": (44.4056, 8.9463),
    "GORIZIA": (45.9402, 13.6223), "GROSSETO": (42.7603, 11.1135), "IMPERIA": (43.8860, 8.0270),
    "ISERNIA": (41.5960, 14.2361), "L'AQUILA": (42.3498, 13.3995), "LA SPEZIA": (44.1025, 9.8241),
    "LATINA": (41.4676, 12.9037), "LECCE": (40.3515, 18.1750), "LECCO": (45.8566, 9.3925),
    "LIVORNO": (43.5485, 10.3106), "LODI": (45.3139, 9.5032), "LUCCA": (43.8429, 10.5027),
    "MACERATA": (43.3003, 13.4533), "MANTOVA": (45.1564, 10.7914), "MASSA-CARRARA": (44.0375, 10.1423),
    "MATERA": (40.6664, 16.6044), "MESSINA": (38.1938, 15.5540), "MILANO": (45.4642, 9.1900),
    "MODENA": (44.6471, 10.9252), "MONZA E DELLA BRIANZA": (45.5845, 9.2744), "NAPOLI": (40.8518, 14.2681),
    "NOVARA": (45.4469, 8.6213), "NUORO": (40.3209, 9.3285), "ORISTANO": (39.9059, 8.5912),
    "PADOVA": (45.4064, 11.8768), "PALERMO": (38.1157, 13.3615), "PARMA": (44.8015, 10.3279),
    "PAVIA": (45.1847, 9.1582), "PERUGIA": (43.1107, 12.3908), "PESARO E URBINO": (43.9102, 12.9133),
    "PESCARA": (42.4647, 14.2142), "PIACENZA": (45.0526, 9.6930), "PISA": (43.7228, 10.4017),
    "PISTOIA": (43.9333, 10.9167), "PORDENONE": (45.9564, 12.6605), "POTENZA": (40.6404, 15.8056),
    "PRATO": (43.8777, 11.1022), "RAGUSA": (36.9269, 14.7255), "RAVENNA": (44.4184, 12.2035),
    "REGGIO DI CALABRIA": (38.1113, 15.6473), "REGGIO CALABRIA": (38.1113, 15.6473), "REGGIO NELL'EMILIA": (44.6983, 10.6307),
    "RIETI": (42.4042, 12.8628), "RIMINI": (44.0678, 12.5695), "ROMA": (41.9028, 12.4964),
    "ROVIGO": (45.0711, 11.7904), "SALERNO": (40.6824, 14.7681), "SASSARI": (40.7259, 8.5556),
    "SAVONA": (44.3069, 8.4808), "SIENA": (43.3188, 11.3308), "SIRACUSA": (37.0755, 15.2866),
    "SONDRIO": (46.1689, 9.8716), "SUD SARDEGNA": (39.1670, 8.5262), "TARANTO": (40.4760, 17.2308),
    "TERAMO": (42.6589, 13.7040), "TERNI": (42.5641, 12.6427), "TORINO": (45.0703, 7.6869),
    "TRAPANI": (38.0176, 12.5150), "TRENTO": (46.0748, 11.1217), "TREVISO": (45.6669, 12.2430),
    "TRIESTE": (45.6495, 13.7768), "UDINE": (46.0626, 13.2372), "VARESE": (45.8206, 8.8251),
    "VENEZIA": (45.4408, 12.3155), "VERBANIA": (45.9220, 8.5516), "VERBANO-CUSIO-OSSOLA": (45.9220, 8.5516),
    "VERCELLI": (45.3268, 8.4233), "VERONA": (45.4384, 10.9916), "VIBO VALENTIA": (38.6757, 16.1018),
    "VICENZA": (45.5455, 11.5356), "VITERBO": (42.4174, 12.1047)
}

def build_fast():
    input_file = os.path.join('local_data', 'processed', 'tripartite_territorial_deserts.csv')
    output_file = os.path.join('frontend', 'src', 'assets', 'province_school_counts.json')

    df = pd.read_csv(input_file)
    prov_stats = df.groupby('PROVINCIA')[['Liceo', 'Tecnico', 'Professionale', 'Is_Total_Desert']].sum().reset_index()

    results = []
    for _, row in prov_stats.iterrows():
        prov = str(row['PROVINCIA']).strip()
        lat, lng = PROVINCE_COORDS.get(prov, (41.8719, 12.5674)) # Default to Rome if unknown
        
        results.append({
            'id': prov,
            'name': prov.title(),
            'lat': lat,
            'lng': lng,
            'liceo_count': int(row['Liceo']),
            'tecnico_count': int(row['Tecnico']),
            'professionale_count': int(row['Professionale']),
            'total_deserts': int(row['Is_Total_Desert'])
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {len(results)} province records in {output_file}")

if __name__ == '__main__':
    build_fast()
