// Global variables
let currentTranscriptData = [];
let currentVideoId = '';

// DOM elements
const youtubeUrlInput = document.getElementById('youtubeUrl');
const languageSelect = document.getElementById('languageSelect');
const fetchTranscriptBtn = document.getElementById('fetchTranscript');
const loadingIndicator = document.getElementById('loadingIndicator');
const errorAlert = document.getElementById('errorAlert');
const errorMessage = document.getElementById('errorMessage');
const successAlert = document.getElementById('successAlert');
const successMessage = document.getElementById('successMessage');
const contentArea = document.getElementById('contentArea');
const transcriptContent = document.getElementById('transcriptContent');
const summaryContent = document.getElementById('summaryContent');
const generateSummaryBtn = document.getElementById('generateSummary');
const summaryLoading = document.getElementById('summaryLoading');
const llmProviderSelect = document.getElementById('llmProvider');
const summaryTypeSelect = document.getElementById('summaryType');
const searchToggle = document.getElementById('searchToggle');
const searchBar = document.getElementById('searchBar');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const clearSearchBtn = document.getElementById('clearSearchBtn');
const searchResults = document.getElementById('searchResults');

// Event listeners
fetchTranscriptBtn.addEventListener('click', fetchTranscript);
generateSummaryBtn.addEventListener('click', generateSummary);
searchToggle.addEventListener('click', toggleSearchBar);
searchBtn.addEventListener('click', searchTranscript);
clearSearchBtn.addEventListener('click', clearSearch);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchTranscript();
});

// Export buttons
document.querySelectorAll('.export-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const format = e.target.getAttribute('data-format');
        exportTranscript(format);
    });
});

// Fetch transcript from YouTube
async function fetchTranscript() {
    const url = youtubeUrlInput.value.trim();
    const language = languageSelect.value;
    
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }
    
    hideAlerts();
    showLoading(true);
    contentArea.style.display = 'none';
    
    try {
        const response = await axios.post('/api/transcript', {
            url: url,
            language: language
        });
        
        if (response.data.success) {
            currentTranscriptData = response.data.transcript_data;
            currentVideoId = response.data.video_id;
            displayTranscript(currentTranscriptData);
            contentArea.style.display = 'block';
            showSuccess(`Transcript loaded successfully (${response.data.language})`);
        } else {
            showError(response.data.error);
        }
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to fetch transcript');
    } finally {
        showLoading(false);
    }
}

// Display transcript in the UI
function displayTranscript(transcriptData) {
    transcriptContent.innerHTML = '';
    
    transcriptData.forEach((item, index) => {
        const transcriptItem = document.createElement('div');
        transcriptItem.className = 'transcript-item';
        transcriptItem.setAttribute('data-index', index);
        
        const timestamp = document.createElement('div');
        timestamp.className = 'timestamp';
        timestamp.textContent = item.formatted_start || formatTimestamp(item.start);
        timestamp.onclick = () => jumpToTimestamp(item.start);
        
        const text = document.createElement('div');
        text.className = 'transcript-text';
        text.textContent = item.text;
        
        transcriptItem.appendChild(timestamp);
        transcriptItem.appendChild(text);
        transcriptContent.appendChild(transcriptItem);
    });
}

// Generate summary using LLM
async function generateSummary() {
    if (!currentTranscriptData.length) {
        showError('Please fetch a transcript first');
        return;
    }
    
    const provider = llmProviderSelect.value;
    const summaryType = summaryTypeSelect.value;
    const fullText = currentTranscriptData.map(item => item.text).join(' ');
    
    summaryContent.innerHTML = '';
    summaryLoading.style.display = 'block';
    generateSummaryBtn.disabled = true;
    
    try {
        const response = await axios.post('/api/summarize', {
            text: fullText,
            summary_type: summaryType,
            llm_provider: provider
        });
        
        if (response.data.success) {
            summaryContent.innerHTML = response.data.summary_html;
            showSuccess(`Summary generated using ${provider}`);
        } else {
            showError(response.data.error);
        }
    } catch (error) {
        showError(error.response?.data?.error || 'Failed to generate summary');
    } finally {
        summaryLoading.style.display = 'none';
        generateSummaryBtn.disabled = false;
    }
}

// Search functionality
function toggleSearchBar() {
    searchBar.style.display = searchBar.style.display === 'none' ? 'block' : 'none';
    if (searchBar.style.display === 'block') {
        searchInput.focus();
    }
}

async function searchTranscript() {
    const query = searchInput.value.trim();
    
    if (!query) {
        showError('Please enter a search query');
        return;
    }
    
    clearHighlights();
    
    try {
        const response = await axios.post('/api/search', {
            transcript_data: currentTranscriptData,
            query: query
        });
        
        if (response.data.success) {
            const results = response.data.results;
            searchResults.textContent = `Found ${results.count} matches`;
            
            // Highlight results
            results.forEach(result => {
                const item = document.querySelector(`[data-index="${result.index}"]`);
                if (item) {
                    item.classList.add('highlight');
                    // Highlight the search term in the text
                    const textElement = item.querySelector('.transcript-text');
                    const text = textElement.textContent;
                    const regex = new RegExp(`(${query})`, 'gi');
                    textElement.innerHTML = text.replace(regex, '<span class="search-highlight">$1</span>');
                }
            });
            
            // Scroll to first result
            if (results.length > 0) {
                const firstResult = document.querySelector(`[data-index="${results[0].index}"]`);
                firstResult.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    } catch (error) {
        showError('Search failed');
    }
}

function clearSearch() {
    searchInput.value = '';
    searchResults.textContent = '';
    clearHighlights();
}

function clearHighlights() {
    document.querySelectorAll('.transcript-item').forEach(item => {
        item.classList.remove('highlight');
        const textElement = item.querySelector('.transcript-text');
        textElement.innerHTML = textElement.textContent;
    });
}

// Export functionality
async function exportTranscript(format) {
    if (!currentTranscriptData.length) {
        showError('No transcript to export');
        return;
    }
    
    try {
        const response = await axios.post('/api/export', {
            transcript_data: currentTranscriptData,
            format: format,
            include_timestamps: true
        }, {
            responseType: 'blob'
        });
        
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `transcript_${currentVideoId}.${format}`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        
        showSuccess(`Transcript exported as ${format.toUpperCase()}`);
    } catch (error) {
        showError('Export failed');
    }
}

// Helper functions
function formatTimestamp(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
        return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
}

function jumpToTimestamp(seconds) {
    // Open YouTube video at specific timestamp
    const url = `https://www.youtube.com/watch?v=${currentVideoId}&t=${Math.floor(seconds)}s`;
    window.open(url, '_blank');
}

function showLoading(show) {
    loadingIndicator.style.display = show ? 'block' : 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorAlert.style.display = 'block';
    successAlert.style.display = 'none';
}

function showSuccess(message) {
    successMessage.textContent = message;
    successAlert.style.display = 'block';
    errorAlert.style.display = 'none';
}

function hideAlerts() {
    errorAlert.style.display = 'none';
    successAlert.style.display = 'none';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Check for URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const videoUrl = urlParams.get('v');
    if (videoUrl) {
        youtubeUrlInput.value = `https://www.youtube.com/watch?v=${videoUrl}`;
        fetchTranscript();
    }
});

// Allow Enter key to fetch transcript
youtubeUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        fetchTranscript();
    }
}); 