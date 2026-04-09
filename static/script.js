document.addEventListener('DOMContentLoaded', function() {
    // Dynamic Row Generation for SGPA
    const sgpaForm = document.getElementById('sgpa-setup-form');
    if (sgpaForm) {
        sgpaForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const nTheory = parseInt(document.getElementById('n_theory').value) || 0;
            const nPractical = parseInt(document.getElementById('n_practical').value) || 0;

            if (nTheory <= 0 && nPractical <= 0) {
                alert('Please enter at least one subject.');
                return;
            }

            const container = document.getElementById('dynamic-fields');
            container.innerHTML = '';
            
            // Theory Subjects
            if (nTheory > 0) {
                const theoryHeader = document.createElement('h3');
                theoryHeader.textContent = 'Theory Subjects';
                theoryHeader.style.margin = '1.5rem 0 1rem 0';
                container.appendChild(theoryHeader);

                for (let i = 1; i <= nTheory; i++) {
                    const row = createRow('th', i, 'Marks (0-100)', 100);
                    container.appendChild(row);
                }
            }

            // Practical Subjects
            if (nPractical > 0) {
                const practicalHeader = document.createElement('h3');
                practicalHeader.textContent = 'Practical Subjects';
                practicalHeader.style.margin = '1.5rem 0 1rem 0';
                container.appendChild(practicalHeader);

                for (let i = 1; i <= nPractical; i++) {
                    const row = createRow('pr', i, 'Marks (0-50)', 50);
                    container.appendChild(row);
                }
            }

            document.getElementById('setup-step').style.display = 'none';
            document.getElementById('calculation-step').style.display = 'block';
            document.getElementById('n_theory_final').value = nTheory;
            document.getElementById('n_practical_final').value = nPractical;
        });
    }

    // Dynamic Row Generation for CGPA
    const cgpaForm = document.getElementById('cgpa-setup-form');
    if (cgpaForm) {
        cgpaForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const nSem = parseInt(document.getElementById('n_sem').value) || 0;

            if (nSem <= 0) {
                alert('Please enter at least one semester.');
                return;
            }

            const container = document.getElementById('dynamic-fields-cgpa');
            container.innerHTML = '';
            
            for (let i = 1; i <= nSem; i++) {
                const row = document.createElement('div');
                row.className = 'subject-row animate-up';
                row.style.animationDelay = `${i * 0.1}s`;
                row.innerHTML = `
                    <div>
                        <label>Semester ${i} SGPA</label>
                        <input type="number" step="0.01" min="0" max="10" name="sem_sgpa_${i}" placeholder="SGPA" required>
                    </div>
                    <div>
                        <label>Credits</label>
                        <input type="number" step="0.5" min="0" name="sem_credit_${i}" placeholder="Credits" required>
                    </div>
                `;
                container.appendChild(row);
            }

            document.getElementById('setup-step').style.display = 'none';
            document.getElementById('calculation-step').style.display = 'block';
            document.getElementById('n_sem_final').value = nSem;
        });
    }

    function createRow(prefix, index, placeholder, maxMarks) {
        const row = document.createElement('div');
        row.className = 'subject-row animate-up';
        row.style.animationDelay = `${index * 0.1}s`;
        row.innerHTML = `
            <div>
                <label>Subject ${index}</label>
                <input type="text" placeholder="Optional Name" disabled style="background: rgba(255,255,255,0.05)">
            </div>
            <div>
                <label>Marks</label>
                <input type="number" step="0.5" min="0" max="${maxMarks}" name="${prefix}_marks_${index}" placeholder="${placeholder}" required>
            </div>
            <div>
                <label>Credits</label>
                <input type="number" step="0.5" min="0" name="${prefix}_credit_${index}" placeholder="Credits" required>
            </div>
        `;
        return row;
    }
});
