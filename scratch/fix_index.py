with open('web/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
'''<option value="frontier_digital">processed/digital_divide_broadband_schools_nuts3.csv [Frontiera 4: Banda Ultra-Larga 1 Gbps]</option>
                    <option value="frontier_legal">processed/comparative_legal_timeline_uk_vs_italy.csv [Frontiera 5: Database Giuridico Comparato]</option>
                    <option value="curriculum_comp">processed/curriculum_subjects_tripartite_vs_comprehensive_panel.csv [Confronto Materie e Ore UK vs IT]</option>
                    <option value="full_raw_catalog">Tutto il catalogo local_data (492 Dataset Grezzi / All 492 Raw Datasets)</option>''',
'''<option value="frontier_digital">processed/digital_divide_broadband_schools_nuts3.csv [Frontiera 4: Banda Ultra-Larga 1 Gbps]</option>
                    <option value="frontier_legal">processed/comparative_legal_timeline_uk_vs_italy.csv [Frontiera 5: Database Giuridico Comparato]</option>
                    <option value="curriculum_comp">processed/curriculum_subjects_tripartite_vs_comprehensive_panel.csv [Confronto Materie e Ore UK vs IT]</option>
                    <option value="catania_map">processed/catania_geospatial_schools_case_study.csv [Mappa Case Study Catania]</option>
                    <option value="national_map">processed/italy_national_schools_geospatial_sample.csv [Mappa Nazionale Scuole]</option>
                    <option value="full_raw_catalog">Tutto il catalogo local_data (492 Dataset Grezzi / All 492 Raw Datasets)</option>'''
)

text = text.replace(
'''} else if(v==='curriculum_comp') {
        url = "https://raw.githubusercontent.com/Eugenix94/Italienation/main/local_data/processed/curriculum_subjects_tripartite_vs_comprehensive_panel.csv";
        desc = "Confronto Curricolare Materie e Ore / UK Comprehensive vs IT Tripartite Subjects & Hours";
    } else if(v==='full_raw_catalog') {''',
'''} else if(v==='curriculum_comp') {
        url = "https://raw.githubusercontent.com/Eugenix94/Italienation/main/local_data/processed/curriculum_subjects_tripartite_vs_comprehensive_panel.csv";
        desc = "Confronto Curricolare Materie e Ore / UK Comprehensive vs IT Tripartite Subjects & Hours";
    } else if(v==='catania_map') {
        url = "https://raw.githubusercontent.com/Eugenix94/Italienation/main/local_data/processed/catania_geospatial_schools_case_study.csv";
        desc = "Coordinate GIS Catania / Catania Geospatial Case Study";
    } else if(v==='national_map') {
        url = "https://raw.githubusercontent.com/Eugenix94/Italienation/main/local_data/processed/italy_national_schools_geospatial_sample.csv";
        desc = "Campione GIS Nazionale / National Geospatial Sample";
    } else if(v==='full_raw_catalog') {'''
)

text = text.replace(
'''{id:'16',f:'16_institutional_expansion_and_comparative_synthesis',tI:'16. Sintesi dei nuovi dati istituzionali e normativi',tE:'16. Institutional expansion and comparative synthesis'},
{id:'17',f:'17_curricular_fragmentation_and_cultural_capital_synthesis',tI:'17. Frammentazione curricolare e capitale umano',tE:'17. Curricular fragmentation and human capital'}
];''',
'''{id:'16',f:'16_institutional_expansion_and_comparative_synthesis',tI:'16. Sintesi dei nuovi dati istituzionali e normativi',tE:'16. Institutional expansion and comparative synthesis'},
{id:'17',f:'17_curricular_fragmentation_and_cultural_capital_synthesis',tI:'17. Frammentazione curricolare e capitale umano',tE:'17. Curricular fragmentation and human capital'},
{id:'18',f:'18_geospatial_catania_case_study_and_national_map',tI:'18. Mappa Geospaziale e Catania Case Study',tE:'18. Geospatial Map & Catania Case Study'}
];'''
)

text = text.replace('''<div class="text-[10px] text-red-400 font-bold uppercase"><span class="i18n" data-it="Costo Libri 1° Anno Superiori" data-en="Year 1 Upper Secondary Textbook Cost"></span></div>
                <select class="w-full bg-zinc-900 text-white text-[10px] p-1.5 rounded border border-zinc-700 mb-2">
                    <option value="frontier_digital">processed/digital_divide_broadband_schools_nuts3.csv [Frontiera 4: Banda Ultra-Larga 1 Gbps]</option>
                    <option value="frontier_legal">processed/comparative_legal_timeline_uk_vs_italy.csv [Frontiera 5: Database Giuridico Comparato]</option>
                    <option value="curriculum_comp">processed/curriculum_subjects_tripartite_vs_comprehensive_panel.csv [Confronto Materie e Ore UK vs IT]</option>
                    <option value="catania_map">processed/catania_geospatial_schools_case_study.csv [Mappa Case Study Catania]</option>
                    <option value="national_map">processed/italy_national_schools_geospatial_sample.csv [Mappa Nazionale Scuole]</option>
                    <option value="full_raw_catalog">Tutto il catalogo local_data (492 Dataset Grezzi / All 492 Raw Datasets)</option>
                    <option value="full_proc_catalog">Tutto il catalogo processed_data (206 Pannelli / All 206 Processed Panels)</option>
                </select>
                <div class="flex items-baseline justify-between pt-1">''',
'''<div class="text-[10px] text-red-400 font-bold uppercase"><span class="i18n" data-it="Costo Libri 1° Anno Superiori" data-en="Year 1 Upper Secondary Textbook Cost"></span></div>
                <div class="flex items-baseline justify-between pt-1">''')

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done fixing!')
