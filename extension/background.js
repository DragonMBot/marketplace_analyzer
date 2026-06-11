const API_BASE = "http://localhost:8000";

async function fetchPrice(productId) {

  const res = await fetch(`${API_BASE}/api/v1/products/parse`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      product_id: productId,
      marketplace: "ozon"
    })
  });

  return await res.json();
}

browser.runtime.onMessage.addListener((msg, sender, sendResponse) => {

  if (msg.type === "GET_PRICE") {

    fetchPrice(msg.productId)
      .then(data => sendResponse({ success: true, data }))
      .catch(err => sendResponse({ success: false, error: err.message }));

    return true; // async
  }
});