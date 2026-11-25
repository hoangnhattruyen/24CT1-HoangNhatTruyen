// Main JavaScript for Concung E-Commerce
document.addEventListener('DOMContentLoaded', () => {
    initFlashSaleCountdown();
    initSearchAutoComplete();
    initImageSearchModal();
    initAddToCartButtons();
});

// 1. Flash Sale Countdown Timer
function initFlashSaleCountdown() {
    const timerElement = document.getElementById('flash-sale-timer');
    if (!timerElement) return;

    const endTimeAttr = timerElement.getAttribute('data-end-time');
    const targetDate = endTimeAttr ? new Date(endTimeAttr).getTime() : (new Date().getTime() + 1000 * 60 * 60 * 5);

    function updateTimer() {
        const now = new Date().getTime();
        const distance = targetDate - now;

        if (distance < 0) {
            timerElement.innerHTML = "<span>Đã kết thúc</span>";
            return;
        }

        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        const pad = (n) => n < 10 ? '0' + n : n;

        const hEl = document.getElementById('timer-hours');
        const mEl = document.getElementById('timer-minutes');
        const sEl = document.getElementById('timer-seconds');

        if (hEl) hEl.textContent = pad(hours);
        if (mEl) mEl.textContent = pad(minutes);
        if (sEl) sEl.textContent = pad(seconds);
    }

    updateTimer();
    setInterval(updateTimer, 1000);
}

// 2. Search Autocomplete API
function initSearchAutoComplete() {
    const searchInput = document.getElementById('search-input');
    const suggestionsBox = document.getElementById('search-suggestions');
    if (!searchInput || !suggestionsBox) return;

    let debounceTimer;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        clearTimeout(debounceTimer);

        if (query.length < 2) {
            suggestionsBox.style.display = 'none';
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/api/search/?q=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => {
                    if (data.results && data.results.length > 0) {
                        let html = `<div class="suggestion-header">Sản phẩm gợi ý cho "${query}"</div>`;
                        data.results.forEach(item => {
                            html += `
                                <a href="${item.url}" class="suggestion-item">
                                    <img src="${item.image}" class="suggestion-thumb" alt="${item.name}">
                                    <div>
                                        <div style="font-weight:700; font-size:13px;">${item.name}</div>
                                        <div style="color:#FF82AB; font-weight:800; font-size:12px;">${item.price}</div>
                                    </div>
                                </a>
                            `;
                        });
                        suggestionsBox.innerHTML = html;
                        suggestionsBox.style.display = 'block';
                    } else {
                        suggestionsBox.style.display = 'none';
                    }
                })
                .catch(() => {
                    suggestionsBox.style.display = 'none';
                });
        }, 250);
    });

    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
            suggestionsBox.style.display = 'none';
        }
    });
}

// 3. Image Search Modal
function initImageSearchModal() {
    const openBtn = document.getElementById('btn-open-img-search');
    const modal = document.getElementById('image-search-modal');
    const closeBtn = document.getElementById('modal-close-btn');
    const fileInput = document.getElementById('image-file-input');
    const dropzone = document.getElementById('modal-dropzone');
    const previewContainer = document.getElementById('image-preview-area');

    if (!openBtn || !modal) return;

    openBtn.addEventListener('click', () => {
        modal.style.display = 'flex';
    });

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    if (dropzone && fileInput) {
        dropzone.addEventListener('click', () => fileInput.click());

        fileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                const reader = new FileReader();
                reader.onload = function(evt) {
                    previewContainer.innerHTML = `
                        <img src="${evt.target.result}" style="max-height:120px; border-radius:8px; margin:0 auto;" />
                        <p style="font-size:13px; font-weight:700; color:#FF82AB; margin-top:8px;">Đang phân tích hình ảnh và tìm kiếm sản phẩm tương tự...</p>
                    `;
                    setTimeout(() => {
                        window.location.href = '/category/sua-bot-cao-cap/?q=search_image';
                    }, 1200);
                };
                reader.readAsDataURL(e.target.files[0]);
            }
        });
    }
}

// 4. AJAX Add to Cart
function initAddToCartButtons() {
    document.addEventListener('click', async function(e) {
        const btn = e.target.closest('.btn-add-to-cart');
        if (!btn) return;

        e.preventDefault();
        const productId = btn.getAttribute('data-product-id');
        const qty = btn.getAttribute('data-quantity') || 1;
        const buyNow = btn.getAttribute('data-buy-now') === 'true';

        if (!productId) {
            showToast('Thiếu thông tin sản phẩm.');
            return;
        }

        const originalText = btn.textContent.trim();
        const loadingText = buyNow ? 'Đang xử lý...' : 'Đang thêm...';
        btn.disabled = true;
        btn.textContent = loadingText;

        const formData = new FormData();
        formData.append('product_id', productId);
        formData.append('quantity', String(qty || 1));

        try {
            const res = await fetch('/orders/cart/add/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Accept': 'application/json'
                },
                body: formData
            });

            const data = await res.json().catch(() => ({
                success: false,
                message: 'Không thể thêm sản phẩm vào giỏ hàng.'
            }));

            if (!res.ok || !data.success) {
                btn.disabled = false;
                btn.textContent = originalText;
                showToast(data.message || 'Không thể thêm sản phẩm vào giỏ hàng.');
                return;
            }

            updateCartBadge(data.cart_count);

            if (buyNow) {
                btn.textContent = 'Đang chuyển...';
                window.location.href = '/orders/cart/';
                return;
            }

            btn.disabled = false;
            btn.textContent = originalText;
            showToast(data.message);
        } catch (error) {
            btn.disabled = false;
            btn.textContent = originalText;
            showToast('Không thể thêm sản phẩm vào giỏ hàng.');
        }
    });
}

function updateCartBadge(count) {
    const badge = document.getElementById('header-cart-count');
    if (badge) badge.textContent = count;
}

function showToast(msg) {
    let toast = document.getElementById('site-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'site-toast';
        toast.className = 'toast-msg';
        document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.style.display = 'block';
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue || '';
}
