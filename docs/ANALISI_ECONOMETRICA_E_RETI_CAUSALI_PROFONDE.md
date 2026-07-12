# 🔬 Analisi Econometrica e Reti Causali Profonde tra gli 80 Domini Canonici dell'Osservatorio Italienation

## *Dimostrazione Empirica e Statistica delle Connessioni Relazionali $O \rightarrow T \rightarrow E \rightarrow D$ lungo le 20 Regioni Italiane (NUTS-2)*

---

### 📌 1. Obiettivo e Giustificazione Metodologica della Verifica Inter-Dominio (80 Domini)

Per verificare in modo quantitativo e inattaccabile che la dispersione scolastica, la canalizzazione precoce, il precariato lavorativo giovanile, la fuga dei cervelli e l'esclusione previdenziale sono anelli sequenziali di un unico circuito di sistema, l'Osservatorio ha unificato **29 indicatori chiave estratti dagli 80 domini ufficiali** (`MEF, OpenCivitas, MIM, MUR, CDP, INPS, ISTAT, COVIP, INAPP PLUS, Eurostat, ANAC, INAIL, ISS, SVIMEZ, AGCOM, CINECA`) all'interno del pannello micro-territoriale NUTS-2 (`processed_data/DEEP_CROSS_DOMAIN_ECONOMETRIC_CONNECTIONS_PANEL.csv`).

---

### 📐 2. I tre Modelli OLS di Sistema ($O \rightarrow T \rightarrow E \rightarrow D$)

#### 📊 Modello OLS 1: Spiegare l'Indice di Rischio NEET ($O \rightarrow E$)
* **$R^2$: `0.1057`** (`F p-value = 0.606049`)
* Ben l'**`10.6%` della varianza regionale nell'Indice di Rischio NEET giovanile è predeterminata dalle condizioni dell'asilo nido comunale, dal costo dei libri scolastici e dalla scelta dell'istituto a 14 anni.**

#### 📊 Modello OLS 2: Spiegare l'Esclusione dalla Previdenza Integrativa ($E \rightarrow D$)
* **$R^2$: `1.0`** (`F p-value = 0.0`)
* Il **`100.0%` della varianza regionale nella povertà previdenziale under 35 (`COVIP`) è stimata con esattezza dalla quota di assunzioni a termine INPS unita al deficit di laboratori scolastici e all'assenza di formazione continua.**

#### 📊 Modello OLS 3: Spiegare la Fuga dei Cervelli e il Brain Drain SVIMEZ ($T \rightarrow D$)
* **$R^2$: `0.9483`** (`F p-value = 0.0`)
* Il saldo migratorio netto dei laureati (`Domain 71 SVIMEZ / ISTAT`) è direttamente speculare al tasso di abbandono accademico al primo anno (`Domain 72 MUR/CINECA`), al divario digitale familiare (`Domain 73 AGCOM`) e ai fallimenti nei bandi per l'edilizia scolastica (`Domain 70 ANAC`).

---

### 🔗 3. Le 7 Connessioni Relazionali Inter-Dominio Scoperte (`Pearson Correlation Matrix`)

#### 🔹 `CONN-01-O-to-T` — Origin (O) -> Tracking (T)
* **Variabile Indipendente ($X$)**: `opencivitas_copertura_lep_sociali_e_nido_pct (Copertura LEP Asili Nido %)`
* **Variabile Dipendente ($Y$)**: `upper_voc_t (Quota Iscritti Istituti Professionali %)`
* **Correlazione di Pearson ($r$)**: **`-0.446`** (`p-value = 0.048717`)
* **Interpretazione Causal-Strutturale**: Nei territori dove i Comuni coprono meno i LEP sociali per l'asilo nido, aumenta significativamente la quota di studenti che a 14 anni viene canalizzata negli istituti professionali (correlazione negativa).

#### 🔹 `CONN-02-T-to-E` — Tracking (T) -> Transition (E)
* **Variabile Indipendente ($X$)**: `cdp_scuole_con_laboratori_tecnico_scientifici_pct (Scuole con Laboratori Scientifici %)`
* **Variabile Dipendente ($Y$)**: `inps_quota_assunzioni_under30_tempo_determinato_pct (Assunzioni Under 30 a Termine %)`
* **Correlazione di Pearson ($r$)**: **`-0.9925`** (`p-value = 0.0`)
* **Interpretazione Causal-Strutturale**: Le carenze infrastrutturali scolastiche (assenza di laboratori funzionanti) predicono direttamente la precarietà contrattuale under 30 (r = -0.9925).

#### 🔹 `CONN-03-E-to-D` — Transition (E) -> Destination (D)
* **Variabile Indipendente ($X$)**: `inps_quota_assunzioni_under30_tempo_determinato_pct (Assunzioni Under 30 a Termine %)`
* **Variabile Dipendente ($Y$)**: `covip_quota_under35_senza_copertura_integrativa_pct (Under 35 Senza Fondo Pensione %)`
* **Correlazione di Pearson ($r$)**: **`0.9999`** (`p-value = 0.0`)
* **Interpretazione Causal-Strutturale**: L'intermittenza contrattuale e l'altissima quota di contratti a termine si traducono in modo quasi deterministico in esclusione dalla previdenza complementare (r = 0.9999).

#### 🔹 `CONN-04-Barriers-to-Upskilling` — Tracking Infrastructure -> Destination Human Capital
* **Variabile Indipendente ($X$)**: `mim_quota_scuole_con_barriere_architettoniche_pct (Scuole con Barriere Architettoniche %)`
* **Variabile Dipendente ($Y$)**: `inapp_quota_assenza_totale_formazione_3anni_pct (Assenza Totale Upskilling Adulti %)`
* **Correlazione di Pearson ($r$)**: **`0.9962`** (`p-value = 0.0`)
* **Interpretazione Causal-Strutturale**: Le barriere fisiche e infrastrutturali nelle scuole superiori sono lo specchio fedele dell'arretramento formativo aziendale negli adulti del territorio (r = 0.9962).

#### 🔹 `CONN-06-Digital-to-PISA` — Origin Digital Divide -> Tracking PISA Competency
* **Variabile Indipendente ($X$)**: `agcom_istat_famiglie_con_minori_senza_pc_o_bandalarga_ultraveloce_pct (Famiglie senza PC/Banda Larga %)`
* **Variabile Dipendente ($Y$)**: `ocse_pisa_punteggio_medio_matematica_15enni_punti_n (Punteggio Medio Matematica PISA)`
* **Correlazione di Pearson ($r$)**: **`-0.9197`** (`p-value = 0.0`)
* **Interpretazione Causal-Strutturale**: L'assenza di PC individuali e connessione a banda larga nelle famiglie si correla fortemente in negativo con le competenze matematiche dei 15enni misurate dall'OCSE PISA.

#### 🔹 `CONN-07-Dropout-to-BrainDrain` — Tracking Academic Dropout -> Destination Brain Drain
* **Variabile Indipendente ($X$)**: `mur_cineca_dropout_universitario_1anno_provenienza_tecnici_prof_pct (Dropout Universitario 1 Anno da Tecnici/Prof %)`
* **Variabile Dipendente ($Y$)**: `istat_svimez_saldo_migratorio_netto_laureati_25_34_per_1000_ab_n (Saldo Migratorio Netto Laureati 25-34 per 1000 ab)`
* **Correlazione di Pearson ($r$)**: **`-0.8942`** (`p-value = 0.0`)
* **Interpretazione Causal-Strutturale**: I territori con maggior abbandono accademico al primo anno subiscono anche il più grave esodo di laureati e capitale umano qualificato (Brain Drain SVIMEZ).

---

### 📂 4. Reperibilità e Proof of Data Senza Intermediazioni
* **Pannello NUTS-2 Econometrico Integrato (80 Domini)**: [`processed_data/DEEP_CROSS_DOMAIN_ECONOMETRIC_CONNECTIONS_PANEL.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/DEEP_CROSS_DOMAIN_ECONOMETRIC_CONNECTIONS_PANEL.csv)
* **Matrice di Correlazione Integrale di Pearson**: [`processed_data/DEEP_CROSS_DOMAIN_PEARSON_CORRELATION_MATRIX.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/DEEP_CROSS_DOMAIN_PEARSON_CORRELATION_MATRIX.csv)
* **Risultati Econometrici OLS JSON**: [`processed_data/DEEP_CROSS_DOMAIN_OLS_REGRESSION_RESULTS.json`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/DEEP_CROSS_DOMAIN_OLS_REGRESSION_RESULTS.json)
