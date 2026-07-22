import re

with open('web/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_cards = """
        <!-- CARD 6: BLIND SPOTS (Span 6) -->
        <div class="md:col-span-6 glass p-6 rounded-3xl border border-cyan-500/30 space-y-4 hover:border-cyan-500/60 transition flex flex-col">
            <div class="flex items-center justify-between mb-2">
                <span class="px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 font-bold text-xs uppercase tracking-wider">Blind Spots</span>
                <span class="text-xs text-zinc-500 font-mono">Future Research</span>
            </div>
            <h3 class="text-xl font-black text-white leading-tight"><span class="i18n" data-it="I Punti Ciechi: Edilizia & Docenti" data-en="Blind Spots: Infrastructure & Teachers"></span></h3>
            <p class="text-zinc-300 text-sm leading-relaxed"><span class="i18n" data-it="Ispirandoci alle metodologie del MOOC 'What Future For Education?', stiamo integrando due domini critici finora inesplorati: <b>Edilizia Scolastica</b> (fatiscenza strutturale che deprime le performance) e <b>Personale Docente</b> (precarizzazione sistemica e distribuzione geografica iniqua). Questi fattori latenti completano la triangolazione del divario Nord-Sud." data-en="Inspired by the 'What Future For Education?' MOOC, we are integrating two critically unexplored domains: <b>School Infrastructure</b> (structural decay depressing performance) and <b>Teaching Staff</b> (systemic precariousness and inequitable geographic distribution). These latent factors complete the triangulation of the North-South divide."></span></p>
        </div>

        <!-- CARD 7: HUGGINGFACE DATA MIRROR (Span 6) -->
        <div class="md:col-span-6 glass p-6 rounded-3xl border border-orange-500/30 space-y-4 hover:border-orange-500/60 transition flex flex-col justify-between bg-gradient-to-br from-zinc-900/50 to-orange-950/20">
            <div class="space-y-4">
                <div class="flex items-center gap-2 mb-2">
                    <span class="px-3 py-1 rounded-full bg-orange-500/20 text-orange-300 font-bold text-xs uppercase tracking-wider">Data Mirror</span>
                </div>
                <h3 class="text-xl font-black text-white leading-tight"><span class="i18n" data-it="HuggingFace Open Dataset" data-en="HuggingFace Open Dataset"></span></h3>
                <p class="text-zinc-300 text-sm leading-relaxed"><span class="i18n" data-it="I link governativi diretti del MIM o dell'ISTAT soffrono spesso di errori 404 e inaccessibilità. Per garantire l'Open Science, abbiamo specchiato interamente i dati ministeriali su HuggingFace. Questo repository immutabile garantisce la riproducibilità totale di ogni statistica presentata nel Manifesto." data-en="Direct government links (MIM/ISTAT) frequently suffer from 404 errors and inaccessibility. To guarantee Open Science, we've entirely mirrored the ministerial data on HuggingFace. This immutable repository ensures total reproducibility for every statistic presented in the Manifesto."></span></p>
            </div>
            <a href="https://huggingface.co/datasets/diatribe00/italian-schools-opendata/tree/main/data" target="_blank" class="block w-full text-center py-3 rounded-xl bg-orange-600 hover:bg-orange-500 text-white font-black text-sm uppercase tracking-wider transition shadow-lg shadow-orange-900/20 mt-4">
                <span class="i18n" data-it="Esplora il Dataset su HuggingFace ↗" data-en="Explore Dataset on HuggingFace ↗"></span>
            </a>
        </div>
"""

# Insert right before the closing </div> of the bento box grid
# The grid ends with `    </div>\n</section>`
replacement = new_cards + "\n    </div>\n</section>"
text = text.replace("    </div>\n</section>", replacement)

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Blind Spots and HF Cards injected successfully.")
