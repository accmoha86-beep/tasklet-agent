/**
 * Tasklet Agent Web UI - Frontend JavaScript
 */

const API_BASE = '/api';
let isExecuting = false;
let currentExecution = null;

// DOM Elements
const taskInput = document.getElementById('taskInput');
const executeBtn = document.getElementById('executeBtn');
const clearMemoryBtn = document.getElementById('clearMemoryBtn');
const historyToggleBtn = document.getElementById('historyToggleBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const resultsContent = document.getElementById('resultsContent');
const historySection = document.getElementById('historySection');
const historyContent = document.getElementById('historyContent');
const memorySection = document.getElementById('memorySection');
const memoryContent = document.getElementById('memoryContent');
const statusIndicator = document.getElementById('statusIndicator');

// Event Listeners
executeBtn.addEventListener('click', handleExecuteTask);
clearMemoryBtn.addEventListener('click', handleClearMemory);
historyToggleBtn.addEventListener('click', handleToggleHistory);
taskInput.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        handleExecuteTask();
    }
});

// Initialize
window.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

/**
 * Initialize the application
 */
async function initializeApp() {
    try {
        const status = await getStatus();
        updateStatusIndicator('running', 'Connected');
        console.log('Agent Status:', status);
    } catch (error) {
        console.error('Failed to connect to agent:', error);
        updateStatusIndicator('error', 'Disconnected');
    }
}

/**
 * Handle task execution
 */
async function handleExecuteTask() {
    const task = taskInput.value.trim();
    
    if (!task) {
        showErrorMessage('Please enter a task');
        return;
    }
    
    if (isExecuting) {
        showErrorMessage('Task is already executing');
        return;
    }
    
    isExecuting = true;
    executeBtn.disabled = true;
    showLoadingSpinner(true);
    resultsSection.classList.add('hidden');
    
    try {
        currentExecution = await executeTask(task);
        displayResults(currentExecution);
        taskInput.value = '';
    } catch (error) {
        showErrorMessage(`Execution failed: ${error.message}`);
        console.error('Execution error:', error);
    } finally {
        isExecuting = false;
        executeBtn.disabled = false;
        showLoadingSpinner(false);
    }
}

/**
 * Handle clear memory
 */
async function handleClearMemory() {
    if (confirm('Are you sure you want to clear agent memory?')) {
        try {
            await clearMemory();
            showSuccessMessage('Memory cleared successfully');
            memorySection.classList.add('hidden');
        } catch (error) {
            showErrorMessage(`Failed to clear memory: ${error.message}`);
        }
    }
}

/**
 * Handle history toggle
 */
async function handleToggleHistory() {
    if (historySection.classList.contains('hidden')) {
        try {
            await loadHistory();
            historySection.classList.remove('hidden');
            historyToggleBtn.textContent = 'Hide History';
        } catch (error) {
            showErrorMessage(`Failed to load history: ${error.message}`);
        }
    } else {
        historySection.classList.add('hidden');
        historyToggleBtn.textContent = 'Show History';
    }
}

/**
 * API: Execute Task
 */
async function executeTask(task) {
    const response = await fetch(`${API_BASE}/execute`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ task })
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Execution failed');
    }
    
    return await response.json();
}

/**
 * API: Get History
 */
async function getHistory() {
    const response = await fetch(`${API_BASE}/history`);
    if (!response.ok) throw new Error('Failed to fetch history');
    return await response.json();
}

/**
 * API: Get Memory
 */
async function getMemory() {
    const response = await fetch(`${API_BASE}/memory`);
    if (!response.ok) throw new Error('Failed to fetch memory');
    return await response.json();
}

/**
 * API: Clear Memory
 */
async function clearMemory() {
    const response = await fetch(`${API_BASE}/clear-memory`, {
        method: 'POST'
    });
    if (!response.ok) throw new Error('Failed to clear memory');
    return await response.json();
}

/**
 * API: Get Status
 */
async function getStatus() {
    const response = await fetch(`${API_BASE}/status`);
    if (!response.ok) throw new Error('Failed to fetch status');
    return await response.json();
}

/**
 * Display execution results
 */
function displayResults(execution) {
    resultsContent.innerHTML = '';
    resultsSection.classList.remove('hidden');
    
    const card = document.createElement('div');
    card.className = `result-card ${execution.status}`;
    
    const header = document.createElement('div');
    header.className = 'result-header';
    header.innerHTML = `
        <span class="task-title">Task Execution ${execution.status === 'success' ? '✓' : '✗'}</span>
        <span class="result-status ${execution.status}">${execution.status.toUpperCase()}</span>
    `;
    
    const timestamp = new Date(execution.timestamp).toLocaleString();
    const duration = execution.duration_seconds ? `${execution.duration_seconds.toFixed(2)}s` : 'N/A';
    
    const details = document.createElement('div');
    details.className = 'task-details';
    
    if (execution.status === 'success') {
        details.innerHTML = `
            <strong>Task:</strong> ${escapeHtml(execution.task)}
            
<strong>Response:</strong>
${escapeHtml(execution.response)}
            
<strong>Duration:</strong> ${duration}
<strong>Plan Steps:</strong> ${execution.plan ? execution.plan.length : 0}
<strong>Timestamp:</strong> ${timestamp}
        `;
    } else {
        details.innerHTML = `
            <strong>Task:</strong> ${escapeHtml(execution.task)}
            
<strong>Error:</strong>
${escapeHtml(execution.error || 'Unknown error')}
            
<strong>Timestamp:</strong> ${timestamp}
        `;
    }
    
    card.appendChild(header);
    card.appendChild(details);
    resultsContent.appendChild(card);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Load and display history
 */
async function loadHistory() {
    const data = await getHistory();
    historyContent.innerHTML = '';
    
    if (!data.executions || data.executions.length === 0) {
        historyContent.innerHTML = '<p style="color: #999; text-align: center;">No execution history yet</p>';
        return;
    }
    
    data.executions.forEach(execution => {
        const item = document.createElement('div');
        item.className = 'history-item';
        
        const date = new Date(execution.timestamp).toLocaleString();
        const status = execution.result.status;
        
        item.innerHTML = `
            <div class="history-item-header">
                <span class="history-item-task" style="color: ${status === 'success' ? '#4caf50' : '#f44336'}">
                    ${escapeHtml(execution.task.substring(0, 60))}${execution.task.length > 60 ? '...' : ''}
                </span>
                <span class="history-item-time">${date}</span>
            </div>
            <small style="color: #999;">
                Status: <strong>${status.toUpperCase()}</strong>
                ${execution.result.duration_seconds ? ` | Duration: ${execution.result.duration_seconds.toFixed(2)}s` : ''}
            </small>
        `;
        
        item.addEventListener('click', () => {
            taskInput.value = execution.task;
            historySection.scrollIntoView({ behavior: 'smooth' });
        });
        
        historyContent.appendChild(item);
    });
}

/**
 * Display loading spinner
 */
function showLoadingSpinner(show) {
    if (show) {
        loadingSpinner.classList.remove('hidden');
    } else {
        loadingSpinner.classList.add('hidden');
    }
}

/**
 * Show error message
 */
function showErrorMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'error-message';
    messageDiv.textContent = message;
    
    resultsSection.classList.remove('hidden');
    resultsContent.innerHTML = '';
    resultsContent.appendChild(messageDiv);
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Show success message
 */
function showSuccessMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'success-message';
    messageDiv.textContent = message;
    
    resultsSection.classList.remove('hidden');
    resultsContent.innerHTML = '';
    resultsContent.appendChild(messageDiv);
}

/**
 * Update status indicator
 */
function updateStatusIndicator(status, text) {
    const dot = statusIndicator.querySelector('.status-dot');
    const textSpan = statusIndicator.querySelector('.status-text');
    
    statusIndicator.className = 'status-indicator';
    
    if (status === 'running') {
        dot.style.background = '#4caf50';
        statusIndicator.classList.add('status-running');
    } else if (status === 'error') {
        dot.style.background = '#f44336';
    } else {
        dot.style.background = '#ff9800';
    }
    
    textSpan.textContent = text;
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
