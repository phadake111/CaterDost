const API_BASE = "https://caterdost-api.onrender.com/api/v1";

let currentUser = JSON.parse(localStorage.getItem("caterdost_user") || "null");
let currentActiveOrderId = null;
let currentOrderData = null;
let currentLang = "mr";

// --- 1. LANGUAGE DICTIONARIES ---
const i18n = {
  mr: {
    langBadge: "मराठी",
    authTag: "तुमची डिजिटल कॅटरिंग नोंद वही",
    loginBtn: "लॉगिन करा",
    regBtn: "खाते तयार करा",
    noAcc: "नवीन आहात? <a href='#' onclick=\"showAuthMode('signup')\">नवीन खाते उघडा</a>",
    haveAcc: "आधीच खाते आहे? <a href='#' onclick=\"showAuthMode('login')\">लॉगिन करा</a>",
    greetBadge: "👋 स्वागत आहे",
    todaySub: "आजच्या दिवसातील कामांची स्थिती",
    pendingUtensils: "बाकी भांडी (Utensils)",
    pendingMoney: "बाकी रक्कम (Pending)",
    todayOrders: "आजच्या ऑर्डर्स",
    upcoming: "पुढील ऑर्डर्स (७ दिवस)",
    checkDateHead: "तारीख तपासा",
    checkDateSub: "नवीन बुकिंग घेण्यापूर्वी त्या तारखेची कामे तपासा",
    btnCheck: "तपासा",
    ownHead: "स्वतःच्या ऑर्डर्स",
    extHead: "बाहेरचे काम",
    ordersHead: "माझ्या ऑर्डर्स",
    extWorkHead: "बाहेरचे काम",
    historyHead: "नोंद वही",
    fab: "नवीन ऑर्डर",
    signout: "बाहेर",
    tabHome: "होम",
    tabSearch: "तपासा",
    tabOrders: "ऑर्डर्स",
    tabExternal: "बाहेरचे",
    tabHistory: "नोंदवही"
  },
  en: {
    langBadge: "EN",
    authTag: "Your Digital Catering Diary",
    loginBtn: "Login",
    regBtn: "Create Account",
    noAcc: "New here? <a href='#' onclick=\"showAuthMode('signup')\">Create account</a>",
    haveAcc: "Have an account? <a href='#' onclick=\"showAuthMode('login')\">Login</a>",
    greetBadge: "👋 Welcome",
    todaySub: "Overview of your commitments today",
    pendingUtensils: "Missing Utensils",
    pendingMoney: "Pending Payment",
    todayOrders: "Today's Orders",
    upcoming: "Upcoming Orders (7 Days)",
    checkDateHead: "Check Date Availability",
    checkDateSub: "Review existing commitments before taking an order",
    btnCheck: "Check",
    ownHead: "Own Orders",
    extHead: "External Work",
    ordersHead: "My Orders",
    extWorkHead: "External Work Shifts",
    historyHead: "History Diary",
    fab: "Quick Book",
    signout: "Logout",
    tabHome: "Home",
    tabSearch: "Check Date",
    tabOrders: "Orders",
    tabExternal: "External",
    tabHistory: "History"
  }
};

function toggleLanguage() {
  currentLang = currentLang === "mr" ? "en" : "mr";
  applyLanguage();
}

function applyLanguage() {
  const t = i18n[currentLang];
  
  document.getElementById("authLangBadge").innerText = t.langBadge;
  const mainBadge = document.getElementById("mainLangBadge");
  if (mainBadge) mainBadge.innerText = t.langBadge;

  document.getElementById("txt-auth-tag").innerText = t.authTag;
  document.getElementById("btn-login").innerText = t.loginBtn;
  document.getElementById("btn-register").innerText = t.regBtn;
  document.getElementById("txt-no-account").innerHTML = t.noAcc;
  document.getElementById("txt-have-account").innerHTML = t.haveAcc;

  const greetBadge = document.getElementById("txt-greet-badge");
  if (greetBadge) greetBadge.innerText = t.greetBadge;
  
  const todaySub = document.getElementById("txt-today-sub");
  if (todaySub) todaySub.innerText = t.todaySub;
  
  const pendingUtensils = document.getElementById("txt-pending-utensils");
  if (pendingUtensils) pendingUtensils.innerText = t.pendingUtensils;
  
  const pendingMoney = document.getElementById("txt-pending-money");
  if (pendingMoney) pendingMoney.innerText = t.pendingMoney;
  
  const todayOrdersHead = document.getElementById("txt-today-orders-head");
  if (todayOrdersHead) todayOrdersHead.innerText = t.todayOrders;
  
  const upcomingHead = document.getElementById("txt-upcoming-head");
  if (upcomingHead) upcomingHead.innerText = t.upcoming;
  
  const dateSearchHead = document.getElementById("txt-date-search-head");
  if (dateSearchHead) dateSearchHead.innerText = t.checkDateHead;
  
  const dateSearchSub = document.getElementById("txt-date-search-sub");
  if (dateSearchSub) dateSearchSub.innerText = t.checkDateSub;
  
  const btnCheckDate = document.getElementById("btn-check-date");
  if (btnCheckDate) btnCheckDate.innerText = t.btnCheck;
  
  const ownCommitmentsHead = document.getElementById("txt-own-commitments-head");
  if (ownCommitmentsHead) ownCommitmentsHead.innerText = t.ownHead;
  
  const extCommitmentsHead = document.getElementById("txt-ext-commitments-head");
  if (extCommitmentsHead) extCommitmentsHead.innerText = t.extHead;
  
  const ordersHead = document.getElementById("txt-orders-head");
  if (ordersHead) ordersHead.innerText = t.ordersHead;
  
  const extWorkHead = document.getElementById("txt-ext-work-head");
  if (extWorkHead) extWorkHead.innerText = t.extWorkHead;
  
  const historyHead = document.getElementById("txt-history-head");
  if (historyHead) historyHead.innerText = t.historyHead;
  
  const txtFab = document.getElementById("txt-fab");
  if (txtFab) txtFab.innerText = t.fab;
  
  const txtSignout = document.getElementById("txt-signout");
  if (txtSignout) txtSignout.innerText = t.signout;

  const tabHome = document.getElementById("tab-home");
  if (tabHome) tabHome.innerText = t.tabHome;
  
  const tabSearch = document.getElementById("tab-search");
  if (tabSearch) tabSearch.innerText = t.tabSearch;
  
  const tabOrders = document.getElementById("tab-orders");
  if (tabOrders) tabOrders.innerText = t.tabOrders;
  
  const tabExternal = document.getElementById("tab-external");
  if (tabExternal) tabExternal.innerText = t.tabExternal;
  
  const tabHistory = document.getElementById("tab-history");
  if (tabHistory) tabHistory.innerText = t.tabHistory;
}

// --- 2. AUTHENTICATION ---
function checkAuth() {
  if (currentUser) {
    document.getElementById("auth-screen").style.display = "none";
    document.getElementById("app-shell").style.display = "block";
    document.getElementById("user-display-name").innerText = currentUser.business_name || "कॅटरर";
    loadDashboard();
  } else {
    document.getElementById("auth-screen").style.display = "flex";
    document.getElementById("app-shell").style.display = "none";
  }
}

function showAuthMode(mode) {
  document.getElementById("login-box").style.display = mode === 'login' ? 'block' : 'none';
  document.getElementById("signup-box").style.display = mode === 'signup' ? 'block' : 'none';
}

async function handleLogin() {
  const phone = document.getElementById("login-phone").value.trim();
  const pin = document.getElementById("login-pin").value.trim();
  if (!phone || !pin) return alert("कृपया फोन आणि पिन टाका");

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ phone, pin })
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem("caterdost_user", JSON.stringify(data));
      currentUser = data;
      checkAuth();
    } else {
      alert(data.detail || "Login failed");
    }
  } catch {
    alert("सर्व्हरशी संपर्क होत नाही");
  }
}

async function handleSignup() {
  const business_name = document.getElementById("reg-name").value.trim();
  const phone = document.getElementById("reg-phone").value.trim();
  const pin = document.getElementById("reg-pin").value.trim();
  if (!business_name || !phone || !pin) return alert("सर्व माहिती भरा");

  try {
    const res = await fetch(`${API_BASE}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ business_name, phone, pin })
    });
    const data = await res.json();
    if (res.ok) {
      alert("खाते तयार झाले! आता लॉगिन करा");
      showAuthMode('login');
    } else {
      alert(data.detail || "Signup failed");
    }
  } catch {
    alert("सर्व्हरशी संपर्क होत नाही");
  }
}

function handleSignOut() {
  if (confirm("तुम्हाला बाहेर पडायचे आहे का? (Sign out?)")) {
    localStorage.removeItem("caterdost_user");
    currentUser = null;
    checkAuth();
  }
}

// --- 3. NAVIGATION SWITCHER ---
function switchTab(viewId, el) {
  document.querySelectorAll(".app-view").forEach(v => v.classList.remove("active"));
  if (el) {
    document.querySelectorAll(".dock-item").forEach(d => d.classList.remove("active"));
    el.classList.add("active");
  }
  document.getElementById(viewId).classList.add("active");

  if (viewId === 'view-dashboard') loadDashboard();
  if (viewId === 'view-orders') loadOrders();
  if (viewId === 'view-external') loadExternalWork();
}

function getBadgeClass(status) {
  if (status === 'COMPLETED') return 'badge-paid';
  if (status === 'CANCELLED') return 'badge-cancelled';
  return 'badge-booked';
}

// --- 4. DASHBOARD ---
async function loadDashboard() {
  try {
    const res = await fetch(`${API_BASE}/dashboard/summary`);
    const data = await res.json();

    document.getElementById("val-missing-utensils").innerText = data.utensil_alerts.length;
    document.getElementById("val-pending-money").innerText = `₹${data.total_pending_client_money}`;

    const todayList = document.getElementById("today-orders-list");
    todayList.innerHTML = data.today_own_orders.length === 0 
      ? `<div class="empty-state">आज कोणतीही ऑर्डर नाही.</div>`
      : data.today_own_orders.map(o => `
        <div class="item-card" onclick="openOrderDetail(${o.order_id})">
          <div>
            <div class="item-title">${o.title} (${o.people_count} people)</div>
            <div class="item-sub">👤 ${o.client_name} • ⏰ ${o.time}</div>
          </div>
          <span class="pill-badge ${getBadgeClass(o.status)}">${o.status}</span>
        </div>
      `).join("");

    const upcomingList = document.getElementById("upcoming-orders-list");
    upcomingList.innerHTML = data.upcoming_orders.length === 0
      ? `<div class="empty-state">पुढील ७ दिवसात ऑर्डर नाहीत.</div>`
      : data.upcoming_orders.map(o => `
        <div class="item-card" onclick="openOrderDetail(${o.order_id})">
          <div>
            <div class="item-title">${o.title} (${o.people_count} people)</div>
            <div class="item-sub">📅 ${o.date}</div>
          </div>
          <span class="pill-badge ${getBadgeClass(o.status)}">${o.status}</span>
        </div>
      `).join("");
  } catch (err) {
    console.error(err);
  }
}

// --- 5. DATE SEARCH ---
async function fetchDateCommitments() {
  const dateVal = document.getElementById("searchDateInput").value;
  if (!dateVal) return alert("तारीख निवडा");

  try {
    const res = await fetch(`${API_BASE}/commitments?search_date=${dateVal}`);
    const data = await res.json();
    document.getElementById("date-results-area").style.display = "block";

    const ownList = document.getElementById("date-own-list");
    ownList.innerHTML = data.own_orders.length === 0
      ? `<div class="empty-state">या तारखेला स्वतःची ऑर्डर नाही.</div>`
      : data.own_orders.map(o => `
        <div class="item-card" onclick="openOrderDetail(${o.order_id})">
          <div>
            <div class="item-title">${o.order_title} (${o.people_count} people)</div>
            <div class="item-sub">👤 ${o.client_name} • ⏰ ${o.event_time}</div>
          </div>
          <span class="pill-badge ${getBadgeClass(o.status)}">${o.status}</span>
        </div>
      `).join("");

    const extList = document.getElementById("date-ext-list");
    extList.innerHTML = data.external_work.length === 0
      ? `<div class="empty-state">या तारखेला बाहेरचे काम नाही.</div>`
      : data.external_work.map(w => `
        <div class="item-card">
          <div>
            <div class="item-title">कॅटरर: ${w.hired_by_name}</div>
            <div class="item-sub">⏰ ${w.reach_time || 'वेळ'} • 📍 ${w.location || ''}</div>
          </div>
          <span class="pill-badge badge-paid">External</span>
        </div>
      `).join("");
  } catch {
    alert("तारीख तपासताना अडचण आली.");
  }
}

// --- 6. LIST OWN ORDERS ---
async function loadOrders() {
  try {
    const res = await fetch(`${API_BASE}/orders`);
    const data = await res.json();
    const list = document.getElementById("all-orders-list");

    list.innerHTML = data.length === 0
      ? `<div class="empty-state">अद्याप ऑर्डर्स नाहीत. नवीन ऑर्डर नोंदवा!</div>`
      : data.map(o => `
        <div class="item-card" onclick="openOrderDetail(${o.order_id})">
          <div>
            <div class="item-title">${o.order_title}</div>
            <div class="item-sub">👤 ${o.client_name} • 📅 ${o.event_date || 'तारीख नाही'}</div>
            <div class="item-sub" style="color: #059669; font-weight: 600;">₹${o.total_paid} मिळाले / ₹${o.pending_amount} बाकी</div>
          </div>
          <span class="pill-badge ${getBadgeClass(o.status)}">${o.status}</span>
        </div>
      `).join("");
  } catch (err) {
    console.error(err);
  }
}

// --- 7. ORDER DETAIL HUB (WITH EDIT CAPABILITIES) ---
async function openOrderDetail(orderId) {
  currentActiveOrderId = orderId;
  switchTab('view-order-detail', null);

  try {
    const res = await fetch(`${API_BASE}/orders/${orderId}`);
    const o = await res.json();
    currentOrderData = o;

    const day1 = o.days[0] || {};

    document.getElementById("order-detail-content").innerHTML = `
      <div class="detail-summary-card">
        <div class="flex-between">
          <h2>${o.order_title}</h2>
          <div style="display: flex; gap: 8px; align-items: center;">
            <button class="edit-header-btn" onclick="openEditOrderModal()">✏️</button>
            <span class="pill-badge ${getBadgeClass(o.status)}">${o.status}</span>
          </div>
        </div>
        <p class="item-sub">👤 <b>${o.client.name}</b> (${o.client.phone})</p>
        <p class="item-sub">📅 ${day1.event_date || '-'} • ⏰ ${day1.event_time || '-'} • 👥 ${day1.people_count || 0} माणसे</p>
        <p class="item-sub">📍 ${day1.location || 'पत्ता नाही'}</p>
        ${o.special_notes ? `<p class="item-sub" style="color:#d97706;">📝 ${o.special_notes}</p>` : ''}
        
        <div style="margin-top: 12px; font-weight: 700; padding-top: 10px; border-top: 1px dashed var(--border);">
          ठरलेली रक्कम: ₹${o.agreed_amount} | जमा: <span style="color:#059669;">₹${o.total_paid}</span> | बाकी: <span style="color:#dc2626;">₹${o.pending_amount}</span>
        </div>

        <div style="margin-top: 14px; padding-top: 12px; border-top: 1px dashed var(--border);">
          <button class="pdf-share-btn" onclick="shareMaterialListPDF(${o.id}, '${o.order_title}')">
            <span>📄</span> सामान यादी PDF डाउनलोड / पाठवा
          </button>
        </div>
      </div>

      <div class="section-title">कामाचे विभाग (Tap to view, add, or edit)</div>
      <div class="hub-grid">
        <div class="hub-tile" onclick="openManageSection('menu')">
          <span class="hub-icon">🍛</span>
          <span class="hub-title">मेन्यू (Menu)</span>
          <span class="hub-badge">${o.menu_items.length} आयटम</span>
        </div>
        <div class="hub-tile" onclick="openManageSection('resources')">
          <span class="hub-icon">🥔</span>
          <span class="hub-title">सामान (Ingredients)</span>
          <span class="hub-badge">${o.resources.length} वस्तू</span>
        </div>
        <div class="hub-tile" onclick="openManageSection('helpers')">
          <span class="hub-icon">👥</span>
          <span class="hub-title">हेल्पर (Helpers)</span>
          <span class="hub-badge">${o.helpers.length} लोक</span>
        </div>
        <div class="hub-tile" onclick="openManageSection('utensils')">
          <span class="hub-icon">🍲</span>
          <span class="hub-title">भांडी (Utensils)</span>
          <span class="hub-badge">${o.utensils.length} नोंदी</span>
        </div>
        <div class="hub-tile" onclick="openManageSection('payments')">
          <span class="hub-icon">💵</span>
          <span class="hub-title">पेमेंट (Payment)</span>
          <span class="hub-badge">₹${o.total_paid}</span>
        </div>
        <div class="hub-tile" onclick="openStatusModal('${o.status}')">
          <span class="hub-icon">🔄</span>
          <span class="hub-title">स्टेटस बदला</span>
          <span class="hub-badge">${o.status}</span>
        </div>
      </div>
    `;
  } catch {
    alert("ऑर्डर तपशील उघडता आला नाही.");
  }
}

// --- 8. EDIT CORE ORDER MODAL ---
function openEditOrderModal() {
  if (!currentOrderData) return;
  const o = currentOrderData;
  const day1 = o.days[0] || {};

  document.getElementById("edit-qb-name").value = o.client.name;
  document.getElementById("edit-qb-phone").value = o.client.phone;
  document.getElementById("edit-qb-title").value = o.order_title;
  document.getElementById("edit-qb-date").value = day1.event_date || "";
  document.getElementById("edit-qb-time").value = day1.event_time || "";
  document.getElementById("edit-qb-people").value = day1.people_count || "";
  document.getElementById("edit-qb-location").value = day1.location || "";
  document.getElementById("edit-qb-agreed").value = o.agreed_amount || "";
  document.getElementById("edit-qb-advance").value = o.advance_amount || "";
  document.getElementById("edit-qb-notes").value = o.special_notes || "";

  document.getElementById("modal-edit-order").style.display = "flex";
}

async function submitEditOrder(e) {
  e.preventDefault();
  if (!confirm("तुम्हाला या ऑर्डरमध्ये बदल सेव्ह करायचे आहेत का? (Confirm save changes?)")) {
    return;
  }

  const payload = {
    client_name: document.getElementById("edit-qb-name").value,
    client_phone: document.getElementById("edit-qb-phone").value,
    order_title: document.getElementById("edit-qb-title").value,
    event_date: document.getElementById("edit-qb-date").value,
    event_time: document.getElementById("edit-qb-time").value,
    people_count: parseInt(document.getElementById("edit-qb-people").value) || 0,
    location: document.getElementById("edit-qb-location").value,
    agreed_amount: parseFloat(document.getElementById("edit-qb-agreed").value) || 0,
    advance_amount: parseFloat(document.getElementById("edit-qb-advance").value) || 0,
    special_notes: document.getElementById("edit-qb-notes").value
  };

  try {
    const res = await fetch(`${API_BASE}/orders/${currentActiveOrderId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      document.getElementById("modal-edit-order").style.display = "none";
      openOrderDetail(currentActiveOrderId);
    } else {
      alert("बदल सेव्ह करताना त्रुटी आली.");
    }
  } catch {
    alert("सर्व्हरशी संपर्क होत नाही.");
  }
}

// --- 9. STATUS CHANGER MODAL ---
function openStatusModal(currentStatus) {
  document.getElementById("select-new-status").value = currentStatus;
  document.getElementById("modal-change-status").style.display = "flex";
}

async function saveStatusChange() {
  const newStatus = document.getElementById("select-new-status").value;
  try {
    const res = await fetch(`${API_BASE}/orders/${currentActiveOrderId}/status?new_status=${newStatus}`, { method: "PATCH" });
    if (res.ok) {
      document.getElementById("modal-change-status").style.display = "none";
      openOrderDetail(currentActiveOrderId);
    } else {
      alert("स्टेटस बदलता आले नाही.");
    }
  } catch {
    alert("सर्व्हरशी संपर्क होत नाही.");
  }
}

// --- 10. SECTION MANAGER (LIST, EDIT, DELETE) ---
function openManageSection(type) {
  const o = currentOrderData;
  const container = document.getElementById("section-items-container");
  const modalTitle = document.getElementById("section-modal-title");
  const addBtn = document.getElementById("btn-add-to-section");

  addBtn.onclick = () => openSubModal(type);
  document.getElementById("modal-manage-section").style.display = "flex";

  if (type === 'menu') {
    modalTitle.innerText = "मेन्यू यादी (Menu Items)";
    container.innerHTML = o.menu_items.length === 0
      ? `<div class="empty-state">कोणतेही मेन्यू आयटम जोडलेले नाहीत.</div>`
      : o.menu_items.map(m => `
        <div class="item-card">
          <div class="item-title">${m.item_name}</div>
          <div class="item-action-btns">
            <button class="btn-icon" onclick="promptEditMenu(${m.id}, '${m.item_name}')">✏️</button>
            <button class="btn-icon btn-delete" onclick="confirmDeleteSubItem('menu', ${m.id})">🗑️</button>
          </div>
        </div>
      `).join("");
  } else if (type === 'resources') {
    modalTitle.innerText = "कच्चा माल / सामान (Ingredients)";
    container.innerHTML = o.resources.length === 0
      ? `<div class="empty-state">कोणतेही सामान जोडलेले नाही.</div>`
      : o.resources.map(r => `
        <div class="item-card">
          <div>
            <div class="item-title">${r.resource_name} — ${r.quantity} ${r.unit}</div>
            <div class="item-sub">${r.is_client_provided ? '✅ ग्राहक देणार' : '📦 स्वतःचे'} ${r.notes ? `• ${r.notes}` : ''}</div>
          </div>
          <div class="item-action-btns">
            <button class="btn-icon btn-delete" onclick="confirmDeleteSubItem('resources', ${r.id})">🗑️</button>
          </div>
        </div>
      `).join("");
  } else if (type === 'helpers') {
    modalTitle.innerText = "हेल्पर यादी (Helpers)";
    container.innerHTML = o.helpers.length === 0
      ? `<div class="empty-state">कोणतेही हेल्पर जोडलेले नाहीत.</div>`
      : o.helpers.map(h => `
        <div class="item-card">
          <div>
            <div class="item-title">${h.helper_name} (₹${h.wage_amount})</div>
            <div class="item-sub">⏰ ${h.reach_time || 'वेळ नाही'} • ${h.payment_status}</div>
          </div>
          <div class="item-action-btns">
            <button class="btn-icon btn-delete" onclick="confirmDeleteSubItem('helpers', ${h.id})">🗑️</button>
          </div>
        </div>
      `).join("");
  } else if (type === 'utensils') {
    modalTitle.innerText = "भांडी नोंद (Utensils)";
    container.innerHTML = o.utensils.length === 0
      ? `<div class="empty-state">भांडी नोंदवलेली नाहीत.</div>`
      : o.utensils.map(u => `
        <div class="item-card">
          <div>
            <div class="item-title">${u.item_name}</div>
            <div class="item-sub">दिलेली: ${u.quantity_sent} | परत आलेली: ${u.quantity_returned}</div>
          </div>
          <div class="item-action-btns">
            <button class="btn-icon" onclick="updateUtensilPrompt(${u.id}, ${u.quantity_returned})">🔄</button>
            <button class="btn-icon btn-delete" onclick="confirmDeleteSubItem('utensils', ${u.id})">🗑️</button>
          </div>
        </div>
      `).join("");
  } else if (type === 'payments') {
    modalTitle.innerText = "पेमेंट नोंदी (Payments)";
    container.innerHTML = o.payments.length === 0
      ? `<div class="empty-state">पेमेंट नोंदवलेले नाही.</div>`
      : o.payments.map(p => `
        <div class="item-card">
          <div>
            <div class="item-title" style="color:#059669;">₹${p.amount}</div>
            <div class="item-sub">मोड: ${p.payment_mode} • तारीख: ${p.payment_date}</div>
          </div>
          <div class="item-action-btns">
            <button class="btn-icon btn-delete" onclick="confirmDeleteSubItem('payments', ${p.id})">🗑️</button>
          </div>
        </div>
      `).join("");
  }
}

// Inline Sub-Item Edits & Confirmed Deletions
async function promptEditMenu(itemId, oldName) {
  const newName = prompt("मेन्यू आयटमचे नवीन नाव टाका:", oldName);
  if (!newName || newName.trim() === "" || newName === oldName) return;

  const res = await fetch(`${API_BASE}/orders/${currentActiveOrderId}/menu/${itemId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ item_name: newName.trim() })
  });
  if (res.ok) {
    await openOrderDetail(currentActiveOrderId);
    openManageSection('menu');
  }
}

async function updateUtensilPrompt(utensilId, currentReturned) {
  const returnedCount = prompt("परत आलेल्या भांड्यांची संख्या टाका (Returned count):", currentReturned);
  if (returnedCount === null) return;

  const res = await fetch(`${API_BASE}/orders/${currentActiveOrderId}/utensils/${utensilId}?quantity_returned=${parseInt(returnedCount) || 0}`, {
    method: "PATCH"
  });
  if (res.ok) {
    await openOrderDetail(currentActiveOrderId);
    openManageSection('utensils');
  }
}

async function confirmDeleteSubItem(type, itemId) {
  if (!confirm("तुम्हाला ही नोंद कायमची काढून टाकायची आहे का? (Confirm delete this record?)")) {
    return;
  }

  const res = await fetch(`${API_BASE}/orders/${currentActiveOrderId}/${type}/${itemId}`, {
    method: "DELETE"
  });
  if (res.ok) {
    await openOrderDetail(currentActiveOrderId);
    openManageSection(type);
  } else {
    alert("नोंद काढताना अडचण आली.");
  }
}

// Sub-Item Add Modal
function openSubModal(type) {
  const container = document.getElementById("subitem-form-container");
  const title = document.getElementById("subitem-modal-title");
  document.getElementById("modal-add-subitem").style.display = "flex";

  if (type === 'menu') {
    title.innerText = "मेन्यू आयटम जोडा (Add Menu Dish)";
    container.innerHTML = `
      <input type="text" id="sub-menu-name" placeholder="उदा. पाव भाजी, पुलाव, गुलाबजाम" required>
      <button class="primary-btn" onclick="saveSubItem('menu')">मेन्यूमध्ये जोडा</button>
    `;
  } else if (type === 'resources') {
    title.innerText = "कच्चा माल / सामान (Add Ingredient)";
    container.innerHTML = `
      <input type="text" id="sub-res-name" placeholder="उदा. बटाटे, कांदा, तेल" required>
      <div class="form-row">
        <input type="number" id="sub-res-qty" placeholder="प्रमाण (Qty)" required>
        <input type="text" id="sub-res-unit" placeholder="एकक (उदा. kg, लिटर)" required>
      </div>
      <label for="sub-res-client" style="font-size:0.85rem; display:flex; align-items:center; gap:8px; margin-bottom:12px; cursor:pointer;">
        <input type="checkbox" id="sub-res-client">
        <span>हे सामान ग्राहक देणार आहे? (Client Provided)</span>
      </label>
      <button class="primary-btn" onclick="saveSubItem('resources')">सामान सेव्ह करा</button>
    `;
  } else if (type === 'helpers') {
    title.innerText = "हेल्पर जोडा (Add Helper)";
    container.innerHTML = `
      <input type="text" id="sub-help-name" placeholder="हेल्परचे नाव (Name)*" required>
      <div class="form-row">
        <input type="text" id="sub-help-reach" placeholder="येण्याची वेळ">
        <input type="number" id="sub-help-wage" placeholder="मजुरी ₹">
      </div>
      <button class="primary-btn" onclick="saveSubItem('helpers')">हेल्पर सेव्ह करा</button>
    `;
  } else if (type === 'utensils') {
    title.innerText = "भांडी नोंद (Utensils Sent)";
    container.innerHTML = `
      <input type="text" id="sub-uten-name" placeholder="भांड्याचे नाव (उदा. पातेले, हंडा)" required>
      <input type="number" id="sub-uten-sent" placeholder="दिलेली संख्या (Sent Count)" required>
      <button class="primary-btn" onclick="saveSubItem('utensils')">भांडी सेव्ह करा</button>
    `;
  } else if (type === 'payments') {
    title.innerText = "पेमेंट नोंदवा (Receive Payment)";
    container.innerHTML = `
      <input type="number" id="sub-pay-amount" placeholder="जमा रक्कम ₹" required>
      <select id="sub-pay-mode" style="width:100%; padding:12px; border-radius:12px; margin-bottom:12px;">
        <option value="Cash">Cash (रोख)</option>
        <option value="GPay">GPay / PhonePe (UPI)</option>
        <option value="Bank">Bank Transfer</option>
      </select>
      <button class="primary-btn" onclick="saveSubItem('payments')">पेमेंट जमा करा</button>
    `;
  }
}

async function saveSubItem(type) {
  let endpoint = `${API_BASE}/orders/${currentActiveOrderId}/${type}`;
  let payload = {};

  if (type === 'menu') {
    payload = { item_name: document.getElementById("sub-menu-name").value };
  } else if (type === 'resources') {
    payload = {
      resource_name: document.getElementById("sub-res-name").value,
      quantity: parseFloat(document.getElementById("sub-res-qty").value),
      unit: document.getElementById("sub-res-unit").value,
      is_client_provided: document.getElementById("sub-res-client").checked
    };
  } else if (type === 'helpers') {
    payload = {
      helper_name: document.getElementById("sub-help-name").value,
      reach_time: document.getElementById("sub-help-reach").value,
      wage_amount: parseFloat(document.getElementById("sub-help-wage").value) || 0
    };
  } else if (type === 'utensils') {
    payload = {
      item_name: document.getElementById("sub-uten-name").value,
      quantity_sent: parseInt(document.getElementById("sub-uten-sent").value) || 0
    };
  } else if (type === 'payments') {
    payload = {
      amount: parseFloat(document.getElementById("sub-pay-amount").value),
      payment_mode: document.getElementById("sub-pay-mode").value
    };
  }

  const res = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    document.getElementById("modal-add-subitem").style.display = "none";
    await openOrderDetail(currentActiveOrderId);
    openManageSection(type);
  }
}

// --- 11. PDF GENERATION & NATIVE WHATSAPP SHARE ---
async function shareMaterialListPDF(orderId, orderTitle) {
  try {
    const res = await fetch(`${API_BASE}/orders/${orderId}/pdf/client-materials?client_provided_only=true`);
    if (!res.ok) throw new Error("Server could not generate PDF");

    const blob = await res.blob();
    const safeTitle = orderTitle.replace(/[^a-zA-Z0-9]/g, '_');
    const filename = `CaterDost_Materials_${safeTitle}.pdf`;
    const file = new File([blob], filename, { type: 'application/pdf' });

    if (navigator.canShare && navigator.canShare({ files: [file] })) {
      await navigator.share({
        files: [file],
        title: `${orderTitle} - Raw Materials List`,
        text: `Here is the raw material requirement list for ${orderTitle}.`
      });
    } else {
      const downloadUrl = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(downloadUrl);
    }
  } catch (err) {
    alert("Error generating PDF: " + err.message);
  }
}

// --- 12. EXTERNAL WORK (RESPONSIBILITY 2) ---
function openExternalWorkModal() {
  document.getElementById("modal-external-work").style.display = "flex";
}

async function submitExternalWork(e) {
  e.preventDefault();
  const payload = {
    hired_by_name: document.getElementById("ext-hired-by").value,
    phone: document.getElementById("ext-phone").value,
    work_date: document.getElementById("ext-date").value,
    reach_time: document.getElementById("ext-reach-time").value,
    location: document.getElementById("ext-location").value,
    agreed_pay: parseFloat(document.getElementById("ext-pay").value) || 0,
    notes: document.getElementById("ext-notes").value
  };

  const res = await fetch(`${API_BASE}/external-work`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    document.getElementById("modal-external-work").style.display = "none";
    document.getElementById("externalWorkForm").reset();
    loadExternalWork();
  }
}

async function loadExternalWork() {
  try {
    const res = await fetch(`${API_BASE}/external-work`);
    const data = await res.json();
    const list = document.getElementById("external-work-list");

    list.innerHTML = data.length === 0
      ? `<div class="empty-state">बाहेरचे कोणतेही काम नोंदवलेले नाही.</div>`
      : data.map(w => `
        <div class="item-card">
          <div>
            <div class="item-title">कॅटरर: ${w.hired_by_name}</div>
            <div class="item-sub">📅 ${w.work_date} • 📍 ${w.location || 'ठिकाण'}</div>
            <div class="item-sub" style="font-weight:600;">पैसे: ₹${w.agreed_pay}</div>
          </div>
          <span class="pill-badge ${w.payment_status === 'PAID' ? 'badge-paid' : 'badge-pending'}">${w.payment_status}</span>
        </div>
      `).join("");
  } catch (err) {
    console.error(err);
  }
}

// --- 13. HISTORY SEARCH ---
async function searchHistory() {
  const q = document.getElementById("historySearchInput").value.trim();
  if (!q) return alert("नाव टाईप करा");

  try {
    const res = await fetch(`${API_BASE}/history/clients?query=${q}`);
    const data = await res.json();
    const results = document.getElementById("history-results");

    results.innerHTML = data.length === 0
      ? `<div class="empty-state">कोणतीही नोंद सापडली नाही.</div>`
      : data.map(c => `
        <div class="item-card">
          <div>
            <div class="item-title">👤 ${c.name} (${c.phone})</div>
            <div class="item-sub">एकूण ऑर्डर्स: ${c.total_orders}</div>
            ${c.orders.map(o => `<div style="font-size:0.8rem; margin-top:4px;">• ${o.order_title} (₹${o.agreed_amount}) - ${o.status}</div>`).join("")}
          </div>
        </div>
      `).join("");
  } catch {
    alert("त्रुटी आली.");
  }
}

// --- 14. QUICK BOOKING MODAL ---
function openQuickBookModal() {
  document.getElementById("modal-quick-book").style.display = "flex";
}

function closeModalOnBackdrop(e, modalId) {
  if (e.target.id === modalId) {
    document.getElementById(modalId).style.display = "none";
  }
}

async function submitQuickBook(e) {
  e.preventDefault();
  const payload = {
    client_name: document.getElementById("qb-name").value,
    client_phone: document.getElementById("qb-phone").value,
    order_title: document.getElementById("qb-title").value,
    event_date: document.getElementById("qb-date").value,
    event_time: document.getElementById("qb-time").value || "11:00 AM",
    people_count: parseInt(document.getElementById("qb-people").value) || 0,
    location: document.getElementById("qb-location").value,
    agreed_amount: parseFloat(document.getElementById("qb-agreed").value) || 0,
    advance_amount: parseFloat(document.getElementById("qb-advance").value) || 0,
    special_notes: document.getElementById("qb-notes").value
  };

  const res = await fetch(`${API_BASE}/orders/quick-book`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    document.getElementById("modal-quick-book").style.display = "none";
    document.getElementById("quickBookForm").reset();
    loadDashboard();
  }
}

// --- 15. APPLICATION INITIALIZATION ---
document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("searchDateInput");
  if (searchInput) searchInput.value = new Date().toISOString().split('T')[0];
  checkAuth();
  applyLanguage();
});