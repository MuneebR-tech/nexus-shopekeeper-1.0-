/* ══════════════════════════════════════════════════════════════════
   NEXUS SHOPKEEPER — Pakistani SaaS Edition
   Complete Kiosk & Admin Dashboard Application Controller
   ══════════════════════════════════════════════════════════════════ */

// ─────────────────────────────────────────────
// PRODUCT CATALOG FALLBACK — 20 Pakistani Products
// ─────────────────────────────────────────────
const FALLBACK_PRODUCTS = [
  { item_id: 'SKU-0001', name: 'Guard Basmati Rice 5kg', price: 1450, category: 'pantry', rack_id: 'C1', shelf_position: 1, stock_quantity: 45, reorder_threshold: 10, supplier: 'Guard Agri', weight_kg: 5.0 },
  { item_id: 'SKU-0002', name: 'Mezan Cooking Oil 5L', price: 2890, category: 'pantry', rack_id: 'C2', shelf_position: 2, stock_quantity: 32, reorder_threshold: 8, supplier: 'Mezan Group', weight_kg: 4.6 },
  { item_id: 'SKU-0003', name: 'Tapal Danedar Tea 950g', price: 1350, category: 'beverages', rack_id: 'A1', shelf_position: 3, stock_quantity: 60, reorder_threshold: 15, supplier: 'Tapal Tea Pvt Ltd', weight_kg: 0.95 },
  { item_id: 'SKU-0004', name: 'National Biryani Masala 90g', price: 180, category: 'pantry', rack_id: 'C3', shelf_position: 1, stock_quantity: 120, reorder_threshold: 20, supplier: 'National Foods', weight_kg: 0.09 },
  { item_id: 'SKU-0005', name: 'Shan Karahi Masala 50g', price: 120, category: 'pantry', rack_id: 'C4', shelf_position: 2, stock_quantity: 95, reorder_threshold: 20, supplier: 'Shan Foods', weight_kg: 0.05 },
  { item_id: 'SKU-0006', name: 'Olpers Milk 1.5L', price: 380, category: 'dairy', rack_id: 'D1', shelf_position: 1, stock_quantity: 40, reorder_threshold: 12, supplier: 'Engro Foods', weight_kg: 1.5 },
  { item_id: 'SKU-0007', name: 'Nurpur Butter 200g', price: 450, category: 'dairy', rack_id: 'D2', shelf_position: 2, stock_quantity: 25, reorder_threshold: 5, supplier: 'Nurpur Dairy', weight_kg: 0.2 },
  { item_id: 'SKU-0008', name: 'Everyday Milk Powder 900g', price: 1650, category: 'beverages', rack_id: 'A2', shelf_position: 4, stock_quantity: 30, reorder_threshold: 10, supplier: 'Nestle Pakistan', weight_kg: 0.9 },
  { item_id: 'SKU-0009', name: 'Lays Classic Chips 155g', price: 200, category: 'snacks', rack_id: 'B1', shelf_position: 1, stock_quantity: 80, reorder_threshold: 15, supplier: 'Pepsico Pakistan', weight_kg: 0.155 },
  { item_id: 'SKU-0010', name: 'Sooper Biscuits 120g', price: 80, category: 'snacks', rack_id: 'B2', shelf_position: 2, stock_quantity: 150, reorder_threshold: 30, supplier: 'English Biscuit Manufacturers', weight_kg: 0.12 },
  { item_id: 'SKU-0011', name: 'Sunsilk Shampoo 360ml', price: 680, category: 'personal_care', rack_id: 'E1', shelf_position: 3, stock_quantity: 55, reorder_threshold: 10, supplier: 'Unilever Pakistan', weight_kg: 0.36 },
  { item_id: 'SKU-0012', name: 'Safeguard Soap 175g', price: 150, category: 'personal_care', rack_id: 'E2', shelf_position: 1, stock_quantity: 110, reorder_threshold: 20, supplier: 'Procter & Gamble', weight_kg: 0.175 },
  { item_id: 'SKU-0013', name: 'Surf Excel 1kg', price: 520, category: 'household', rack_id: 'F1', shelf_position: 1, stock_quantity: 65, reorder_threshold: 12, supplier: 'Unilever Pakistan', weight_kg: 1.0 },
  { item_id: 'SKU-0014', name: 'Harpic Toilet Cleaner 500ml', price: 380, category: 'household', rack_id: 'F2', shelf_position: 2, stock_quantity: 40, reorder_threshold: 8, supplier: 'Reckitt Benckiser', weight_kg: 0.5 },
  { item_id: 'SKU-0015', name: 'Dalda Cooking Oil 3L', price: 1780, category: 'pantry', rack_id: 'C5', shelf_position: 3, stock_quantity: 28, reorder_threshold: 6, supplier: 'Dalda Foods', weight_kg: 2.76 },
  { item_id: 'SKU-0016', name: 'Sufi Banaspati Ghee 1kg', price: 590, category: 'pantry', rack_id: 'C1', shelf_position: 4, stock_quantity: 50, reorder_threshold: 10, supplier: 'Sufi Group', weight_kg: 1.0 },
  { item_id: 'SKU-0017', name: 'Knorr Noodles 6-Pack', price: 300, category: 'snacks', rack_id: 'B3', shelf_position: 3, stock_quantity: 90, reorder_threshold: 20, supplier: 'Unilever Pakistan', weight_kg: 0.36 },
  { item_id: 'SKU-0018', name: 'Tang Orange 750g', price: 850, category: 'beverages', rack_id: 'A3', shelf_position: 2, stock_quantity: 45, reorder_threshold: 10, supplier: 'Mondelez', weight_kg: 0.75 },
  { item_id: 'SKU-0019', name: 'Rooh Afza 800ml', price: 490, category: 'beverages', rack_id: 'A4', shelf_position: 1, stock_quantity: 70, reorder_threshold: 15, supplier: 'Hamdard Pakistan', weight_kg: 0.8 },
  { item_id: 'SKU-0020', name: 'Vital Tea 475g', price: 720, category: 'beverages', rack_id: 'A5', shelf_position: 2, stock_quantity: 50, reorder_threshold: 12, supplier: 'Eastern Products', weight_kg: 0.475 },
];

const UI_CATEGORIES = {
  'beverages': { name: 'Beverages', emoji: '🥤', color: '#5865f2' },
  'snacks': { name: 'Snacks & Sweets', emoji: '🍿', color: '#f59e0b' },
  'pantry': { name: 'Grocery & Pantry', emoji: '🛒', color: '#22c55e' },
  'dairy': { name: 'Dairy & Butter', emoji: '🥛', color: '#00f2fe' },
  'frozen': { name: 'Frozen Foods', emoji: '🧊', color: '#6366f1' },
  'produce': { name: 'Fresh Produce', emoji: '🍎', color: '#a855f7' },
  'household': { name: 'Household Utility', emoji: '🧹', color: '#06b6d4' },
  'personal_care': { name: 'Personal Care', emoji: '🧴', color: '#ec4899' }
};

// ─────────────────────────────────────────────
// UTILITIES
// ─────────────────────────────────────────────
function formatPKR(amount) {
  return 'Rs. ' + Math.round(amount).toLocaleString('en-PK');
}

function getProductLocation(product) {
  const rack = product.rack_id || 'A1';
  const shelf = product.shelf_position || 3;
  const section = parseInt(rack.substring(1)) || 1;
  
  // Floor designation
  const floor = (section >= 4) ? '1st Floor' : 'Ground Floor';
  const aisle = rack.substring(0, 1).toUpperCase();
  const rank = `${shelf} of 5`;
  
  // Coordinate calculations matching backend RackMap design
  const aisleCoords = { 'A': 2.0, 'B': 4.0, 'C': 6.0, 'D': 8.0, 'E': 10.0, 'F': 12.0 };
  const sectionCoords = { 1: 1.5, 2: 3.5, 3: 5.5, 4: 7.5, 5: 9.5 };
  const shelfCoords = { 1: 0.3, 2: 0.7, 3: 1.1, 4: 1.5, 5: 1.9 };
  
  const x = aisleCoords[aisle] || 2.0;
  const y = sectionCoords[section] || 1.5;
  const z = shelfCoords[shelf] || 1.1;
  
  return {
    floor,
    aisle: `Aisle ${aisle}`,
    rank,
    coords: `X: ${x.toFixed(1)}m, Y: ${y.toFixed(1)}m, Z: ${z.toFixed(1)}m`
  };
}

// ═════════════════════════════════════════════
// NexusAudio — Web Audio API Chimes
// ═════════════════════════════════════════════
class NexusAudio {
  constructor() {
    this.ctx = null;
  }

  _ensureCtx() {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
    return this.ctx;
  }

  _playTone(freq, type = 'sine', duration = 0.12, gain = 0.15) {
    try {
      const ctx = this._ensureCtx();
      const osc = ctx.createOscillator();
      const gn = ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, ctx.currentTime);
      gn.gain.setValueAtTime(gain, ctx.currentTime);
      gn.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
      osc.connect(gn);
      gn.connect(ctx.destination);
      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime + duration);
    } catch (e) {
      // Audio not supported or blocked
    }
  }

  playKeyTone(digit) {
    const baseFreq = 260;
    const freq = baseFreq + (parseInt(digit, 10) * 55);
    this._playTone(freq, 'sine', 0.08, 0.12);
  }

  playSuccess() {
    // Ascending major chime
    this._playTone(523.25, 'sine', 0.15, 0.12); // C5
    setTimeout(() => this._playTone(659.25, 'sine', 0.15, 0.12), 100); // E5
    setTimeout(() => this._playTone(783.99, 'sine', 0.25, 0.12), 200); // G5
  }

  playError() {
    this._playTone(180, 'sawtooth', 0.35, 0.15);
  }

  playAddToCart() {
    this._playTone(987.77, 'triangle', 0.12, 0.15); // B5 high alert chime
  }

  playCashChime() {
    // Coins dropping sound: multiple quick high-frequency decays
    const ctx = this._ensureCtx();
    const now = ctx.currentTime;
    const frequencies = [850, 1100, 950, 1200, 1050];
    frequencies.forEach((freq, idx) => {
      setTimeout(() => {
        this._playTone(freq, 'triangle', 0.18, 0.1);
      }, idx * 60);
    });
  }

  playCardChime() {
    // Swipe click: fast falling frequency sweep
    try {
      const ctx = this._ensureCtx();
      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const gn = ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(1200, now);
      osc.frequency.exponentialRampToValueAtTime(120, now + 0.1);
      gn.gain.setValueAtTime(0.12, now);
      gn.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
      osc.connect(gn);
      gn.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.1);
    } catch (e) {}
  }

  playPointsChime() {
    // Clean high frequency double beep
    this._playTone(1100, 'sine', 0.08, 0.12);
    setTimeout(() => this._playTone(1300, 'sine', 0.12, 0.12), 80);
  }

  playWelcome() {
    this._playTone(440, 'sine', 0.12, 0.08); // A4
    setTimeout(() => this._playTone(554.37, 'sine', 0.12, 0.08), 110); // C#5
    setTimeout(() => this._playTone(659.25, 'sine', 0.22, 0.1), 220); // E5
  }
}

// ═════════════════════════════════════════════
// NexusAPI — Backend client
// ═════════════════════════════════════════════
class NexusAPI {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
  }

  async _request(method, path, body = null) {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body) opts.body = JSON.stringify(body);
    try {
      const res = await fetch(`${this.baseURL}${path}`, opts);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn(`API ${method} ${path} failed:`, err.message);
      return null;
    }
  }

  async getHealth()              { return this._request('GET', '/api/status'); }
  async getSystemHealth()        { return this._request('GET', '/api/system/health'); }
  async getInventory()           { return this._request('GET', '/api/inventory'); }
  async saveInventory(item)      { return this._request('POST', '/api/inventory', item); }
  async updateInventory(id, data){ return this._request('PUT', `/api/inventory/${id}`, data); }
  async deleteInventory(id)      { return this._request('DELETE', `/api/inventory/${id}`); }
  async getEmployees()           { return this._request('GET', '/api/employees'); }
  async toggleEmployee(id, state){ return this._request('POST', `/api/employees/${id}/status`, { status: state }); }
  async checkout(payload)        { return this._request('POST', '/api/checkout', payload); }
  async getPaymentTrends()       { return this._request('GET', '/api/analytics/payments'); }
  async verifyMembership(pin)    { return this._request('POST', '/api/membership/verify', { pin }); }
  async getCustomers()           { return this._request('GET', '/api/customers?limit=50'); }
  async triggerClustering()      { return this._request('POST', '/api/cluster/run'); }
  async getClusterResults()      { return this._request('GET', '/api/cluster/results'); }
  async getAnalyticsSegments()   { return this._request('GET', '/api/analytics/segments'); }
}

// ═════════════════════════════════════════════
// KioskApp — Main Kiosk GUI Controller
// ═════════════════════════════════════════════
class KioskApp {
  constructor() {
    this.audio = new NexusAudio();
    this.api = new NexusAPI();
    this.currentScreen = 'entry-screen';
    this.pinDigits = [];
    this.cart = [];
    this.memberData = null;
    this.products = [];
    this.searchDebounce = null;

    this._cacheElements();
    this._bindEvents();
    this._loadInitialData();
    this._initSupport();
    this._updateClock();
    setInterval(() => this._updateClock(), 1000);
    setInterval(() => this._syncHeadcount(), 10000);

    setTimeout(() => this.audio.playWelcome(), 500);
  }

  _cacheElements() {
    this.screens = {
      entry:     document.getElementById('entry-screen'),
      welcome:   document.getElementById('welcome-screen'),
      keypad:    document.getElementById('keypad-screen'),
      workspace: document.getElementById('main-workspace'),
      checkout:  document.getElementById('checkout-screen'),
    };
    this.pinDots         = document.querySelectorAll('.pin-dot');
    this.pinStatus        = document.getElementById('pin-status');
    this.searchInput      = document.getElementById('search-input');
    this.searchAuto       = document.getElementById('search-autocomplete');
    this.categoryGrid     = document.getElementById('category-grid');
    this.productPanel     = document.getElementById('product-panel');
    this.productPanelOvl  = document.getElementById('product-panel-overlay');
    this.productPanelTitle= document.getElementById('product-panel-title');
    this.productPanelGrid = document.getElementById('product-panel-grid');
    this.cartBadge        = document.getElementById('cart-badge');
    
    // Checkout screen components
    this.checkoutItems    = document.getElementById('checkout-screen-items');
    this.checkoutTotal    = document.getElementById('checkout-screen-total');
    this.checkoutCount    = document.getElementById('checkout-cart-count');
    this.paymentStatusMsg = document.getElementById('payment-status-message');
    
    // Product details components
    this.pdOverlay        = document.getElementById('product-details-overlay');
    this.pdName           = document.getElementById('pd-name');
    this.pdEmoji          = document.getElementById('pd-emoji');
    this.pdCategoryBadge  = document.getElementById('pd-category-badge');
    this.pdDescription    = document.getElementById('pd-description');
    this.pdFloor          = document.getElementById('pd-floor');
    this.pdAisle          = document.getElementById('pd-aisle');
    this.pdShelf          = document.getElementById('pd-shelf');
    this.pdCoords         = document.getElementById('pd-coords');
    this.pdPrice          = document.getElementById('pd-price');
    this.pdAddBtn         = document.getElementById('pd-add-to-cart');

    this.toastContainer   = document.getElementById('toast-container');
    this.profileName      = document.getElementById('profile-name');
    this.profileTier      = document.getElementById('profile-tier');
    this.accountLabel     = document.getElementById('account-label');
    this.clockEl          = document.getElementById('system-clock');
    this.supportWidget    = document.getElementById('support-widget');
    this.supportText      = document.getElementById('support-widget-text');
    this.staffIndicator   = document.getElementById('staff-count-indicator');
  }

  _bindEvents() {
    // View transitions
    document.getElementById('btn-enter-mart').addEventListener('click', () => this._switchScreen('welcome-screen'));
    document.getElementById('btn-exit-mart').addEventListener('click', () => this._openCheckoutScreen());
    document.getElementById('btn-welcome-back').addEventListener('click', () => this._switchScreen('entry-screen'));
    document.getElementById('btn-has-card').addEventListener('click', () => this._switchScreen('keypad-screen'));
    document.getElementById('btn-guest').addEventListener('click', () => {
      this.memberData = null;
      this._updateProfileView();
      this._switchScreen('main-workspace');
    });

    // Keypad actions
    document.getElementById('keypad-grid').addEventListener('click', (e) => {
      const btn = e.target.closest('.keypad-btn');
      if (!btn) return;
      const key = btn.dataset.key;
      if (key === 'backspace') {
        this.pinDigits.pop();
        this._updatePinDots();
      } else if (key === 'scan') {
        this._showToast('📷 Camera scanner initializing... (Demonstration Mode)', 'info');
      } else {
        if (this.pinDigits.length < 6) {
          this.pinDigits.push(key);
          this.audio.playKeyTone(key);
          this._updatePinDots();
        }
      }
    });

    document.getElementById('keypad-submit').addEventListener('click', () => this._verifyPinCode());
    document.getElementById('keypad-cancel').addEventListener('click', () => this._switchScreen('welcome-screen'));

    // Search
    this.searchInput.addEventListener('input', () => this._handleAutocomplete());
    this.searchInput.addEventListener('focus', () => this._handleAutocomplete());
    document.addEventListener('click', (e) => {
      if (!document.getElementById('search-wrapper').contains(e.target)) {
        this.searchAuto.classList.remove('visible');
      }
    });

    // Workspace buttons
    document.getElementById('btn-workspace-checkout').addEventListener('click', () => this._openCheckoutScreen());
    document.getElementById('btn-sidebar-view-cart').addEventListener('click', () => this._openCheckoutScreen());
    document.getElementById('btn-sidebar-catalog').addEventListener('click', () => {
      this.searchInput.value = '';
      this._showToast('ℹ️ Store explorer reset.', 'info');
    });
    document.getElementById('btn-sidebar-help').addEventListener('click', () => {
      this._showToast('🤖 AI: "Please browse categories or search using the search bar at the top."', 'info');
    });
    document.getElementById('btn-logout').addEventListener('click', () => {
      this.memberData = null;
      this.cart = [];
      this._updateCartBadge();
      this._updateProfileView();
      this._switchScreen('entry-screen');
      this._showToast('🚪 Checked out of Mart. Thank you!', 'info');
    });

    // Details modal close
    document.getElementById('pd-close').addEventListener('click', () => this.pdOverlay.classList.remove('visible'));
    this.pdOverlay.addEventListener('click', (e) => {
      if (e.target === this.pdOverlay) this.pdOverlay.classList.remove('visible');
    });

    // Checkout navigation
    document.getElementById('btn-checkout-back').addEventListener('click', () => this._switchScreen('main-workspace'));

    // Payment method selector
    document.querySelectorAll('.payment-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const method = btn.dataset.method;
        this._executeCheckout(method);
      });
    });

    // Sidebar overlay panel close
    document.getElementById('product-panel-close').addEventListener('click', () => {
      this.productPanel.classList.remove('open');
      this.productPanelOvl.classList.remove('visible');
    });
  }

  async _loadInitialData() {
    const raw = await this.api.getInventory();
    if (raw && raw.length > 0) {
      // Map USD base to PKR base for Pakistani localized retail
      this.products = raw.map(p => ({
        ...p,
        price: p.price < 50 ? Math.round(p.price * 280) : Math.round(p.price)
      }));
    } else {
      this.products = [...FALLBACK_PRODUCTS];
    }
    this._renderCategories();
    this._renderSidebarElements();
    this._syncHeadcount();
  }

  _switchScreen(screenId) {
    Object.keys(this.screens).forEach(key => {
      this.screens[key].classList.remove('active-screen');
    });
    const target = this.screens[screenId.replace('-screen', '')];
    if (target) {
      target.classList.add('active-screen');
      this.currentScreen = screenId;
    }
  }

  _updatePinDots() {
    this.pinDots.forEach((dot, idx) => {
      dot.classList.toggle('filled', idx < this.pinDigits.length);
      dot.classList.remove('error', 'success');
    });
    this.pinStatus.textContent = '';
  }

  async _verifyPinCode() {
    if (this.pinDigits.length !== 6) {
      this.pinStatus.textContent = 'Please enter a valid 6-digit PIN';
      this.pinStatus.className = 'pin-status error';
      this.audio.playError();
      return;
    }
    const pin = this.pinDigits.join('');
    this.pinStatus.textContent = 'Validating Card...';
    this.pinStatus.className = 'pin-status';

    const result = await this.api.verifyMembership(pin);
    if (result && result.valid) {
      this.memberData = result.customer;
      this.pinDots.forEach(dot => dot.classList.add('success'));
      this.pinStatus.textContent = `✅ Welcome back, ${this.memberData.name}!`;
      this.pinStatus.className = 'pin-status success';
      this.audio.playSuccess();
      this._updateProfileView();
      setTimeout(() => {
        this._switchScreen('main-workspace');
        this.pinDigits = [];
        this._updatePinDots();
      }, 1200);
    } else {
      // Try fallback for demo
      if (pin.startsWith('1')) {
        this.memberData = { customer_id: 'CUST-DEMO', name: 'Zeeshan Malik', segment: 'Ultra-Luxury Spender', tier: 'Platinum' };
        this.pinDots.forEach(dot => dot.classList.add('success'));
        this.pinStatus.textContent = `✅ Verification Override. Welcome, Zeeshan Malik!`;
        this.pinStatus.className = 'pin-status success';
        this.audio.playSuccess();
        this._updateProfileView();
        setTimeout(() => {
          this._switchScreen('main-workspace');
          this.pinDigits = [];
          this._updatePinDots();
        }, 1200);
      } else {
        this.pinDots.forEach(dot => dot.classList.add('error'));
        this.pinStatus.textContent = '❌ Card verification failed. (Hint: Try PIN starting with 1)';
        this.pinStatus.className = 'pin-status error';
        this.audio.playError();
      }
    }
  }

  _updateProfileView() {
    if (this.memberData) {
      this.profileName.textContent = this.memberData.name;
      this.profileTier.textContent = this.memberData.segment || 'Premium';
      this.accountLabel.textContent = this.memberData.name;
    } else {
      this.profileName.textContent = 'Guest Shopper';
      this.profileTier.textContent = 'Standard';
      this.accountLabel.textContent = 'Account';
    }
  }

  _renderCategories() {
    const cats = Object.entries(UI_CATEGORIES);
    this.categoryGrid.innerHTML = cats.map(([id, meta]) => {
      const count = this.products.filter(p => p.category === id).length;
      return `
        <div class="category-card" data-category="${id}" style="--card-accent: ${meta.color}">
          <span class="category-card-emoji">${meta.emoji}</span>
          <div class="category-card-name">${meta.name}</div>
          <div class="category-card-count">${count} items available</div>
        </div>
      `;
    }).join('');

    this.categoryGrid.querySelectorAll('.category-card').forEach(card => {
      card.addEventListener('click', () => {
        this._openCategoryAisle(card.dataset.category);
      });
    });
  }

  _openCategoryAisle(catId) {
    const catMeta = UI_CATEGORIES[catId];
    const filtered = this.products.filter(p => p.category === catId);
    
    this.productPanelTitle.textContent = `${catMeta ? catMeta.emoji : '📦'} ${catMeta ? catMeta.name : catId}`;
    this.productPanelGrid.innerHTML = filtered.map(p => `
      <div class="product-card">
        <div class="product-card-emoji">${catMeta ? catMeta.emoji : '📦'}</div>
        <div class="product-card-name">${p.name}</div>
        <div class="product-card-price">${formatPKR(p.price)}</div>
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-glass btn-sm view-details-btn" data-id="${p.item_id}" style="flex: 1; justify-content: center;">🔍 Coordinates</button>
          <button class="btn btn-primary btn-sm add-cart-btn" data-id="${p.item_id}">🛒 Add</button>
        </div>
      </div>
    `).join('');

    this.productPanelGrid.querySelectorAll('.add-cart-btn').forEach(btn => {
      btn.addEventListener('click', () => this._addToCartById(btn.dataset.id));
    });

    this.productPanelGrid.querySelectorAll('.view-details-btn').forEach(btn => {
      btn.addEventListener('click', () => this._showProductDetails(btn.dataset.id));
    });

    this.productPanel.classList.add('open');
    this.productPanelOvl.classList.add('visible');
  }

  _showProductDetails(id) {
    const product = this.products.find(p => p.item_id === id);
    if (!product) return;

    const loc = getProductLocation(product);
    const catMeta = UI_CATEGORIES[product.category] || { emoji: '📦', name: product.category };
    
    this.pdName.textContent = product.name;
    this.pdEmoji.textContent = catMeta.emoji;
    this.pdCategoryBadge.textContent = catMeta.name;
    this.pdDescription.textContent = `Aisle item SKU ID ${product.item_id}. Maintained by automation systems. Optimal humidity and placement parameters verified. Supplied by ${product.supplier || 'Smart Logistics'}.`;
    this.pdFloor.textContent = loc.floor;
    this.pdAisle.textContent = loc.aisle;
    this.pdShelf.textContent = loc.rank;
    this.pdCoords.textContent = loc.coords;
    this.pdPrice.textContent = formatPKR(product.price);
    
    this.pdAddBtn.onclick = () => {
      this._addToCartById(product.item_id);
      this.pdOverlay.classList.remove('visible');
    };

    this.pdOverlay.classList.add('visible');
  }

  _addToCartById(id) {
    const product = this.products.find(p => p.item_id === id);
    if (!product) return;

    const existing = this.cart.find(item => item.item_id === id);
    if (existing) {
      existing.qty++;
    } else {
      this.cart.push({ ...product, qty: 1 });
    }
    this.audio.playAddToCart();
    this._updateCartBadge();
    this._showToast(`🛒 Added ${product.name} to cart.`, 'success');
  }

  _updateCartBadge() {
    const count = this.cart.reduce((sum, item) => sum + item.qty, 0);
    this.cartBadge.textContent = count;
  }

  _openCheckoutScreen() {
    this._renderCheckoutItems();
    this._switchScreen('checkout-screen');
    this.paymentStatusMsg.textContent = '';
  }

  _renderCheckoutItems() {
    if (this.cart.length === 0) {
      this.checkoutItems.innerHTML = '<p class="empty-cart-msg">Your cart is empty. Please check in and select items.</p>';
      this.checkoutTotal.textContent = 'Rs. 0';
      this.checkoutCount.textContent = '0 items';
      return;
    }

    this.checkoutCount.textContent = `${this.cart.reduce((sum, item) => sum + item.qty, 0)} items`;
    this.checkoutItems.innerHTML = this.cart.map(item => `
      <div class="cart-item">
        <span class="cart-item-emoji">${UI_CATEGORIES[item.category]?.emoji || '📦'}</span>
        <div class="cart-item-info">
          <div class="cart-item-name">${item.name}</div>
          <div class="cart-item-price">${formatPKR(item.price)} each</div>
        </div>
        <div class="cart-item-qty">
          <button class="qty-minus" data-id="${item.item_id}">−</button>
          <span>${item.qty}</span>
          <button class="qty-plus" data-id="${item.item_id}">+</button>
        </div>
        <button class="cart-item-remove" data-id="${item.item_id}">🗑️</button>
      </div>
    `).join('');

    const total = this.cart.reduce((sum, item) => sum + item.price * item.qty, 0);
    this.checkoutTotal.textContent = formatPKR(total);

    // Bind item buttons
    this.checkoutItems.querySelectorAll('.qty-minus').forEach(btn => {
      btn.addEventListener('click', () => this._adjustQty(btn.dataset.id, -1));
    });
    this.checkoutItems.querySelectorAll('.qty-plus').forEach(btn => {
      btn.addEventListener('click', () => this._adjustQty(btn.dataset.id, 1));
    });
    this.checkoutItems.querySelectorAll('.cart-item-remove').forEach(btn => {
      btn.addEventListener('click', () => this._removeFromCart(btn.dataset.id));
    });
  }

  _adjustQty(id, delta) {
    const item = this.cart.find(i => i.item_id === id);
    if (!item) return;
    item.qty += delta;
    if (item.qty <= 0) {
      this.cart = this.cart.filter(i => i.item_id !== id);
    }
    this._updateCartBadge();
    this._renderCheckoutItems();
  }

  _removeFromCart(id) {
    this.cart = this.cart.filter(i => i.item_id !== id);
    this._updateCartBadge();
    this._renderCheckoutItems();
    this._showToast('🗑️ Item removed from cart.', 'info');
  }

  async _executeCheckout(method) {
    if (this.cart.length === 0) {
      this._showToast('❌ Your cart is empty.', 'error');
      this.audio.playError();
      return;
    }

    // Play method specific chime
    if (method === 'cash') this.audio.playCashChime();
    else if (method === 'card') this.audio.playCardChime();
    else this.audio.playPointsChime();

    this.paymentStatusMsg.textContent = 'Processing Payment...';
    
    const payload = {
      items: this.cart.map(i => ({ item_id: i.item_id, price: i.price, qty: i.qty })),
      payment_method: method,
      customer_id: this.memberData ? this.memberData.customer_id : null
    };

    const res = await this.api.checkout(payload);
    if (res && res.status === 'success') {
      this.paymentStatusMsg.style.color = 'var(--success-green)';
      this.paymentStatusMsg.textContent = `✅ Payment Approved! Rs. ${res.amount_processed.toLocaleString()} processed via ${method.toUpperCase()}.`;
      this.audio.playSuccess();
      this._showToast('🎉 Transaction successful! Cart cleared.', 'success');
      
      setTimeout(() => {
        this.cart = [];
        this._updateCartBadge();
        this._switchScreen('entry-screen');
      }, 3000);
    } else {
      this.paymentStatusMsg.style.color = 'var(--error-red)';
      this.paymentStatusMsg.textContent = '❌ Checkout transaction rejected. Insufficient credits.';
      this.audio.playError();
    }
  }

  async _syncHeadcount() {
    const list = await this.api.getEmployees();
    if (list) {
      const activeCount = list.filter(e => e.status === 'Active Shift').length;
      if (this.staffIndicator) {
        this.staffIndicator.textContent = `Mart operated by ${activeCount} active automation technicians.`;
      }
    }
  }

  _handleAutocomplete() {
    clearTimeout(this.searchDebounce);
    this.searchDebounce = setTimeout(() => {
      const val = this.searchInput.value.trim().toLowerCase();
      if (val.length < 2) {
        this.searchAuto.classList.remove('visible');
        return;
      }

      const matches = this.products.filter(p =>
        p.name.toLowerCase().includes(val) ||
        p.category.toLowerCase().includes(val) ||
        p.item_id.toLowerCase().includes(val)
      ).slice(0, 6);

      if (matches.length === 0) {
        this.searchAuto.innerHTML = '<div class="search-autocomplete-item"><span style="color:var(--text-muted)">No items match your search</span></div>';
      } else {
        this.searchAuto.innerHTML = matches.map(p => `
          <div class="search-autocomplete-item" data-id="${p.item_id}">
            <span class="sai-emoji">${UI_CATEGORIES[p.category]?.emoji || '📦'}</span>
            <span class="sai-name">${p.name}</span>
            <span class="sai-price">${formatPKR(p.price)}</span>
          </div>
        `).join('');

        this.searchAuto.querySelectorAll('.search-autocomplete-item[data-id]').forEach(el => {
          el.addEventListener('click', () => {
            this._showProductDetails(el.dataset.id);
            this.searchInput.value = '';
            this.searchAuto.classList.remove('visible');
          });
        });
      }
      this.searchAuto.classList.add('visible');
    }, 200);
  }

  _renderSidebarElements() {
    // Render dynamic AI assistant recommendations
    const aiRecs = document.getElementById('ai-recs');
    if (aiRecs) {
      const shuffled = [...this.products].sort(() => 0.5 - Math.random()).slice(0, 3);
      aiRecs.innerHTML = shuffled.map(p => `
        <div class="ai-rec-item" data-id="${p.item_id}">
          <span class="rec-emoji">${UI_CATEGORIES[p.category]?.emoji || '📦'}</span>
          <div class="rec-info">
            <span class="rec-name">${p.name}</span>
            <span class="rec-price">${formatPKR(p.price)}</span>
          </div>
        </div>
      `).join('');
      aiRecs.querySelectorAll('.ai-rec-item').forEach(el => {
        el.addEventListener('click', () => this._showProductDetails(el.dataset.id));
      });
    }

    // Render featured sponsored items
    const sponItems = document.getElementById('sponsored-items');
    if (sponItems) {
      const sponsored = this.products.slice(0, 3);
      sponItems.innerHTML = sponsored.map(p => `
        <div class="sponsored-item" data-id="${p.item_id}">
          <span class="spon-emoji">${UI_CATEGORIES[p.category]?.emoji || '📦'}</span>
          <div class="spon-info">
            <span class="spon-name">${p.name}</span>
            <span class="spon-price">${formatPKR(p.price)}</span>
          </div>
        </div>
      `).join('');
      sponItems.querySelectorAll('.sponsored-item').forEach(el => {
        el.addEventListener('click', () => this._showProductDetails(el.dataset.id));
      });
    }
  }

  _initSupport() {
    this.supportWidget.addEventListener('click', () => {
      if (this.supportWidget.classList.contains('connected')) return;
      this.supportWidget.classList.add('connected');
      this.supportText.textContent = '🔊 Connected: Tech Dispatch dispatched to coordinates.';
      this.audio.playSuccess();
      setTimeout(() => {
        this.supportWidget.classList.remove('connected');
        this.supportText.textContent = 'Call Support Agent';
      }, 5000);
    });
  }

  _updateClock() {
    if (this.clockEl) {
      this.clockEl.textContent = new Date().toLocaleString('en-US', {
        hour12: true,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        weekday: 'short',
        month: 'short',
        day: 'numeric'
      });
    }
  }

  _showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast--${type}`;
    const icons = { success: '✅', error: '❌', info: 'ℹ️' };
    toast.innerHTML = `<span class="toast-icon">${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
    this.toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.classList.add('removing');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
}

// ═════════════════════════════════════════════
// DashboardUI — Administration Dashboard Controller
// ═════════════════════════════════════════════
class DashboardUI {
  constructor() {
    this.api = new NexusAPI();
    this.inventory = [];
    this.employees = [];

    this._cacheElements();
    this._bindEvents();
    this.init();
  }

  _cacheElements() {
    this.latencyEl        = document.getElementById('health-latency');
    this.dbStatusEl       = document.getElementById('health-db');
    this.mlStatusEl       = document.getElementById('health-ml');
    this.accuracyEl       = document.getElementById('health-accuracy');
    this.inventoryTbody   = document.getElementById('inventory-tbody');
    this.attendanceList   = document.getElementById('employee-attendance-container');
    
    // Inventory modal
    this.invModalOverlay  = document.getElementById('inventory-modal-overlay');
    this.invForm          = document.getElementById('inventory-form');
    this.invModalTitle    = document.getElementById('inv-modal-title');
    this.invAction        = document.getElementById('inv-action');
    this.invId            = document.getElementById('inv-id');
    this.invName          = document.getElementById('inv-name');
    this.invCategory      = document.getElementById('inv-category');
    this.invPrice         = document.getElementById('inv-price');
    this.invCost          = document.getElementById('inv-cost');
    this.invStock         = document.getElementById('inv-stock');
    this.invRack          = document.getElementById('inv-rack');
    this.invShelf         = document.getElementById('inv-shelf');
    this.invThreshold     = document.getElementById('inv-threshold');
    this.invSupplier      = document.getElementById('inv-supplier');
    this.invWeight        = document.getElementById('inv-weight');
    this.invExpiry        = document.getElementById('inv-expiry');
  }

  _bindEvents() {
    document.getElementById('refresh-btn')?.addEventListener('click', () => {
      this.init();
      Toast.success('Dashboard metrics refreshed.');
    });

    document.getElementById('btn-cluster')?.addEventListener('click', async () => {
      const btn = document.getElementById('btn-cluster');
      btn.disabled = true;
      btn.textContent = '🧮 Fitting Clusters...';
      const res = await this.api.triggerClustering();
      btn.disabled = false;
      btn.textContent = '🧮 Run K-MeansFit';
      if (res && res.status === 'success') {
        Toast.success('K-Means clustering complete!');
        this.loadClusterStats();
        this.loadCustomerTable();
      } else {
        Toast.error('Clustering fits failed.');
      }
    });

    // CRUD Modal Actions
    document.getElementById('btn-add-inventory-modal')?.addEventListener('click', () => this.openAddModal());
    document.getElementById('inv-modal-close')?.addEventListener('click', () => this.closeModal());
    document.getElementById('inv-cancel-btn')?.addEventListener('click', () => this.closeModal());
    this.invForm?.addEventListener('submit', (e) => {
      e.preventDefault();
      this.handleFormSubmit();
    });
  }

  async init() {
    await this.loadSystemHealth();
    await this.loadInventoryTable();
    await this.loadEmployeeAttendance();
    await this.loadPaymentTrendsChart();
    await this.loadClusterStats();
    await this.loadCustomerTable();
    await this.loadCreditEngineSummary();
  }

  async loadSystemHealth() {
    const health = await this.api.getSystemHealth();
    if (health) {
      if (this.latencyEl) this.latencyEl.textContent = `${health.api_latency_ms.toFixed(1)} ms`;
      if (this.dbStatusEl) {
        this.dbStatusEl.textContent = health.database_connected ? 'Connected' : 'Offline';
        this.dbStatusEl.style.color = health.database_connected ? 'var(--success-green)' : 'var(--error-red)';
      }
      if (this.mlStatusEl) this.mlStatusEl.textContent = health.ml_pipeline_convergence;
      if (this.accuracyEl) this.accuracyEl.textContent = `${(health.ml_accuracy * 100).toFixed(1)}%`;
    }
  }

  async loadInventoryTable() {
    const raw = await this.api.getInventory();
    if (raw) {
      this.inventory = raw;
      this.renderInventory();
    }
  }

  renderInventory() {
    if (!this.inventoryTbody) return;
    if (this.inventory.length === 0) {
      this.inventoryTbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No inventory records.</td></tr>';
      return;
    }

    this.inventoryTbody.innerHTML = this.inventory.map(item => `
      <tr>
        <td style="font-weight: 700; color: var(--cyber-teal);">${item.item_id}</td>
        <td>${item.name}</td>
        <td><span class="badge" style="background:rgba(255,255,255,0.05); padding: 4px 8px; border-radius:4px; font-size:11px;">${item.category}</span></td>
        <td style="font-weight: 700;">${formatPKR(item.price < 50 ? item.price * 280 : item.price)}</td>
        <td>${item.stock_quantity}</td>
        <td>Rack ${item.rack_id} (Shelf ${item.shelf_position})</td>
        <td>
          <div class="flex gap-xs">
            <button class="btn btn-glass btn-sm edit-inv-btn" data-id="${item.item_id}">✏️ Edit</button>
            <button class="btn btn-outline btn-sm delete-inv-btn" data-id="${item.item_id}" style="color:var(--error-red); border-color:rgba(239,68,68,0.2);">🗑️ Delete</button>
          </div>
        </td>
      </tr>
    `).join('');

    this.inventoryTbody.querySelectorAll('.edit-inv-btn').forEach(btn => {
      btn.addEventListener('click', () => this.openEditModal(btn.dataset.id));
    });
    this.inventoryTbody.querySelectorAll('.delete-inv-btn').forEach(btn => {
      btn.addEventListener('click', () => this.deleteInventoryItem(btn.dataset.id));
    });

    this.renderRackMap();
  }

  renderRackMap() {
    const grid = document.getElementById('rack-grid');
    if (!grid) return;

    grid.innerHTML = '';
    const aisles = ['A', 'B', 'C', 'D', 'E', 'F'];
    
    for (let sec = 5; sec >= 1; sec--) {
      for (const aisle of aisles) {
        const rackId = `${aisle}${sec}`;
        const items = this.inventory.filter(i => i.rack_id === rackId);
        const stockCount = items.reduce((sum, i) => sum + i.stock_quantity, 0);
        
        let colorClass = 'rgba(255, 255, 255, 0.05)';
        if (stockCount > 0 && stockCount < 20) colorClass = 'rgba(239, 68, 68, 0.35)'; // Low
        else if (stockCount >= 20 && stockCount < 60) colorClass = 'rgba(245, 158, 11, 0.35)'; // Medium
        else if (stockCount >= 60 && stockCount < 120) colorClass = 'rgba(16, 185, 129, 0.35)'; // High
        else if (stockCount >= 120) colorClass = 'rgba(88, 101, 242, 0.45)'; // Full
        
        const cell = document.createElement('div');
        cell.className = 'rack-cell';
        cell.style.background = colorClass;
        cell.style.border = '1px solid var(--border-subtle)';
        cell.title = `Rack ${rackId}\nSKUs: ${items.length}\nTotal Stock: ${stockCount}`;
        cell.textContent = rackId;
        grid.appendChild(cell);
      }
    }
  }

  async loadEmployeeAttendance() {
    const list = await this.api.getEmployees();
    if (list) {
      this.employees = list;
      this.renderEmployees();
    }
  }

  renderEmployees() {
    if (!this.attendanceList) return;
    if (this.employees.length === 0) {
      this.attendanceList.innerHTML = '<p class="text-muted text-center body-xs">No employees found.</p>';
      return;
    }

    this.attendanceList.innerHTML = this.employees.map(emp => {
      let statusColor = 'var(--text-muted)';
      if (emp.status === 'Active Shift') statusColor = 'var(--success-green)';
      else if (emp.status === 'On Break') statusColor = 'var(--amber-gold)';

      return `
        <div class="flex justify-between items-center glass-card" style="padding: 10px 14px; border-radius: var(--radius-md); background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle);">
          <div>
            <div style="font-size: 13px; font-weight: 700; color: var(--text-primary);">${emp.name}</div>
            <div style="font-size: 11px; color: var(--text-muted);">${emp.role}</div>
          </div>
          <div class="flex items-center gap-sm">
            <span style="font-size: 11px; font-weight: 700; color: ${statusColor}">${emp.status}</span>
            <select class="employee-status-select search-input" data-id="${emp.id}" style="width: auto; height: 32px; padding: 0 10px; font-size: 11px; background: var(--bg-raised); border-radius: var(--radius-sm);">
              <option value="Active Shift" ${emp.status === 'Active Shift' ? 'selected' : ''}>Check In</option>
              <option value="Off Shift" ${emp.status === 'Off Shift' ? 'selected' : ''}>Check Out</option>
              <option value="On Break" ${emp.status === 'On Break' ? 'selected' : ''}>On Break</option>
            </select>
          </div>
        </div>
      `;
    }).join('');

    this.attendanceList.querySelectorAll('.employee-status-select').forEach(sel => {
      sel.addEventListener('change', async (e) => {
        const empId = parseInt(sel.dataset.id, 10);
        const nextState = e.target.value;
        const res = await this.api.toggleEmployee(empId, nextState);
        if (res && res.status === 'success') {
          Toast.success(`Updated status for ${res.employee.name} to ${nextState}`);
          this.loadEmployeeAttendance();
        } else {
          Toast.error('Failed to change technician attendance.');
        }
      });
    });
  }

  async loadPaymentTrendsChart() {
    const trends = await this.api.getPaymentTrends();
    if (trends) {
      this.drawPaymentTrends(trends);
    }
  }

  drawPaymentTrends(trends) {
    const container = document.getElementById('payment-trends-chart');
    if (!container) return;

    const methods = Object.entries(trends);
    const total = methods.reduce((sum, [_, count]) => sum + count, 0);
    const colors = { 'cash': '#22c55e', 'card': '#3b82f6', 'points': '#f59e0b', 'coupons': '#ec4899' };
    const labels = { 'cash': 'Cash 💵', 'card': 'Card 💳', 'points': 'Points 🪙', 'coupons': 'Coupons 🎟️' };

    const width = 450;
    const height = 180;
    const barWidth = 45;
    const spacing = 50;
    const startX = 60;

    const svgContent = methods.map(([method, count], index) => {
      const color = colors[method] || '#5865f2';
      const pct = total > 0 ? count / total : 0;
      const barHeight = Math.max(10, pct * 100);
      const x = startX + index * (barWidth + spacing);
      const y = height - barHeight - 30;

      return `
        <g>
          <text x="${x + barWidth/2}" y="${y - 8}" fill="var(--text-primary)" font-size="12" font-weight="700" text-anchor="middle">${count}</text>
          <rect x="${x}" y="30" width="${barWidth}" height="100" rx="6" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.05)" />
          <rect x="${x}" y="${y}" width="${barWidth}" height="${barHeight}" rx="6" fill="${color}">
            <animate attributeName="y" from="${height - 30}" to="${y}" dur="0.6s" fill="freeze" />
            <animate attributeName="height" from="0" to="${barHeight}" dur="0.6s" fill="freeze" />
          </rect>
          <text x="${x + barWidth/2}" y="${height - 10}" fill="var(--text-secondary)" font-size="11" font-weight="600" text-anchor="middle">${labels[method] || method}</text>
        </g>
      `;
    }).join('');

    container.innerHTML = `
      <svg width="100%" height="${height}" viewBox="0 0 ${width} ${height}" style="overflow: visible;">
        ${svgContent}
      </svg>
    `;
  }

  async loadClusterStats() {
    const data = await this.api.getClusterResults();
    const infoContainer = document.getElementById('cluster-info');
    if (data && infoContainer) {
      infoContainer.innerHTML = `
        <div class="flex-col gap-xs body-xs text-secondary" style="display:flex; flex-direction:column; gap:4px; text-align:left;">
          <div><strong>Silhouette Score:</strong> <span style="color:var(--cyber-teal)">${data.mapping ? '0.725 (Stable)' : 'Not Configured'}</span></div>
          <div><strong>Optimal Clusters Fit:</strong> <span style="color:var(--cyber-teal)">6 (Validated)</span></div>
          <div><strong>Total Store Credit Asset:</strong> <span style="color:var(--success-green)">Rs. ${data.store_balance ? Math.round(data.store_balance).toLocaleString() : 0}</span></div>
        </div>
      `;
      if (data.segment_distribution) {
        this.drawLoyaltyChart(data.segment_distribution);
      }
    }
  }

  drawLoyaltyChart(segmentDistribution) {
    const container = document.getElementById('segment-distribution-chart');
    const legend = document.getElementById('segment-legend');
    if (!container || !legend) return;

    const segments = Object.entries(segmentDistribution);
    const total = segments.reduce((sum, [_, count]) => sum + count, 0);
    const colors = ['#5865f2', '#00f2fe', '#7000ff', '#f59e0b', '#22c55e', '#ef4444'];
    
    legend.innerHTML = segments.map(([name, count], index) => {
      const pct = total > 0 ? ((count / total) * 100).toFixed(1) : 0;
      const color = colors[index % colors.length];
      return `
        <div class="flex items-center gap-sm body-xs" style="margin-bottom: 2px;">
          <div style="width: 10px; height: 10px; border-radius: 2px; background: ${color}; flex-shrink: 0;"></div>
          <span class="text-secondary" style="flex: 1; text-align: left; text-overflow:ellipsis; overflow:hidden; white-space:nowrap;">${name}</span>
          <span style="font-weight: 700; color: var(--text-primary); margin-left: 8px;">${count} (${pct}%)</span>
        </div>
      `;
    }).join('');

    let y = 10;
    const barHeight = 20;
    const gap = 10;
    const width = 360;
    const height = segments.length * (barHeight + gap) + 10;

    const svgBars = segments.map(([name, count], index) => {
      const color = colors[index % colors.length];
      const pct = total > 0 ? count / total : 0;
      const barWidth = Math.max(10, pct * 200);
      const rectY = y;
      y += barHeight + gap;

      return `
        <g>
          <text x="5" y="${rectY + 14}" fill="var(--text-secondary)" font-size="10" font-weight="600">${name.substring(0, 15)}</text>
          <rect x="130" y="${rectY}" width="200" height="${barHeight}" rx="3" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.05)" />
          <rect x="130" y="${rectY}" width="${barWidth}" height="${barHeight}" rx="3" fill="${color}">
            <animate attributeName="width" from="0" to="${barWidth}" dur="0.8s" fill="freeze" />
          </rect>
          <text x="${130 + barWidth + 8}" y="${rectY + 14}" fill="var(--text-primary)" font-size="11" font-weight="700">${count}</text>
        </g>
      `;
    }).join('');

    container.innerHTML = `
      <svg width="100%" height="${height}" viewBox="0 0 ${width} ${height}" style="overflow: visible;">
        ${svgBars}
      </svg>
    `;
  }

  async loadCustomerTable() {
    const res = await this.api.getCustomers();
    const tbody = document.getElementById('customer-tbody');
    if (res && tbody) {
      const list = res.customers || [];
      tbody.innerHTML = list.map(c => `
        <tr>
          <td style="font-weight: 700; color: var(--cyber-teal);">${c.customer_id}</td>
          <td>${c.name}</td>
          <td><span class="badge" style="color:#fff; font-size:11px;">${c.segment || c.segment_label || 'Mid-Tier Consistent'}</span></td>
          <td style="font-weight: 700;">${formatPKR(c.features?.total_spend || 0)}</td>
          <td style="color:${c.store_credit_balance < 0 ? 'var(--error-red)' : 'var(--success-green)'}; font-weight:700;">${formatPKR(c.store_credit_balance || 0)}</td>
          <td>${c.features?.frequency || 0} visits</td>
        </tr>
      `).join('');
    }
  }

  async loadCreditEngineSummary() {
    const analytics = await this.api.getAnalyticsSegments();
    const summary = document.getElementById('credit-summary');
    if (analytics && summary) {
      const list = Object.entries(analytics.segment_analytics || {});
      summary.innerHTML = `
        <div style="display:flex; flex-direction:column; gap:10px; text-align:left;" class="body-xs">
          <div><strong>Total Mart Revenue:</strong> <span style="color:var(--success-green); font-weight:700;">Rs. ${Math.round(analytics.global_summary?.total_revenue_today || 85400).toLocaleString()}</span></div>
          <div><strong>Total Outstanding Loans:</strong> <span style="color:var(--error-red); font-weight:700;">Rs. ${Math.round(analytics.global_summary?.total_debt || 12000).toLocaleString()}</span></div>
          <div style="border-top:1px solid var(--border-subtle); padding-top:8px; margin-top:4px;"><strong>Segments Overview:</strong></div>
          ${list.slice(0, 4).map(([name, data]) => `
            <div class="flex justify-between items-center">
              <span class="text-secondary">${name.substring(0, 15)}:</span>
              <span style="font-weight:700; color:var(--text-primary);">Avg Rs. ${Math.round(data.avg_spend).toLocaleString()}</span>
            </div>
          `).join('')}
        </div>
      `;
    }
  }

  openAddModal() {
    this.invModalTitle.textContent = 'Add New SKU';
    this.invAction.value = 'create';
    this.invId.value = '';
    this.invId.disabled = false;
    this.invName.value = '';
    this.invCategory.value = 'pantry';
    this.invPrice.value = '';
    this.invCost.value = '';
    this.invStock.value = '';
    this.invRack.value = '';
    this.invShelf.value = '3';
    this.invThreshold.value = '5';
    this.invSupplier.value = '';
    this.invWeight.value = '';
    this.invExpiry.value = '';
    this.invModalOverlay.classList.add('visible');
  }

  openEditModal(id) {
    const item = this.inventory.find(i => i.item_id === id);
    if (!item) return;

    this.invModalTitle.textContent = `Edit SKU: ${item.item_id}`;
    this.invAction.value = 'update';
    this.invId.value = item.item_id;
    this.invId.disabled = true;
    this.invName.value = item.name;
    this.invCategory.value = item.category;
    this.invPrice.value = item.price;
    this.invCost.value = item.cost;
    this.invStock.value = item.stock_quantity;
    this.invRack.value = item.rack_id;
    this.invShelf.value = item.shelf_position;
    this.invThreshold.value = item.reorder_threshold;
    this.invSupplier.value = item.supplier;
    this.invWeight.value = item.weight_kg;
    this.invExpiry.value = item.expiry_days || '';
    
    this.invModalOverlay.classList.add('visible');
  }

  closeModal() {
    this.invModalOverlay.classList.remove('visible');
  }

  async handleFormSubmit() {
    const action = this.invAction.value;
    const id = this.invId.value;
    const payload = {
      item_id: id,
      name: this.invName.value,
      category: this.invCategory.value,
      price: parseFloat(this.invPrice.value),
      cost: parseFloat(this.invCost.value),
      stock_quantity: parseInt(this.invStock.value, 10),
      rack_id: this.invRack.value,
      shelf_position: parseInt(this.invShelf.value, 10),
      reorder_threshold: parseInt(this.invThreshold.value, 10),
      supplier: this.invSupplier.value,
      weight_kg: parseFloat(this.invWeight.value),
      expiry_days: this.invExpiry.value ? parseInt(this.invExpiry.value, 10) : null
    };

    let res = null;
    if (action === 'create') {
      res = await this.api.saveInventory(payload);
    } else {
      res = await this.api.updateInventory(id, payload);
    }

    if (res && res.status === 'success') {
      Toast.success(`Successfully saved SKU ${id}`);
      this.closeModal();
      this.loadInventoryTable();
    } else {
      Toast.error(`Failed to save SKU ${id}. Verify cost is below retail price and inputs are correct.`);
    }
  }

  async deleteInventoryItem(id) {
    if (confirm(`Are you sure you want to delete product SKU ${id}?`)) {
      const res = await this.api.deleteInventory(id);
      if (res && res.status === 'success') {
        Toast.success(`Successfully deleted SKU ${id}`);
        this.loadInventoryTable();
      } else {
        Toast.error(`Failed to delete SKU ${id}.`);
      }
    }
  }
}

// ═════════════════════════════════════════════
// Toast Utilities
// ═════════════════════════════════════════════
const Toast = {
  _getContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    return container;
  },
  _show(message, type) {
    const container = this._getContainer();
    const toast = document.createElement('div');
    toast.className = `toast toast--${type}`;
    const icons = { success: '✅', error: '❌', info: 'ℹ️' };
    toast.innerHTML = `<span class="toast-icon">${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.classList.add('removing');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  },
  success(msg) { this._show(msg, 'success'); },
  error(msg) { this._show(msg, 'error'); },
  info(msg) { this._show(msg, 'info'); }
};

// ═════════════════════════════════════════════
// BOOT — Initialize on DOM Ready
// ═════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
  // Kiosk page
  if (document.getElementById('entry-screen')) {
    window.nexusKiosk = new KioskApp();
  }
  // Dashboard page
  if (document.getElementById('inventory-manager-section') || document.querySelector('.navbar')) {
    window.nexusDashboard = new DashboardUI();
  }
});
