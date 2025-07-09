// flask-server/static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const productGrid = document.getElementById('product-grid');
    const loadingMessage = document.getElementById('loading-message');
    const errorMessage = document.getElementById('error-message');
    const noShoesMessage = document.getElementById('no-shoes-message');

    // Function to hide all messages
    const hideAllMessages = () => {
        loadingMessage.style.display = 'none';
        errorMessage.style.display = 'none';
        noShoesMessage.style.display = 'none';
    };

    // Function to display error message
    const displayError = (message) => {
        hideAllMessages();
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    };

    // Function to display no shoes message
    const displayNoShoes = () => {
        hideAllMessages();
        noShoesMessage.style.display = 'block';
    };

    // Function to create a product card element
    const createProductCard = (shoe) => {
        const card = document.createElement('div');
        // Added 'border border-gray-200' for a subtle border
        card.className = 'bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 overflow-hidden border border-gray-200';

        card.innerHTML = `
            <div class="h-48 flex items-center justify-center bg-gray-50 p-2">
                <img src="${shoe.s3link}" alt="${shoe.name}" class="max-w-full max-h-full object-contain rounded-t-xl"
                     onerror="this.onerror=null;this.src='https://placehold.co/400x300/e0e0e0/555555?text=No+Image';">
            </div>
            <div class="p-6">
                <h3 class="text-xl font-semibold text-gray-900 mb-2">${shoe.name}</h3>
                <p class="text-gray-600 text-sm mb-4">Size: <span class="font-medium">${shoe.size}</span></p>
                <button class="view-details-btn bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition-colors duration-300 w-full focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 font-bold">
                    View Details
                </button>
            </div>
        `;

        // Add event listener to the "View Details" button
        const viewDetailsButton = card.querySelector('.view-details-btn');
        viewDetailsButton.addEventListener('click', (event) => {
            const shoeId = event.target.dataset.shoeId;
            const shoeName = event.target.dataset.shoeName;
            console.log(`View Details clicked for Shoe ID: ${shoeId}, Name: ${shoeName}`);
            // In a real e-commerce site, you would navigate to a product details page
            // window.location.href = `/product/${shoeId}`;
            alert(`You clicked "View Details" for ${shoeName}! (ID: ${shoeId})`);
        });

        return card;
    };

    // Function to fetch and display shoes
    const fetchShoes = async () => {
        hideAllMessages(); // Hide any initial messages
        loadingMessage.style.display = 'block'; // Show loading message

        try {
            // Fetch data from the Flask API endpoint
            const response = await fetch('/api/shoes');

            if (!response.ok) {
                // If the response is not OK (e.g., 404, 500), throw an error
                const errorData = await response.json();
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            }

            const shoes = await response.json();

            hideAllMessages(); // Hide loading message after successful fetch

            if (shoes.length === 0) {
                displayNoShoes();
                return;
            }

            // Clear existing product cards
            productGrid.innerHTML = '';

            // Populate the grid with fetched data
            shoes.forEach(shoe => {
                const card = createProductCard(shoe);
                productGrid.appendChild(card);
            });
        } catch (error) {
            console.error('Error fetching shoes:', error);
            displayError(`Failed to load shoe data: ${error.message}. Please check the backend server and network connection.`);
        }
    };

    // Call the fetch function when the DOM is fully loaded
    fetchShoes();
});
