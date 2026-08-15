const content = document.getElementById("content");
const connectionBadge = document.getElementById("connectionBadge");
const lastUpdated = document.getElementById("lastUpdated");
const refreshButton = document.getElementById("refreshButton");
const routeButtons = Array.from(document.querySelectorAll("[data-route]"));

const state = {
  status: null,
  chain: [],
  selectedBlockIndex: null,
  selectedBlockDetails: null,
  route: "dashboard",
  loading: true,
  error: null,
  lastRefresh: null,
  notice: null,
  merkleProof: null,
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function truncateHash(value, start = 10, end = 10) {
  if (!value) {
    return "—";
  }

  const text = String(value);
  if (text.length <= start + end + 3) {
    return text;
  }
  return `${text.slice(0, start)}...${text.slice(-end)}`;
}

const CARD_HASH_TRUNCATION = { start: 20, end: 16 };
const DETAIL_HASH_TRUNCATION = { start: 20, end: 14 };
const TREE_HASH_TRUNCATION = { start: 12, end: 10 };

function formatAmount(value) {
  if (value === null || value === undefined || value === "") {
    return "—";
  }
  const number = Number(value);
  if (Number.isNaN(number)) {
    return String(value);
  }
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: 8 }).format(number);
}

function formatTimestamp(value) {
  if (value === null || value === undefined || value === "") {
    return "—";
  }

  let date = null;
  if (typeof value === "number") {
    date = new Date(value > 1e12 ? value : value * 1000);
  } else if (typeof value === "string") {
    const numeric = Number(value);
    if (!Number.isNaN(numeric) && value.trim() !== "") {
      date = new Date(numeric > 1e12 ? numeric : numeric * 1000);
    } else {
      date = new Date(value);
    }
  } else {
    date = new Date(value);
  }

  if (!date || Number.isNaN(date.getTime())) {
    return String(value);
  }

  return date.toLocaleString();
}

function getBlocks() {
  if (Array.isArray(state.chain)) {
    return state.chain;
  }
  return [];
}

function getBlockCount() {
  return getBlocks().length;
}

function getTotalTransactions() {
  return getBlocks().reduce((sum, block) => sum + (Array.isArray(block.transactions) ? block.transactions.length : 0), 0);
}

function getPendingTransactions() {
  return Array.isArray(state.status?.pending_transactions) ? state.status.pending_transactions : [];
}

function getSelectedBlockIndex() {
  if (state.selectedBlockIndex !== null && state.selectedBlockIndex !== undefined) {
    return state.selectedBlockIndex;
  }
  if (state.status?.last_block_index !== null && state.status?.last_block_index !== undefined) {
    return state.status.last_block_index;
  }
  const blocks = getBlocks();
  return blocks.length > 0 ? blocks[blocks.length - 1].index : 0;
}

function getBlockIndexList() {
  return getBlocks().map((block) => block.index);
}

function parseRoute() {
  const raw = location.hash.replace(/^#\/?/, "");
  if (!raw) {
    return { route: "dashboard", index: null };
  }

  const [routePart, indexPart] = raw.split("/");
  const allowedRoutes = new Set(["dashboard", "blockchain", "details", "merkle"]);
  const route = allowedRoutes.has(routePart) ? routePart : "dashboard";
  const index = indexPart === undefined ? null : Number.parseInt(indexPart, 10);
  return { route, index: Number.isNaN(index) ? null : index };
}

function navigate(route, index = null) {
  if (index === null || index === undefined) {
    location.hash = `#/${route}`;
    return;
  }
  location.hash = `#/${route}/${index}`;
}

function setActiveRouteButtons(route) {
  routeButtons.forEach((button) => {
    const buttonRoute = button.dataset.route;
    button.classList.toggle("is-active", buttonRoute === route);
  });
}

function setConnectionBadge(kind, text) {
  connectionBadge.className = `status-chip ${kind}`;
  connectionBadge.textContent = text;
}

function updateLastUpdated() {
  if (!state.lastRefresh) {
    lastUpdated.textContent = "Waiting for blockchain data.";
    return;
  }

  lastUpdated.textContent = `Last refreshed ${state.lastRefresh.toLocaleString()}`;
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`${response.status} ${response.statusText}${body ? ` - ${body}` : ""}`);
  }

  return response.json();
}

async function loadBlockchainOverview() {
  state.loading = true;
  state.error = null;
  setConnectionBadge("status-chip--loading", "Loading blockchain data...");
  render();

  try {
    const [status, chainResponse] = await Promise.all([
      fetchJson("/blockchain/status"),
      fetchJson("/blockchain"),
    ]);

    state.status = status;
    state.chain = Array.isArray(chainResponse.chain) ? chainResponse.chain : [];
    const fallbackIndex = status?.last_block_index ?? (state.chain.length > 0 ? state.chain[state.chain.length - 1].index : 0);
    if (state.selectedBlockIndex === null || !getBlockIndexList().includes(state.selectedBlockIndex)) {
      state.selectedBlockIndex = fallbackIndex;
    }

    if (state.selectedBlockIndex !== null && state.selectedBlockIndex !== undefined) {
      await loadBlockDetails(state.selectedBlockIndex);
    }

    state.lastRefresh = new Date();
    setConnectionBadge(
      status?.blockchain_valid ? "status-chip--ok" : "status-chip--bad",
      status?.blockchain_valid ? "Blockchain valid" : "Blockchain has integrity issues",
    );
  } catch (error) {
    state.error = error instanceof Error ? error.message : String(error);
    setConnectionBadge("status-chip--bad", "Failed to load blockchain data");
  } finally {
    state.loading = false;
    updateLastUpdated();
    render();
  }
}

async function loadBlockDetails(index) {
  if (index === null || index === undefined) {
    state.selectedBlockDetails = null;
    return null;
  }

  const cached = state.selectedBlockDetails;
  if (cached && cached.index === index) {
    return cached;
  }

  const block = await fetchJson(`/blockchain/blocks/${index}`);
  state.selectedBlockDetails = block;
  state.selectedBlockIndex = index;
  return block;
}

function buildStatCard(label, value, helper, accent = false) {
  return `
    <article class="stat-card">
      <div class="stat-label">${escapeHtml(label)}</div>
      <div class="stat-value ${accent ? "stat-value--accent" : ""}">${escapeHtml(value)}</div>
      ${helper ? `<div class="stat-helper">${escapeHtml(helper)}</div>` : ""}
    </article>
  `;
}

function buildDashboardView() {
  const status = state.status;
  const blocks = getBlocks();
  const pending = getPendingTransactions();
  const selectedBlock = blocks.find((block) => block.index === getSelectedBlockIndex());
  const totalTransactions = getTotalTransactions();

  return `
    <section class="view">
      <div class="view-header">
        <div>
          <h2 class="view-title">Dashboard</h2>
          <p class="view-subtitle">Current chain state and high-level blockchain health.</p>
        </div>
        <div class="badge-row">
          <span class="badge ${status?.blockchain_valid ? "badge--accent" : "badge--danger"}">
            ${escapeHtml(status?.blockchain_valid ? "Valid chain" : "Invalid chain")}
          </span>
          <span class="badge">${escapeHtml(blocks.length)} blocks</span>
          <span class="badge">${escapeHtml(totalTransactions)} total transactions</span>
        </div>
      </div>

      <div class="stat-grid">
        ${buildStatCard("Blocks", blocks.length, "Includes the genesis block and every mined block.")}
        ${buildStatCard("Total transactions", totalTransactions, "Sum of all transactions stored in the chain.")}
        ${buildStatCard("Pending transactions", pending.length, "Transactions waiting to be packed into the next block.")}
        ${buildStatCard("Blockchain valid", status?.blockchain_valid ? "Yes" : "No", "Integrity check from the backend status endpoint.", true)}
        ${buildStatCard("Last block hash", status?.last_block_hash ? truncateHash(status.last_block_hash, CARD_HASH_TRUNCATION.start, CARD_HASH_TRUNCATION.end) : "—", "Hash of the latest block currently in the chain.")}
      </div>

      <div class="detail-columns">
        <section class="section-card">
          <div class="section-header">
            <div>
              <h3>Latest block</h3>
              <p>Quick summary of the selected block.</p>
            </div>
            <button class="secondary-button" type="button" data-open-route="details">Open block details</button>
          </div>

          ${selectedBlock ? `
            <div class="helper-grid" style="margin-top: 14px;">
              <div class="detail-pair">
                <span>Index</span>
                <strong>${escapeHtml(selectedBlock.index)}</strong>
              </div>
              <div class="detail-pair">
                <span>Valid</span>
                <strong>${escapeHtml(selectedBlock.valid ? "Yes" : "No")}</strong>
              </div>
              <div class="detail-pair">
                <span>Merkle root</span>
                <strong>${escapeHtml(truncateHash(selectedBlock.merkle_root, CARD_HASH_TRUNCATION.start, CARD_HASH_TRUNCATION.end))}</strong>
              </div>
              <div class="detail-pair">
                <span>Block hash</span>
                <strong>${escapeHtml(truncateHash(selectedBlock.hash, CARD_HASH_TRUNCATION.start, CARD_HASH_TRUNCATION.end))}</strong>
              </div>
            </div>
          ` : `
            <div class="empty-state" style="margin-top: 14px;">
              <h3>No block selected</h3>
              <p>Load data or choose a block from the Blockchain view.</p>
            </div>
          `}
        </section>

        <section class="section-card">
          <div class="section-header">
            <div>
              <h3>Pending transactions</h3>
              <p>Transactions not yet included in a block.</p>
            </div>
            <span class="badge">${escapeHtml(pending.length)} pending</span>
          </div>

          ${pending.length > 0 ? `
            <div class="pending-grid">
              ${pending.map((tx) => `
                <article class="pending-item">
                  <strong>${escapeHtml(truncateHash(tx.hash, 12, 12))}</strong>
                  <div>${escapeHtml(tx.sender ?? "—")} → ${escapeHtml(tx.receiver ?? "—")}</div>
                  <div>${escapeHtml(formatAmount(tx.amount))}</div>
                  <div class="small-note">${escapeHtml(formatTimestamp(tx.timestamp))}</div>
                  ${tx.metadata ? `<div class="small-note">${escapeHtml(tx.metadata)}</div>` : ""}
                </article>
              `).join("")}
            </div>
          ` : `
            <div class="empty-state" style="margin-top: 14px;">
              <h3>No pending transactions</h3>
              <p>New transactions will appear here until a block is created.</p>
            </div>
          `}
        </section>
      </div>

      <section class="action-panel">
        <div class="section-header">
          <div>
            <h3>Quick actions</h3>
            <p>Submit a transaction or package the pending pool into a new block.</p>
          </div>
          <button id="createBlockButton" class="secondary-button" type="button">Create block</button>
        </div>

        <form id="transactionForm" class="action-form">
          <div class="field-grid">
            <label class="field">
              <span>Sender</span>
              <input type="text" name="sender" placeholder="Alice" required />
            </label>
            <label class="field">
              <span>Receiver</span>
              <input type="text" name="receiver" placeholder="Bob" required />
            </label>
            <label class="field">
              <span>Amount</span>
              <input type="number" name="amount" min="0.01" step="0.01" placeholder="10.00" required />
            </label>
            <label class="field field--wide">
              <span>Metadata</span>
              <input type="text" name="metadata" placeholder="Optional note" />
            </label>
          </div>
          <div class="form-actions">
            <button class="primary-button" type="submit">Add transaction</button>
          </div>
        </form>
      </section>
    </section>
  `;
}

function buildBlockchainView() {
  const blocks = getBlocks();

  return `
    <section class="view">
      <div class="view-header">
        <div>
          <h2 class="view-title">Blockchain</h2>
          <p class="view-subtitle">Each block card shows the summary fields and the hash pointer to the previous block.</p>
        </div>
        <div class="badge-row">
          <span class="badge">${escapeHtml(blocks.length)} blocks</span>
          <span class="badge">Selected block ${escapeHtml(getSelectedBlockIndex())}</span>
        </div>
      </div>

      ${blocks.length > 0 ? `
        <div class="block-grid" style="margin-top: 18px;">
          ${blocks.map((block, index) => `
            <article class="block-card ${block.index === getSelectedBlockIndex() ? "is-selected" : ""}" style="--delay: ${index * 60}ms;">
              <div class="card-header">
                <div>
                  <h3>Block ${escapeHtml(block.index)}</h3>
                  <p>${escapeHtml(block.valid ? "Validated" : "Invalid")}</p>
                </div>
                <span class="badge ${block.valid ? "badge--accent" : "badge--danger"}">${escapeHtml(block.valid ? "Valid" : "Invalid")}</span>
              </div>

              <div class="hash-block">
                <div class="hash-line">
                  <span>Merkle root</span>
                  <code title="${escapeHtml(block.merkle_root)}">${escapeHtml(block.merkle_root ? block.merkle_root : "—")}</code>
                </div>
                <div class="hash-line">
                  <span>Block hash</span>
                  <code title="${escapeHtml(block.hash)}">${escapeHtml(block.hash ? block.hash : "—")}</code>
                </div>
                <div class="hash-line">
                  <span>Previous hash pointer</span>
                  <code title="${escapeHtml(block.previous_hash)}">${escapeHtml(block.previous_hash ? block.previous_hash : "—")}</code>
                </div>
              </div>

              <div class="block-meta">
                <span class="badge">${escapeHtml(Array.isArray(block.transactions) ? block.transactions.length : 0)} tx</span>
                <span class="badge">Nonce ${escapeHtml(block.nonce)}</span>
                <span class="badge">Difficulty ${escapeHtml(block.difficulty)}</span>
              </div>

              <div class="card-actions">
                <button type="button" data-open-route="details" data-block-index="${escapeHtml(block.index)}">View details</button>
                <button class="muted" type="button" data-open-route="merkle" data-block-index="${escapeHtml(block.index)}">Inspect Merkle tree</button>
              </div>
            </article>
          `).join("")}
        </div>
      ` : `
        <div class="empty-state">
          <h3>No blocks available</h3>
          <p>When the backend creates blocks, they will appear here automatically.</p>
        </div>
      `}
    </section>
  `;
}

function buildBlockDetailsView() {
  const index = getSelectedBlockIndex();
  const block = state.selectedBlockDetails;

  return `
    <section class="view">
      <div class="view-header">
        <div>
          <h2 class="view-title">Block Details</h2>
          <p class="view-subtitle">Full information for the selected block and its transactions.</p>
        </div>
        <div class="badge-row">
          <span class="badge">Selected block ${escapeHtml(index)}</span>
          <span class="badge">${escapeHtml(block?.transactions?.length ?? 0)} transactions</span>
        </div>
      </div>

      <div class="toolbar">
        <div class="group">
          <label class="small-note" for="blockSelect">Choose a block</label>
          <select id="blockSelect" class="select">
            ${getBlockIndexList().map((blockIndex) => `<option value="${escapeHtml(blockIndex)}" ${blockIndex === index ? "selected" : ""}>Block ${escapeHtml(blockIndex)}</option>`).join("")}
          </select>
        </div>
        <div class="group">
          <button class="secondary-button" type="button" data-open-route="merkle" data-block-index="${escapeHtml(index)}">Open Merkle tree</button>
        </div>
      </div>

      ${block ? `
        <div class="detail-columns">
          <section class="detail-stack">
            <div class="section-card">
              <h3>Block header</h3>
              <div class="details-grid" style="margin-top: 14px; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));">
                <div class="detail-pair"><span>Index</span><strong>${escapeHtml(block.index)}</strong></div>
                <div class="detail-pair"><span>Valid</span><strong>${escapeHtml(block.valid ? "Yes" : "No")}</strong></div>
                <div class="detail-pair"><span>Timestamp</span><strong>${escapeHtml(formatTimestamp(block.timestamp))}</strong></div>
                <div class="detail-pair"><span>Nonce</span><strong>${escapeHtml(block.nonce)}</strong></div>
                <div class="detail-pair"><span>Difficulty</span><strong>${escapeHtml(block.difficulty)}</strong></div>
                <div class="detail-pair"><span>Previous hash</span><strong>${escapeHtml(truncateHash(block.previous_hash, 10, 10))}</strong></div>
              </div>
            </div>

            <div class="section-card">
              <h3>Block hashes</h3>
              <div class="helper-grid" style="margin-top: 14px;">
                <div class="hash-line">
                  <span>Merkle root</span>
                  <code title="${escapeHtml(block.merkle_root)}">${escapeHtml(block.merkle_root || "—")}</code>
                </div>
                <div class="hash-line">
                  <span>Current hash</span>
                  <code title="${escapeHtml(block.hash)}">${escapeHtml(block.hash || "—")}</code>
                </div>
              </div>
            </div>
          </section>

          <section class="detail-stack">
            <div class="section-card">
              <h3>Transactions</h3>
              ${Array.isArray(block.transactions) && block.transactions.length > 0 ? `
                <div style="margin-top: 14px; overflow-x: auto;">
                  <table class="tx-table">
                    <thead>
                      <tr>
                        <th>Sender</th>
                        <th>Receiver</th>
                        <th>Amount</th>
                        <th>Metadata</th>
                        <th>Timestamp</th>
                        <th>Hash</th>
                      </tr>
                    </thead>
                    <tbody>
                      ${block.transactions.map((tx) => `
                        <tr>
                          <td>${escapeHtml(tx.sender ?? "—")}</td>
                          <td>${escapeHtml(tx.receiver ?? "—")}</td>
                          <td>${escapeHtml(formatAmount(tx.amount))}</td>
                          <td>${escapeHtml(tx.metadata ?? "—")}</td>
                          <td>${escapeHtml(formatTimestamp(tx.timestamp))}</td>
                          <td class="tx-hash">${escapeHtml(truncateHash(tx.hash, 16, 14))}</td>
                        </tr>
                      `).join("")}
                    </tbody>
                  </table>
                </div>
              ` : `
                <div class="empty-state" style="margin-top: 14px;">
                  <h3>No transactions in this block</h3>
                  <p>This is the genesis block or an empty block without transactions.</p>
                </div>
              `}
            </div>

            ${Array.isArray(block.transactions) && block.transactions.length > 0 ? `
              <div class="section-card">
                <div class="section-header">
                  <div>
                    <h3>Tamper transaction</h3>
                    <p>Replace one transaction in the selected block to demonstrate integrity drift.</p>
                  </div>
                </div>

                <form id="tamperForm" class="action-form" style="margin-top: 14px;">
                  <div class="field-grid">
                    <label class="field">
                      <span>Transaction index</span>
                      <select id="tamperTransactionIndex" name="transactionIndex">
                        ${block.transactions.map((_, transactionIndex) => `<option value="${transactionIndex}">#${transactionIndex}</option>`).join("")}
                      </select>
                    </label>
                    <label class="field">
                      <span>Sender</span>
                      <input type="text" name="sender" value="${escapeHtml(block.transactions[0]?.sender ?? "Alice")}" required />
                    </label>
                    <label class="field">
                      <span>Receiver</span>
                      <input type="text" name="receiver" value="${escapeHtml(block.transactions[0]?.receiver ?? "Bob")}" required />
                    </label>
                    <label class="field">
                      <span>Amount</span>
                      <input type="number" name="amount" min="0.01" step="0.01" value="${escapeHtml(Number(block.transactions[0]?.amount ?? 1).toFixed(2))}" required />
                    </label>
                    <label class="field field--wide">
                      <span>Metadata</span>
                      <input type="text" name="metadata" value="${escapeHtml(block.transactions[0]?.metadata ?? "tampered")}" />
                    </label>
                  </div>
                  <div class="form-actions">
                    <button class="primary-button" type="submit">Apply tamper</button>
                  </div>
                </form>
              </div>
            ` : ""}
          </section>
        </div>
      ` : `
        <div class="empty-state">
          <h3>Block not loaded yet</h3>
          <p>Refresh the data or choose a block from the selector above.</p>
        </div>
      `}
    </section>
  `;
}

function buildMerkleNode(node, isRoot = false, label = "node") {
  if (!node) {
    return "";
  }

  const hasChildren = Boolean(node.left || node.right);
  const children = [node.left ? buildMerkleNode(node.left, false, "left") : "", node.right ? buildMerkleNode(node.right, false, "right") : ""].filter(Boolean).join("");
  const truncatedHash = truncateHash(node.hash, TREE_HASH_TRUNCATION.start, TREE_HASH_TRUNCATION.end);

  return `
    <li>
      <div class="merkle-node" data-root="${isRoot ? "true" : "false"}" data-label="${escapeHtml(isRoot ? "root" : label)}">
        <strong class="merkle-node__title">${escapeHtml(truncatedHash)}</strong>
        <code class="merkle-node__hash" title="${escapeHtml(node.hash)}">${escapeHtml(node.hash)}</code>
      </div>
      ${hasChildren ? `<ul>${children}</ul>` : ""}
    </li>
  `;
}

function buildMerkleTreeView() {
  const index = getSelectedBlockIndex();
  const block = state.selectedBlockDetails;
  const root = block?.merkle_tree?.root;
  const proof = state.merkleProof;

  return `
    <section class="view">
      <div class="view-header">
        <div>
          <h2 class="view-title">Merkle Tree</h2>
          <p class="view-subtitle">Graphic visualization of the selected block's Merkle tree.</p>
        </div>
        <div class="badge-row">
          <span class="badge">Block ${escapeHtml(index)}</span>
          <span class="badge">${escapeHtml(block?.transactions?.length ?? 0)} leaves</span>
        </div>
      </div>

      <div class="toolbar">
        <div class="group">
          <label class="small-note" for="treeSelect">Choose a block</label>
          <select id="treeSelect" class="select">
            ${getBlockIndexList().map((blockIndex) => `<option value="${escapeHtml(blockIndex)}" ${blockIndex === index ? "selected" : ""}>Block ${escapeHtml(blockIndex)}</option>`).join("")}
          </select>
        </div>
        <div class="group">
          <button class="secondary-button" type="button" data-open-route="details" data-block-index="${escapeHtml(index)}">Open block details</button>
        </div>
      </div>

      <section class="tree-shell">
        <h3>Merkle tree structure</h3>
        <p style="margin-top: 8px;">Nodes are rendered from the backend tree payload and update with the selected block.</p>

        ${root ? `
          <div class="merkle-tree">
            <div class="merkle-tree-root">
              <ul>${buildMerkleNode(root, true, "root")}</ul>
            </div>
          </div>
        ` : `
          <div class="empty-state" style="margin-top: 14px;">
            <h3>No Merkle tree available</h3>
            <p>The selected block has no transactions, so there is no Merkle tree to render.</p>
          </div>
        `}
      </section>

      <section class="proof-shell">
        <div class="section-header">
          <div>
            <h3>Merkle proof</h3>
            <p>Inspect the proof for any transaction in this block.</p>
          </div>
        </div>

        ${Array.isArray(block?.transactions) && block.transactions.length > 0 ? `
          <form id="proofForm" class="proof-form" style="margin-top: 14px;">
            <label class="field">
              <span>Transaction index</span>
              <select id="proofTransactionIndex" name="proofTransactionIndex">
                ${block.transactions.map((_, transactionIndex) => `<option value="${transactionIndex}">#${transactionIndex}</option>`).join("")}
              </select>
            </label>
            <button class="secondary-button" type="submit">Verify proof</button>
          </form>
        ` : ""}

        ${proof ? `
          <div class="proof-result ${proof.valid ? "proof-result--valid" : "proof-result--invalid"}">
            <div class="proof-status">${proof.valid ? "Valid proof" : "Invalid proof"}</div>
            <div class="proof-row"><span>Transaction hash</span><code>${escapeHtml(proof.proof.transaction_hash)}</code></div>
            <div class="proof-row"><span>Merkle root</span><code>${escapeHtml(proof.proof.merkle_root)}</code></div>
            <ul class="proof-list">
              ${proof.proof.proof_steps.map((step, stepIndex) => `
                <li class="proof-item">
                  <span>Step ${stepIndex + 1}</span>
                  <strong>${escapeHtml(step.direction)}</strong>
                  <code>${escapeHtml(step.hash)}</code>
                </li>
              `).join("")}
            </ul>
          </div>
        ` : Array.isArray(block?.transactions) && block.transactions.length > 0 ? `
          <div class="empty-state" style="margin-top: 14px;">
            <h3>No proof generated yet</h3>
            <p>Select a transaction and run the proof verification to inspect the authentication path.</p>
          </div>
        ` : ""}
      </section>
    </section>
  `;
}

function buildLoadingView() {
  return `
    <section class="view">
      <div class="empty-state">
        <h3>Loading blockchain data</h3>
        <p>The frontend is connecting to the backend and fetching the current chain state.</p>
      </div>
    </section>
  `;
}

function buildErrorView() {
  return `
    <section class="view">
      <div class="error-state">
        <h3>Unable to load blockchain data</h3>
        <p>${escapeHtml(state.error ?? "An unknown error occurred.")}</p>
      </div>
    </section>
  `;
}

function renderNotice() {
  if (!state.notice) {
    return "";
  }

  const kind = state.notice.type === "error" ? "inline-banner--error" : "inline-banner--success";
  return `
    <div class="inline-banner ${kind}">${escapeHtml(state.notice.text)}</div>
  `;
}

function render() {
  setActiveRouteButtons(state.route);

  if (state.loading && !state.status && !state.error) {
    content.innerHTML = buildLoadingView();
    return;
  }

  if (state.error && !state.status) {
    content.innerHTML = buildErrorView();
    return;
  }

  let nextView = "";
  if (state.route === "blockchain") {
    nextView = buildBlockchainView();
  } else if (state.route === "details") {
    nextView = buildBlockDetailsView();
  } else if (state.route === "merkle") {
    nextView = buildMerkleTreeView();
  } else {
    nextView = buildDashboardView();
  }

  content.innerHTML = `${renderNotice()}${nextView}`;
  bindDynamicHandlers();
}

function bindDynamicHandlers() {
  document.querySelectorAll("[data-open-route]").forEach((button) => {
    button.addEventListener("click", () => {
      const route = button.dataset.openRoute;
      const index = Number(button.dataset.blockIndex);
      if (route === "details" || route === "merkle") {
        navigate(route, Number.isNaN(index) ? getSelectedBlockIndex() : index);
      }
    });
  });

  const blockSelect = document.getElementById("blockSelect");
  if (blockSelect) {
    blockSelect.addEventListener("change", async (event) => {
      const nextIndex = Number.parseInt(event.target.value, 10);
      state.selectedBlockIndex = nextIndex;
      await loadBlockDetails(nextIndex);
      navigate("details", nextIndex);
    });
  }

  const treeSelect = document.getElementById("treeSelect");
  if (treeSelect) {
    treeSelect.addEventListener("change", async (event) => {
      const nextIndex = Number.parseInt(event.target.value, 10);
      state.selectedBlockIndex = nextIndex;
      await loadBlockDetails(nextIndex);
      navigate("merkle", nextIndex);
    });
  }

  const transactionForm = document.getElementById("transactionForm");
  if (transactionForm) {
    transactionForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(transactionForm);
      const payload = {
        sender: String(formData.get("sender") || "").trim(),
        receiver: String(formData.get("receiver") || "").trim(),
        amount: Number(formData.get("amount")),
        metadata: String(formData.get("metadata") || "").trim() || null,
      };

      try {
        const response = await fetchJson("/transactions/add", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        state.notice = { type: "success", text: `Transaction added: ${response.sender} → ${response.receiver}.` };
        transactionForm.reset();
        await loadBlockchainOverview();
      } catch (error) {
        state.notice = { type: "error", text: error instanceof Error ? error.message : String(error) };
        render();
      }
    });
  }

  const createBlockButton = document.getElementById("createBlockButton");
  if (createBlockButton) {
    createBlockButton.addEventListener("click", async () => {
      try {
        await fetchJson("/blockchain/blocks");
        state.notice = { type: "success", text: "A new block was created from the pending transactions." };
        await loadBlockchainOverview();
      } catch (error) {
        state.notice = { type: "error", text: error instanceof Error ? error.message : String(error) };
        render();
      }
    });
  }

  const tamperForm = document.getElementById("tamperForm");
  if (tamperForm) {
    const txIndexField = document.getElementById("tamperTransactionIndex");
    const fillTamperFields = (transactionIndex) => {
      const tx = state.selectedBlockDetails?.transactions?.[transactionIndex];
      if (!tx) {
        return;
      }
      tamperForm.elements.sender.value = tx.sender ?? "Alice";
      tamperForm.elements.receiver.value = tx.receiver ?? "Bob";
      tamperForm.elements.amount.value = Number(tx.amount ?? 1).toFixed(2);
      tamperForm.elements.metadata.value = tx.metadata ?? "tampered";
    };

    if (txIndexField) {
      txIndexField.addEventListener("change", (event) => {
        fillTamperFields(Number(event.target.value));
      });
      fillTamperFields(Number(txIndexField.value));
    }

    tamperForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const transactionIndex = Number(tamperForm.elements.transactionIndex.value);
      const payload = {
        sender: String(tamperForm.elements.sender.value || "").trim(),
        receiver: String(tamperForm.elements.receiver.value || "").trim(),
        amount: Number(tamperForm.elements.amount.value),
        metadata: String(tamperForm.elements.metadata.value || "").trim() || null,
      };

      try {
        await fetchJson(`/transactions/tamper?block_index=${state.selectedBlockIndex}&transaction_index=${transactionIndex}`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
        state.notice = { type: "success", text: `Tamper applied to block ${state.selectedBlockIndex}, transaction #${transactionIndex}.` };
        state.merkleProof = null;
        await loadBlockchainOverview();
      } catch (error) {
        state.notice = { type: "error", text: error instanceof Error ? error.message : String(error) };
        render();
      }
    });
  }

  const proofForm = document.getElementById("proofForm");
  if (proofForm) {
    proofForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const transactionIndex = Number(new FormData(proofForm).get("proofTransactionIndex"));
      const blockIndex = state.selectedBlockIndex;

      try {
        state.merkleProof = await fetchJson(`/blockchain/blocks/${blockIndex}/transactions/${transactionIndex}/merkle-proof`);
        render();
      } catch (error) {
        state.notice = { type: "error", text: error instanceof Error ? error.message : String(error) };
        render();
      }
    });
  }
}

async function syncRoute() {
  const { route, index } = parseRoute();
  state.route = route;
  if (index !== null && index !== undefined) {
    state.selectedBlockIndex = index;
  }

  if (route === "details" || route === "merkle") {
    try {
      await loadBlockDetails(getSelectedBlockIndex());
    } catch (error) {
      state.error = error instanceof Error ? error.message : String(error);
      setConnectionBadge("status-chip--bad", "Failed to load selected block");
    }
  }

  render();
}

refreshButton.addEventListener("click", async () => {
  state.notice = null;
  state.merkleProof = null;
  await loadBlockchainOverview();
  await syncRoute();
});

routeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const route = button.dataset.route;
    if (!route) {
      return;
    }
    navigate(route, route === "dashboard" || route === "blockchain" ? null : getSelectedBlockIndex());
  });
});

window.addEventListener("hashchange", syncRoute);

(async function bootstrap() {
  if (!location.hash) {
    location.hash = "#/dashboard";
  }

  await loadBlockchainOverview();
  await syncRoute();
})();
