let allJobs = [];

async function searchJobs() {
    const query = document.getElementById('query').value;
    const location = document.getElementById('location').value;

    if (!query.trim()) {
        alert('Please enter a job position');
        return;
    }

    // Show loader
    showLoader();

    try {
        const formData = new FormData();
        formData.append('query', query);
        formData.append('location', location);

        const response = await fetch('/search', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Search failed');
        }

        const jobs = await response.json();
        allJobs = jobs;

        // Populate table
        populateJobTable(jobs);
        
        // Update filters based on results
        updateFilters(jobs);
        
        // Update job count
        document.getElementById('jobCount').textContent = `Found ${jobs.length} job${jobs.length !== 1 ? 's' : ''}`;

        // Show download button if jobs exist
        if (jobs.length > 0) {
            document.getElementById('downloadBtn').classList.remove('hidden');
        }

    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while searching. Please try again.');
        document.getElementById('jobTable').innerHTML = '';
        document.getElementById('jobCount').textContent = '';
    } finally {
        // Hide loader
        hideLoader();
    }
}

function populateJobTable(jobs) {
    const jobTable = document.getElementById('jobTable');
    jobTable.innerHTML = '';

    if (jobs.length === 0) {
        jobTable.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-gray-500">No jobs found</td></tr>';
        return;
    }

    jobs.forEach((job, index) => {
        const row = document.createElement('tr');
        const score = Math.round((parseFloat(job.final_score || 0) * 100));
        // console.log(job);
        row.innerHTML = `
            <td>${index + 1}</td>
            <td><strong>${job.title || 'N/A'}</strong></td>
            <td>${job.date || 'N/A'}</td>
            <td><i data-lucide="map-pin"></i> ${job.location || 'N/A'}</td>
            <td>${job.company || 'N/A'}</td>
            <td>${job.url || 'N/A'}</td>
            <td><span class="score-badge">${score}%</span></td>
            <td>
                <a href="${job.url || '#'}" target="_blank" class="action-link">
                    <i data-lucide="external-link"></i> View
                </a>
            </td>
        `;
        jobTable.appendChild(row);
    });
    
    // Re-render lucide icons after adding new elements
    lucide.createIcons();
}

function getDateRange(dateString) {
    if (!dateString) return null;
    
    const jobDate = new Date(dateString);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const diffTime = today - jobDate;
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays <= 1) return 'last_24h';
    if (diffDays <= 7) return 'last_7d';
    if (diffDays <= 30) return 'last_30d';
    return 'older';
}

function updateFilters(jobs) {
    // Extract unique date ranges
    const dateRanges = new Set(jobs.map(job => getDateRange(job.date)).filter(range => range));
    
    const dateRangeLabels = {
        'last_24h': 'Last 24 hours',
        'last_7d': 'Last 7 days',
        'last_30d': 'Last 30 days',
        'older': 'Older'
    };

    // Update date filter
    const dateSelect = document.querySelector('.filter-date');
    if (dateSelect) {
        const currentValue = dateSelect.value;
        dateSelect.innerHTML = '<option value="">Any time</option>';
        
        const orderedRanges = ['last_24h', 'last_7d', 'last_30d', 'older'];
        orderedRanges.forEach(range => {
            if (dateRanges.has(range)) {
                const option = document.createElement('option');
                option.value = range;
                option.textContent = dateRangeLabels[range];
                dateSelect.appendChild(option);
            }
        });
        
        if (currentValue && dateRanges.has(currentValue)) {
            dateSelect.value = currentValue;
        }
    }

    // Extract unique locations
    const locations = [...new Set(jobs.map(job => job.location).filter(loc => loc))];
    locations.sort();

    // Update location filter
    const locationSelect = document.querySelector('.filter-location');
    if (locationSelect) {
        const currentValue = locationSelect.value;
        locationSelect.innerHTML = '<option value="">All Locations</option>';
        locations.forEach(location => {
            const option = document.createElement('option');
            option.value = location;
            option.textContent = location;
            locationSelect.appendChild(option);
        });
        if (currentValue && locations.includes(currentValue)) {
            locationSelect.value = currentValue;
        }
    }

    // Update minimum score slider based on max available score
    const scores = jobs
        .map(job => Math.round((parseFloat(job.final_score || 0) * 100)))
        .filter(score => score > 0);
    
    if (scores.length > 0) {
        const maxScore = Math.max(...scores);
        const scoreSlider = document.querySelector('.filter-score');
        if (scoreSlider) {
            scoreSlider.max = maxScore;
            scoreSlider.value = 0;
        }
    }
}

function showLoader() {
    // Create loader if it doesn't exist
    let loader = document.getElementById('searchLoader');
    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'searchLoader';
        loader.className = 'loader-container';
        loader.innerHTML = `
            <div class="loader-backdrop">
                <div class="loader-content">
                    <div class="spinner"></div>
                    <p class="loader-text">Searching for jobs...</p>
                </div>
            </div>
        `;
        document.body.appendChild(loader);
    }
    loader.style.display = 'flex';
}

function hideLoader() {
    const loader = document.getElementById('searchLoader');
    if (loader) {
        loader.style.display = 'none';
    }
}

async function downloadExcel() {
    if (allJobs.length === 0) {
        alert('No jobs to download');
        return;
    }

    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(allJobs)
        });

        if (!response.ok) {
            throw new Error('Download failed');
        }

        // Get the blob and create download link
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'jobs.xlsx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to download file. Please try again.');
    }
}

// Allow Enter key to trigger search
document.addEventListener('DOMContentLoaded', function() {
    const queryInput = document.getElementById('query');
    const locationInput = document.getElementById('location');
    
    [queryInput, locationInput].forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchJobs();
            }
        });
    });

    // Add filter event listeners
    const dateFilter = document.querySelector('.filter-date');
    const locationFilter = document.querySelector('.filter-location');
    const scoreSlider = document.querySelector('.filter-score');

    if (dateFilter) dateFilter.addEventListener('change', applyFilters);
    if (locationFilter) locationFilter.addEventListener('change', applyFilters);
    if (scoreSlider) scoreSlider.addEventListener('input', applyFilters);
});

function applyFilters() {
    if (allJobs.length === 0) return;

    const dateFilter = document.querySelector('.filter-date').value;
    const locationFilter = document.querySelector('.filter-location').value;
    const scoreSlider = document.querySelector('.filter-score').value;

    // Filter jobs based on selected criteria
    let filteredJobs = allJobs.filter(job => {
        const matchesDate = !dateFilter || getDateRange(job.date) === dateFilter;
        const matchesLocation = !locationFilter || job.location === locationFilter;
        const jobScore = Math.round((parseFloat(job.final_score || 0) * 100));
        const matchesScore = jobScore >= scoreSlider;

        return matchesDate && matchesLocation && matchesScore;
    });

    // Update table with filtered results
    populateJobTable(filteredJobs);
    
    // Update job count
    document.getElementById('jobCount').textContent = `Found ${filteredJobs.length} of ${allJobs.length} job${filteredJobs.length !== 1 ? 's' : ''}`;
}