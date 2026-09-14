/**
 * ==============================================================================
 * APEX NATIONAL BANK — ENTERPRISE CORE CONTROLLER (app.js)
 * Classic Corporate Banking / Enterprise Banking Architecture
 * ==============================================================================
 */

// Application State
const state = {
  activeView: 'dashboard',
  activeAccountNum: null,
  activeAccountData: null,
  accountsList: [],
  allTransactions: [],
  filteredTransactions: [],
  txFilter: 'ALL',
  txSearchQuery: '',
  accountsSearchQuery: '',
  accountsTypeFilter: 'ALL',
  emailLogs: [],
  bstTreeData: null,
  currentOpMode: 'DEPOSIT', // 'DEPOSIT' or 'WITHDRAWAL'
  activeDSATab: 'linked-list',
  systemStatus: null,
  fraudResolveTargetAcc: null,
};

const API_BASE = '/api';

// DOM Element Cache
const DOM = {
  // Sidebar & Navigation
  sidebar: document.getElementById('sidebar'),
  btnMobileToggle: document.getElementById('btnMobileToggle'),
  accountSelect: document.getElementById('accountSelect'),
  sidebarAccountsCount: document.getElementById('sidebarAccountsCount'),
  sidebarFraudBadge: document.getElementById('sidebarFraudBadge'),
  sidebarEmailCount: document.getElementById('sidebarEmailCount'),
  sidebarStatusText: document.getElementById('sidebarStatusText'),
  currentBreadcrumb: document.getElementById('currentBreadcrumb'),
  currentTimestamp: document.getElementById('currentTimestamp'),
  btnGlobalRefresh: document.getElementById('btnGlobalRefresh'),
  btnQuickOpenAccount: document.getElementById('btnQuickOpenAccount'),
  btnQuickTransfer: document.getElementById('btnQuickTransfer'),
  
  // Views
  views: {
    dashboard: document.getElementById('view-dashboard'),
    accounts: document.getElementById('view-accounts'),
    transactions: document.getElementById('view-transactions'),
    fraud: document.getElementById('view-fraud'),
    dsa: document.getElementById('view-dsa'),
    emails: document.getElementById('view-emails'),
    settings: document.getElementById('view-settings'),
  },
  navButtons: {
    dashboard: document.getElementById('navDashboard'),
    accounts: document.getElementById('navAccounts'),
    transactions: document.getElementById('navTransactions'),
    fraud: document.getElementById('navFraud'),
    dsa: document.getElementById('navDSA'),
    emails: document.getElementById('navEmails'),
    settings: document.getElementById('navSettings'),
  },

  // Fraud Alert Global Banner
  fraudAlertBanner: document.getElementById('fraudAlertBanner'),
  fraudAlertMessage: document.getElementById('fraudAlertMessage'),
  btnResolveFraudBanner: document.getElementById('btnResolveFraudBanner'),

  // Dashboard View Elements
  dashboardActiveAccBadge: document.getElementById('dashboardActiveAccBadge'),
  kpiActiveBalance: document.getElementById('kpiActiveBalance'),
  kpiAccountStatus: document.getElementById('kpiAccountStatus'),
  kpiAccountType: document.getElementById('kpiAccountType'),
  kpiTotalDeposits: document.getElementById('kpiTotalDeposits'),
  kpiTotalAccountsCount: document.getElementById('kpiTotalAccountsCount'),
  kpiTotalTransactions: document.getElementById('kpiTotalTransactions'),
  kpiRiskCard: document.getElementById('kpiRiskCard'),
  kpiRiskLevel: document.getElementById('kpiRiskLevel'),
  kpiRiskSubtext: document.getElementById('kpiRiskSubtext'),
  
  // Dashboard Account Profile
  dashHolderName: document.getElementById('dashHolderName'),
  dashAccNumber: document.getElementById('dashAccNumber'),
  dashAccType: document.getElementById('dashAccType'),
  dashEmail: document.getElementById('dashEmail'),
  dashPhone: document.getElementById('dashPhone'),
  dashCreatedDate: document.getElementById('dashCreatedDate'),
  dashStatusBadge: document.getElementById('dashStatusBadge'),
  btnCopyDashboardAcc: document.getElementById('btnCopyDashboardAcc'),

  // Dashboard Operations Panel
  tabOpDeposit: document.getElementById('tabOpDeposit'),
  tabOpWithdraw: document.getElementById('tabOpWithdraw'),
  dashTxAmount: document.getElementById('dashTxAmount'),
  dashTxDesc: document.getElementById('dashTxDesc'),
  prevCurrentBal: document.getElementById('prevCurrentBal'),
  prevPostBal: document.getElementById('prevPostBal'),
  btnDashExecuteTx: document.getElementById('btnDashExecuteTx'),
  btnDashExecuteText: document.getElementById('btnDashExecuteText'),
  presetButtons: document.querySelectorAll('.btn-preset'),

  // Dashboard Sliding Window Monitor
  dashWindowSlots: document.getElementById('dashWindowSlots'),
  dashWindowSum: document.getElementById('dashWindowSum'),
  dashThresholdPctLabel: document.getElementById('dashThresholdPctLabel'),
  dashThresholdLimitLabel: document.getElementById('dashThresholdLimitLabel'),
  dashThresholdFill: document.getElementById('dashThresholdFill'),
  dashWindowRecentTable: document.getElementById('dashWindowRecentTable'),
  dashRecentTxBody: document.getElementById('dashRecentTxBody'),
  btnViewAllTransactions: document.getElementById('btnViewAllTransactions'),

  // Accounts Roster View
  accountsSearchInput: document.getElementById('accountsSearchInput'),
  accountsTypeFilter: document.getElementById('accountsTypeFilter'),
  accountsRosterBody: document.getElementById('accountsRosterBody'),
  btnOpenAccountModalFromRoster: document.getElementById('btnOpenAccountModalFromRoster'),

  // Transactions Ledger View
  txLedgerHeadSnippet: document.getElementById('txLedgerHeadSnippet'),
  txFilterTabs: document.getElementById('txFilterTabs'),
  txSearchInput: document.getElementById('txSearchInput'),
  fullTxTableBody: document.getElementById('fullTxTableBody'),
  btnRefreshTxLedger: document.getElementById('btnRefreshTxLedger'),

  // Fraud Center View
  fraudRiskLevelVal: document.getElementById('fraudRiskLevelVal'),
  fraudRiskStatusReason: document.getElementById('fraudRiskStatusReason'),
  fraudWindowSumVal: document.getElementById('fraudWindowSumVal'),
  fraudWindowOpsCount: document.getElementById('fraudWindowOpsCount'),
  fraudThresholdLimitVal: document.getElementById('fraudThresholdLimitVal'),
  fraudHoldStatusVal: document.getElementById('fraudHoldStatusVal'),
  btnResolveFraudCenter: document.getElementById('btnResolveFraudCenter'),
  fraudQueueVisual: document.getElementById('fraudQueueVisual'),
  fraudCenterPct: document.getElementById('fraudCenterPct'),
  fraudCenterMax: document.getElementById('fraudCenterMax'),
  fraudCenterBar: document.getElementById('fraudCenterBar'),
  fraudAlertsBody: document.getElementById('fraudAlertsBody'),

  // DSA Engine Visualizers
  dsaTabs: document.querySelectorAll('.dsa-tab'),
  dsaPanes: {
    'linked-list': document.getElementById('dsa-pane-linked-list'),
    'bst': document.getElementById('dsa-pane-bst'),
    'sliding-window': document.getElementById('dsa-pane-sliding-window'),
    'hash-map': document.getElementById('dsa-pane-hash-map'),
  },
  dsaLLCanvas: document.getElementById('dsaLLCanvas'),
  dsaBSTSearchInput: document.getElementById('dsaBSTSearchInput'),
  btnDSASearchBST: document.getElementById('btnDSASearchBST'),
  dsaBSTSearchFeedback: document.getElementById('dsaBSTSearchFeedback'),
  dsaTreeHierarchy: document.getElementById('dsaTreeHierarchy'),
  dsaBSTInorderList: document.getElementById('dsaBSTInorderList'),
  dsaSlidingWindowDiagram: document.getElementById('dsaSlidingWindowDiagram'),
  dsaHashMapBody: document.getElementById('dsaHashMapBody'),

  // Email & Audit Logs View
  emailDeliveryModeText: document.getElementById('emailDeliveryModeText'),
  emailTotalLoggedBadge: document.getElementById('emailTotalLoggedBadge'),
  emailLogsBody: document.getElementById('emailLogsBody'),
  btnRefreshEmailsView: document.getElementById('btnRefreshEmailsView'),

  // Settings View
  setWindowK: document.getElementById('setWindowK'),
  setFraudThreshold: document.getElementById('setFraudThreshold'),
  btnSaveFraudSettings: document.getElementById('btnSaveFraudSettings'),
  diagSmtpMode: document.getElementById('diagSmtpMode'),

  // Modals
  createAccountModal: document.getElementById('createAccountModal'),
  btnCloseCreateAccountModal: document.getElementById('btnCloseCreateAccountModal'),
  btnCancelCreateAccountModal: document.getElementById('btnCancelCreateAccountModal'),
  btnSubmitCreateAccount: document.getElementById('btnSubmitCreateAccount'),
  createAccountModalForm: document.getElementById('createAccountModalForm'),
  inputNewName: document.getElementById('inputNewName'),
  inputNewEmail: document.getElementById('inputNewEmail'),
  inputNewAccNum: document.getElementById('inputNewAccNum'),
  inputNewAccType: document.getElementById('inputNewAccType'),
  inputNewInitialDeposit: document.getElementById('inputNewInitialDeposit'),
  inputNewPhone: document.getElementById('inputNewPhone'),

  // Email Preview Modal
  emailPreviewModal: document.getElementById('emailPreviewModal'),
  btnCloseEmailPreviewModal: document.getElementById('btnCloseEmailPreviewModal'),
  btnCloseEmailPreviewBtn: document.getElementById('btnCloseEmailPreviewBtn'),
  modalEmailSubject: document.getElementById('modalEmailSubject'),
  emailPreviewMeta: document.getElementById('emailPreviewMeta'),
  emailPreviewHtmlContainer: document.getElementById('emailPreviewHtmlContainer'),

  // Fraud Resolution Modal
  fraudResolutionModal: document.getElementById('fraudResolutionModal'),
  btnCloseFraudModal: document.getElementById('btnCloseFraudModal'),
  btnCancelFraudModal: document.getElementById('btnCancelFraudModal'),
  btnConfirmFraudResolution: document.getElementById('btnConfirmFraudResolution'),
  fraudResolveAccNum: document.getElementById('fraudResolveAccNum'),

  // Toast Container
  toastContainer: document.getElementById('toastContainer'),
};

// ==============================================================================
// UTILITY FUNCTIONS
// ==============================================================================

function formatCurrency(amount) {
  return new Intl.NumberFormat('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount || 0);
}

function showToast(title, message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  let iconClass = 'fa-solid fa-circle-info';
  if (type === 'success') iconClass = 'fa-solid fa-circle-check';
  if (type === 'danger') iconClass = 'fa-solid fa-triangle-exclamation';
  if (type === 'warning') iconClass = 'fa-solid fa-shield-halved';
  
  toast.innerHTML = `
    <i class="${iconClass} toast-icon"></i>
    <div class="toast-content">
      <div class="toast-title">${title}</div>
      <div class="toast-msg">${message}</div>
    </div>
    <button class="toast-close" aria-label="Close notification">&times;</button>
  `;
  
  toast.querySelector('.toast-close').onclick = () => toast.remove();
  DOM.toastContainer.appendChild(toast);
  
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(20px)';
    setTimeout(() => toast.remove(), 250);
  }, 4500);
}

// ==============================================================================
// API CLIENT
// ==============================================================================

async function apiRequest(endpoint, options = {}) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'API Request Failed');
    }
    return data;
  } catch (err) {
    console.error(`API Error [${endpoint}]:`, err);
    throw err;
  }
}

// ==============================================================================
// VIEW ROUTER & NAVIGATION
// ==============================================================================

const VIEW_TITLES = {
  dashboard: 'Executive Dashboard',
  accounts: 'Bank Accounts Roster',
  transactions: 'Transactions Ledger',
  fraud: 'Fraud Detection & Risk Center',
  dsa: 'Core DSA Algorithmic Engine',
  emails: 'Email & Notification Logs',
  settings: 'System & Algorithmic Settings',
};

function switchView(viewName) {
  if (!DOM.views[viewName]) return;
  state.activeView = viewName;

  // Toggle View Containers
  Object.keys(DOM.views).forEach(key => {
    if (key === viewName) {
      DOM.views[key].classList.remove('hidden');
      DOM.views[key].classList.add('active');
    } else {
      DOM.views[key].classList.add('hidden');
      DOM.views[key].classList.remove('active');
    }
  });

  // Toggle Navigation Link Active Classes
  Object.keys(DOM.navButtons).forEach(key => {
    if (key === viewName) {
      DOM.navButtons[key].classList.add('active');
    } else {
      DOM.navButtons[key].classList.remove('active');
    }
  });

  // Update Breadcrumb
  DOM.currentBreadcrumb.textContent = VIEW_TITLES[viewName] || 'Enterprise Portal';

  // Trigger view-specific refreshes
  if (viewName === 'accounts') renderAccountsRoster();
  if (viewName === 'transactions') renderFullTransactionsLedger();
  if (viewName === 'fraud') renderFraudCenter();
  if (viewName === 'dsa') renderDSAVisualizers();
  if (viewName === 'emails') loadEmailLogs();

  // Close mobile sidebar if open
  DOM.sidebar.classList.remove('mobile-open');
}

// ==============================================================================
// CORE DATA LOADING & ACCOUNT MANAGEMENT
// ==============================================================================

async function loadAccounts(preferredAccountNum = null) {
  try {
    const data = await apiRequest('/accounts');
    state.accountsList = data.accounts || [];
    
    // Update sidebar accounts count
    DOM.sidebarAccountsCount.textContent = state.accountsList.length;

    // Populate Sidebar Account Selector
    DOM.accountSelect.innerHTML = '';
    state.accountsList.forEach(acc => {
      const opt = document.createElement('option');
      opt.value = acc.account_number;
      opt.textContent = `${acc.account_name} (#${acc.account_number}) — ₹${formatCurrency(acc.balance)}`;
      DOM.accountSelect.appendChild(opt);
    });

    // Determine target account
    let targetNum = preferredAccountNum || state.activeAccountNum;
    if (!targetNum && state.accountsList.length > 0) {
      targetNum = state.accountsList[0].account_number;
    }

    if (targetNum) {
      DOM.accountSelect.value = targetNum;
      await selectAccount(targetNum);
    }

    await refreshSystemStatus();
    loadEmailLogs();
    loadBSTVisualizer();
  } catch (err) {
    showToast('Failed to Load Accounts', err.message, 'danger');
  }
}

async function selectAccount(accountNum) {
  if (!accountNum) return;
  state.activeAccountNum = accountNum;
  DOM.accountSelect.value = accountNum;

  try {
    const accountData = await apiRequest(`/accounts/${accountNum}`);
    state.activeAccountData = accountData;

    renderDashboardAccountProfile(accountData);
    renderDashboardSlidingWindow(accountData.fraud_metrics);
    await loadAccountTransactions(accountNum);

    // Refresh current active view components
    if (state.activeView === 'fraud') renderFraudCenter();
    if (state.activeView === 'dsa') renderDSAVisualizers();
  } catch (err) {
    showToast('Error Loading Account', err.message, 'danger');
  }
}

async function refreshSystemStatus() {
  try {
    const data = await apiRequest('/system/status');
    state.systemStatus = data;

    DOM.kpiTotalDeposits.textContent = formatCurrency(data.total_deposits);
    DOM.kpiTotalAccountsCount.textContent = `Across ${data.total_accounts} registered accounts`;
    DOM.kpiTotalTransactions.textContent = data.total_transactions;
    DOM.sidebarStatusText.textContent = `${data.total_accounts} Accounts • ${data.total_transactions} Transactions`;

    // Flagged accounts count check
    if (data.flagged_accounts_count > 0) {
      DOM.sidebarFraudBadge.classList.remove('hidden');
      DOM.sidebarFraudBadge.textContent = `${data.flagged_accounts_count} FLAGGED`;
    } else {
      DOM.sidebarFraudBadge.classList.add('hidden');
    }
  } catch (err) {
    DOM.sidebarStatusText.textContent = 'Backend Offline';
  }
}

// ==============================================================================
// DASHBOARD RENDERING
// ==============================================================================

function renderDashboardAccountProfile(acc) {
  if (!acc) return;

  DOM.dashboardActiveAccBadge.textContent = `Account: #${acc.account_number}`;
  DOM.kpiActiveBalance.textContent = formatCurrency(acc.balance);
  DOM.kpiAccountType.textContent = `${acc.account_type || 'SAVINGS'} ACCOUNT`;

  // Account Profile Table
  DOM.dashHolderName.textContent = acc.account_name;
  DOM.dashAccNumber.textContent = acc.account_number;
  DOM.dashAccType.textContent = acc.account_type || 'SAVINGS';
  DOM.dashEmail.textContent = acc.email;
  DOM.dashPhone.textContent = acc.phone || '+91 98765 43210';
  DOM.dashCreatedDate.textContent = (acc.created_at || '').split(' ')[0] || 'Today';

  const isFlagged = acc.status === 'FLAGGED' || (acc.fraud_metrics && acc.fraud_metrics.is_flagged);

  if (isFlagged) {
    DOM.kpiAccountStatus.textContent = 'FLAGGED (HIGH RISK)';
    DOM.kpiAccountStatus.className = 'kpi-status-tag bg-danger text-danger';
    DOM.dashStatusBadge.textContent = 'FLAGGED';
    DOM.dashStatusBadge.className = 'status-badge badge-flagged';

    DOM.kpiRiskLevel.textContent = 'CRITICAL FRAUD';
    DOM.kpiRiskLevel.className = 'kpi-value text-danger';
    DOM.kpiRiskSubtext.textContent = 'Security hold triggered by Sliding Window';

    // Global Alert Banner
    DOM.fraudAlertBanner.classList.remove('hidden');
    const reason = (acc.fraud_metrics && acc.fraud_metrics.reason) ||
      `Velocity breach: Window sum ₹${formatCurrency(acc.fraud_metrics?.window_sum)} exceeded ₹${formatCurrency(acc.fraud_metrics?.threshold)}.`;
    DOM.fraudAlertMessage.textContent = reason;
  } else {
    DOM.kpiAccountStatus.textContent = 'ACTIVE';
    DOM.kpiAccountStatus.className = 'kpi-status-tag';
    DOM.dashStatusBadge.textContent = 'ACTIVE';
    DOM.dashStatusBadge.className = 'status-badge badge-active';

    DOM.kpiRiskLevel.textContent = 'SAFE';
    DOM.kpiRiskLevel.className = 'kpi-value text-success';
    DOM.kpiRiskSubtext.textContent = 'Normal velocity within authorized parameters';

    DOM.fraudAlertBanner.classList.add('hidden');
  }

  updateLiveBalancePreview();
}

function renderDashboardSlidingWindow(metrics) {
  if (!metrics) return;

  const kSize = metrics.window_size || 3;
  const amounts = metrics.window_amounts || [];
  const currentSum = metrics.window_sum || 0;
  const threshold = metrics.threshold || 50000;
  const pct = Math.min(100, Math.round((currentSum / threshold) * 100));
  const isFlagged = metrics.is_flagged;

  // Window Slots
  DOM.dashWindowSlots.innerHTML = '';
  for (let i = 0; i < kSize; i++) {
    const slot = document.createElement('span');
    if (i < amounts.length) {
      slot.className = isFlagged ? 'slot-badge flagged' : 'slot-badge filled';
      slot.textContent = `₹${formatCurrency(amounts[i])}`;
    } else {
      slot.className = 'slot-badge empty';
      slot.textContent = `Slot ${i + 1}: Empty`;
    }
    DOM.dashWindowSlots.appendChild(slot);
  }

  // Window Sum & Progress Bar
  DOM.dashWindowSum.textContent = `₹${formatCurrency(currentSum)}`;
  DOM.dashThresholdPctLabel.textContent = `${pct}% of security limit (${kSize} operations frame)`;
  DOM.dashThresholdLimitLabel.textContent = `Limit: ₹${formatCurrency(threshold)}`;
  DOM.dashThresholdFill.style.width = `${pct}%`;

  DOM.dashThresholdFill.className = 'progress-fill';
  if (isFlagged || pct >= 100) {
    DOM.dashThresholdFill.classList.add('danger');
  } else if (pct >= 75) {
    DOM.dashThresholdFill.classList.add('warn');
  }

  // Active Window Operations List
  if (amounts.length === 0) {
    DOM.dashWindowRecentTable.innerHTML = `<div class="empty-state-sm">No operations in active evaluation window.</div>`;
  } else {
    DOM.dashWindowRecentTable.innerHTML = amounts.map((amt, idx) => `
      <div class="window-op-row">
        <span>Window Operation #${idx + 1}</span>
        <strong class="font-mono">₹${formatCurrency(amt)}</strong>
      </div>
    `).join('');
  }
}

// ==============================================================================
// TRANSACTIONS LEDGER & OPERATIONS
// ==============================================================================

async function loadAccountTransactions(accountNum) {
  try {
    const data = await apiRequest(`/transactions/${accountNum}`);
    state.allTransactions = data.transactions || [];
    
    renderDashboardRecentTransactions(state.allTransactions.slice(0, 5));
    renderFullTransactionsLedger();
  } catch (err) {
    console.error('Failed to load transactions:', err);
  }
}

function renderDashboardRecentTransactions(transactions) {
  if (!transactions || transactions.length === 0) {
    DOM.dashRecentTxBody.innerHTML = `
      <tr><td colspan="7" class="empty-state-sm">No transactions recorded for this account.</td></tr>
    `;
    return;
  }

  DOM.dashRecentTxBody.innerHTML = transactions.map(tx => {
    const isCredit = tx.tx_type === 'DEPOSIT' || tx.tx_type === 'INITIAL_DEPOSIT';
    const sign = isCredit ? '+' : '-';
    const typeClass = isCredit ? 'tx-type-credit' : 'tx-type-debit';
    const amountClass = isCredit ? 'amount-credit' : 'amount-debit';
    const statusBadge = tx.status === 'FLAGGED' ? 'badge-flagged' : 'badge-completed';

    return `
      <tr>
        <td class="font-mono font-bold">${tx.tx_id}</td>
        <td style="white-space:nowrap; font-size:11.5px; color:var(--text-muted);">${tx.timestamp}</td>
        <td><strong>${tx.description || '-'}</strong></td>
        <td><span class="tx-type-badge ${typeClass}">${tx.tx_type}</span></td>
        <td class="text-right ${amountClass}">${sign}₹${formatCurrency(tx.amount)}</td>
        <td class="text-right font-mono font-bold">₹${formatCurrency(tx.balance_after)}</td>
        <td class="text-center"><span class="status-badge ${statusBadge}">${tx.status}</span></td>
      </tr>
    `;
  }).join('');
}

function renderFullTransactionsLedger() {
  let list = state.allTransactions;

  // Filter by Type
  if (state.txFilter === 'DEPOSIT') {
    list = list.filter(t => t.tx_type === 'DEPOSIT' || t.tx_type === 'INITIAL_DEPOSIT');
  } else if (state.txFilter === 'WITHDRAWAL') {
    list = list.filter(t => t.tx_type === 'WITHDRAWAL');
  } else if (state.txFilter === 'FLAGGED') {
    list = list.filter(t => t.is_fraud_flagged || t.status === 'FLAGGED');
  }

  // Filter by Search Query
  if (state.txSearchQuery) {
    const q = state.txSearchQuery.toLowerCase();
    list = list.filter(t => 
      t.tx_id.toLowerCase().includes(q) || 
      (t.description && t.description.toLowerCase().includes(q))
    );
  }

  // Update Head Pointer Ribbon
  if (state.allTransactions.length > 0) {
    const head = state.allTransactions[0];
    DOM.txLedgerHeadSnippet.textContent = `HEAD -> Node(ID: ${head.tx_id} | ${head.tx_type} ₹${formatCurrency(head.amount)} | Balance: ₹${formatCurrency(head.balance_after)}) -> Next`;
  } else {
    DOM.txLedgerHeadSnippet.textContent = 'HEAD -> [NULL (Empty Singly Linked List)]';
  }

  if (list.length === 0) {
    DOM.fullTxTableBody.innerHTML = `
      <tr><td colspan="7" class="empty-state-sm">No transaction records found matching active filter.</td></tr>
    `;
    return;
  }

  DOM.fullTxTableBody.innerHTML = list.map(tx => {
    const isCredit = tx.tx_type === 'DEPOSIT' || tx.tx_type === 'INITIAL_DEPOSIT';
    const sign = isCredit ? '+' : '-';
    const typeClass = isCredit ? 'tx-type-credit' : 'tx-type-debit';
    const amountClass = isCredit ? 'amount-credit' : 'amount-debit';
    const statusBadge = tx.status === 'FLAGGED' ? 'badge-flagged' : 'badge-completed';

    return `
      <tr>
        <td class="font-mono font-bold">${tx.tx_id}</td>
        <td style="white-space:nowrap; font-size:11.5px; color:var(--text-muted);">${tx.timestamp}</td>
        <td><strong>${tx.description || '-'}</strong></td>
        <td><span class="tx-type-badge ${typeClass}">${tx.tx_type}</span></td>
        <td class="text-right ${amountClass}">${sign}₹${formatCurrency(tx.amount)}</td>
        <td class="text-right font-mono font-bold">₹${formatCurrency(tx.balance_after)}</td>
        <td class="text-center"><span class="status-badge ${statusBadge}">${tx.status}</span></td>
      </tr>
    `;
  }).join('');
}

function updateLiveBalancePreview() {
  const amt = parseFloat(DOM.dashTxAmount.value) || 0;
  const currentBal = state.activeAccountData ? state.activeAccountData.balance : 0;
  
  DOM.prevCurrentBal.textContent = `₹${formatCurrency(currentBal)}`;
  
  let postBal = currentBal;
  if (state.currentOpMode === 'DEPOSIT') {
    postBal = currentBal + amt;
  } else {
    postBal = currentBal - amt;
  }

  DOM.prevPostBal.textContent = `₹${formatCurrency(postBal)}`;
  if (postBal < 0) {
    DOM.prevPostBal.className = 'preview-amount font-mono font-bold text-danger';
  } else {
    DOM.prevPostBal.className = 'preview-amount font-mono font-bold text-primary';
  }
}

async function executeBankingOperation() {
  const amount = parseFloat(DOM.dashTxAmount.value);
  const description = DOM.dashTxDesc.value.trim();
  const accNum = state.activeAccountNum;

  if (!accNum) {
    showToast('No Account Selected', 'Please select an operating bank account first.', 'warning');
    return;
  }

  if (!amount || amount <= 0) {
    showToast('Invalid Amount', 'Transaction amount must be strictly greater than zero.', 'warning');
    DOM.dashTxAmount.focus();
    return;
  }

  const endpoint = state.currentOpMode === 'DEPOSIT' ? '/deposit' : '/withdraw';
  const label = state.currentOpMode === 'DEPOSIT' ? 'Deposit' : 'Withdrawal';

  DOM.btnDashExecuteTx.disabled = true;
  DOM.btnDashExecuteText.textContent = `Executing ${label}...`;

  try {
    const res = await apiRequest(endpoint, {
      method: 'POST',
      body: JSON.stringify({
        account_number: accNum,
        amount: amount,
        description: description || `${label} Operation`,
      }),
    });

    DOM.dashTxAmount.value = '';
    DOM.dashTxDesc.value = '';

    const fraudEval = res.fraud_evaluation;
    if (fraudEval && fraudEval.is_flagged) {
      showToast(
        'Security Velocity Alert Triggered',
        `Sliding Window flagged cumulative volume of ₹${formatCurrency(fraudEval.window_sum)} exceeding limit of ₹${formatCurrency(fraudEval.threshold)}. Security email dispatched.`,
        'danger'
      );
    } else {
      showToast(
        `${label} Successful`,
        `₹${formatCurrency(amount)} processed successfully. Clear balance updated to ₹${formatCurrency(res.new_balance)}.`,
        'success'
      );
    }

    await selectAccount(accNum);
    await refreshSystemStatus();
    loadEmailLogs();
    loadBSTVisualizer();
  } catch (err) {
    showToast(`${label} Failed`, err.message, 'danger');
  } finally {
    DOM.btnDashExecuteTx.disabled = false;
    DOM.btnDashExecuteText.textContent = `Execute ${label}`;
    updateLiveBalancePreview();
  }
}

// ==============================================================================
// ACCOUNTS ROSTER VIEW
// ==============================================================================

function renderAccountsRoster() {
  let list = state.accountsList || [];

  // Filter by Type
  if (state.accountsTypeFilter !== 'ALL') {
    list = list.filter(a => a.account_type === state.accountsTypeFilter);
  }

  // Search Filter
  if (state.accountsSearchQuery) {
    const q = state.accountsSearchQuery.toLowerCase();
    list = list.filter(a => 
      a.account_number.toLowerCase().includes(q) || 
      a.account_name.toLowerCase().includes(q) ||
      a.email.toLowerCase().includes(q)
    );
  }

  if (list.length === 0) {
    DOM.accountsRosterBody.innerHTML = `
      <tr><td colspan="9" class="empty-state-sm">No accounts found matching search/filter criteria.</td></tr>
    `;
    return;
  }

  DOM.accountsRosterBody.innerHTML = list.map(acc => {
    const isFlagged = acc.status === 'FLAGGED';
    const statusBadge = isFlagged ? 'badge-flagged' : 'badge-active';
    const isCurrentActive = acc.account_number === state.activeAccountNum;

    return `
      <tr style="${isCurrentActive ? 'background-color: #EFF6FF;' : ''}">
        <td class="font-mono font-bold text-primary">#${acc.account_number}</td>
        <td><strong>${acc.account_name}</strong></td>
        <td>${acc.email}</td>
        <td style="color: var(--text-muted);">${acc.phone || '+91 98765 43210'}</td>
        <td><span class="badge badge-outline">${acc.account_type || 'SAVINGS'}</span></td>
        <td class="text-right font-mono font-bold">₹${formatCurrency(acc.balance)}</td>
        <td class="text-center"><span class="status-badge ${statusBadge}">${acc.status}</span></td>
        <td style="white-space:nowrap; font-size:11.5px; color:var(--text-muted);">${(acc.created_at || '').split(' ')[0]}</td>
        <td class="text-center">
          <button class="btn btn-secondary btn-xs" onclick="selectAndGoToDashboard('${acc.account_number}')">
            ${isCurrentActive ? '<i class="fa-solid fa-check"></i> Active' : 'Select'}
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

window.selectAndGoToDashboard = async function(accNum) {
  await selectAccount(accNum);
  switchView('dashboard');
};

// ==============================================================================
// FRAUD DETECTION CENTER
// ==============================================================================

function renderFraudCenter() {
  const acc = state.activeAccountData;
  if (!acc) return;

  const metrics = acc.fraud_metrics || {};
  const isFlagged = acc.status === 'FLAGGED' || metrics.is_flagged;
  const currentSum = metrics.window_sum || 0;
  const threshold = metrics.threshold || 50000;
  const kSize = metrics.window_size || 3;
  const pct = Math.min(100, Math.round((currentSum / threshold) * 100));

  DOM.fraudRiskLevelVal.textContent = isFlagged ? 'CRITICAL FRAUD' : (pct >= 75 ? 'MODERATE' : 'SAFE');
  DOM.fraudRiskLevelVal.className = isFlagged ? 'kpi-value text-danger' : (pct >= 75 ? 'kpi-value text-warning' : 'kpi-value text-success');
  DOM.fraudRiskStatusReason.textContent = isFlagged ? 'High velocity spike detected' : 'Operating within standard parameters';

  DOM.fraudWindowSumVal.textContent = formatCurrency(currentSum);
  DOM.fraudWindowOpsCount.textContent = `Last ${metrics.window_count || 0} of ${kSize} operations frame`;
  DOM.fraudThresholdLimitVal.textContent = formatCurrency(threshold);
  DOM.fraudHoldStatusVal.textContent = isFlagged ? 'HOLD ACTIVE' : 'CLEARED';
  DOM.fraudHoldStatusVal.className = isFlagged ? 'kpi-value text-danger font-bold' : 'kpi-value text-success';

  // Queue visualizer
  const amounts = metrics.window_amounts || [];
  DOM.fraudQueueVisual.innerHTML = '';
  for (let i = 0; i < kSize; i++) {
    const box = document.createElement('div');
    box.className = 'vmetric-box';
    if (i < amounts.length) {
      box.innerHTML = `
        <span class="vmetric-label">Slot #${i + 1}</span>
        <div class="vmetric-value font-mono ${isFlagged ? 'text-danger' : 'text-primary'}">₹${formatCurrency(amounts[i])}</div>
      `;
    } else {
      box.innerHTML = `
        <span class="vmetric-label">Slot #${i + 1}</span>
        <div class="vmetric-value font-mono text-muted">Empty</div>
      `;
    }
    DOM.fraudQueueVisual.appendChild(box);
  }

  // Progress Bar
  DOM.fraudCenterPct.textContent = `${pct}% of safety limit`;
  DOM.fraudCenterMax.textContent = `Threshold: ₹${formatCurrency(threshold)}`;
  DOM.fraudCenterBar.style.width = `${pct}%`;
  DOM.fraudCenterBar.className = 'progress-fill';
  if (isFlagged || pct >= 100) DOM.fraudCenterBar.classList.add('danger');
  else if (pct >= 75) DOM.fraudCenterBar.classList.add('warn');

  // Security Alert History
  const alerts = metrics.alert_history || [];
  if (alerts.length === 0) {
    DOM.fraudAlertsBody.innerHTML = `
      <tr><td colspan="4" class="empty-state-sm">No security alert incidents recorded for this account.</td></tr>
    `;
  } else {
    DOM.fraudAlertsBody.innerHTML = alerts.map(al => `
      <tr>
        <td style="white-space:nowrap; font-size:11.5px; color:var(--text-muted);">${al.timestamp}</td>
        <td>${al.reason}</td>
        <td class="text-right font-mono font-bold text-danger">₹${formatCurrency(al.window_sum)}</td>
        <td class="text-center"><span class="status-badge badge-flagged">${al.risk_level}</span></td>
      </tr>
    `).join('');
  }
}

function openFraudResolutionModal(accNum) {
  state.fraudResolveTargetAcc = accNum || state.activeAccountNum;
  DOM.fraudResolveAccNum.textContent = `#${state.fraudResolveTargetAcc}`;
  DOM.fraudResolutionModal.classList.remove('hidden');
}

async function confirmFraudResolution() {
  const accNum = state.fraudResolveTargetAcc;
  if (!accNum) return;

  try {
    const res = await apiRequest(`/fraud-alerts/${accNum}/resolve`, { method: 'POST' });
    showToast('Security Hold Cleared', res.message, 'success');
    DOM.fraudResolutionModal.classList.add('hidden');

    await selectAccount(accNum);
    await refreshSystemStatus();
  } catch (err) {
    showToast('Failed to Clear Hold', err.message, 'danger');
  }
}

// ==============================================================================
// CORE DSA ENGINES & VISUALIZERS
// ==============================================================================

function renderDSAVisualizers() {
  renderDSALinkedList();
  loadBSTVisualizer();
  renderDSASlidingWindowDiagram();
  renderDSAHashMap();
}

function renderDSALinkedList() {
  const transactions = state.allTransactions || [];

  if (transactions.length === 0) {
    DOM.dsaLLCanvas.innerHTML = `
      <div class="ll-pointer-head">HEAD -> NULL (Empty Singly Linked List)</div>
    `;
    return;
  }

  let html = `
    <div class="ll-pointer-head">
      <span>HEAD POINTER</span>
      <small style="font-size: 10px; opacity: 0.85;">O(1) Prepend</small>
    </div>
    <div class="ll-arrow"><i class="fa-solid fa-arrow-right"></i></div>
  `;

  const sliceNodes = transactions.slice(0, 6);
  sliceNodes.forEach((node, idx) => {
    const isCredit = node.tx_type === 'DEPOSIT' || node.tx_type === 'INITIAL_DEPOSIT';
    const isHead = idx === 0;

    html += `
      <div class="ll-node ${isHead ? 'is-head' : ''}">
        <div class="ll-node-id">${node.tx_id}</div>
        <div class="ll-node-amount ${isCredit ? 'text-success' : 'text-primary'}">
          ${isCredit ? '+' : '-'}₹${formatCurrency(node.amount)}
        </div>
        <div class="ll-node-meta">Post Bal: ₹${formatCurrency(node.balance_after)}</div>
        <div class="ll-node-meta">${node.tx_type}</div>
      </div>
      <div class="ll-arrow"><i class="fa-solid fa-arrow-right"></i></div>
    `;
  });

  if (transactions.length > 6) {
    html += `
      <div class="ll-null">+${transactions.length - 6} more nodes...</div>
      <div class="ll-arrow"><i class="fa-solid fa-arrow-right"></i></div>
    `;
  }

  html += `<div class="ll-null">NULL (Genesis)</div>`;
  DOM.dsaLLCanvas.innerHTML = html;
}

async function loadBSTVisualizer() {
  try {
    const data = await apiRequest('/system/tree');
    state.bstTreeData = data.tree;
    renderBSTTree(data.tree);

    // In-Order Traversal list from /accounts endpoint
    const accountsData = await apiRequest('/accounts');
    const sorted = accountsData.accounts || [];

    DOM.dsaBSTInorderList.innerHTML = sorted.map(acc => `
      <div class="inorder-chip" onclick="selectAndGoToDashboard('${acc.account_number}')" title="Click to inspect account">
        <span class="font-mono font-bold text-primary">#${acc.account_number}</span>
        <span>${acc.account_name}</span>
        <span class="font-mono font-bold text-success">₹${formatCurrency(acc.balance)}</span>
      </div>
    `).join('');
  } catch (err) {
    console.error('Failed to load BST visualizer:', err);
  }
}

function renderBSTTree(treeNode) {
  if (!treeNode) {
    DOM.dsaTreeHierarchy.innerHTML = '<div class="empty-state-sm">Binary Search Tree is empty.</div>';
    return;
  }

  function buildNodeHTML(node) {
    if (!node) return '';
    const isCurrentActive = node.account_number === state.activeAccountNum;

    let childrenHTML = '';
    if (node.children && node.children.length > 0) {
      childrenHTML = `
        <div style="display: flex; gap: 24px; justify-content: center; margin-top: 14px; border-top: 1px dashed var(--border-color); padding-top: 14px;">
          ${node.children.map(child => buildNodeHTML(child)).join('')}
        </div>
      `;
    }

    return `
      <div style="display: flex; flex-direction: column; align-items: center;" id="bst-node-${node.account_number}">
        <div class="tree-node-card ${isCurrentActive ? 'highlight' : ''}" onclick="selectAndGoToDashboard('${node.account_number}')">
          <div class="tree-node-acc">#${node.account_number}</div>
          <div class="tree-node-name">${node.account_name}</div>
          <div class="tree-node-bal">₹${formatCurrency(node.balance)}</div>
        </div>
        ${childrenHTML}
      </div>
    `;
  }

  DOM.dsaTreeHierarchy.innerHTML = buildNodeHTML(treeNode);
}

async function handleDSABSTSearch() {
  const query = DOM.dsaBSTSearchInput.value.trim();
  if (!query) return;

  try {
    const res = await apiRequest(`/dsa/bst/search?account_number=${encodeURIComponent(query)}`);
    DOM.dsaBSTSearchFeedback.className = 'search-feedback-box success';
    DOM.dsaBSTSearchFeedback.innerHTML = `
      <strong>BST Search O(log N) Match Found!</strong> Account #${res.account.account_number} (${res.account.account_name}) located in Binary Search Tree. Balance: ₹${formatCurrency(res.account.balance)}.
    `;
    DOM.dsaBSTSearchFeedback.classList.remove('hidden');

    // Highlight node on canvas
    document.querySelectorAll('.tree-node-card').forEach(el => el.classList.remove('highlight'));
    const target = document.getElementById(`bst-node-${query}`);
    if (target) {
      const card = target.querySelector('.tree-node-card');
      if (card) card.classList.add('highlight');
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  } catch (err) {
    DOM.dsaBSTSearchFeedback.className = 'search-feedback-box error';
    DOM.dsaBSTSearchFeedback.innerHTML = `<strong>Search Result:</strong> Account #${query} was not found in the BST index.`;
    DOM.dsaBSTSearchFeedback.classList.remove('hidden');
  }
}

function renderDSASlidingWindowDiagram() {
  const acc = state.activeAccountData;
  const metrics = (acc && acc.fraud_metrics) || {};
  const kSize = metrics.window_size || 3;
  const amounts = metrics.window_amounts || [];
  const currentSum = metrics.window_sum || 0;
  const threshold = metrics.threshold || 50000;

  DOM.dsaSlidingWindowDiagram.innerHTML = `
    <div style="display: flex; flex-direction: column; gap: 14px;">
      <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
        <strong>Active Buffer Frame (K=${kSize}):</strong>
        ${amounts.map((a, i) => `
          <span class="slot-badge filled">Slot ${i + 1}: ₹${formatCurrency(a)}</span>
        `).join('')}
        ${Array.from({ length: Math.max(0, kSize - amounts.length) }).map((_, i) => `
          <span class="slot-badge empty">Slot ${amounts.length + i + 1}: Empty</span>
        `).join('')}
      </div>

      <div class="callout-box">
        <strong>Mathematical Evaluation Formula:</strong><br>
        <code>Current Window Sum = ${amounts.length > 0 ? amounts.map(a => `₹${formatCurrency(a)}`).join(' + ') : '₹0.00'} = ₹${formatCurrency(currentSum)}</code><br>
        <code>Threshold Limit = ₹${formatCurrency(threshold)} | Status: ${currentSum >= threshold ? '<span class="text-danger font-bold">BREACHED (CRITICAL FRAUD)</span>' : '<span class="text-success font-bold">SAFE</span>'}</code>
      </div>
    </div>
  `;
}

function renderDSAHashMap() {
  const list = state.accountsList || [];
  DOM.dsaHashMapBody.innerHTML = list.map(acc => `
    <tr>
      <td class="font-mono font-bold text-primary">Key("${acc.account_number}")</td>
      <td class="font-mono" style="color: var(--text-muted);">hash("${acc.account_number}") &rarr; 0x${(parseInt(acc.account_number) || 12345).toString(16).toUpperCase()}</td>
      <td><strong>${acc.account_name}</strong></td>
      <td class="font-mono font-bold">₹${formatCurrency(acc.balance)}</td>
      <td><span class="status-badge ${acc.status === 'FLAGGED' ? 'badge-flagged' : 'badge-active'}">${acc.status}</span></td>
      <td class="text-center"><span class="badge badge-neutral font-mono">O(1) Constant</span></td>
    </tr>
  `).join('');
}

// ==============================================================================
// EMAIL & AUDIT LOGS
// ==============================================================================

async function loadEmailLogs() {
  try {
    const data = await apiRequest('/emails');
    state.emailLogs = data.emails || [];
    
    DOM.sidebarEmailCount.textContent = state.emailLogs.length;
    DOM.emailTotalLoggedBadge.textContent = `Total Dispatched: ${state.emailLogs.length}`;
    DOM.emailDeliveryModeText.textContent = `Delivery Engine: ${state.systemStatus?.smtp_mode || 'MOCK CONSOLE & IN-MEMORY'}`;
    DOM.diagSmtpMode.textContent = state.systemStatus?.smtp_mode || 'MOCK CONSOLE & IN-MEMORY';

    renderEmailLogsTable();
  } catch (err) {
    console.error('Failed to load email logs:', err);
  }
}

function renderEmailLogsTable() {
  if (state.emailLogs.length === 0) {
    DOM.emailLogsBody.innerHTML = `
      <tr><td colspan="7" class="empty-state-sm">No outbound notifications dispatched yet. Execute a transaction or open an account to generate official statements.</td></tr>
    `;
    return;
  }

  DOM.emailLogsBody.innerHTML = state.emailLogs.map((em, idx) => {
    let typeClass = 'email-type-transaction';
    if (em.email_type === 'WELCOME') typeClass = 'email-type-welcome';
    if (em.email_type === 'SECURITY_ALERT') typeClass = 'email-type-alert';

    return `
      <tr>
        <td class="font-mono font-bold text-primary">${em.email_id}</td>
        <td style="white-space:nowrap; font-size:11.5px; color:var(--text-muted);">${em.sent_at}</td>
        <td><strong>${em.to_email}</strong></td>
        <td><span class="email-type-tag ${typeClass}">${em.email_type}</span></td>
        <td>${em.subject}</td>
        <td><span class="badge badge-neutral">${em.delivery_mode}</span></td>
        <td class="text-center">
          <button class="btn btn-secondary btn-xs" onclick="openEmailStatementPreview(${idx})">
            <i class="fa-solid fa-eye"></i> View Statement
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

window.openEmailStatementPreview = function(idx) {
  const email = state.emailLogs[idx];
  if (!email) return;

  DOM.modalEmailSubject.textContent = email.subject;
  DOM.emailPreviewMeta.innerHTML = `
    <div><strong>Recipient:</strong> ${email.to_email} | <strong>Mode:</strong> ${email.delivery_mode} | <strong>Status:</strong> ${email.status}</div>
    <div style="font-size: 11px; margin-top: 3px;">Dispatched: ${email.sent_at} | Statement ID: ${email.email_id}</div>
  `;

  DOM.emailPreviewHtmlContainer.innerHTML = email.body_html || `<pre class="font-mono">${email.body_text}</pre>`;
  DOM.emailPreviewModal.classList.remove('hidden');
};

// ==============================================================================
// MODAL FORMS & SETTINGS
// ==============================================================================

async function handleCreateAccountSubmit() {
  const name = DOM.inputNewName.value.trim();
  const email = DOM.inputNewEmail.value.trim();
  const accNum = DOM.inputNewAccNum.value.trim();
  const accType = DOM.inputNewAccType.value;
  const initialDeposit = parseFloat(DOM.inputNewInitialDeposit.value) || 0;
  const phone = DOM.inputNewPhone.value.trim();

  if (!name || !email) {
    showToast('Missing Required Fields', 'Account holder full name and email are mandatory.', 'warning');
    return;
  }

  DOM.btnSubmitCreateAccount.disabled = true;
  DOM.btnSubmitCreateAccount.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Establishing Account...';

  try {
    const res = await apiRequest('/accounts', {
      method: 'POST',
      body: JSON.stringify({
        account_name: name,
        email: email,
        account_number: accNum || null,
        account_type: accType,
        initial_deposit: initialDeposit,
        phone: phone || '+91 98765 43210',
      }),
    });

    showToast(
      'Account Established Successfully',
      `Account #${res.account.account_number} created for ${name}. Onboarding statement dispatched to ${email}.`,
      'success'
    );

    DOM.createAccountModal.classList.add('hidden');
    DOM.createAccountModalForm.reset();

    await loadAccounts(res.account.account_number);
    switchView('dashboard');
  } catch (err) {
    showToast('Account Creation Failed', err.message, 'danger');
  } finally {
    DOM.btnSubmitCreateAccount.disabled = false;
    DOM.btnSubmitCreateAccount.innerHTML = '<i class="fa-solid fa-check"></i> Establish Account';
  }
}

async function handleSaveFraudSettings() {
  const k = parseInt(DOM.setWindowK.value);
  const threshold = parseFloat(DOM.setFraudThreshold.value);

  if (!k || k < 1 || !threshold || threshold < 100) {
    showToast('Invalid Parameters', 'Sliding Window K must be >= 1 and threshold >= ₹100.', 'warning');
    return;
  }

  try {
    const res = await apiRequest('/settings/fraud', {
      method: 'POST',
      body: JSON.stringify({
        k_window: k,
        fraud_threshold: threshold,
      }),
    });

    showToast('Settings Applied', res.message, 'success');
    if (state.activeAccountNum) {
      await selectAccount(state.activeAccountNum);
    }
  } catch (err) {
    showToast('Settings Update Failed', err.message, 'danger');
  }
}

// ==============================================================================
// EVENT LISTENERS INITIALIZATION
// ==============================================================================

function initEventListeners() {
  // Mobile Sidebar Toggle
  DOM.btnMobileToggle.addEventListener('click', () => {
    DOM.sidebar.classList.toggle('mobile-open');
  });

  // Global Refresh Button
  DOM.btnGlobalRefresh.addEventListener('click', async () => {
    if (state.activeAccountNum) await selectAccount(state.activeAccountNum);
    await refreshSystemStatus();
    loadEmailLogs();
    showToast('Data Synchronized', 'Bank database, ledger, and DSA indices refreshed.', 'info');
  });

  // Navigation Links
  Object.keys(DOM.navButtons).forEach(viewKey => {
    DOM.navButtons[viewKey].addEventListener('click', () => switchView(viewKey));
  });

  // Sidebar Account Switcher
  DOM.accountSelect.addEventListener('change', (e) => selectAccount(e.target.value));

  // Copy Account Number
  DOM.btnCopyDashboardAcc.addEventListener('click', () => {
    if (state.activeAccountNum) {
      navigator.clipboard.writeText(state.activeAccountNum);
      showToast('Copied to Clipboard', `Account #${state.activeAccountNum} copied.`, 'info');
    }
  });

  // Operation Tab Switching (Deposit / Withdraw)
  DOM.tabOpDeposit.addEventListener('click', () => {
    state.currentOpMode = 'DEPOSIT';
    DOM.tabOpDeposit.classList.add('active');
    DOM.tabOpWithdraw.classList.remove('active');
    DOM.btnDashExecuteText.textContent = 'Execute Deposit';
    updateLiveBalancePreview();
  });

  DOM.tabOpWithdraw.addEventListener('click', () => {
    state.currentOpMode = 'WITHDRAWAL';
    DOM.tabOpWithdraw.classList.add('active');
    DOM.tabOpDeposit.classList.remove('active');
    DOM.btnDashExecuteText.textContent = 'Execute Withdrawal';
    updateLiveBalancePreview();
  });

  // Live input balance estimation
  DOM.dashTxAmount.addEventListener('input', updateLiveBalancePreview);

  // Preset Buttons
  DOM.presetButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const amt = btn.getAttribute('data-amount');
      DOM.dashTxAmount.value = amt;
      updateLiveBalancePreview();
    });
  });

  // Execute Banking Operation
  DOM.btnDashExecuteTx.addEventListener('click', executeBankingOperation);

  // Quick Action Buttons
  DOM.btnQuickOpenAccount.addEventListener('click', () => DOM.createAccountModal.classList.remove('hidden'));
  DOM.btnOpenAccountModalFromRoster.addEventListener('click', () => DOM.createAccountModal.classList.remove('hidden'));
  DOM.btnQuickTransfer.addEventListener('click', () => {
    switchView('dashboard');
    DOM.dashTxAmount.focus();
  });
  DOM.btnViewAllTransactions.addEventListener('click', () => switchView('transactions'));

  // Accounts Search & Filter
  DOM.accountsSearchInput.addEventListener('input', (e) => {
    state.accountsSearchQuery = e.target.value.trim();
    renderAccountsRoster();
  });

  DOM.accountsTypeFilter.addEventListener('change', (e) => {
    state.accountsTypeFilter = e.target.value;
    renderAccountsRoster();
  });

  // Transactions Search & Filter
  DOM.txFilterTabs.querySelectorAll('.filter-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      DOM.txFilterTabs.querySelectorAll('.filter-tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.txFilter = btn.getAttribute('data-filter');
      renderFullTransactionsLedger();
    });
  });

  DOM.txSearchInput.addEventListener('input', (e) => {
    state.txSearchQuery = e.target.value.trim();
    renderFullTransactionsLedger();
  });

  DOM.btnRefreshTxLedger.addEventListener('click', () => {
    if (state.activeAccountNum) loadAccountTransactions(state.activeAccountNum);
  });

  // Fraud Resolution Banner & Buttons
  DOM.btnResolveFraudBanner.addEventListener('click', () => openFraudResolutionModal(state.activeAccountNum));
  DOM.btnResolveFraudCenter.addEventListener('click', () => openFraudResolutionModal(state.activeAccountNum));

  // DSA Sub-Tabs
  DOM.dsaTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      DOM.dsaTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const dsaKey = tab.getAttribute('data-dsa');
      state.activeDSATab = dsaKey;

      Object.keys(DOM.dsaPanes).forEach(k => {
        if (k === dsaKey) DOM.dsaPanes[k].classList.remove('hidden');
        else DOM.dsaPanes[k].classList.add('hidden');
      });
    });
  });

  DOM.btnDSASearchBST.addEventListener('click', handleDSABSTSearch);
  DOM.dsaBSTSearchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') handleDSABSTSearch();
  });

  // Email Refresh
  DOM.btnRefreshEmailsView.addEventListener('click', loadEmailLogs);

  // Settings Save
  DOM.btnSaveFraudSettings.addEventListener('click', handleSaveFraudSettings);

  // Modal Closures
  DOM.btnCloseCreateAccountModal.addEventListener('click', () => DOM.createAccountModal.classList.add('hidden'));
  DOM.btnCancelCreateAccountModal.addEventListener('click', () => DOM.createAccountModal.classList.add('hidden'));
  DOM.btnSubmitCreateAccount.addEventListener('click', handleCreateAccountSubmit);

  DOM.btnCloseEmailPreviewModal.addEventListener('click', () => DOM.emailPreviewModal.classList.add('hidden'));
  DOM.btnCloseEmailPreviewBtn.addEventListener('click', () => DOM.emailPreviewModal.classList.add('hidden'));

  DOM.btnCloseFraudModal.addEventListener('click', () => DOM.fraudResolutionModal.classList.add('hidden'));
  DOM.btnCancelFraudModal.addEventListener('click', () => DOM.fraudResolutionModal.classList.add('hidden'));
  DOM.btnConfirmFraudResolution.addEventListener('click', confirmFraudResolution);

  // Close modals on clicking backdrop
  window.addEventListener('click', (e) => {
    if (e.target === DOM.createAccountModal) DOM.createAccountModal.classList.add('hidden');
    if (e.target === DOM.emailPreviewModal) DOM.emailPreviewModal.classList.add('hidden');
    if (e.target === DOM.fraudResolutionModal) DOM.fraudResolutionModal.classList.add('hidden');
  });

  // Close modals on Escape key
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      DOM.createAccountModal.classList.add('hidden');
      DOM.emailPreviewModal.classList.add('hidden');
      DOM.fraudResolutionModal.classList.add('hidden');
    }
  });

  // Live Clock Tick
  setInterval(() => {
    const now = new Date();
    DOM.currentTimestamp.textContent = now.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true,
    });
  }, 1000);
}

// ==============================================================================
// APPLICATION INITIALIZATION
// ==============================================================================

document.addEventListener('DOMContentLoaded', () => {
  initEventListeners();
  loadAccounts();
});
