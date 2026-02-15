document.getElementById("searchForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const query = document.getElementById("query").value;

    fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(cars => {
            const carsResutlsElement = document.getElementById("results")
            if(!carsResutlsElement)
                return;

            if (cars.lenght === 0) {
                carsResutlsElement.innerHTML = "<p>No cars found.</p>";
                return;
            }

            carsResutlsElement.innerHTML = "";

            cars.forEach(car => {
                const carElement = document.createElement("div");
                carElement.className = "car-item";
                carElement.innerHTML = `
                    <img src="/static/assets/${car.img}" alt="${car.name}" style="width:300px; vertical-align: middle; margin-right:10px;">
                    <div class=car-info>
                        <p> Model: <span> ${car.name} </span> </p>
                        <p> Company name: <span> ${car.brand} </span> </p>
                        <p> Production year: <span> ${car.year} </span> </p>
                        <p> Price: <span> $${car.price} </span> </p>
                    </div>
                `;
                carsResutlsElement.className = "cars-list";
                carsResutlsElement.appendChild(carElement);
            });
        })
        .catch(error => console.error("Error:", error));
});

document.getElementById("carForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const MAX_SIZE_MB = 1;
    const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;

    const fileInput = document.getElementById("imgInput");
    const file = fileInput.files[0];
    
    if (file) {
        if (file.size > MAX_SIZE_BYTES) {
            alert("File is to0o large. Maximum size is 1MB.");
            return;
        }
    } else if (!file) {
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
            alert(response?.message);
            this.reset();
        })
        .catch(error => {
            alert("Error: something went wrong.");
            console.error(error);
        });
});
