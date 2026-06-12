const searchForm = document.getElementById("searchForm");
const queryInput = document.getElementById("query");
const sortSelect = document.getElementById("sortSelect");
const carsResultsElement = document.getElementById("results");
const initialTable = document.getElementById("initialTable");

function getSortUrl(query, sort) {
    let url = "/search?";
    const params = new URLSearchParams();
    if (query) params.append("query", query);
    if (sort) params.append("sort", sort);
    return url + params.toString();
}

function renderCars(cars) {
    if (!carsResultsElement) return;

    if (cars.length === 0) {
        carsResultsElement.innerHTML = "<p>No cars found.</p>";
        return;
    }

    let html = `
        <table class="car-table">
            <thead>
                <tr>
                    <th>Photo</th>
                    <th>Model</th>
                    <th>Brand</th>
                    <th>Year</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
    `;

    cars.forEach(car => {
        html += `
            <tr>
                <td><img class="table-car-image" src="/static/uploads/${car.img}" alt="${car.model}"></td>
                <td>${car.model}</td>
                <td>${car.brandName}</td>
                <td>${car.productionYear}</td>
                <td>$${car.price}</td>
            </tr>
        `;
    });

    html += `</tbody></table>`;
    carsResultsElement.innerHTML = html;
}

function searchCars() {
    const query = queryInput.value.trim();
    const sort = sortSelect.value;
    const url = getSortUrl(query, sort);

    fetch(url)
        .then(response => response.json())
        .then(cars => {
            renderCars(cars);
            if (initialTable) initialTable.style.display = "none";
        })
        .catch(error => console.error("Error:", error));
}

if (searchForm) {
    searchForm.addEventListener("submit", function (e) {
        e.preventDefault();
        searchCars();
    });
}

if (sortSelect) {
    sortSelect.addEventListener("change", function () {
        searchCars();
    });
}

const carForm = document.getElementById("carForm");
if (carForm) {
    carForm.addEventListener("submit", function (e) {
        e.preventDefault();

    const MAX_SIZE_MB = 1;
    const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;

    const fileInput = document.getElementById("imgInput");
    const file = fileInput.files[0];
    
    if (file) {
        if (file.size > MAX_SIZE_BYTES) {
            alert("File is too large. Maximum size is 1MB.");
            return;
        }
    } else {
        alert("Please select an image.");
        return;
    }

    const formData = new FormData(this);

    fetch("/add", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(response => {
            localStorage.setItem("carAdded", response?.message);
            window.location.href = "/";
        })
        .catch(error => {
            alert("Error: something went wrong.");
            console.error(error);
        });
    });
}
