(async function buildCatalogs() {
    const container = document.getElementById('catalogs-container');
    if (!container) return;

    container.innerHTML = '<div class="text-center text-zinc-500 py-8">Loading Transparent Data Hub...</div>';

    async function fetchCatalog(url) {
        try {
            const res = await fetch(url);
            if(!res.ok) return [];
            return await res.json();
        } catch(e) {
            console.error(e);
            return [];
        }
    }

    const [raw, processed] = await Promise.all([
        fetchCatalog('catalog_raw.json'),
        fetchCatalog('catalog_processed.json')
    ]);

    function getOfficialLink(institution) {
        if (!institution) return { url: "https://dati.gov.it", label: "🏛️ Dati.gov.it" };
        const lower = institution.toLowerCase();
        if (lower.includes("istat")) return { url: "http://dati.istat.it/", label: "🏛️ Portale ISTAT" };
        if (lower.includes("ministero dell'istruzione") || lower.includes("mim")) return { url: "https://dati.istruzione.it/", label: "🏫 Dati MIM" };
        if (lower.includes("mur") || lower.includes("università")) return { url: "https://dati.mur.gov.it/", label: "🎓 Dati MUR" };
        if (lower.includes("eurostat")) return { url: "https://ec.europa.eu/eurostat/data/database", label: "🇪🇺 Eurostat Database" };
        if (lower.includes("oecd") || lower.includes("ocse")) return { url: "https://data.oecd.org/", label: "🌐 OECD Data" };
        if (lower.includes("world bank") || lower.includes("banca mondiale")) return { url: "https://data.worldbank.org/", label: "🌐 World Bank" };
        if (lower.includes("openpolis")) return { url: "https://www.openpolis.it/", label: "📊 Openpolis" };
        if (lower.includes("anpal")) return { url: "https://www.anpal.gov.it/dati-e-pubblicazioni", label: "💼 Dati ANPAL" };
        return { url: "https://dati.gov.it", label: "🏛️ Fonte Ufficiale" };
    }

    function createTableHTML(title, desc, data, badgeColor) {
        if(data.length === 0) return '';
        
        let rows = data.map(item => {
            const official = getOfficialLink(item.institution || item.category);
            return `
            <tr class="hover:bg-zinc-800/80 transition text-sm">
                <td class="px-4 py-3 border-b border-zinc-800 text-zinc-300 font-medium">${item.name}</td>
                <td class="px-4 py-3 border-b border-zinc-800 text-zinc-500 hidden sm:table-cell">${item.institution || item.category}</td>
                <td class="px-4 py-3 border-b border-zinc-800 text-right flex items-center justify-end gap-2">
                    <a href="${official.url}" target="_blank" rel="noopener" class="inline-flex items-center gap-1 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-md text-xs font-bold transition shadow-sm">
                        ${official.label} ↗
                    </a>
                    <a href="${item.source}" target="_blank" rel="noopener" title="Scarica CSV" class="inline-flex items-center justify-center w-8 h-8 bg-zinc-800 hover:bg-zinc-700 text-zinc-400 hover:text-white rounded-md transition border border-zinc-700">
                        ⬇️
                    </a>
                </td>
            </tr>
        `}).join('');

        return `
            <div class="bg-zinc-900/40 rounded-2xl border border-zinc-800 overflow-hidden mb-8">
                <div class="p-6 border-b border-zinc-800 bg-zinc-900/80">
                    <div class="flex items-center gap-3 mb-2">
                        <span class="px-2.5 py-1 rounded bg-${badgeColor}-500/20 text-${badgeColor}-400 text-[10px] font-black uppercase tracking-wider">${data.length} DATASETS</span>
                        <h3 class="text-xl font-bold text-white">${title}</h3>
                    </div>
                    <p class="text-sm text-zinc-400">${desc}</p>
                </div>
                <div class="overflow-x-auto max-h-[400px] overflow-y-auto">
                    <table class="w-full text-left border-collapse">
                        <thead class="sticky top-0 bg-zinc-900 text-xs text-zinc-500 uppercase font-bold tracking-wider">
                            <tr>
                                <th class="px-4 py-3 border-b border-zinc-800">Dataset Name</th>
                                <th class="px-4 py-3 border-b border-zinc-800 hidden sm:table-cell">Source / Institution</th>
                                <th class="px-4 py-3 border-b border-zinc-800 text-right">Access</th>
                            </tr>
                        </thead>
                        <tbody>${rows}</tbody>
                    </table>
                </div>
            </div>
        `;
    }

    const html = []
    if(raw.length > 0) {
        html.push(createTableHTML(
            "Raw Data Catalog", 
            "I dataset originali, non alterati, estratti da ISTAT, Ministero dell'Istruzione, Eurostat e OCSE. La base fondante della nostra ricerca.",
            raw,
            "blue"
        ));
    }
    
    if(processed.length > 0) {
        html.push(createTableHTML(
            "Processed Data Catalog", 
            "Tabelle e panel ripuliti, uniti e pronti per il machine learning. Rappresentano il lavoro di sintesi del progetto Italienation.",
            processed,
            "emerald"
        ));
    }

    if(html.length > 0) {
        container.innerHTML = html.join('');
    } else {
        container.innerHTML = '<div class="text-center text-zinc-500 py-8 border border-red-500/20 bg-red-500/5 rounded-xl">Error loading data catalogs. Run scripts/rebuild_catalogs_with_direct_links.py</div>';
    }
})();
