import React, { useState, useEffect, useMemo } from 'react';
import oedData from '../assets/oed_international_migration_calculator.json';
import { T } from './T';

const PROFILE_ICONS = {
  dropout: '🚫',
  vocational: '🔧',
  technical: '⚙️',
  academic: '🎓',
};

const MetricRing = ({ value, maxValue = 1, label, sublabel, color, format = 'pct', prevValue }) => {
  const displayVal = format === 'pct' ? `${(value * 100).toFixed(0)}%` : format === 'eur' ? `€${value?.toLocaleString()}` : value;
  const fraction = format === 'pct' ? value : format === 'index' ? value / 10 : Math.min(value / 4000, 1);
  const delta = prevValue != null ? value - prevValue : null;

  return (
    <div className="flex flex-col items-center text-center">
      <div className="relative w-28 h-28 mb-3">
        <svg viewBox="0 0 120 120" className="w-full h-full">
          <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
          <circle cx="60" cy="60" r="52" fill="none" stroke={color} strokeWidth="8"
            strokeDasharray={`${fraction * 327} 327`}
            strokeLinecap="round"
            style={{ transform: 'rotate(-90deg)', transformOrigin: 'center', transition: 'stroke-dasharray 0.8s ease-out' }}
          />
        </svg>
        <span className="absolute inset-0 flex items-center justify-center text-xl font-bold text-white">{displayVal}</span>
      </div>
      <h4 className="text-sm font-bold text-white mb-0.5">{label}</h4>
      <p className="text-xs text-zinc-500">{sublabel}</p>
      {delta != null && (
        <span className={`mt-1 text-xs font-bold px-2 py-0.5 rounded-full ${delta < 0 ? 'bg-emerald-500/20 text-emerald-400' : delta > 0 ? 'bg-rose-500/20 text-rose-400' : 'bg-zinc-700 text-zinc-400'}`}>
          {format === 'pct' ? `${delta > 0 ? '+' : ''}${(delta * 100).toFixed(0)}pp` :
           format === 'eur' ? `${delta > 0 ? '+' : ''}€${delta.toLocaleString()}` :
           `${delta > 0 ? '+' : ''}${delta.toFixed(1)}`}
        </span>
      )}
    </div>
  );
};

const OEDSimulator = () => {
  const [originCountry, setOriginCountry] = useState('Italy');
  const [profile, setProfile] = useState('dropout');
  const [migrationEnabled, setMigrationEnabled] = useState(false);
  const [destCountry, setDestCountry] = useState('Sweden');

  const countries = Object.keys(oedData.countries);
  const originData = oedData.countries[originCountry];
  const originOutcomes = originData?.outcomes?.[profile];

  const migrationDestinations = useMemo(() => {
    const paths = oedData.migration_pathways?.[originCountry];
    return paths ? Object.keys(paths) : [];
  }, [originCountry]);

  useEffect(() => {
    if (migrationEnabled && !migrationDestinations.includes(destCountry)) {
      setDestCountry(migrationDestinations[0] || '');
    }
  }, [originCountry, migrationEnabled, migrationDestinations, destCountry]);

  const migrationData = migrationEnabled
    ? oedData.migration_pathways?.[originCountry]?.[destCountry]?.[profile]
    : null;

  if (!originOutcomes) return null;

  const neetVal = migrationData ? migrationData.new_prob_neet : originOutcomes.prob_neet;
  const tertiaryVal = migrationData ? migrationData.new_prob_tertiary_access : originOutcomes.prob_tertiary_access;
  const mobilityVal = migrationData ? migrationData.new_mobility_index : originOutcomes.social_mobility_index;
  const incomeVal = migrationData ? migrationData.new_expected_income_eur : originOutcomes.expected_monthly_income_eur;

  const neetColor = neetVal > 0.4 ? '#f43f5e' : neetVal > 0.2 ? '#f59e0b' : '#10b981';
  const tertiaryColor = tertiaryVal < 0.1 ? '#f43f5e' : tertiaryVal < 0.3 ? '#f59e0b' : '#10b981';
  const mobilityColor = mobilityVal < 4 ? '#f43f5e' : mobilityVal < 6 ? '#f59e0b' : '#10b981';

  return (
    <div className="bg-white/[0.02] border border-white/5 rounded-2xl p-6 md:p-8 space-y-8">

      {/* Step 1: Origin Country */}
      <div className="space-y-3">
        <label className="text-sm font-bold uppercase tracking-wider text-zinc-400">
          <T it="1. Paese di Origine (Educazione)" en="1. Origin Country (Education)" />
        </label>
        <div className="flex flex-wrap gap-2">
          {countries.map(c => (
            <button key={c}
              onClick={() => setOriginCountry(c)}
              className={`px-4 py-2.5 rounded-xl font-semibold text-sm transition-all ${originCountry === c ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/30' : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700'}`}
            >
              {oedData.countries[c].flag} {c}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap items-center gap-3 pt-2">
          <span className={`text-xs font-bold px-3 py-1 rounded-full ${originData.diploma_strictly_required_for_uni ? 'bg-rose-500/15 text-rose-400' : 'bg-emerald-500/15 text-emerald-400'}`}>
            {originData.diploma_strictly_required_for_uni ? '🔒 Diploma Required for University' : '🔓 Alternative Pathways Available'}
          </span>
          <span className="text-xs text-zinc-500">{originData.system_type}</span>
        </div>
      </div>

      {/* Step 2: Student Profile */}
      <div className="space-y-3">
        <label className="text-sm font-bold uppercase tracking-wider text-zinc-400">
          <T it="2. Profilo Studente" en="2. Student Profile" />
        </label>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {Object.entries(originData.outcomes).map(([key, val]) => (
            <button key={key}
              onClick={() => setProfile(key)}
              className={`flex flex-col items-center gap-1 p-4 rounded-xl transition-all ${profile === key ? 'bg-indigo-600/20 border-2 border-indigo-500 text-white' : 'bg-zinc-800/50 border-2 border-transparent text-zinc-400 hover:bg-zinc-700/50'}`}
            >
              <span className="text-2xl">{PROFILE_ICONS[key]}</span>
              <span className="text-xs font-bold text-center">{val.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Domestic Outcomes */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-white">
          {oedData.countries[originCountry].flag} <T it="Esiti nel Paese d'Origine" en="Domestic Outcomes" />
          {migrationEnabled && <span className="text-zinc-500 text-sm font-normal ml-2">(<T it="prima della migrazione" en="pre-migration" />)</span>}
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <MetricRing value={originOutcomes.prob_neet} label="NEET" sublabel="Risk %" color={migrationEnabled ? '#555' : neetColor} format="pct" />
          <MetricRing value={originOutcomes.prob_tertiary_access} label="University" sublabel="Access %" color={migrationEnabled ? '#555' : tertiaryColor} format="pct" />
          <MetricRing value={originOutcomes.social_mobility_index} label="Mobility" sublabel="Index (0-10)" color={migrationEnabled ? '#555' : mobilityColor} format="index" />
          <MetricRing value={originOutcomes.expected_monthly_income_eur} label="Income" sublabel="€/month" color={migrationEnabled ? '#555' : '#4f46e5'} format="eur" />
        </div>
      </div>

      {/* Step 3: Migration Toggle */}
      <div className="border-t border-zinc-800 pt-6 space-y-4">
        <div className="flex items-center justify-between">
          <label className="text-sm font-bold uppercase tracking-wider text-zinc-400">
            <T it="3. Migrazione Post-Educazione" en="3. Post-Education Migration" />
          </label>
          <button
            onClick={() => setMigrationEnabled(!migrationEnabled)}
            className={`relative w-14 h-7 rounded-full transition-all ${migrationEnabled ? 'bg-indigo-600' : 'bg-zinc-700'}`}
          >
            <span className={`absolute top-0.5 w-6 h-6 rounded-full bg-white shadow-md transition-all ${migrationEnabled ? 'left-7' : 'left-0.5'}`} />
          </button>
        </div>

        {migrationEnabled && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-300">
            <div className="space-y-2">
              <label className="text-xs text-zinc-500">
                <T it="Paese di destinazione (lavoro / università)" en="Destination country (work / university)" />
              </label>
              <div className="flex flex-wrap gap-2">
                {migrationDestinations.map(c => (
                  <button key={c}
                    onClick={() => setDestCountry(c)}
                    className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all ${destCountry === c ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-500/30' : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700'}`}
                  >
                    {oedData.countries[c]?.flag} {c}
                  </button>
                ))}
              </div>
            </div>

            {migrationData && (
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <h3 className="text-lg font-bold text-white">
                    {oedData.countries[originCountry].flag} → {oedData.countries[destCountry]?.flag} <T it="Esiti Post-Migrazione" en="Post-Migration Outcomes" />
                  </h3>
                  <span className="text-xs bg-indigo-500/15 text-indigo-400 font-bold px-3 py-1 rounded-full">
                    {migrationData.pathway}
                  </span>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                  <MetricRing value={migrationData.new_prob_neet} prevValue={originOutcomes.prob_neet} label="NEET" sublabel="Risk %" color={neetColor} format="pct" />
                  <MetricRing value={migrationData.new_prob_tertiary_access} prevValue={originOutcomes.prob_tertiary_access} label="University" sublabel="Access %" color={tertiaryColor} format="pct" />
                  <MetricRing value={migrationData.new_mobility_index} prevValue={originOutcomes.social_mobility_index} label="Mobility" sublabel="Index (0-10)" color={mobilityColor} format="index" />
                  <MetricRing value={migrationData.new_expected_income_eur} prevValue={originOutcomes.expected_monthly_income_eur} label="Income" sublabel="€/month" color="#4f46e5" format="eur" />
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Key Features */}
      {originData.key_features && (
        <div className="border-t border-zinc-800 pt-6">
          <h4 className="text-sm font-bold uppercase tracking-wider text-zinc-400 mb-3">
            {oedData.countries[originCountry].flag} <T it="Caratteristiche del Sistema" en="System Features" />
          </h4>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {originData.key_features.map((f, i) => (
              <li key={i} className="text-sm text-zinc-400 flex items-start gap-2">
                <span className="text-indigo-400 mt-0.5">•</span>{f}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default OEDSimulator;
