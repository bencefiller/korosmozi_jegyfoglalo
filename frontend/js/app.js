/* Cinema Booking System Frontend JavaScript */

// API Base URL
const API_BASE_URL = "http://localhost:8000/api";

// Global State
let currentUser = null;
let allMovies = [];
let selectedMovie = null;
let selectedScreening = null;
let selectedSeat = null;

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
    checkAuthStatus();
    loadMovies();
});

// ===== AUTHENTICATION FUNCTIONS =====

function showLogin() {
    hideAllPages();
    document.getElementById("loginPage").classList.add("active");
}

function showRegister() {
    hideAllPages();
    document.getElementById("registerPage").classList.add("active");
}

function showHome() {
    hideAllPages();
    document.getElementById("homePage").classList.add("active");
    loadMovies();
}

function showBookings() {
    if (!currentUser) {
        showLogin();
        return;
    }
    hideAllPages();
    document.getElementById("bookingsPage").classList.add("active");
    loadUserBookings();
}

function hideAllPages() {
    const pages = document.querySelectorAll(".page");
    pages.forEach(page => page.classList.remove("active"));
}

async function checkAuthStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
            method: "GET",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            const data = await response.json();
            currentUser = data.user;
            updateNavBar();
        } else {
            currentUser = null;
            updateNavBar();
        }
    } catch (error) {
        console.error("Auth check error:", error);
        currentUser = null;
        updateNavBar();
    }
}

function updateNavBar() {
    const loginBtn = document.getElementById("loginBtn");
    const logoutBtn = document.getElementById("logoutBtn");

    if (currentUser) {
        loginBtn.style.display = "none";
        logoutBtn.style.display = "block";
    } else {
        loginBtn.style.display = "block";
        logoutBtn.style.display = "none";
    }
}

async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    const errorDiv = document.getElementById("loginError");

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            currentUser = data.user;
            updateNavBar();
            errorDiv.textContent = "";
            document.getElementById("loginForm").reset();
            showHome();
        } else {
            const error = await response.json();
            errorDiv.textContent = error.detail || "Bejelentkezés sikertelen.";
        }
    } catch (error) {
        errorDiv.textContent = "Hálózati hiba. Próbálkozz később!";
        console.error("Login error:", error);
    }
}

async function handleRegister(event) {
    event.preventDefault();

    const fullName = document.getElementById("registerName").value;
    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;
    const errorDiv = document.getElementById("registerError");

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password, full_name: fullName })
        });

        if (response.ok) {
            errorDiv.textContent = "";
            document.getElementById("registerForm").reset();
            showLogin();
        } else {
            const error = await response.json();
            errorDiv.textContent = error.detail || "Regisztráció sikertelen.";
        }
    } catch (error) {
        errorDiv.textContent = "Hálózati hiba. Próbálkozz később!";
        console.error("Register error:", error);
    }
}

async function logout() {
    try {
        await fetch(`${API_BASE_URL}/auth/logout`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            }
        });

        currentUser = null;
        updateNavBar();
        showHome();
    } catch (error) {
        console.error("Logout error:", error);
    }
}

// ===== MOVIES & SCREENINGS FUNCTIONS =====

async function loadMovies() {
    try {
        const response = await fetch(`${API_BASE_URL}/movies`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            const data = await response.json();
            allMovies = data.data.movies;
            displayMovies(allMovies);
        }
    } catch (error) {
        console.error("Load movies error:", error);
        document.getElementById("moviesContainer").innerHTML =
            '<p class="error-message">Nem lehet betölteni a filmeket. Próbálkozz később!</p>';
    }
}

function displayMovies(movies) {
    const container = document.getElementById("moviesContainer");

    if (movies.length === 0) {
        container.innerHTML = '<p class="empty-state">Nincsenek elérhető filmek.</p>';
        return;
    }

    container.innerHTML = movies.map(movie => `
        <div class="movie-card" onclick="showMovieDetail(${movie.id})">
            <img src="${movie.poster_url || 'https://via.placeholder.com/300x450?text=No+Image'}" 
                 alt="${movie.title}" class="movie-poster">
            <div class="movie-info">
                <h3 class="movie-title">${movie.title}</h3>
                <p class="movie-genre">${movie.genre || 'Nincs kategória'}</p>
                <p class="movie-duration">${movie.duration_minutes} perc</p>
            </div>
        </div>
    `).join("");
}

function filterMovies() {
    const filterValue = document.getElementById("genreFilter").value.toLowerCase();
    const filteredMovies = allMovies.filter(movie =>
        (movie.genre || "").toLowerCase().includes(filterValue) ||
        movie.title.toLowerCase().includes(filterValue)
    );
    displayMovies(filteredMovies);
}

async function showMovieDetail(movieId) {
    try {
        const movieResponse = await fetch(`${API_BASE_URL}/movies/${movieId}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        const screeningsResponse = await fetch(`${API_BASE_URL}/screenings?movie_id=${movieId}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (movieResponse.ok && screeningsResponse.ok) {
            const movieData = await movieResponse.json();
            const screeningsData = await screeningsResponse.json();

            selectedMovie = movieData.data;
            displayMovieDetail(selectedMovie, screeningsData.data.screenings);

            hideAllPages();
            document.getElementById("movieDetailPage").classList.add("active");
        }
    } catch (error) {
        console.error("Load movie detail error:", error);
    }
}

function displayMovieDetail(movie, screenings) {
    const content = document.getElementById("movieDetailContent");

    if (screenings.length === 0) {
        content.innerHTML = `
            <div class="movie-detail">
                <button class="btn-back" onclick="showHome()">← Vissza</button>
                <div class="movie-detail-header">
                    <img src="${movie.poster_url || 'https://via.placeholder.com/300x450?text=No+Image'}" 
                         alt="${movie.title}" class="movie-detail-poster">
                    <div class="movie-detail-info">
                        <h2>${movie.title}</h2>
                        <p><strong>Műfaj:</strong> ${movie.genre || "Nem megadva"}</p>
                        <p><strong>Hossz:</strong> ${movie.duration_minutes} perc</p>
                        <p><strong>Leírás:</strong> ${movie.description || "Nincs leírás"}</p>
                    </div>
                </div>
                <div class="empty-state" style="margin-top: 2rem;">
                    <h3>Jelenleg nincsenek elérhető vetítések.</h3>
                </div>
            </div>
        `;
        return;
    }

    content.innerHTML = `
        <div class="movie-detail">
            <button class="btn-back" onclick="showHome()">← Vissza</button>
            <div class="movie-detail-header">
                <img src="${movie.poster_url || 'https://via.placeholder.com/300x450?text=No+Image'}" 
                     alt="${movie.title}" class="movie-detail-poster">
                <div class="movie-detail-info">
                    <h2>${movie.title}</h2>
                    <p><strong>Műfaj:</strong> ${movie.genre || "Nem megadva"}</p>
                    <p><strong>Hossz:</strong> ${movie.duration_minutes} perc</p>
                    <p><strong>Leírás:</strong> ${movie.description || "Nincs leírás"}</p>
                </div>
            </div>
            <div class="screenings-section">
                <h3>Elérhető vetítések:</h3>
                <div class="screening-list">
                    ${screenings.map(screening => `
                        <div class="screening-item">
                            <div class="screening-info">
                                <div class="screening-time">${formatDateTime(screening.screening_datetime)}</div>
                                <div class="screening-price">${screening.price_per_ticket} Ft</div>
                                <div class="screening-seats">Szabad helyek: ${screening.available_seats}/${screening.total_seats}</div>
                            </div>
                            <button class="btn btn-primary" 
                                    onclick="showBookingForm(${screening.id})"
                                    ${screening.available_seats === 0 ? "disabled" : ""}>
                                ${screening.available_seats === 0 ? "Nincs szabad hely" : "Foglalás"}
                            </button>
                        </div>
                    `).join("")}
                </div>
            </div>
        </div>
    `;
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString("hu-HU", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit"
    });
}

function showBookingForm(screeningId) {
    if (!currentUser) {
        showLogin();
        return;
    }

    selectedScreening = screeningId;
    selectedSeat = null;

    const screening = allMovies
        .flatMap(m => m.screenings || [])
        .find(s => s.id === screeningId);

    if (!screening) {
        alert("Vetítés nem található.");
        return;
    }

    // Create modal or update UI for seat selection
    const seatGrid = createSeatGrid(screening.total_seats, screening.available_seats);

    const bookingForm = `
        <div class="booking-form" style="margin-top: 2rem;">
            <h3>Szék kiválasztása</h3>
            ${seatGrid}
            <div style="margin-top: 1.5rem; text-align: center;">
                <button class="btn btn-primary" onclick="confirmBooking()" ${selectedSeat ? "" : "disabled"}>
                    Foglalás megerősítése
                </button>
                <button class="btn btn-secondary" onclick="showMovieDetail(${selectedMovie.id})" style="margin-left: 0.5rem;">
                    Mégsem
                </button>
            </div>
        </div>
    `;

    const detailContent = document.getElementById("movieDetailContent");
    detailContent.innerHTML = detailContent.innerHTML + bookingForm;
}

function createSeatGrid(totalSeats, availableSeats) {
    let seatNumbers = [];
    for (let index = 1; index <= totalSeats; index++) {
        seatNumbers.push(index);
    }

    return `
        <div class="seat-grid">
            ${seatNumbers.map(seatNumber => `
                <button class="seat" 
                        onclick="selectSeat(${seatNumber})" 
                        id="seat-${seatNumber}">
                    ${seatNumber}
                </button>
            `).join("")}
        </div>
        <p style="text-align: center; margin-top: 1rem;">
            Kiválasztott szék: <strong id="selectedSeatDisplay">Nincs</strong>
        </p>
    `;
}

function selectSeat(seatNumber) {
    // Clear previous selection
    if (selectedSeat) {
        const prevSeat = document.getElementById(`seat-${selectedSeat}`);
        if (prevSeat) {
            prevSeat.classList.remove("seat-selected");
        }
    }

    selectedSeat = seatNumber;
    const seatElement = document.getElementById(`seat-${seatNumber}`);
    if (seatElement) {
        seatElement.classList.add("seat-selected");
    }

    const displayElement = document.getElementById("selectedSeatDisplay");
    if (displayElement) {
        displayElement.textContent = seatNumber;
    }
}

async function confirmBooking() {
    if (!selectedSeat || !selectedScreening || !currentUser) {
        alert("Kérlek válassz széket!");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/bookings`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                screening_id: selectedScreening,
                seat_number: selectedSeat
            })
        });

        if (response.ok) {
            const data = await response.json();
            alert("Foglalás sikeres! Kódzám: " + data.data.id);
            selectedSeat = null;
            selectedScreening = null;
            showHome();
        } else {
            const error = await response.json();
            alert("Foglalás sikertelen: " + (error.detail || "Ismeretlen hiba"));
        }
    } catch (error) {
        alert("Hálózati hiba. Próbálkozz később!");
        console.error("Booking error:", error);
    }
}

// ===== USER BOOKINGS FUNCTIONS =====

async function loadUserBookings() {
    try {
        const response = await fetch(`${API_BASE_URL}/bookings`, {
            method: "GET",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            const data = await response.json();
            displayUserBookings(data.data.bookings);
        } else {
            document.getElementById("bookingsContent").innerHTML =
                '<p class="error-message">Nem lehet betölteni a foglalásokat.</p>';
        }
    } catch (error) {
        console.error("Load bookings error:", error);
        document.getElementById("bookingsContent").innerHTML =
            '<p class="error-message">Hálózati hiba. Próbálkozz később!</p>';
    }
}

function displayUserBookings(bookings) {
    const container = document.getElementById("bookingsContent");

    if (bookings.length === 0) {
        container.innerHTML = '<p class="empty-state">Nincsenek foglalásaid. <a href="#" onclick="showHome()">Foglalj most!</a></p>';
        return;
    }

    container.innerHTML = `
        <div class="booking-list">
            ${bookings.map(booking => `
                <div class="booking-card">
                    <div class="booking-details">
                        <h3>${booking.movie_title}</h3>
                        <p class="booking-info">
                            <strong>Vetítés:</strong> ${formatDateTime(booking.screening_datetime)}
                        </p>
                        <p class="booking-info">
                            <strong>Szék:</strong> ${booking.seat_number}
                        </p>
                        <p class="booking-info">
                            <strong>Ár:</strong> ${booking.price} Ft
                        </p>
                        <span class="booking-status status-${booking.status}">
                            ${booking.status === "active" ? "Aktív" : "Lemondva"}
                        </span>
                    </div>
                    ${booking.status === "active" ? `
                        <button class="btn btn-danger" onclick="cancelBooking(${booking.id})">
                            Foglalás lemondása
                        </button>
                    ` : ""}
                </div>
            `).join("")}
        </div>
    `;
}

async function cancelBooking(bookingId) {
    if (!confirm("Biztosan lemondod ezt a foglalást?")) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/bookings/${bookingId}`, {
            method: "DELETE",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            alert("Foglalás sikeresen lemondva!");
            loadUserBookings();
        } else {
            const error = await response.json();
            alert("Lemondás sikertelen: " + (error.detail || "Ismeretlen hiba"));
        }
    } catch (error) {
        alert("Hálózati hiba. Próbálkozz később!");
        console.error("Cancel booking error:", error);
    }
}
