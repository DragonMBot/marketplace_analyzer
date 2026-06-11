const API_URL = "http://localhost:8000";

const authSection = document.getElementById("authSection");
const appSection = document.getElementById("appSection");

const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");

const addProductBtn = document.getElementById("addProductBtn");
const logoutBtn = document.getElementById("logoutBtn");

const productsList = document.getElementById("productsList");
const message = document.getElementById("message");

function showMessage(text) {
    message.textContent = text;
}

async function saveToken(token) {
    await browser.storage.local.set({
        access_token: token
    });
}

async function getToken() {
    const data = await browser.storage.local.get(
        "access_token"
    );

    return data.access_token;
}

async function removeToken() {
    await browser.storage.local.remove(
        "access_token"
    );
}

async function checkAuth() {

    const token = await getToken();

    if (token) {
        authSection.classList.add("hidden");
        appSection.classList.remove("hidden");

        loadProducts();
    }
}

async function register() {

    try {

        const response = await fetch(
            `${API_URL}/api/v1/auth/register`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: emailInput.value,
                    password: passwordInput.value
                })
            }
        );

        if (!response.ok) {
            throw new Error("Ошибка регистрации");
        }

        showMessage("Регистрация выполнена");

    } catch (e) {

        showMessage(e.message);
    }
}

async function login() {

    try {

        const response = await fetch(
            `${API_URL}/api/v1/auth/login`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: emailInput.value,
                    password: passwordInput.value
                })
            }
        );

        if (!response.ok) {
            throw new Error("Ошибка авторизации");
        }

        const data = await response.json();

        await saveToken(
            data.access_token
        );

        authSection.classList.add("hidden");
        appSection.classList.remove("hidden");

        loadProducts();

    } catch (e) {

        showMessage(e.message);
    }
}

async function loadProducts() {

    const items = await browser.storage.local.get(
        "tracked_products"
    );

    const products =
        items.tracked_products || [];

    productsList.innerHTML = "";

    for (const product of products) {

        const div = document.createElement("div");

        div.className = "product-card";

        div.innerHTML = `
            <div>
                <b>ID:</b> ${product}
            </div>

            <button
                class="delete-btn"
                data-id="${product}"
            >
                Удалить
            </button>
        `;

        productsList.appendChild(div);
    }

    document
        .querySelectorAll(".delete-btn")
        .forEach(btn => {

            btn.addEventListener(
                "click",
                deleteProduct
            );
        });
}

async function addProduct() {

    const id =
        document
            .getElementById("productId")
            .value
            .trim();

    if (!id) {
        return;
    }

    const data =
        await browser.storage.local.get(
            "tracked_products"
        );

    const products =
        data.tracked_products || [];

    if (!products.includes(id)) {
        products.push(id);
    }

    await browser.storage.local.set({
        tracked_products: products
    });

    loadProducts();
}

async function deleteProduct(event) {

    const productId =
        event.target.dataset.id;

    const data =
        await browser.storage.local.get(
            "tracked_products"
        );

    const products =
        data.tracked_products || [];

    const filtered =
        products.filter(
            p => p !== productId
        );

    await browser.storage.local.set({
        tracked_products: filtered
    });

    loadProducts();
}

async function logout() {

    await removeToken();

    authSection.classList.remove("hidden");
    appSection.classList.add("hidden");
}

loginBtn.addEventListener(
    "click",
    login
);

registerBtn.addEventListener(
    "click",
    register
);

addProductBtn.addEventListener(
    "click",
    addProduct
);

logoutBtn.addEventListener(
    "click",
    logout
);

checkAuth();