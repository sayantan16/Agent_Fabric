// flask_app/static/js/app.js - Complete Implementation
// Global JavaScript for Agentic Fabric UI

// Global state management
window.AgenticFabric = {
  currentWorkflow: null,
  notifications: [],
  systemStatus: 'unknown',
};

// window.updateWorkflowPanel = function (workflowData) {
//   // Update global state
//   window.AgenticFabric.currentWorkflow = workflowData;

//   // Force refresh of the workflow panel
//   const workflowPanel = document.querySelector('[x-data*="workflowPanelData"]');
//   if (workflowPanel) {
//     const alpineData = Alpine.$data(workflowPanel);
//     if (alpineData && alpineData.updateFromExecution) {
//       alpineData.updateFromExecution(workflowData);
//     }
//   }
// };

// Initialize application
document.addEventListener('DOMContentLoaded', function () {
  // Clear chat functionality
  const clearChatBtn = document.getElementById('clear-chat-btn');
  if (clearChatBtn) {
    clearChatBtn.addEventListener('click', async () => {
      if (confirm('Are you sure you want to clear the chat history?')) {
        try {
          const response = await fetch('/api/chat/clear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
          });

          if (response.ok) {
            // (Optional) Clear UI immediately
            const chatMessages = document.getElementById('chat-messages');
            if (chatMessages) chatMessages.innerHTML = '';

            showNotification('Chat history cleared', 'success');

            // Refresh the entire page to reset any state
            setTimeout(() => window.location.reload(), 150);
          } else {
            showNotification('Failed to clear chat', 'error');
          }
        } catch (error) {
          console.error('Error clearing chat:', error);
          showNotification('Failed to clear chat', 'error');
        }
      }
    });
  }

  // Helper function for notifications
  function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-4 py-2 rounded-lg text-white ${
      type === 'success'
        ? 'bg-green-500'
        : type === 'error'
        ? 'bg-red-500'
        : 'bg-blue-500'
    } z-50 animate-slide-in`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 3000);
  }
  // Call your existing initialization functions first
  initializeApplication();
  setupGlobalEventListeners();
  checkSystemHealth();

  // Then add the file upload functionality
  initializeFileUpload();
});

// Separate function for file upload initialization
function initializeFileUpload() {
  const fileInput = document.getElementById('file-upload-input');
  const fileButton = document.getElementById('file-upload-btn');
  const filePreview = document.getElementById('file-preview');
  const fileList = document.getElementById('file-list');

  // Make this globally visible and kept in sync
  window.selectedFiles = [];

  if (fileButton) {
    fileButton.addEventListener('click', () => {
      fileInput.click();
    });
  }

  if (fileInput) {
    fileInput.addEventListener('change', function (e) {
      window.selectedFiles = Array.from(e.target.files);

      if (window.selectedFiles.length > 0) {
        // Show preview
        fileList.innerHTML = '';
        window.selectedFiles.forEach((file) => {
          const fileItem = document.createElement('div');
          fileItem.className = 'py-1';
          fileItem.innerHTML = `
            <span class="font-medium">${file.name}</span>
            <span class="text-gray-500 text-xs">(${formatFileSize(
              file.size
            )})</span>
          `;
          fileList.appendChild(fileItem);
        });
        filePreview.classList.remove('hidden');
        fileButton.classList.add('text-blue-600');
      } else {
        // No files selected -> hide preview
        filePreview.classList.add('hidden');
        fileButton.classList.remove('text-blue-600');
        fileList.innerHTML = '';
      }
    });
  }

  // Provide a global reset so Alpine can call it after sending
  window.resetFileSelection = function () {
    if (fileInput) fileInput.value = '';
    window.selectedFiles = [];
    if (fileList) fileList.innerHTML = '';
    if (filePreview) filePreview.classList.add('hidden');
    if (fileButton) fileButton.classList.remove('text-blue-600');
  };
}

// Helper function for file size
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// Main initialization
function initializeApplication() {
  // Initialize notification system
  initializeNotificationSystem();

  // Setup global shortcuts
  setupKeyboardShortcuts();

  // Initialize workflow visualization if present
  if (document.getElementById('workflow-panel')) {
    initializeWorkflowVisualization();
  }

  // Initialize auto-resize for textareas
  initializeAutoResize();

  // Setup periodic health checks
  startHealthMonitoring();
}

// Notification System
function initializeNotificationSystem() {
  // Create notification container if it doesn't exist
  if (!document.getElementById('notification-container')) {
    const container = document.createElement('div');
    container.id = 'notification-container';
    container.className = 'fixed top-4 right-4 z-50 space-y-2';
    document.body.appendChild(container);
  }
}

function showNotification(message, type = 'info', duration = 5000) {
  const container = document.getElementById('notification-container');
  if (!container) return;

  const notification = document.createElement('div');
  notification.className = `
        max-w-sm p-4 rounded-lg shadow-lg transform transition-all duration-300 ease-in-out
        ${
          type === 'success'
            ? 'bg-green-500 text-white'
            : type === 'error'
            ? 'bg-red-500 text-white'
            : type === 'warning'
            ? 'bg-yellow-500 text-black'
            : 'bg-blue-500 text-white'
        }
    `;

  notification.innerHTML = `
        <div class="flex items-center justify-between">
            <div class="flex items-center">
                <span class="mr-2">
                    ${
                      type === 'success'
                        ? '✅'
                        : type === 'error'
                        ? '❌'
                        : type === 'warning'
                        ? '⚠️'
                        : 'ℹ️'
                    }
                </span>
                <span>${message}</span>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" 
                    class="ml-2 text-lg opacity-70 hover:opacity-100">×</button>
        </div>
    `;

  container.appendChild(notification);

  // Auto-remove after duration
  if (duration > 0) {
    setTimeout(() => {
      if (notification.parentElement) {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
      }
    }, duration);
  }
}

// Workflow Visualization
function initializeWorkflowVisualization() {
  console.log('🔄 Initializing workflow visualization...');

  // Make visualization function globally available
  window.showWorkflowVisualization = function (workflowData) {
    console.log('📊 Displaying workflow:', workflowData);

    const panel = document.getElementById('workflow-panel');
    if (!panel) {
      console.warn('Workflow panel not found');
      return;
    }

    // Update workflow info
    updateWorkflowInfo(workflowData);

    // Create workflow diagram
    if (workflowData.workflow && workflowData.workflow.steps) {
      createWorkflowDiagram(workflowData.workflow.steps, workflowData.status);
    }

    // Show the panel
    panel.classList.remove('hidden');

    // Store current workflow
    window.AgenticFabric.currentWorkflow = workflowData;
  };

  window.hideWorkflowVisualization = function () {
    const panel = document.getElementById('workflow-panel');
    if (panel) {
      panel.classList.add('hidden');
    }
    window.AgenticFabric.currentWorkflow = null;
  };
}

function updateWorkflowInfo(workflowData) {
  // Update workflow ID
  const idElement = document.getElementById('workflow-id');
  if (idElement) {
    idElement.textContent = workflowData.workflow_id || 'Unknown';
  }

  // Update status
  const statusElement = document.getElementById('workflow-status');
  if (statusElement) {
    statusElement.textContent = workflowData.status || 'Unknown';
    statusElement.className = `px-2 py-1 rounded-full text-xs font-medium
            ${
              workflowData.status === 'success'
                ? 'bg-green-100 text-green-800'
                : workflowData.status === 'error'
                ? 'bg-red-100 text-red-800'
                : workflowData.status === 'processing'
                ? 'bg-yellow-100 text-yellow-800'
                : 'bg-gray-100 text-gray-800'
            }`;
  }

  // Update execution time
  const timeElement = document.getElementById('workflow-time');
  if (timeElement && workflowData.execution_time) {
    timeElement.textContent = `${workflowData.execution_time.toFixed(1)}s`;
  }

  // Update agents used
  const agentsElement = document.getElementById('workflow-agents');
  if (
    agentsElement &&
    workflowData.metadata &&
    workflowData.metadata.agents_used
  ) {
    agentsElement.innerHTML = workflowData.metadata.agents_used
      .map(
        (agent) =>
          `<span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mr-1">${agent}</span>`
      )
      .join('');
  }
}

function createWorkflowDiagram(steps, status = 'unknown') {
  const diagramContainer = document.getElementById('workflow-diagram');
  if (!diagramContainer) return;

  // Create simple visual workflow
  const diagram = steps
    .map((step, index) => {
      const isCompleted = status === 'success' || status === 'completed';
      const isActive = status === 'processing' && index === 0;

      return `
            <div class="flex items-center ${
              index < steps.length - 1 ? 'mb-2' : ''
            }">
                <div class="flex items-center justify-center w-8 h-8 rounded-full text-xs font-medium
                    ${
                      isCompleted
                        ? 'bg-green-500 text-white'
                        : isActive
                        ? 'bg-yellow-500 text-white animate-pulse'
                        : 'bg-gray-300 text-gray-600'
                    }">
                    ${index + 1}
                </div>
                <div class="ml-3 flex-1">
                    <div class="text-sm font-medium text-gray-900">${step}</div>
                </div>
                ${
                  isCompleted
                    ? '<div class="text-green-500 text-sm">✓</div>'
                    : ''
                }
            </div>
            ${
              index < steps.length - 1
                ? '<div class="w-0.5 h-4 bg-gray-300 ml-4"></div>'
                : ''
            }
        `;
    })
    .join('');

  diagramContainer.innerHTML = diagram;
}

// Health Monitoring
function checkSystemHealth() {
  fetch('/api/health')
    .then((response) => response.json())
    .then((data) => {
      window.AgenticFabric.systemStatus = data.status;
      updateSystemStatusUI(data);
    })
    .catch((error) => {
      console.error('Health check failed:', error);
      window.AgenticFabric.systemStatus = 'error';
      updateSystemStatusUI({ status: 'error' });
    });
}

function updateSystemStatusUI(healthData) {
  const statusElement = document.getElementById('backend-status');
  if (!statusElement) return;

  const status = healthData.status;
  statusElement.textContent =
    status === 'healthy'
      ? 'Connected'
      : status === 'degraded'
      ? 'Degraded'
      : 'Disconnected';

  statusElement.className =
    status === 'healthy'
      ? 'text-green-600'
      : status === 'degraded'
      ? 'text-yellow-600'
      : 'text-red-600';

  // Update status indicator dot
  const dotElement = statusElement.previousElementSibling;
  if (dotElement) {
    dotElement.className = `w-2 h-2 rounded-full mr-1 ${
      status === 'healthy'
        ? 'bg-green-500'
        : status === 'degraded'
        ? 'bg-yellow-500'
        : 'bg-red-500'
    }`;
  }
}

function startHealthMonitoring() {
  // Check every 30 seconds
  setInterval(checkSystemHealth, 500000);
}

// Auto-resize functionality
function initializeAutoResize() {
  document.addEventListener('input', function (e) {
    if (
      e.target.tagName === 'TEXTAREA' &&
      e.target.hasAttribute('data-autoresize')
    ) {
      autoResizeTextarea(e.target);
    }
  });
}

function autoResizeTextarea(textarea) {
  textarea.style.height = 'auto';
  const maxHeight = parseInt(textarea.dataset.maxHeight) || 120;
  textarea.style.height = Math.min(textarea.scrollHeight, maxHeight) + 'px';
}

// Keyboard shortcuts
function setupKeyboardShortcuts() {
  document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + K to focus search/message input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      const messageInput = document.querySelector(
        '#message-input, [x-ref="messageInput"]'
      );
      if (messageInput) {
        messageInput.focus();
      }
    }

    // Escape to close modals/panels
    if (e.key === 'Escape') {
      const workflowPanel = document.getElementById('workflow-panel');
      if (workflowPanel && !workflowPanel.classList.contains('hidden')) {
        window.hideWorkflowVisualization();
      }
    }
  });
}

// Global event listeners
function setupGlobalEventListeners() {
  // Handle HTMX events
  document.addEventListener('htmx:afterRequest', function (e) {
    if (e.detail.xhr.status >= 400) {
      showNotification('Request failed. Please try again.', 'error');
    }
  });

  // Handle form submissions (skip chat form; Alpine manages it)
  document.addEventListener('submit', function (e) {
    const form = e.target;

    // Skip the chat form
    if (form && form.id === 'chat-form') {
      return;
    }

    if (form.classList.contains('processing')) {
      e.preventDefault();
      return false;
    }

    form.classList.add('processing');
    setTimeout(() => {
      form.classList.remove('processing');
    }, 5000);
  });

  // Handle file drag and drop globally
  let dragCounter = 0;

  document.addEventListener('dragenter', function (e) {
    e.preventDefault();
    dragCounter++;
    if (dragCounter === 1) {
      document.body.classList.add('drag-active');
    }
  });

  document.addEventListener('dragleave', function (e) {
    e.preventDefault();
    dragCounter--;
    if (dragCounter === 0) {
      document.body.classList.remove('drag-active');
    }
  });

  document.addEventListener('drop', function (e) {
    e.preventDefault();
    dragCounter = 0;
    document.body.classList.remove('drag-active');
  });
}

// Utility functions
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatTimestamp(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// API helpers
window.API = {
  async get(url) {
    const response = await fetch(url, {
      headers: { 'Content-Type': 'application/json' },
    });
    return response.json();
  },

  async post(url, data) {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },

  async upload(url, formData) {
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
    });
    return response.json();
  },
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    showNotification,
    showWorkflowVisualization: window.showWorkflowVisualization,
    formatFileSize,
    formatTimestamp,
    API: window.API,
  };
}

function updateChatWithResponse(result) {
  const chatMessages = document.getElementById('chat-messages');

  // Create message element
  const messageDiv = document.createElement('div');
  messageDiv.className = 'flex justify-start mb-4';

  const timestamp = new Date().toLocaleTimeString();

  messageDiv.innerHTML = `
        <div class="max-w-3xl">
            <div class="bg-gray-100 rounded-lg p-4">
                <div class="text-sm text-gray-500 mb-1">AI Assistant • ${timestamp}</div>
                <div class="prose max-w-none">
                    ${formatResponse(result.response || 'Processing complete')}
                </div>
                ${
                  result.workflow
                    ? `
                    <div class="mt-2 text-xs text-gray-500">
                        Agents used: ${result.workflow.steps.join(', ')} • 
                        Time: ${result.execution_time?.toFixed(1) || 0}s
                    </div>
                `
                    : ''
                }
            </div>
        </div>
    `;

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatResponse(text) {
  // Convert markdown-like formatting to HTML
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>')
    .replace(/• /g, '&bull; ');
}

// ADD these functions to handle pipeline responses in app.js:

function displayPipelineInfo(pipelineInfo, messageContainer) {
  if (!pipelineInfo || pipelineInfo.type === 'simple') {
    return; // No pipeline info to display for simple requests
  }

  const pipelineDiv = document.createElement('div');
  pipelineDiv.className = 'pipeline-info mt-2 p-3 bg-light rounded';

  let pipelineHtml = `
        <div class="pipeline-header d-flex justify-content-between align-items-center mb-2">
            <h6 class="mb-0">
                <i class="fas fa-sitemap me-2"></i>
                ${
                  pipelineInfo.type === 'pipeline'
                    ? 'Multi-Step Pipeline'
                    : 'Complex Pipeline'
                }
            </h6>
            <span class="badge bg-${getStatusBadgeColor(
              pipelineInfo.performance_grade || 'unknown'
            )}">
                ${pipelineInfo.performance_grade || 'unknown'}
            </span>
        </div>
    `;

  // Pipeline steps
  if (pipelineInfo.steps && pipelineInfo.steps.length > 0) {
    pipelineHtml += `
            <div class="pipeline-steps mb-2">
                <div class="row">
                    <div class="col-md-6">
                        <small class="text-muted">Steps Executed:</small>
                        <div class="steps-list">
        `;

    pipelineInfo.steps.forEach((step, index) => {
      const isCompleted = index < pipelineInfo.steps_completed;
      const icon = isCompleted
        ? 'fas fa-check-circle text-success'
        : 'fas fa-circle text-muted';
      pipelineHtml += `
                <div class="step-item d-flex align-items-center mb-1">
                    <i class="${icon} me-2"></i>
                    <span class="${
                      isCompleted ? 'text-dark' : 'text-muted'
                    }">${step}</span>
                </div>
            `;
    });

    pipelineHtml += `
                        </div>
                    </div>
                    <div class="col-md-6">
                        <small class="text-muted">Execution Details:</small>
                        <div class="execution-stats">
                            <div><strong>Progress:</strong> ${
                              pipelineInfo.steps_completed
                            }/${pipelineInfo.total_steps} steps</div>
                            <div><strong>Strategy:</strong> ${
                              pipelineInfo.execution_strategy
                            }</div>
                            <div><strong>Time:</strong> ${pipelineInfo.execution_time.toFixed(
                              1
                            )}s</div>
        `;

    if (pipelineInfo.components_created > 0) {
      pipelineHtml += `<div><strong>Created:</strong> ${pipelineInfo.components_created} new components</div>`;
    }

    if (pipelineInfo.adaptations > 0) {
      pipelineHtml += `<div><strong>Adaptations:</strong> ${pipelineInfo.adaptations} intelligent adjustments</div>`;
    }

    pipelineHtml += `
                        </div>
                    </div>
                </div>
            </div>
        `;
  }

  pipelineDiv.innerHTML = pipelineHtml;
  messageContainer.appendChild(pipelineDiv);
}

function getStatusBadgeColor(grade) {
  switch (grade) {
    case 'excellent':
      return 'success';
    case 'good':
      return 'primary';
    case 'acceptable':
      return 'warning';
    case 'needs_improvement':
      return 'danger';
    default:
      return 'secondary';
  }
}

function displayStepResults(stepResults, messageContainer) {
  if (!stepResults || Object.keys(stepResults).length === 0) {
    return;
  }

  const stepsDiv = document.createElement('div');
  stepsDiv.className = 'step-results mt-2';

  let stepsHtml = `
        <div class="accordion" id="stepResultsAccordion">
            <div class="accordion-item">
                <h2 class="accordion-header" id="stepResultsHeader">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                            data-bs-target="#stepResultsCollapse" aria-expanded="false">
                        <i class="fas fa-list me-2"></i>
                        Step Details (${Object.keys(stepResults).length} steps)
                    </button>
                </h2>
                <div id="stepResultsCollapse" class="accordion-collapse collapse" 
                     data-bs-parent="#stepResultsAccordion">
                    <div class="accordion-body">
    `;

  Object.entries(stepResults).forEach(([stepName, result], index) => {
    const status = result.status || 'unknown';
    const statusIcon =
      status === 'success'
        ? 'fas fa-check-circle text-success'
        : 'fas fa-exclamation-circle text-danger';

    stepsHtml += `
            <div class="step-result mb-3 p-2 border rounded">
                <div class="d-flex justify-content-between align-items-center">
                    <h6 class="mb-1">
                        <i class="${statusIcon} me-2"></i>
                        ${stepName}
                    </h6>
                    <span class="badge bg-${
                      status === 'success' ? 'success' : 'danger'
                    }">${status}</span>
                </div>
        `;

    if (result.data) {
      const dataPreview = getDataPreview(result.data);
      if (dataPreview) {
        stepsHtml += `<div class="step-data mt-2"><small class="text-muted">${dataPreview}</small></div>`;
      }
    }

    if (result.error) {
      stepsHtml += `<div class="step-error mt-2"><small class="text-danger">Error: ${result.error}</small></div>`;
    }

    stepsHtml += `</div>`;
  });

  stepsHtml += `
                    </div>
                </div>
            </div>
        </div>
    `;

  stepsDiv.innerHTML = stepsHtml;
  messageContainer.appendChild(stepsDiv);
}

function getDataPreview(data) {
  if (Array.isArray(data)) {
    return `Generated ${data.length} items`;
  } else if (typeof data === 'object' && data !== null) {
    const keys = Object.keys(data);
    if (keys.length > 0) {
      return `Generated data: ${keys.slice(0, 3).join(', ')}${
        keys.length > 3 ? '...' : ''
      }`;
    }
  } else if (typeof data === 'string') {
    return `Generated text (${data.length} characters)`;
  }
  return 'Data generated successfully';
}

// MODIFY the existing displayAssistantMessage function to include pipeline info:
function displayAssistantMessage(message) {
  const messageDiv = document.createElement('div');
  messageDiv.className = 'message assistant-message';
  messageDiv.setAttribute('data-message-id', message.id);

  const messageContainer = document.createElement('div');
  messageContainer.className = 'message-content';

  // Main response content
  const contentDiv = document.createElement('div');
  contentDiv.className = 'response-content';
  contentDiv.innerHTML = formatMessageContent(message.content);
  messageContainer.appendChild(contentDiv);

  // NEW: Add pipeline information if present
  if (message.pipeline_info) {
    displayPipelineInfo(message.pipeline_info, messageContainer);
  }

  // NEW: Add step results if present
  if (message.step_results) {
    displayStepResults(message.step_results, messageContainer);
  }

  // Status and workflow info
  if (message.status && message.status !== 'success') {
    const statusDiv = document.createElement('div');
    statusDiv.className = `alert alert-${
      message.status === 'error' ? 'danger' : 'warning'
    } mt-2`;
    statusDiv.innerHTML = `<small>Status: ${message.status}</small>`;
    messageContainer.appendChild(statusDiv);
  }

  // Timestamp
  const timestampDiv = document.createElement('div');
  timestampDiv.className = 'message-timestamp';
  timestampDiv.textContent = new Date(message.timestamp).toLocaleTimeString();
  messageContainer.appendChild(timestampDiv);

  messageDiv.appendChild(messageContainer);
  return messageDiv;
}

// MODIFY the sendMessage function to handle pipeline responses:
async function sendMessage() {
  const messageInput = document.getElementById('messageInput');
  const message = messageInput.value.trim();

  if (!message) return;

  // Display user message
  displayUserMessage({
    id: Date.now().toString(),
    content: message,
    timestamp: new Date().toISOString(),
    files: uploadedFiles.length,
  });

  messageInput.value = '';

  // Show typing indicator
  showTypingIndicator();

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        auto_create: true,
      }),
    });

    const result = await response.json();

    // Hide typing indicator
    hideTypingIndicator();

    if (response.ok) {
      // Display assistant response with pipeline info
      displayAssistantMessage({
        ...result.response,
        pipeline_info: result.pipeline_info,
        step_results: result.step_results,
        workflow_id: result.workflow_id,
      });

      // Display generated files if any
      if (result.generated_files && result.generated_files.length > 0) {
        displayGeneratedFiles(result.generated_files);
      }

      // Update workflow visualization if available
      if (result.workflow) {
        updateWorkflowVisualization(result.workflow);
      }
    } else {
      displayErrorMessage(result.error || 'An error occurred');
    }
  } catch (error) {
    hideTypingIndicator();
    displayErrorMessage('Network error occurred');
    console.error('Error:', error);
  }

  // Clear uploaded files
  uploadedFiles = [];
  updateFilesList();
}

// ADD new function for workflow visualization:
function updateWorkflowVisualization(workflow) {
  const workflowPanel = document.getElementById('workflow-panel');
  if (!workflowPanel) return;

  if (workflow.type === 'pipeline' && workflow.steps) {
    const stepsHtml = workflow.steps
      .map((step, index) => {
        const isCompleted = index < (workflow.steps_completed || 0);
        const stepClass = isCompleted ? 'completed' : 'pending';
        return `
                <div class="workflow-step ${stepClass}">
                    <div class="step-number">${index + 1}</div>
                    <div class="step-name">${step}</div>
                </div>
            `;
      })
      .join('');

    workflowPanel.innerHTML = `
            <div class="workflow-header">
                <h6>Workflow Execution</h6>
                <span class="workflow-type">${workflow.execution_strategy}</span>
            </div>
            <div class="workflow-steps">
                ${stepsHtml}
            </div>
        `;
  }
}
