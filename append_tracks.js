const fs = require('fs');

const file = 'frontend/public/data/tripartite_curriculum.json';
const data = JSON.parse(fs.readFileSync(file, 'utf8'));

const newTracks = [
  {
    "id": "liceo_coreutico",
    "macroTrackId": "liceo",
    "name": {
      "it": "Liceo Coreutico",
      "en": "Dance and Choreography Lyceum"
    },
    "description": {
      "it": "Formazione accademica focalizzata sulle arti performative, danza e coreografia.",
      "en": "Academic training focused on performing arts, dance, and choreography."
    },
    "weeklyHours": 32,
    "textbookCost": 320,
    "fslHours": 90,
    "implicitDropout": "3%",
    "universityEnrollment": "82%",
    "curriculum": [
      { "subject": { "it": "Letteratura", "en": "Literature" }, "hours": 4 },
      { "subject": { "it": "Storia della Danza", "en": "History of Dance" }, "hours": 3 },
      { "subject": { "it": "Tecnica della Danza", "en": "Dance Technique" }, "hours": 8 },
      { "subject": { "it": "Matematica", "en": "Mathematics" }, "hours": 2 }
    ],
    "demographics": {
      "it": "Estrazione sociale medio-alta, forte prevalenza femminile.",
      "en": "Upper-middle social extraction, strong female prevalence."
    }
  },
  {
    "id": "liceo_scienze_applicate",
    "macroTrackId": "liceo",
    "name": {
      "it": "Scienze Applicate",
      "en": "Applied Sciences"
    },
    "description": {
      "it": "Variante dello scientifico senza Latino, potenziata in informatica e laboratori.",
      "en": "Scientific variant without Latin, enhanced with computer science and labs."
    },
    "weeklyHours": 30,
    "textbookCost": 340,
    "fslHours": 90,
    "implicitDropout": "4%",
    "universityEnrollment": "85%",
    "curriculum": [
      { "subject": { "it": "Matematica", "en": "Mathematics" }, "hours": 5 },
      { "subject": { "it": "Informatica", "en": "Computer Science" }, "hours": 2 },
      { "subject": { "it": "Scienze", "en": "Sciences" }, "hours": 5 },
      { "subject": { "it": "Italiano", "en": "Italian" }, "hours": 4 }
    ],
    "demographics": {
      "it": "Ceto medio, prevalenza maschile, mobilità sociale dinamica.",
      "en": "Middle class, male prevalence, dynamic social mobility."
    }
  },
  {
    "id": "liceo_sportivo",
    "macroTrackId": "liceo",
    "name": {
      "it": "Liceo Sportivo",
      "en": "Sports Lyceum"
    },
    "description": {
      "it": "Focalizzato su discipline sportive, economia dello sport e diritto sportivo.",
      "en": "Focused on sports disciplines, sports economics, and sports law."
    },
    "weeklyHours": 30,
    "textbookCost": 310,
    "fslHours": 90,
    "implicitDropout": "5%",
    "universityEnrollment": "75%",
    "curriculum": [
      { "subject": { "it": "Discipline Sportive", "en": "Sports Disciplines" }, "hours": 6 },
      { "subject": { "it": "Diritto dello Sport", "en": "Sports Law" }, "hours": 3 },
      { "subject": { "it": "Matematica", "en": "Mathematics" }, "hours": 3 },
      { "subject": { "it": "Italiano", "en": "Italian" }, "hours": 4 }
    ],
    "demographics": {
      "it": "Estrazione trasversale, forte prevalenza maschile.",
      "en": "Transversal extraction, strong male prevalence."
    }
  },
  {
    "id": "tecnico_agrario",
    "macroTrackId": "tecnico",
    "name": {
      "it": "Istituto Tecnico Agrario",
      "en": "Agricultural Technical Institute"
    },
    "description": {
      "it": "Specializzazione in produzioni agricole, agroalimentare e gestione del territorio.",
      "en": "Specialization in agricultural production, agri-food, and land management."
    },
    "weeklyHours": 32,
    "textbookCost": 280,
    "fslHours": 150,
    "implicitDropout": "12%",
    "universityEnrollment": "30%",
    "curriculum": [
      { "subject": { "it": "Agronomia", "en": "Agronomy" }, "hours": 4 },
      { "subject": { "it": "Scienze Naturali", "en": "Natural Sciences" }, "hours": 4 },
      { "subject": { "it": "Laboratorio", "en": "Laboratory" }, "hours": 6 },
      { "subject": { "it": "Matematica", "en": "Mathematics" }, "hours": 3 }
    ],
    "demographics": {
      "it": "Forte radicamento territoriale provinciale, estrazione medio-bassa.",
      "en": "Strong provincial territorial rooting, lower-middle extraction."
    }
  },
  {
    "id": "tecnico_nautico",
    "macroTrackId": "tecnico",
    "name": {
      "it": "Istituto Nautico / Aeronautico",
      "en": "Nautical / Aeronautical Institute"
    },
    "description": {
      "it": "Formazione iper-specializzata per conduzione di mezzi navali o aerei e logistica.",
      "en": "Hyper-specialized training for maritime or air vehicle operations and logistics."
    },
    "weeklyHours": 32,
    "textbookCost": 300,
    "fslHours": 150,
    "implicitDropout": "10%",
    "universityEnrollment": "25%",
    "curriculum": [
      { "subject": { "it": "Navigazione", "en": "Navigation" }, "hours": 6 },
      { "subject": { "it": "Macchine e Sistemi", "en": "Machinery Systems" }, "hours": 4 },
      { "subject": { "it": "Inglese Tecnico", "en": "Technical English" }, "hours": 3 },
      { "subject": { "it": "Matematica", "en": "Mathematics" }, "hours": 3 }
    ],
    "demographics": {
      "it": "Prevalenza maschile in città costiere o poli logistici.",
      "en": "Male prevalence in coastal cities or logistics hubs."
    }
  }
];

// Avoid adding duplicates
const existingIds = data.specificTracks.map(t => t.id);
newTracks.forEach(track => {
  if (!existingIds.includes(track.id)) {
    data.specificTracks.push(track);
  }
});

fs.writeFileSync(file, JSON.stringify(data, null, 2));
console.log('Added new tracks to tripartite_curriculum.json');
