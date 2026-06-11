function getProductId() {
    const match = window.location.href.match(/\/product\/(\d+)/);
    return match ? match[1] : null;
}

browser.runtime.onMessage.addListener((msg) => {
    if (msg.type === "GET_PRODUCT_ID") {
        return Promise.resolve({
            productId: getProductId()
        });
    }
});