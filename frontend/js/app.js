/* Mozi Jegyfoglaló frontend JavaScript */

// API alap URL
const API_BASE_URL = "http://localhost:8000/api";

// Globális állapot
let currentUser = null;
let allMovies = [];
let currentScreenings = [];
let selectedMovie = null;
let selectedScreening = null;
let selectedSeats = [];
let userBookings = [];

// Inicializálás oldal betöltésekor
document.addEventListener("DOMContentLoaded", () => {
    checkAuthStatus();
    loadMovies();
    setupMobileMenu();
    
    // Modal bezárása, ha a felhasználó a sötét háttérre kattint
    window.addEventListener("click", function(event) {
        const modal = document.getElementById("videoModal");
        if (event.target === modal) {
            closeVideoModal();
        }
    });
});

// ===== HITELLESÍTÉSI FUNKCIÓK =====

function showLogin() {
    hideAllPages();
    document.getElementById("loginPage").classList.add("active");
    hideMobileMenu();
}

function showRegister() {
    hideAllPages();
    document.getElementById("registerPage").classList.add("active");
    hideMobileMenu();
}

function showHome() {
    hideAllPages();
    document.getElementById("homePage").classList.add("active");
    loadMovies();
    hideMobileMenu();
}

function showBookings() {
    if (!currentUser) {
        showLogin();
        return;
    }
    hideAllPages();
    document.getElementById("bookingsPage").classList.add("active");
    loadUserBookings();
    hideMobileMenu();
}

function hideAllPages() {
    const pages = document.querySelectorAll(".page");
    pages.forEach(page => page.classList.remove("active"));
    window.scrollTo(0, 0);
}

function setupMobileMenu() {
    const mobileBtn = document.getElementById("mobileMenuBtn");
    const navMenu = document.getElementById("navbarMenu");
    
    if (mobileBtn && navMenu) {
        mobileBtn.addEventListener("click", () => {
            navMenu.classList.toggle("mobile-active");
        });
    }
}

function hideMobileMenu() {
    const navMenu = document.getElementById("navbarMenu");
    if (navMenu && navMenu.classList.contains("mobile-active")) {
        navMenu.classList.remove("mobile-active");
    }
}

async function checkAuthStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
            method: "GET",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-Session-ID": localStorage.getItem("session_id") || ""
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
    const navBookings = document.getElementById("navBookings");
    
    // Üdvözlő szöveg létrehozása, ha még nincs
    let userGreeting = document.getElementById("userGreeting");
    if (!userGreeting) {
        userGreeting = document.createElement("span");
        userGreeting.id = "userGreeting";
        userGreeting.style.color = "var(--light-text)";
        userGreeting.style.marginRight = "15px";
        userGreeting.style.fontWeight = "bold";
        // Beszúrjuk a Kijelentkezés gomb elé
        logoutBtn.parentNode.insertBefore(userGreeting, logoutBtn);
    }

    if (currentUser) {
        loginBtn.style.display = "none";
        logoutBtn.style.display = "block";
        userGreeting.style.display = "inline";
        userGreeting.textContent = `Üdv, ${currentUser.full_name}!`;
        if (navBookings) navBookings.classList.remove("hidden");
    } else {
        loginBtn.style.display = "block";
        logoutBtn.style.display = "none";
        userGreeting.style.display = "none";
        if (navBookings) navBookings.classList.add("hidden");
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
            if (data.session_id) {
                localStorage.setItem("session_id", data.session_id);
            }
            currentUser = data.user;
            updateNavBar();
            errorDiv.textContent = "";
            document.getElementById("loginForm").reset();
            showHome();
        } else {
            const error = await response.json();
            if (Array.isArray(error.detail)) {
                errorDiv.textContent = "Kérlek add meg az e-mailt és a jelszót is!";
            } else {
                errorDiv.textContent = error.detail || "Bejelentkezés sikertelen.";
            }
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
            const data = await response.json();
            if (data.session_id) {
                localStorage.setItem("session_id", data.session_id);
            }
            errorDiv.style.color = "var(--success-color, #4CAF50)";
            errorDiv.textContent = "Sikeres regisztráció! Automatikus bejelentkezés...";
            setTimeout(() => {
                errorDiv.textContent = "";
                errorDiv.style.color = ""; // Visszaállítjuk az eredeti piros színt
                document.getElementById("registerForm").reset();
                currentUser = data.user;
                updateNavBar();
                showHome();
            }, 2000);
        } else {
            const error = await response.json();
            // Ha a FastAPI validációs hibát dob, az egy tömb lesz
            if (Array.isArray(error.detail)) {
                let errMsg = "Hibás adatok: ";
                if (error.detail.some(e => e.loc.includes("password"))) {
                    errMsg += "A jelszónak legalább 8 karakternek kell lennie! ";
                }
                if (error.detail.some(e => e.loc.includes("email"))) {
                    errMsg += "Érvénytelen email formátum! ";
                }
                errorDiv.textContent = errMsg || "Tölts ki minden mezőt helyesen!";
            } else {
                errorDiv.textContent = error.detail || "Regisztráció sikertelen.";
            }
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
                "Content-Type": "application/json",
                "X-Session-ID": localStorage.getItem("session_id") || ""
            }
        });

        localStorage.removeItem("session_id");
        currentUser = null;
        updateNavBar();
        showHome();
    } catch (error) {
        console.error("Logout error:", error);
    }
}

// ===== FILMEK ÉS VETÍTÉSEK FUNKCIÓK =====

async function loadMovies() {
    try {
        const response = await fetch(`${API_BASE_URL}/movies?limit=100`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            const data = await response.json();
            allMovies = data.data.movies;
            populateGenreFilter(allMovies);
            displayMovies(allMovies);
        }
    } catch (error) {
        console.error("Load movies error:", error);
        const container = document.getElementById("moviesContainer");
        if (container) {
            container.innerHTML = '<p class="error-message" style="text-align: center; padding: 2rem;">Hálózati hiba: Nem lehet betölteni a filmeket.<br>Ellenőrizd, hogy elindítottad-e a Python backendet!</p>';
        }
    }
}

function displayMovies(movies) {
    const container = document.getElementById("moviesContainer");

    if (!container) {
        console.error("Hiba: 'moviesContainer' nem található a HTML-ben. Valószínűleg nem frissítetted az index.html-t!");
        return;
    }

    if (movies.length === 0) {
        container.innerHTML = '<p class="empty-state">Nincsenek elérhető filmek.</p>';
        return;
    }

    container.innerHTML = movies.map(movie => `
        <div class="movie-card" onclick="showMovieDetail(${movie.id})">
            <img src="${movie.poster_url || 'https://placehold.co/300x450/1a1f3a/d4a574?text=Nincs+K%C3%A9p'}" 
                 alt="${movie.title}" class="movie-poster">
            <div class="movie-info">
                <h3 class="movie-title">${movie.title}</h3>
                <p class="movie-genre">${movie.genre || 'Nincs kategória'}</p>
                <p class="movie-duration">${movie.duration_minutes} perc</p>
            </div>
        </div>
    `).join("");
}

function populateGenreFilter(movies) {
    const genreFilter = document.getElementById("genreFilter");
    if (!genreFilter || genreFilter.tagName !== "SELECT") return;

    const currentValue = genreFilter.value;
    
    // Kinyerjük az egyedi műfajokat a betöltött filmekből, majd ábécé sorrendbe tesszük
    const genres = [...new Set(movies.map(m => m.genre).filter(Boolean))].sort();

    let optionsHTML = '<option value="">Minden műfaj</option>';
    genres.forEach(genre => {
        optionsHTML += `<option value="${genre.toLowerCase()}">${genre}</option>`;
    });

    genreFilter.innerHTML = optionsHTML;

    // Visszaállítjuk a korábbi kiválasztást (ha létezett és még érvényes)
    if (currentValue && genres.some(g => g.toLowerCase() === currentValue)) {
        genreFilter.value = currentValue;
    }
}

function filterMovies() {
    const genreFilter = document.getElementById("genreFilter");
    const searchInput = document.getElementById("searchInput");
    
    const genreValue = genreFilter ? genreFilter.value.toLowerCase() : "";
    const searchValue = searchInput ? searchInput.value.toLowerCase() : "";
    
    const filteredMovies = allMovies.filter(movie => {
        const matchesGenre = genreValue === "" || (movie.genre || "").toLowerCase() === genreValue;
        const matchesTitle = searchValue === "" || movie.title.toLowerCase().includes(searchValue);
        return matchesGenre && matchesTitle;
    });
    
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
            currentScreenings = screeningsData.data.screenings;
            displayMovieDetail(selectedMovie, currentScreenings);

            hideAllPages();
            document.getElementById("movieDetailPage").classList.add("active");
        }
    } catch (error) {
        console.error("Load movie detail error:", error);
        alert("Hálózati hiba: Nem sikerült betölteni a film adatait. Győződj meg róla, hogy a backend API (localhost:8000) fut!");
    }
}

function displayMovieDetail(movie, screenings) {
    const content = document.getElementById("movieDetailContent");

    const posterImg = movie.poster_url || 'https://placehold.co/300x450/1a1f3a/d4a574?text=Nincs+K%C3%A9p';
    
    // Hivatalos YouTube trailer linkek a magyar címekhez kötve
    const trailerLinks = {
        "A sötét lovag": "https://www.youtube.com/watch?v=EXeTwQWrcwY",
        "Schindler listája": "https://www.youtube.com/watch?v=gG22XNhtnoY",
        "A Gyűrűk Ura: A Gyűrű Szövetsége": "https://www.youtube.com/watch?v=V75dMMIW2B4",
        "Harcosok klubja": "https://www.youtube.com/watch?v=SUXWAEX2jlg",
        "Star Wars: V. rész - A Birodalom visszavág": "https://www.youtube.com/watch?v=JNwNXF9Y6kY",
        "Száll a kakukk fészkére": "https://www.youtube.com/watch?v=OXrcDonY-B8",
        "Az élet csodaszép": "https://www.youtube.com/watch?v=iLR3gZrU2Xo",
        "Ryan közlegény megmentése": "https://www.youtube.com/watch?v=9CiW_DgxCnQ",
        "Halálsoron": "https://www.youtube.com/watch?v=Ki4haFrqSrw",
        "Vissza a jövőbe": "https://www.youtube.com/watch?v=qvsgGtivCgs",
        "A zongorista": "https://www.youtube.com/watch?v=BFwGqLa_oAo",
        "Az oroszlánkirály": "https://www.youtube.com/watch?v=lFzVJEksoDY",
        "A tégla": "https://www.youtube.com/watch?v=iojhqm0JTW4",
        "Whiplash": "https://www.youtube.com/watch?v=7d_jQycdQGo",
        "Harakiri": "https://www.youtube.com/watch?v=gmP3FHXF2iQ",
        "Volt egyszer egy Vadnyugat": "https://www.youtube.com/watch?v=c8CJ6L0I6W8",
        "Nagyvárosi fények": "https://www.youtube.com/watch?v=7vl7F8S4cpQ",
        "Memento": "https://www.youtube.com/watch?v=0vS0E9bBSL0",
        "WALL·E": "https://www.youtube.com/watch?v=CZ1CATNbXg0",
        "A dicsőség ösvényei": "https://www.youtube.com/watch?v=nmDA60CvjR8",
        "A vád tanúja": "https://www.youtube.com/watch?v=P8iPMo66M3c",
        "Amerikai szépség": "https://www.youtube.com/watch?v=Ly7rq5EsTC8",
        "A sötét lovag - Felemelkedés": "https://www.youtube.com/watch?v=g8evyE9TuYk",
        "Amadeus": "https://www.youtube.com/watch?v=r7kWQj9FCGY",
        "A rettenthetetlen": "https://www.youtube.com/watch?v=1NJO0jxBtMo",
        "A vadon hercegnője": "https://www.youtube.com/watch?v=4OiMOHRDs14",
        "Volt egyszer egy Amerika": "https://www.youtube.com/watch?v=LCPGahgcgHU",
        "Ének az esőben": "https://www.youtube.com/watch?v=5_EVHeNEIJY",
        "Star Wars: VI. rész - A Jedi visszatér": "https://www.youtube.com/watch?v=7L8p7_SLzvU",
        "Kutyaszorítóban": "https://www.youtube.com/watch?v=vayksn4Y93A",
        "Jöjj és lásd!": "https://www.youtube.com/watch?v=UHaSQU-4wss",
        "Észak-Északnyugat": "https://www.youtube.com/watch?v=ek7T9Gyl_J4",
        "Blöff": "https://www.youtube.com/watch?v=9Jar2XkBboo"
    };
    
    const trailerUrl = trailerLinks[movie.title] || `https://duckduckgo.com/?q=${encodeURIComponent('!ducky ' + movie.title + ' trailer youtube')}`;

    if (screenings.length === 0) {
        content.innerHTML = `
            <div class="movie-detail" style="background-image: linear-gradient(to bottom, rgba(11, 37, 58, 0.93), rgba(4, 20, 33, 0.98)), url('${posterImg}'); background-size: cover; background-position: center;">
                <button class="btn-back" onclick="showHome()">← Vissza</button>
                <div class="movie-detail-header">
                    <img src="${posterImg}" 
                         alt="${movie.title}" class="movie-detail-poster">
                    <div class="movie-detail-info">
                        <h2>${movie.title}</h2>
                        <p><strong>Műfaj:</strong> ${movie.genre || "Nem megadva"}</p>
                        <p><strong>Hossz:</strong> ${movie.duration_minutes} perc</p>
                        <p><strong>Leírás:</strong> ${movie.description || "Nincs leírás"}</p>
                        
                        <div style="margin-top: 1.5rem;">
                            ${trailerLinks[movie.title] ? `
                                <button onclick="openVideoModal('${trailerUrl}')" class="btn btn-trailer">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
                                    Hivatalos Trailer
                                </button>
                            ` : `
                                <a href="${trailerUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-trailer">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
                                    Trailer Keresése
                                </a>
                            `}
                        </div>
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
        <div class="movie-detail" style="background-image: linear-gradient(to bottom, rgba(11, 37, 58, 0.93), rgba(4, 20, 33, 0.98)), url('${posterImg}'); background-size: cover; background-position: center;">
            <button class="btn-back" onclick="showHome()">← Vissza</button>
            <div class="movie-detail-header">
                <img src="${posterImg}" 
                     alt="${movie.title}" class="movie-detail-poster">
                <div class="movie-detail-info">
                    <h2>${movie.title}</h2>
                    <p><strong>Műfaj:</strong> ${movie.genre || "Nem megadva"}</p>
                    <p><strong>Hossz:</strong> ${movie.duration_minutes} perc</p>
                    <p><strong>Leírás:</strong> ${movie.description || "Nincs leírás"}</p>
                    
                    <div style="margin-top: 1.5rem;">
                        ${trailerLinks[movie.title] ? `
                            <button onclick="openVideoModal('${trailerUrl}')" class="btn btn-trailer">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
                                Hivatalos Trailer
                            </button>
                        ` : `
                            <a href="${trailerUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-trailer">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
                                Trailer Keresése
                            </a>
                        `}
                    </div>
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

function openVideoModal(url) {
    const modal = document.getElementById("videoModal");
    const player = document.getElementById("youtubePlayer");
    const externalLink = document.getElementById("youtubeExternalLink");
    
    // Konvertáljuk a normál YouTube linket embed linkké
    const embedUrl = url.replace("youtube.com/watch?v=", "youtube-nocookie.com/embed/") + "?autoplay=1";
    player.src = embedUrl;
    
    if (externalLink) {
        externalLink.href = url;
    }
    
    modal.classList.add("active");
}

function closeVideoModal() {
    const modal = document.getElementById("videoModal");
    const player = document.getElementById("youtubePlayer");
    
    modal.classList.remove("active");
    player.src = ""; // Ez leállítja a videót a háttérben
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

async function showBookingForm(screeningId) {
    if (!currentUser) {
        showLogin();
        return;
    }

    selectedScreening = screeningId;
    selectedSeats = [];

    const screening = currentScreenings.find(s => s.id === screeningId);

    if (!screening) {
        alert("Vetítés nem található.");
        return;
    }
    
    // Lekérjük a ténylegesen foglalt székeket a backendről!
    let actuallyBookedSeats = [];
    try {
        const response = await fetch(`${API_BASE_URL}/bookings/screening/${screeningId}`);
        if (response.ok) {
            const data = await response.json();
            actuallyBookedSeats = data.data.booked_seats || [];
        }
    } catch (err) {
        console.error("Nem sikerült lekérni a foglalt székeket:", err);
    }

    // Modal létrehozása vagy az UI frissítése a szék kiválasztásához
    const seatGrid = createSeatGrid(screening.total_seats, actuallyBookedSeats, screening.price_per_ticket);

    const bookingForm = `
        <div class="booking-form">
            <h3>Szék kiválasztása</h3>
            ${seatGrid}
            <div class="booking-actions">
                <button class="btn btn-primary" id="confirmBookingBtn" onclick="confirmBooking()" disabled>
                    Foglalás megerősítése (0 Ft)
                </button>
                <button class="btn btn-secondary" onclick="showMovieDetail(${selectedMovie.id})">
                    Mégsem
                </button>
            </div>
        </div>
    `;

    const detailContent = document.getElementById("movieDetailContent");
    detailContent.innerHTML = detailContent.innerHTML + bookingForm;
}

function createSeatGrid(totalSeats, bookedSeatsArray, pricePerTicket) {
    let seatNumbers = [];
    for (let index = 1; index <= totalSeats; index++) {
        seatNumbers.push(index);
    }

    return `
        <div class="seat-map">
            <div class="screen">Vászon</div>
            <div class="seat-grid">
                ${seatNumbers.map(seatNumber => {
                    const isBooked = bookedSeatsArray.includes(seatNumber);
                    const row = Math.ceil(seatNumber / 10);
                    const seatInRow = (seatNumber - 1) % 10 + 1;
                    
                    let html = `
                    <button class="seat ${isBooked ? 'seat-booked' : ''}" 
                            onclick="${isBooked ? '' : `selectSeat(${seatNumber}, ${pricePerTicket})`}" 
                            id="seat-${seatNumber}"
                        ${isBooked ? 'disabled' : ''}
                        title="${row}. sor ${seatInRow}. szék${isBooked ? ' (Foglalt)' : ' (Szabad)'}">
                        ${seatNumber}
                    </button>
                    `;
                    
                    if (seatInRow === 5) {
                        html += `<div class="corridor"></div>`;
                    }
                    return html;
                }).join("")}
            </div>
        </div>
        <div class="booking-summary">
            <p>Kiválasztott székek: <strong id="selectedSeatDisplay">Nincs</strong></p>
            <p>Jegyár: <strong>${pricePerTicket} Ft / db</strong></p>
            <p class="booking-total">
                Fizetendő összesen: <strong id="totalPriceDisplay">0</strong> Ft
            </p>
        </div>
    `;
}

function selectSeat(seatNumber, pricePerTicket) {
    const seatElement = document.getElementById(`seat-${seatNumber}`);
    const index = selectedSeats.indexOf(seatNumber);
    
    // Ha már ki volt választva, akkor levesszük a listáról
    if (index > -1) {
        selectedSeats.splice(index, 1);
        seatElement.classList.remove("seat-selected");
    } else {
        // Különben hozzáadjuk a tömbhöz
        selectedSeats.push(seatNumber);
        seatElement.classList.add("seat-selected");
    }

    const displayElement = document.getElementById("selectedSeatDisplay");
    const totalElement = document.getElementById("totalPriceDisplay");
    const confirmBtn = document.getElementById("confirmBookingBtn");

    if (selectedSeats.length > 0) {
        // Székek listájának megjelenítése sorbarendezve
        selectedSeats.sort((a, b) => a - b);
        
        const formattedSeats = selectedSeats.map(sn => {
            const r = Math.ceil(sn / 10);
            const s = (sn - 1) % 10 + 1;
            return `${r}. sor ${s}. szék`;
        });
        displayElement.textContent = formattedSeats.join(", ");
        
        // Teljes ár kiszámítása
        const totalPrice = selectedSeats.length * pricePerTicket;
        totalElement.textContent = totalPrice;
        
        // Gomb engedélyezése és szöveg frissítése
        confirmBtn.textContent = `Foglalás megerősítése (${totalPrice} Ft)`;
        confirmBtn.disabled = false;
    } else {
        // Ha nincs egy szék sem kiválasztva
        displayElement.textContent = "Nincs";
        totalElement.textContent = "0";
        confirmBtn.textContent = "Foglalás megerősítése (0 Ft)";
        confirmBtn.disabled = true;
    }
}

async function confirmBooking() {
    if (selectedSeats.length === 0 || !selectedScreening || !currentUser) {
        alert("Kérlek válassz legalább egy széket!");
        return;
    }

    try {
        let successfulBookings = [];
        let failedBookings = [];

        // API request minden kiválasztott székre
        for (const seatNumber of selectedSeats) {
            const response = await fetch(`${API_BASE_URL}/bookings`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                    "X-Session-ID": localStorage.getItem("session_id") || ""
                },
                body: JSON.stringify({
                    screening_id: selectedScreening,
                    seat_number: seatNumber
                })
            });

            if (response.ok) {
                const data = await response.json();
                const r = Math.ceil(seatNumber / 10);
                const s = (seatNumber - 1) % 10 + 1;
                successfulBookings.push(`- ${r}. sor ${s}. szék (Kód: ${data.data.id})`);
            } else {
                const error = await response.json();
                failedBookings.push(`${seatNumber}. szék: ${error.detail || "Ismeretlen hiba"}`);
            }
        }

        if (successfulBookings.length > 0) {
            alert("Sikeres foglalás!\n\nA következő helyeket foglaltad le:\n" + successfulBookings.join("\n"));
        }
        if (failedBookings.length > 0) {
            alert("Néhány foglalás sikertelen volt:\n" + failedBookings.join("\n"));
        }

        selectedSeats = [];
            selectedScreening = null;
            showHome();
    } catch (error) {
        alert("Hálózati hiba. Próbálkozz később!");
        console.error("Booking error:", error);
    }
}

// ===== FELHASZNÁLÓI FOGLALÁSOK FUNKCIÓI =====

async function loadUserBookings() {
    try {
        const response = await fetch(`${API_BASE_URL}/bookings`, {
            method: "GET",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-Session-ID": localStorage.getItem("session_id") || ""
            }
        });

        if (response.ok) {
            const data = await response.json();
            userBookings = data.data.bookings;
            showBookingsView('active'); // Alapértelmezetten az aktívakat mutatjuk
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

function showBookingsView(status) {
    // Gombok stílusának frissítése (aktív/inaktív állapot)
    const btnActive = document.getElementById("btnFilterActive");
    const btnHistory = document.getElementById("btnFilterHistory");
    
    if (btnActive && btnHistory) {
        btnActive.className = status === 'active' ? "btn btn-primary" : "btn btn-secondary";
        btnHistory.className = status === 'cancelled' ? "btn btn-primary" : "btn btn-secondary";
    }
    
    // Foglalások szűrése a kért státusz alapján
    const filteredBookings = userBookings.filter(b => b.status === status);
    displayUserBookings(filteredBookings, status);
}

function displayUserBookings(bookings, status = 'active') {
    const container = document.getElementById("bookingsContent");

    if (bookings.length === 0) {
        if (status === 'active') {
            container.innerHTML = '<p class="empty-state">Nincsenek aktív foglalásaid. <a href="#" onclick="showHome()">Foglalj most!</a></p>';
        } else {
            container.innerHTML = '<p class="empty-state">Nincsenek korábbi/lemondott foglalásaid.</p>';
        }
        return;
    }

    container.innerHTML = `
        <div class="booking-list">
            ${bookings.map(booking => `
                <div class="booking-card" style="background-image: linear-gradient(to right, rgba(11, 37, 58, 0.95) 30%, rgba(4, 20, 33, 0.7) 100%), url('${booking.poster_url || 'https://placehold.co/300x150/1a1f3a/d4a574?text=Nincs+K%C3%A9p'}'); background-size: cover; background-position: center right;">
                    <div class="booking-details">
                        <h3>${booking.movie_title}</h3>
                        <p class="booking-info">
                            <strong>Vetítés:</strong> ${formatDateTime(booking.screening_datetime)}
                        </p>
                        <p class="booking-info">
                            <strong>Szék:</strong> ${Math.ceil(booking.seat_number / 10)}. sor ${((booking.seat_number - 1) % 10) + 1}. szék
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
                "Content-Type": "application/json",
                "X-Session-ID": localStorage.getItem("session_id") || ""
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
