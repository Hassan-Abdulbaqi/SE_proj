// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// State Management
const state = {
    user: null,
    services: [],
    orders: []
};

// DOM Elements
const authSection = document.getElementById('auth-section');
const dashboardSection = document.getElementById('dashboard-section');
const userInfo = document.getElementById('user-info');
const logoutBtn = document.getElementById('logout-btn');

const signupForm = document.getElementById('signup-form');
const signinForm = document.getElementById('signin-form');

const servicesList = document.getElementById('services-list');
const calculatorForm = document.getElementById('calculator-form');
const calculatorResult = document.getElementById('calculator-result');
const calcServiceSelect = document.getElementById('calc-service-select');

const checkoutForm = document.getElementById('checkout-form');
const checkoutResult = document.getElementById('checkout-result');
const checkoutServiceSelect = document.getElementById('checkout-service-select');

const ordersList = document.getElementById('orders-list');
const refreshOrdersBtn = document.getElementById('refresh-orders-btn');

// Utility Functions
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    const container = document.getElementById('toast-container');
    container.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 100);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IQ', {
        style: 'currency',
        currency: 'IQD',
        minimumFractionDigits: 2
    }).format(amount);
}

// API Functions
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };
    
    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            // Handle field-specific errors
            if (data.mobile_number) {
                throw new Error(data.mobile_number[0] || data.mobile_number);
            }
            if (data.password) {
                throw new Error(data.password[0] || data.password);
            }
            if (data.username) {
                throw new Error(data.username[0] || data.username);
            }
            // Handle general errors
            if (data.non_field_errors) {
                throw new Error(data.non_field_errors[0] || data.non_field_errors);
            }
            throw new Error(data.error || data.detail || 'Request failed');
        }
        
        return data;
    } catch (error) {
        throw error;
    }
}

// Authentication Functions
async function signup(formData) {
    try {
        const data = await apiRequest('/auth/signup/', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        state.user = data.user;
        showToast('Account created successfully!', 'success');
        showDashboard();
        loadServices();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function signin(formData) {
    try {
        const data = await apiRequest('/auth/signin/', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        state.user = data.user;
        showToast('Signed in successfully!', 'success');
        showDashboard();
        loadServices();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function logout() {
    try {
        await apiRequest('/auth/signout/', { method: 'POST' });
        state.user = null;
        state.services = [];
        state.orders = [];
        showToast('Logged out successfully', 'success');
        showAuth();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// Services Functions
async function loadServices() {
    try {
        const services = await apiRequest('/services/');
        state.services = services;
        renderServices();
        populateServiceSelects();
    } catch (error) {
        showToast('Failed to load services', 'error');
    }
}

function renderServices() {
    servicesList.innerHTML = state.services.map(service => `
        <div class="service-card">
            <div class="service-icon">${getServiceIcon(service.service_type)}</div>
            <h3>${service.name_en}</h3>
            <p class="service-name-ar">${service.name_ar}</p>
            <div class="service-price">
                <strong>${formatCurrency(service.price_per_unit)}</strong>
                <span>per ${service.unit_name}</span>
            </div>
        </div>
    `).join('');
}

function populateServiceSelects() {
    const options = state.services.map(service => 
        `<option value="${service.id}">${service.name_en} - ${formatCurrency(service.price_per_unit)}/${service.unit_name}</option>`
    ).join('');
    
    calcServiceSelect.innerHTML = '<option value="">-- Choose Service --</option>' + options;
    checkoutServiceSelect.innerHTML = '<option value="">-- Choose Service --</option>' + options;
}

function getServiceIcon(type) {
    const icons = {
        electricity: '⚡',
        water: '💧',
        gas: '🔥'
    };
    return icons[type] || '📦';
}

// Calculator Functions
async function calculateCost(serviceId, quantity) {
    try {
        const data = await apiRequest(`/services/calculate_cost/?service_id=${serviceId}&quantity=${quantity}`);
        
        calculatorResult.innerHTML = `
            <div class="result-success">
                <h3>Cost Calculation</h3>
                <div class="result-details">
                    <p><strong>Service:</strong> ${data.service.name_en} (${data.service.name_ar})</p>
                    <p><strong>Quantity:</strong> ${data.quantity} ${data.service.unit_name}</p>
                    <p><strong>Price per unit:</strong> ${formatCurrency(data.service.price_per_unit)}</p>
                    <p class="result-total"><strong>Total Cost:</strong> ${formatCurrency(data.cost)}</p>
                </div>
            </div>
        `;
    } catch (error) {
        calculatorResult.innerHTML = `<div class="result-error">${error.message}</div>`;
    }
}

// Order Functions
async function createOrder(formData) {
    try {
        const data = await apiRequest('/orders/checkout/', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        showToast('Order created successfully!', 'success');
        checkoutResult.innerHTML = `
            <div class="result-success">
                <h3>Order Created! 🎉</h3>
                <div class="result-details">
                    <p><strong>Order ID:</strong> ${data.order.id}</p>
                    <p><strong>Service:</strong> ${data.order.service.name_en}</p>
                    <p><strong>Quantity:</strong> ${data.order.quantity} ${data.order.service.unit_name}</p>
                    <p><strong>Service Cost:</strong> ${formatCurrency(data.order.service_cost)}</p>
                    <p><strong>Delivery Cost:</strong> ${formatCurrency(data.order.delivery_cost)}</p>
                    <p class="result-total"><strong>Total:</strong> ${formatCurrency(data.order.total_cost)}</p>
                    <p><strong>Status:</strong> <span class="status-badge status-${data.order.status}">${data.order.status}</span></p>
                </div>
            </div>
        `;
        
        checkoutForm.reset();
        loadOrders();
    } catch (error) {
        checkoutResult.innerHTML = `<div class="result-error">${error.message}</div>`;
        showToast(error.message, 'error');
    }
}

async function loadOrders() {
    try {
        const orders = await apiRequest('/orders/');
        state.orders = orders;
        renderOrders();
    } catch (error) {
        showToast('Failed to load orders', 'error');
    }
}

function renderOrders() {
    if (state.orders.length === 0) {
        ordersList.innerHTML = '<p class="empty-state">No orders yet. Place your first order above!</p>';
        return;
    }
    
    ordersList.innerHTML = state.orders.map(order => `
        <div class="order-card">
            <div class="order-header">
                <h4>Order #${order.id}</h4>
                <span class="status-badge status-${order.status}">${order.status}</span>
            </div>
            <div class="order-body">
                <p><strong>Service:</strong> ${order.service.name_en} (${order.service.name_ar})</p>
                <p><strong>Quantity:</strong> ${order.quantity} ${order.service.unit_name}</p>
                <p><strong>Location:</strong> ${order.location}</p>
                <p><strong>Payment:</strong> ${order.payment_method}</p>
                <p><strong>Service Cost:</strong> ${formatCurrency(order.service_cost)}</p>
                <p><strong>Delivery Cost:</strong> ${formatCurrency(order.delivery_cost)}</p>
                <p class="order-total"><strong>Total:</strong> ${formatCurrency(order.total_cost)}</p>
                ${order.notes ? `<p><strong>Notes:</strong> ${order.notes}</p>` : ''}
                <p class="order-date"><small>Ordered: ${new Date(order.created_at).toLocaleString()}</small></p>
            </div>
        </div>
    `).join('');
}

// UI Functions
function showAuth() {
    authSection.style.display = 'block';
    dashboardSection.style.display = 'none';
    userInfo.textContent = '';
    logoutBtn.style.display = 'none';
}

function showDashboard() {
    authSection.style.display = 'none';
    dashboardSection.style.display = 'block';
    userInfo.textContent = `Welcome, ${state.user.username}!`;
    logoutBtn.style.display = 'inline-block';
    loadOrders();
}

// Event Listeners
signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = Object.fromEntries(new FormData(e.target));
    
    if (formData.password !== formData.password_confirm) {
        showToast('Passwords do not match', 'error');
        return;
    }
    
    if (!formData.email) {
        delete formData.email;
    }
    
    await signup(formData);
});

signinForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = Object.fromEntries(new FormData(e.target));
    await signin(formData);
});

logoutBtn.addEventListener('click', logout);

calculatorForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = Object.fromEntries(new FormData(e.target));
    await calculateCost(formData.service_id, formData.quantity);
});

checkoutForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = Object.fromEntries(new FormData(e.target));
    
    // Convert numeric fields
    formData.service_id = parseInt(formData.service_id);
    formData.quantity = parseFloat(formData.quantity);
    formData.delivery_cost = parseFloat(formData.delivery_cost);
    formData.estimated_delivery_time = parseInt(formData.estimated_delivery_time);
    
    if (!formData.notes) {
        delete formData.notes;
    }
    
    await createOrder(formData);
});

refreshOrdersBtn.addEventListener('click', loadOrders);

// Initialize
async function init() {
    try {
        // Try to get profile (check if already logged in)
        const profile = await apiRequest('/profile/');
        state.user = profile;
        showDashboard();
        loadServices();
    } catch (error) {
        // Not logged in, show auth
        showAuth();
    }
}

// Start the app
init();
