/**
 * Main JavaScript for Agentic Fabric POC
 * Handles Alpine.js data, HTMX events, and UI interactions
 */

// Alpine.js global data - FIXED VERSION
function appData() {
  return {
    // UI State
    darkMode: localStorage.getItem('darkMode') === 'true',
    mobileMenuOpen: false,

    // System Status - FIXED: Proper initialization
    systemStatus: {
      connected: false,
      message: 'Checking...',
      lastChecked: null,
      services: {
        orchestrator: false,
        registry: false,
        workflow: false,
      },
    },

    // Chat State
    chatState: {
      isProcessing: false,
      currentWorkflowId: null,
      messages: [],
    },

    // Methods
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      localStorage.setItem('darkMode', this.darkMode);
      document.documentElement.classList.toggle('dark', this.darkMode);
    },

    // FIXED: Proper status update handler
    updateSystemStatus(event) {
      try {
        if (event.detail.xhr.status === 200) {
          const response = JSON.parse(event.detail.xhr.responseText);

          // Update connection status
          this.systemStatus.connected = response.status === 'healthy';
          this.systemStatus.message = this.systemStatus.connected
            ? 'Connected'
            : 'Disconnected';
          this.systemStatus.lastChecked = new Date().toLocaleTimeString();

          // Update individual services
          if (response.services) {
            this.systemStatus.services = response.services;
          }

          console.log('Status updated:', this.systemStatus);
        } else {
          this.systemStatus.connected = false;
          this.systemStatus.message = 'Error';
        }
      } catch (error) {
        console.error('Error updating system status:', error);
        this.systemStatus.connected = false;
        this.systemStatus.message = 'Error';
      }
    },

    showLoading() {
      const overlay = document.getElementById('loading-overlay');
      if (overlay) {
        overlay.classList.remove('hidden');
        overlay.classList.add('flex');
      }
    },

    hideLoading() {
      const overlay = document.getElementById('loading-overlay');
      if (overlay) {
        overlay.classList.add('hidden');
        overlay.classList.remove('flex');
      }
    },

    // ADDED: Manual status check
    async checkSystemStatus() {
      try {
        const response = await fetch('/api/health');
        const data = await response.json();

        this.systemStatus.connected = data.status === 'healthy';
        this.systemStatus.message = this.systemStatus.connected
          ? 'Connected'
          : 'Disconnected';
        this.systemStatus.lastChecked = new Date().toLocaleTimeString();

        if (data.services) {
          this.systemStatus.services = data.services;
        }
      } catch (error) {
        console.error('Manual status check failed:', error);
        this.systemStatus.connected = false;
        this.systemStatus.message = 'Disconnected';
      }
    },
  };
}

// HTMX Event Handlers - ENHANCED VERSION
document.addEventListener('DOMContentLoaded', function () {
  // FIXED: Initialize Alpine.js and check status immediately
  setTimeout(() => {
    // Trigger initial status check
    if (window.Alpine && window.Alpine.store) {
      const app =
        window.Alpine.store('app') ||
        document.querySelector('[x-data="appData()"]').__x.$data;
      if (app && app.checkSystemStatus) {
        app.checkSystemStatus();
      }
    }

    // Also trigger HTMX status check
    const statusIndicator = document.getElementById('status-indicator');
    if (statusIndicator) {
      htmx.trigger(statusIndicator, 'htmx:trigger');
    }
  }, 100);

  // Handle HTMX requests
  document.body.addEventListener('htmx:beforeRequest', function (event) {
    if (!event.detail.pathInfo.requestPath.includes('/health')) {
      showGlobalLoading();
    }
  });

  document.body.addEventListener('htmx:afterRequest', function (event) {
    hideGlobalLoading();

    // FIXED: Handle health check responses specifically
    if (event.detail.pathInfo.requestPath.includes('/health')) {
      // The updateSystemStatus will be called by the hx-on:htmx:after-request attribute
      return;
    }

    // Handle API errors
    if (event.detail.xhr.status >= 400) {
      const errorMessage = getErrorMessage(event.detail.xhr);
      showNotification(errorMessage, 'error');
    }
  });

  // Handle SSE connections
  document.body.addEventListener('htmx:sseError', function (event) {
    console.error('SSE Error:', event);
    showNotification('Real-time connection lost', 'warning');
  });

  // Initialize other components
  initializeFileUpload();
  initializeWorkflowViz();
  initializeChatAutoScroll();
});

// ADDED: Global status check function
async function checkBackendStatus() {
  try {
    const response = await fetch('/api/health');
    const data = await response.json();

    // Update the status in the sidebar if it exists
    const backendStatus = document.getElementById('backend-status');
    if (backendStatus) {
      if (data.status === 'healthy') {
        backendStatus.textContent = 'Connected';
        backendStatus.className = 'text-green-600';
      } else {
        backendStatus.textContent = 'Disconnected';
        backendStatus.className = 'text-red-600';
      }
    }

    return data.status === 'healthy';
  } catch (error) {
    console.error('Backend status check failed:', error);
    const backendStatus = document.getElementById('backend-status');
    if (backendStatus) {
      backendStatus.textContent = 'Disconnected';
      backendStatus.className = 'text-red-600';
    }
    return false;
  }
}

// FIXED: Make updateSystemStatus globally available
window.updateSystemStatus = function (event) {
  try {
    if (event.detail.xhr.status === 200) {
      const response = JSON.parse(event.detail.xhr.responseText);

      // Update Alpine.js store if available
      if (window.Alpine) {
        const appData = document.querySelector('[x-data="appData()"]');
        if (appData && appData.__x) {
          appData.__x.$data.systemStatus.connected =
            response.status === 'healthy';
          appData.__x.$data.systemStatus.message =
            response.status === 'healthy' ? 'Connected' : 'Disconnected';
          appData.__x.$data.systemStatus.lastChecked =
            new Date().toLocaleTimeString();
        }
      }

      // Also update sidebar status
      checkBackendStatus();
    } else {
      // Handle error status
      if (window.Alpine) {
        const appData = document.querySelector('[x-data="appData()"]');
        if (appData && appData.__x) {
          appData.__x.$data.systemStatus.connected = false;
          appData.__x.$data.systemStatus.message = 'Error';
        }
      }
    }
  } catch (error) {
    console.error('Error in updateSystemStatus:', error);
  }
};

// Utility Functions
function showGlobalLoading() {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) {
    overlay.classList.remove('hidden');
    overlay.classList.add('flex');
  }
}

function hideGlobalLoading() {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) {
    overlay.classList.add('hidden');
    overlay.classList.remove('flex');
  }
}

function showNotification(message, type = 'info', duration = 5000) {
  const notification = document.createElement('div');
  notification.className = `alert alert-${type} animate-slide-up fixed top-20 right-4 z-50`;
  notification.innerHTML = `
        <div class="flex items-center justify-between">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" 
                    class="ml-4 text-white hover:text-gray-200">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        </div>
    `;

  document.body.appendChild(notification);

  setTimeout(() => {
    if (notification.parentNode) {
      notification.remove();
    }
  }, duration);
}

function getErrorMessage(xhr) {
  try {
    const response = JSON.parse(xhr.responseText);
    return response.message || response.error || 'An error occurred';
  } catch (e) {
    return `HTTP ${xhr.status}: ${xhr.statusText}`;
  }
}

// File Upload Functions
function initializeFileUpload() {
  const dropZones = document.querySelectorAll('.file-drop-zone');

  dropZones.forEach((zone) => {
    zone.addEventListener('dragover', function (e) {
      e.preventDefault();
      this.classList.add('dragover');
    });

    zone.addEventListener('dragleave', function (e) {
      e.preventDefault();
      this.classList.remove('dragover');
    });

    zone.addEventListener('drop', function (e) {
      e.preventDefault();
      this.classList.remove('dragover');

      const files = Array.from(e.dataTransfer.files);
      handleFileUpload(files);
    });
  });
}

function handleFileUpload(files) {
  if (!files || files.length === 0) return;

  const formData = new FormData();
  files.forEach((file) => formData.append('files', file));

  showGlobalLoading();

  fetch('/api/upload', {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
    .then((response) => response.json())
    .then((data) => {
      hideGlobalLoading();

      if (data.status === 'success') {
        showNotification(
          `Uploaded ${data.count} file(s) successfully`,
          'success'
        );
        updateFileList(data.files);
      } else {
        showNotification(data.error || 'Upload failed', 'error');
      }
    })
    .catch((error) => {
      hideGlobalLoading();
      showNotification('Upload failed: ' + error.message, 'error');
    });
}

function updateFileList(files) {
  // Implementation for file list updates
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Workflow Visualization Functions
function initializeWorkflowViz() {
  if (typeof mermaid !== 'undefined') {
    mermaid.init();
  }
  initializeCharts();
}

function initializeCharts() {
  // Chart initialization code here
}

// Chat Functions
function initializeChatAutoScroll() {
  const chatContainer = document.getElementById('chat-messages');
  if (chatContainer) {
    const observer = new MutationObserver(() => {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    });

    observer.observe(chatContainer, {
      childList: true,
      subtree: true,
    });
  }
}

// Keyboard Shortcuts
document.addEventListener('keydown', function (e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    const chatInput = document.getElementById('message-input');
    if (chatInput && document.activeElement === chatInput) {
      sendMessage(); // This function is defined in index.jinja2
    }
  }

  if (e.key === 'Escape') {
    const mobileMenu = document.querySelector('[x-data]');
    if (mobileMenu && mobileMenu.__x) {
      mobileMenu.__x.$data.mobileMenuOpen = false;
    }
  }
});

// Initialize dark mode on load
document.addEventListener('DOMContentLoaded', function () {
  const darkMode = localStorage.getItem('darkMode') === 'true';
  document.documentElement.classList.toggle('dark', darkMode);

  // Start periodic status checks
  setInterval(checkBackendStatus, 30000); // Check every 30 seconds
});

// Export for global use
window.appUtils = {
  showNotification,
  formatFileSize,
  checkBackendStatus,
};
