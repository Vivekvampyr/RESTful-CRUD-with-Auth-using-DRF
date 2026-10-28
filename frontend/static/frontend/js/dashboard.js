const elements = {
    count: document.getElementById("product-count"),
    message: document.getElementById("product-message"),
    loading: document.getElementById("product-loading"),
    error: document.getElementById("product-error"),
    errorText: document.getElementById("product-error-text"),
    empty: document.getElementById("product-empty"),
    tableContainer: document.getElementById("product-table-container"),
    tableBody: document.getElementById("product-table-body"),
    pagination: document.getElementById("product-pagination"),
    paginationInfo: document.getElementById("pagination-info"),
    previous: document.getElementById("previous-page"),
    next: document.getElementById("next-page"),
    refresh: document.getElementById("refresh-products"),
    retry: document.getElementById("retry-products"),
};

let nextPageUrl = null;
let previousPageUrl = null;
let currentPageUrl = "/api/products/";
let isLoading = false;


function hideAllStates() {
    elements.loading.hidden = true;
    elements.error.hidden = true;
    elements.empty.hidden = true;
    elements.tableContainer.hidden = true;
    elements.pagination.hidden = true;
}


function showLoading() {
    hideAllStates();
    elements.loading.hidden = false;
    elements.message.hidden = true;
}


function showError(message) {
    hideAllStates();

    elements.errorText.textContent = message;
    elements.error.hidden = false;
    elements.message.hidden = true;
}


function showEmpty() {
    hideAllStates();
    elements.empty.hidden = false;
    elements.message.hidden = true;
}


function formatPrice(value) {
    if (value === null || value === undefined || value === "") {
        return "—";
    }

    const number = Number(value);

    if (!Number.isFinite(number)) {
        return "—";
    }

    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 2,
    }).format(number);
}


function createCell(value, className = "") {
    const cell = document.createElement("td");

    if (className) {
        cell.className = className;
    }

    cell.textContent = value;
    return cell;
}


function renderProducts(products) {
    elements.tableBody.replaceChildren();

    for (const product of products) {
        const row = document.createElement("tr");

        const nameCell = createCell(product.name, "product-name");
        const description = document.createElement("span");

        description.className = "product-description";
        description.textContent = product.description || "No description";

        nameCell.appendChild(document.createElement("br"));
        nameCell.appendChild(description);

        const salePrice = product.sale_price
            ? formatPrice(product.sale_price)
            : "—";

        const status = product.is_active ? "Active" : "Inactive";
        const statusCell = createCell(status);

        const statusBadge = document.createElement("span");
        statusBadge.className = product.is_active
            ? "status-badge status-active"
            : "status-badge status-inactive";
        statusBadge.textContent = status;

        statusCell.replaceChildren(statusBadge);

        row.append(
            nameCell,
            createCell(formatPrice(product.price)),
            createCell(salePrice),
            createCell(String(product.stock)),
            statusCell,
        );

        elements.tableBody.appendChild(row);
    }
}


function renderPagination(data, pageUrl) {
    nextPageUrl = data.next;
    previousPageUrl = data.previous;
    currentPageUrl = pageUrl;

    elements.pagination.hidden = false;
    elements.paginationInfo.textContent =
        `${data.count} product${data.count === 1 ? "" : "s"} total`;

    elements.previous.disabled = !previousPageUrl;
    elements.next.disabled = !nextPageUrl;
}


async function loadProducts(url = "/api/products/") {
    if (isLoading) {
        return;
    }

    isLoading = true;
    showLoading();

    elements.refresh.disabled = true;
    elements.retry.disabled = true;

    try {
        const response = await fetch(url, {
            method: "GET",
            credentials: "same-origin",
            headers: {
                "Accept": "application/json",
            },
        });

        if (response.status === 401 || response.status === 403) {
            throw new Error(
                "Your session may have expired. Please log in again."
            );
        }

        if (!response.ok) {
            throw new Error(
                `The server returned an error (${response.status}).`
            );
        }

        const data = await response.json();

        // Support both paginated and non-paginated API responses.
        const products = Array.isArray(data)
            ? data
            : data.results;

        if (!Array.isArray(products)) {
            throw new Error("The API returned an unexpected response.");
        }

        const totalCount = Array.isArray(data)
            ? products.length
            : data.count;

        elements.count.textContent = totalCount;

        if (products.length === 0) {
            hideAllStates();
            showEmpty();

            // Keep pagination available if the current page is empty
            // but the API still provides pagination metadata.
            if (!Array.isArray(data) && data.count > 0) {
                renderPagination(data, url);
            }

            return;
        }

        hideAllStates();
        renderProducts(products);
        elements.tableContainer.hidden = false;

        if (!Array.isArray(data)) {
            renderPagination(data, url);
        }

    } catch (error) {
        showError(error.message || "An unexpected error occurred.");
    } finally {
        isLoading = false;
        elements.refresh.disabled = false;
        elements.retry.disabled = false;
    }
}


elements.refresh.addEventListener("click", () => {
    loadProducts(currentPageUrl);
});

elements.retry.addEventListener("click", () => {
    loadProducts(currentPageUrl);
});

elements.previous.addEventListener("click", () => {
    if (previousPageUrl) {
        loadProducts(previousPageUrl);
    }
});

elements.next.addEventListener("click", () => {
    if (nextPageUrl) {
        loadProducts(nextPageUrl);
    }
});

loadProducts();