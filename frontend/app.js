document.addEventListener('DOMContentLoaded', async () => {
    
    // --- 1. Scrollytelling Engine (Intersection Observer) ---
    const steps = document.querySelectorAll('.step');
    const graphics = document.querySelectorAll('.graphic-content');

    const observerOptions = {
        root: null,
        rootMargin: '-50% 0px -50% 0px', // Trigger exactly when the step hits the middle of the screen
        threshold: 0
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Dim all steps
                steps.forEach(s => s.classList.remove('is-active'));
                // Highlight current step
                entry.target.classList.add('is-active');

                // Switch the graphic
                const stepIndex = entry.target.getAttribute('data-step');
                graphics.forEach(g => g.classList.remove('active'));
                const activeGraphic = document.getElementById(`viz-${stepIndex}`);
                if (activeGraphic) {
                    activeGraphic.classList.add('active');
                }
            }
        });
    }, observerOptions);

    steps.forEach(step => observer.observe(step));


    // --- 2. Dynamic Citation Engine ---
    const drawer = document.getElementById('citation-drawer');
    const closeBtn = document.getElementById('close-drawer');
    const citeTokens = document.querySelectorAll('.cite-token');
    
    // UI Elements in Drawer
    const uiTitle = document.getElementById('cite-title');
    const uiSource = document.getElementById('cite-source');
    const uiLicense = document.getElementById('cite-license');
    const uiDesc = document.getElementById('cite-desc');
    const uiLink = document.getElementById('cite-link');
    const tbody = document.getElementById('dataset-tbody');

    let datapackage = null;

    // Fetch the single source of truth
    try {
        const response = await fetch('../datapackage.json');
        datapackage = await response.json();
        
        // Populate the Data Terminal Table
        if (datapackage && datapackage.resources) {
            // Sort to show processed ones first, or just show a subset
            const processed = datapackage.resources.filter(r => r.path && r.path.includes('processed'));
            
            processed.forEach(res => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${res.name}</strong></td>
                    <td>${res.description.includes('ISTAT') ? 'ISTAT' : (res.description.includes('INVALSI') ? 'INVALSI' : 'Institutional Data')}</td>
                    <td>CC-BY 4.0 / IODL 2.0</td>
                    <td><a href="../${res.path}" target="_blank">Download CSV</a></td>
                `;
                tbody.appendChild(tr);
            });
        }

    } catch (error) {
        console.error("Failed to load datapackage.json for citations:", error);
    }

    // Helper to find resource in datapackage
    function findResource(id) {
        if (!datapackage || !datapackage.resources) return null;
        return datapackage.resources.find(r => r.name === id || r.path.includes(id));
    }

    // Bind Click Events to Tokens
    citeTokens.forEach(token => {
        token.addEventListener('click', (e) => {
            const sourceId = token.getAttribute('data-source-id');
            const resource = findResource(sourceId);

            if (resource) {
                uiTitle.textContent = resource.name;
                uiSource.textContent = "Italienation Verified Source"; // Could be dynamically parsed
                uiLicense.textContent = "CC-BY 4.0 / Open Data";
                uiDesc.textContent = resource.description || "No description provided.";
                uiLink.href = `../${resource.path}`;
                uiLink.textContent = "View Raw Dataset";
            } else {
                uiTitle.textContent = sourceId;
                uiSource.textContent = "Local Processed Data";
                uiLicense.textContent = "N/A";
                uiDesc.textContent = "This dataset is synthesized locally.";
                uiLink.href = "#";
                uiLink.textContent = "Data Not Found";
            }

            // Open Drawer
            drawer.classList.add('open');
        });
    });

    // Close Drawer
    closeBtn.addEventListener('click', () => {
        drawer.classList.remove('open');
    });

});
