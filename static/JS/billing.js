const roomName = "lobby";
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

// Cache for messages
const messageCache = {};
const messageListEl = document.getElementById('message-list');

// Default QR (shared)
let qrSrc = "http://172.25.206.124:8000/static/admin/img/scanner.jpeg";

// Render detail card
function renderDetail(data) {
    document.getElementById('car-number').innerText = `Car Number: ${data.car_number}`;
    document.getElementById('distance').innerText = `Distance Travelled: ${data.distance_travelled} km`;
    document.getElementById('charge-per-km').innerText = `Charge per km: ₹${data.charge_per_km_cars}`;
    document.getElementById('total-charge').innerText = `Total Charge: ₹${data.total_charge}`;
    document.getElementById('payment-qr').src = qrSrc || `data:image/jpeg;base64,${data.payment_account}`;

}

// Add item to list
function addMessageItem(data) {
    const id = data.car_number + '_' + Date.now(); // unique id
    messageCache[id] = data;

    const item = document.createElement('div');
    item.className = 'list-item';
    item.id = id;
    item.innerText = `${data.car_number} - ₹${data.total_charge}`;

    item.onclick = () => {
        // Remove active class from other items
        document.querySelectorAll('.list-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');
        renderDetail(data);
    }

    messageListEl.prepend(item); // newest on top
}

// Clear button
document.getElementById('clear-btn').onclick = () => {
    messageListEl.innerHTML = '';
    Object.keys(messageCache).forEach(k => delete messageCache[k]);
    renderDetail({car_number: '--', distance: '--', charge_per_km_cars: '--', total_charge: '--'});
    qrSrc = "";
}

// WebSocket message
chatSocket.onmessage = function (e) {
    const eventData = JSON.parse(e.data);
    const data = JSON.parse(eventData.message);
    addMessageItem(data);
}

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};