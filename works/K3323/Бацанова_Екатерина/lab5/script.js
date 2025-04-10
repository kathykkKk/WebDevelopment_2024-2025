document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("video-container").style.display = "none";
    document.getElementById("hidden-text").style.display = "none";
});

function playVideo(event, x1, y1, x2, y2) {
    event.preventDefault();

    const videoContainer = document.getElementById("video-container");
    const whiteCover = document.getElementById("white-cover");
    const video = document.getElementById("overlay-video");
    const image = document.getElementById("main-image");

    const scaleX = image.clientWidth / image.naturalWidth;
    const scaleY = image.clientHeight / image.naturalHeight;

    const width = (x2 - x1) * scaleX;
    const height = (y2 - y1) * scaleY;
    const left = x1 * scaleX;
    const top = y1 * scaleY;

    videoContainer.style.width = `${width}px`;
    videoContainer.style.height = `${height}px`;
    videoContainer.style.top = `${top}px`;
    videoContainer.style.left = `${left}px`;
    videoContainer.style.display = "block";

    whiteCover.style.width = `${width}px`;
    whiteCover.style.height = `${height}px`;
    whiteCover.style.position = "absolute";
    whiteCover.style.top = "0";
    whiteCover.style.left = "0";
    whiteCover.style.background = "white";
    whiteCover.style.opacity = "1";

    video.style.width = `${width * 3}px`;
    video.style.height = `${height * 3}px`;
    video.style.position = "absolute";
    video.style.top = "50%";
    video.style.left = "50%";
    video.style.transform = "translate(-50%, -50%)";
    video.style.zIndex = "11";

    video.play();

    video.onended = function () {
        videoContainer.style.display = "none";
    };
}


let isMusicPlaying = false;
let audio = new Audio('data/meowmeow.mp3');

function toggleMusic(event) {
    if (event) event.preventDefault();
    if (isMusicPlaying) {
        audio.pause();
        audio.currentTime = 0;
    } else {
        audio.play();
    }
    isMusicPlaying = !isMusicPlaying;
}

function setReminder(event) {
    event.preventDefault();

    alert("Не забудьте о важном событии! :)");
    setTimeout(function() {
        alert("Прошло 5 секунд! Напоминаем еще раз.");
    }, 5000);
}

function toggleText(event, x1, y1, x2, y2) {
    event.preventDefault();
    const textElement = document.getElementById("hidden-text");
    const image = document.getElementById("main-image");

    const scaleX = image.clientWidth / image.naturalWidth;
    const scaleY = image.clientHeight / image.naturalHeight;

    const width = (x2 - x1) * scaleX;
    const height = (y2 - y1) * scaleY;
    const left = (x1 + 70) * scaleX;
    const top = (y1 + 80) * scaleY;

    textElement.style.width = `${width}px`;
    textElement.style.height = `${height / 5}px`;
    textElement.style.top = `${top}px`;
    textElement.style.left = `${left}px`;

    if (textElement.style.display === "none") {
        textElement.style.display = "block";
    } else {
        textElement.style.display = "none";
    }
}

function guessNumber() {
    const number = Math.floor(Math.random() * 10) + 1;
    const guess = prompt("Угадайте число от 1 до 10:");

    if (guess === null) {
        return;
    }

    if (parseInt(guess) === number) {
        alert("Правильно!");
    } else {
        alert(`Неверно, правильный ответ: ${number}`);
    }
}

let ball;
let ballX, ballY;
let mouseX, mouseY;
let speed = 1;
let ballSpeedX = 0;
let ballSpeedY = 0;
let interval;
let isBallMoving = false;
let isGameActive = false;

function loadGameState() {
    if (localStorage.getItem("ballX")) {
        ballX = parseFloat(localStorage.getItem("ballX"));
        ballY = parseFloat(localStorage.getItem("ballY"));
        speed = parseFloat(localStorage.getItem("speed"));
        ballSpeedX = parseFloat(localStorage.getItem("ballSpeedX"));
        ballSpeedY = parseFloat(localStorage.getItem("ballSpeedY"));
        isBallMoving = true;
    } else {
        resetBall();
    }
}

function saveGameState() {
    localStorage.setItem("ballX", ballX);
    localStorage.setItem("ballY", ballY);
    localStorage.setItem("speed", speed);
    localStorage.setItem("ballSpeedX", ballSpeedX);
    localStorage.setItem("ballSpeedY", ballSpeedY);
}

function resetBall() {
    ballX = 0;
    ballY = 0;
    speed = 1;
    ballSpeedX = 0;
    ballSpeedY = 0;
}

setInterval(() => {
    if (isBallMoving) {
        speed += 1.5;
        saveGameState();
    }
}, 1000);

document.addEventListener("mousemove", function(event) {
    mouseX = event.pageX;
    mouseY = event.pageY;
});

function moveBall() {
    let deltaX = mouseX - ballX;
    let deltaY = mouseY - ballY;
    let distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

    if (distance > 1) {
        ballSpeedX = deltaX / distance * speed;
        ballSpeedY = deltaY / distance * speed;

        ballX += ballSpeedX;
        ballY += ballSpeedY;

        ball.style.position = "absolute";
        ball.style.left = ballX - 25 + "px";
        ball.style.top = ballY - 25 + "px";
        ball.style.width = "50px";
        ball.style.height = "50px";
        ball.style.backgroundColor = "#00FF00";
        ball.style.border = "3px solid black";
        ball.style.borderRadius = "50%";
    }

    if (Math.abs(mouseX - ballX) < 25 && Math.abs(mouseY - ballY) < 25) {
        ball.remove();
        alert("Вы проиграли!");
        clearInterval(interval);
        isBallMoving = false;
        localStorage.removeItem("ballX");
        localStorage.removeItem("ballY");
        localStorage.removeItem("speed");
        localStorage.removeItem("ballSpeedX");
        localStorage.removeItem("ballSpeedY");
        isGameActive = false;
    }
}

function startBallMovement() {
    if (isGameActive) {
        return;
    }
    
    isGameActive = true;
    resetBall();
    ball = document.createElement("div");
    document.body.appendChild(ball);

    alert("Убеги от шарика!");

    isBallMoving = true;
    interval = setInterval(moveBall, 10);
}

document.querySelector('area[alt="Рандом"]').addEventListener('click', startBallMovement);
window.onload = loadGameState;

function updateMapLink(latitude, longitude) {
    const mapLink = document.querySelector('#map-area');
    const url = `https://yandex.ru/maps/?ll=${longitude},${latitude}&z=17`;
    mapLink.href = url;
}

document.querySelector('#map-area').addEventListener('click', function(event) {
    event.preventDefault();

    navigator.geolocation.getCurrentPosition(function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        updateMapLink(latitude, longitude);
        window.open(document.querySelector('#map-area').href, '_blank');
    })
});