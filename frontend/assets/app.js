const API_BASE = "";

function getToken() {
    return localStorage.getItem("access_token");
}

function setToken(token) {
    localStorage.setItem("access_token", token);
}

function clearToken() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_email");
    localStorage.removeItem("user_role");
}

function showError(message) {
    const errorBox = document.getElementById("errorBox");
    if (errorBox) {
        errorBox.style.display = "block";
        errorBox.innerText = message;
    }
}

function setPage(title, subtitle) {
    const pageTitle = document.getElementById("pageTitle");
    const pageSubtitle = document.getElementById("pageSubtitle");

    if (pageTitle) pageTitle.innerText = title;
    if (pageSubtitle) pageSubtitle.innerText = subtitle;
}

function setMainContent(html) {
    const mainContent = document.getElementById("mainContent");
    if (mainContent) {
        mainContent.innerHTML = html;
    }
}

async function login(email, password) {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const response = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Login failed");
    }

    setToken(data.access_token);
    localStorage.setItem("user_email", data.user.email);
    localStorage.setItem("user_role", data.user.role);

    window.location.href = "/site/dashboard.html";
}

async function apiGet(path) {
    const token = getToken();

    const response = await fetch(path, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Request failed");
    }

    return data;
}

async function apiPost(path, body) {
    const token = getToken();

    const response = await fetch(path, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Request failed");
    }

    return data;
}

function logout() {
    clearToken();
    window.location.href = "/site/login.html";
}

async function loadMe() {
    const token = getToken();

    if (!token) {
        window.location.href = "/site/login.html";
        return;
    }

    try {
        const user = await apiGet("/auth/me");

        const accountInfo = document.getElementById("accountInfo");
        if (accountInfo) {
            accountInfo.innerText = `${user.email} (${user.role})`;
        }
    } catch (error) {
        clearToken();
        window.location.href = "/site/login.html";
    }
}

function renderTable(data) {
    if (!Array.isArray(data)) {
        data = [data];
    }

    if (data.length === 0) {
        return "<p>No data found.</p>";
    }

    const keys = Object.keys(data[0]);

    let html = "<table><thead><tr>";

    keys.forEach(key => {
        html += `<th>${key}</th>`;
    });

    html += "</tr></thead><tbody>";

    data.forEach(row => {
        html += "<tr>";

        keys.forEach(key => {
            let value = row[key];

            if (Array.isArray(value)) {
                value = JSON.stringify(value);
            } else if (typeof value === "object" && value !== null) {
                value = JSON.stringify(value);
            }

            html += `<td>${value ?? ""}</td>`;
        });

        html += "</tr>";
    });

    html += "</tbody></table>";
    return html;
}

function showMessage(message, type = "success") {
    const messageBox = document.getElementById("messageBox");

    if (messageBox) {
        messageBox.className = type === "success" ? "message success" : "message error";
        messageBox.innerText = message;
        messageBox.style.display = "block";
    }
}

function loadDashboard() {
    setPage("Dashboard", "Manage your fashion store inventory, sales, orders, payments and reports.");

    setMainContent(`
        <div class="cards">
            <div class="card" onclick="loadCategoriesPage()">
                <h3>Categories</h3>
                <p>Create and view fashion categories.</p>
            </div>

            <div class="card" onclick="loadProductsPage()">
                <h3>Products</h3>
                <p>Create products and search products.</p>
            </div>

            <div class="card" onclick="loadVariantsPage()">
                <h3>Variants</h3>
                <p>Create size, color, price and stock variants.</p>
            </div>

            <div class="card" onclick="loadSection('reports')">
                <h3>Reports</h3>
                <p>View sales, profit and stock reports.</p>
            </div>
        </div>
    `);
}

async function loadCategoriesPage() {
    setPage("Categories", "Create, view and manage product categories.");

    setMainContent(`
        <div class="content-box">
            <h2>Create Category</h2>
            <div id="messageBox" class="message"></div>

            <form id="categoryForm" class="form-grid">
                <input type="text" id="categoryName" placeholder="Category name" required>
                <input type="text" id="categoryDescription" placeholder="Description">
                <button type="submit">Create Category</button>
            </form>
        </div>

        <div class="content-box">
            <h2>Category List</h2>
            <div id="categoryTable">Loading...</div>
        </div>
    `);

    document.getElementById("categoryForm").addEventListener("submit", async (event) => {
        event.preventDefault();

        const name = document.getElementById("categoryName").value;
        const description = document.getElementById("categoryDescription").value;

        try {
            await apiPost("/categories/", { name, description });
            showMessage("Category created successfully");
            loadCategoriesPage();
        } catch (error) {
            showMessage(error.message, "error");
        }
    });

    await refreshCategoriesTable();
}

async function refreshCategoriesTable() {
    try {
        const categories = await apiGet("/categories/");
        document.getElementById("categoryTable").innerHTML = renderTable(categories);
    } catch (error) {
        document.getElementById("categoryTable").innerHTML = `<p class="error-text">${error.message}</p>`;
    }
}

async function loadProductsPage() {
    setPage("Products", "Create products, view products and search by name.");

    setMainContent(`
        <div class="content-box">
            <h2>Create Product</h2>
            <div id="messageBox" class="message"></div>

            <form id="productForm" class="form-grid">
                <input type="text" id="productName" placeholder="Product name" required>
                <select id="productCategory" required>
                    <option value="">Select category</option>
                </select>
                <input type="text" id="productBrand" placeholder="Brand">
                <input type="text" id="productDescription" placeholder="Description">
                <button type="submit">Create Product</button>
            </form>
        </div>

        <div class="content-box">
            <h2>Search Products</h2>
            <div class="form-grid">
                <input type="text" id="productSearch" placeholder="Search product name">
                <button onclick="searchProducts()">Search</button>
                <button onclick="refreshProductsTable()">Show All</button>
            </div>
        </div>

        <div class="content-box">
            <h2>Product List</h2>
            <div id="productTable">Loading...</div>
        </div>
    `);

    await loadCategoryDropdown();

    document.getElementById("productForm").addEventListener("submit", async (event) => {
        event.preventDefault();

        const name = document.getElementById("productName").value;
        const category_id = Number(document.getElementById("productCategory").value);
        const brand = document.getElementById("productBrand").value;
        const description = document.getElementById("productDescription").value;

        try {
            await apiPost("/products/", {
                name,
                category_id,
                brand,
                description
            });

            showMessage("Product created successfully");
            loadProductsPage();
        } catch (error) {
            showMessage(error.message, "error");
        }
    });

    await refreshProductsTable();
}

async function loadCategoryDropdown() {
    const select = document.getElementById("productCategory");

    try {
        const categories = await apiGet("/categories/");

        categories.forEach(category => {
            const option = document.createElement("option");
            option.value = category.id;
            option.innerText = `${category.id} - ${category.name}`;
            select.appendChild(option);
        });
    } catch (error) {
        showMessage("Could not load categories. Create category first.", "error");
    }
}

async function refreshProductsTable() {
    try {
        const products = await apiGet("/products/");
        document.getElementById("productTable").innerHTML = renderTable(products);
    } catch (error) {
        document.getElementById("productTable").innerHTML = `<p class="error-text">${error.message}</p>`;
    }
}

async function searchProducts() {
    const search = document.getElementById("productSearch").value;

    try {
        const products = await apiGet(`/products/?search=${encodeURIComponent(search)}`);
        document.getElementById("productTable").innerHTML = renderTable(products);
    } catch (error) {
        document.getElementById("productTable").innerHTML = `<p class="error-text">${error.message}</p>`;
    }
}

async function loadVariantsPage() {
    setPage("Product Variants", "Create variants with size, color, price, stock and SKU.");

    setMainContent(`
        <div class="content-box">
            <h2>Create Variant</h2>
            <div id="messageBox" class="message"></div>

            <form id="variantForm" class="form-grid">
                <select id="variantProduct" required>
                    <option value="">Select product</option>
                </select>
                <input type="text" id="variantSize" placeholder="Size: M / L / XL" required>
                <input type="text" id="variantColor" placeholder="Color" required>
                <input type="number" id="variantBuyPrice" placeholder="Buy price" required>
                <input type="number" id="variantSellPrice" placeholder="Sell price" required>
                <input type="number" id="variantStock" placeholder="Stock quantity" required>
                <input type="text" id="variantSku" placeholder="SKU" required>
                <button type="submit">Create Variant</button>
            </form>
        </div>

        <div class="content-box">
            <h2>Variant List</h2>
            <div id="variantTable">Loading...</div>
        </div>
    `);

    await loadProductDropdown();

    document.getElementById("variantForm").addEventListener("submit", async (event) => {
        event.preventDefault();

        const product_id = Number(document.getElementById("variantProduct").value);
        const size = document.getElementById("variantSize").value;
        const color = document.getElementById("variantColor").value;
        const buy_price = Number(document.getElementById("variantBuyPrice").value);
        const sell_price = Number(document.getElementById("variantSellPrice").value);
        const stock_quantity = Number(document.getElementById("variantStock").value);
        const sku = document.getElementById("variantSku").value;

        try {
            await apiPost("/variants/", {
                product_id,
                size,
                color,
                buy_price,
                sell_price,
                stock_quantity,
                sku
            });

            showMessage("Variant created successfully");
            loadVariantsPage();
        } catch (error) {
            showMessage(error.message, "error");
        }
    });

    await refreshVariantsTable();
}

async function loadProductDropdown() {
    const select = document.getElementById("variantProduct");

    try {
        const products = await apiGet("/products/");

        products.forEach(product => {
            const option = document.createElement("option");
            option.value = product.id;
            option.innerText = `${product.id} - ${product.name}`;
            select.appendChild(option);
        });
    } catch (error) {
        showMessage("Could not load products. Create product first.", "error");
    }
}

async function refreshVariantsTable() {
    try {
        const variants = await apiGet("/variants/");
        document.getElementById("variantTable").innerHTML = renderTable(variants);
    } catch (error) {
        document.getElementById("variantTable").innerHTML = `<p class="error-text">${error.message}</p>`;
    }
}

async function loadSection(section) {
    setPage(section.toUpperCase(), `Quick view for ${section}.`);

    setMainContent(`
        <div class="content-box">
            <h2>${section.toUpperCase()}</h2>
            <div id="quickTable">Loading...</div>
        </div>
    `);

    const routes = {
        stock: "/stock/history",
        customers: "/customers/",
        orders: "/orders/",
        payments: "/payments/",
        invoices: "/invoices/",
        reports: "/reports/profit",
        users: "/users/"
    };

    try {
        const data = await apiGet(routes[section]);
        document.getElementById("quickTable").innerHTML = renderTable(data);
    } catch (error) {
        document.getElementById("quickTable").innerHTML = `<p class="error-text">${error.message}</p>`;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            try {
                await login(email, password);
            } catch (error) {
                showError(error.message);
            }
        });
    }

    if (window.location.pathname.includes("dashboard.html")) {
        loadMe();
    }
});
