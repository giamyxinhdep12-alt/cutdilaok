import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Anime Clash 1v1",
    page_icon="⚡",
    layout="wide"
)

GAME_HTML = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: #10131b;
    font-family: Arial, sans-serif;
}

#game {
    position: relative;
    width: 100%;
    max-width: 1150px;
    height: 700px;
    margin: auto;
    overflow: hidden;
    background:
        radial-gradient(circle at 50% 25%, #394b70 0%, #20283b 38%, #111620 100%);
    border-radius: 14px;
}

canvas {
    display: block;
    width: 100%;
    height: 100%;
}

#hud {
    position: absolute;
    left: 20px;
    right: 20px;
    top: 15px;
    z-index: 10;
    pointer-events: none;
}

.hud-row {
    display: flex;
    align-items: center;
    gap: 14px;
}

.player-box {
    flex: 1;
    color: white;
}

.player-name {
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 5px;
}

.bar {
    width: 100%;
    height: 22px;
    background: rgba(0,0,0,0.55);
    border: 2px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    overflow: hidden;
}

.hp {
    height: 100%;
    width: 100%;
    background: #4ddd78;
    transition: width 0.12s;
}

.energy {
    height: 100%;
    width: 0%;
    background: #62c7ff;
    transition: width 0.12s;
}

.mana-bar {
    height: 10px;
    margin-top: 5px;
}

#p2hp {
    background: #ff6378;
}

#p2energy {
    background: #b56cff;
}

#timer {
    width: 80px;
    text-align: center;
    color: white;
    font-size: 32px;
    font-weight: bold;
    text-shadow: 0 3px 10px #000;
}

#controls {
    position: absolute;
    bottom: 12px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 12;
    color: rgba(255,255,255,0.82);
    background: rgba(5,8,15,0.72);
    border-radius: 12px;
    padding: 8px 15px;
    font-size: 13px;
    text-align: center;
}

#message {
    position: absolute;
    inset: 0;
    z-index: 50;
    display: none;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: rgba(5,7,12,0.72);
    color: white;
}

.message-box {
    padding: 30px;
}

.message-box h1 {
    font-size: 58px;
    margin: 0 0 10px;
    text-shadow: 0 4px 20px #000;
}

.message-box p {
    font-size: 20px;
}

button {
    border: 0;
    border-radius: 10px;
    padding: 13px 28px;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
    background: #f5c84c;
    color: #111;
}

#start {
    position: absolute;
    inset: 0;
    z-index: 60;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
    background: rgba(6,9,16,0.94);
}

.start-box h1 {
    font-size: 64px;
    margin: 0;
    letter-spacing: 3px;
    color: #f5c84c;
}

.start-box p {
    color: #d5d9e2;
    font-size: 18px;
}

#countdown {
    position: absolute;
    inset: 0;
    z-index: 40;
    display: none;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 110px;
    font-weight: bold;
    text-shadow: 0 5px 30px #000;
    pointer-events: none;
}

.tip {
    opacity: 0.7;
    font-size: 13px;
}
</style>
</head>

<body>

<div id="game">

    <canvas id="canvas"></canvas>

    <div id="hud">
        <div class="hud-row">

            <div class="player-box">
                <div class="player-name">⚡ PLAYER 1</div>

                <div class="bar">
                    <div id="p1hp" class="hp"></div>
                </div>

                <div class="bar mana-bar">
                    <div id="p1energy" class="energy"></div>
                </div>
            </div>

            <div id="timer">60</div>

            <div class="player-box">
                <div class="player-name" style="text-align:right">
                    PLAYER 2 ⚡
                </div>

                <div class="bar">
                    <div id="p2hp" class="hp"></div>
                </div>

                <div class="bar mana-bar">
                    <div id="p2energy" class="energy"></div>
                </div>
            </div>

        </div>
    </div>

    <div id="countdown">3</div>

    <div id="controls">
        P1: <b>A/D</b> di chuyển • <b>W</b> nhảy •
        <b>F</b> đánh • <b>G</b> skill • <b>H</b> ulti
        &nbsp;&nbsp;|&nbsp;&nbsp;
        P2: <b>←/→</b> di chuyển • <b>↑</b> nhảy •
        <b>K</b> đánh • <b>L</b> skill • <b>;</b> ulti
    </div>

    <div id="start">
        <div class="start-box">
            <h1>ANIME CLASH</h1>
            <p>⚡ 1v1 ARENA ⚡</p>
            <p>Đấu đối kháng 2 người trên cùng bàn phím.</p>

            <button id="startButton">
                ▶ BẮT ĐẦU TRẬN
            </button>

            <p class="tip">
                Không cần ảnh hay file ngoài.
            </p>
        </div>
    </div>

    <div id="message">
        <div class="message-box">
            <h1 id="winner"></h1>
            <p id="resultText"></p>
            <button id="again">CHƠI LẠI</button>
        </div>
    </div>

</div>

<script>
(function () {

"use strict";

var game = document.getElementById("game");
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

var p1hp = document.getElementById("p1hp");
var p2hp = document.getElementById("p2hp");
var p1energy = document.getElementById("p1energy");
var p2energy = document.getElementById("p2energy");
var timerElement = document.getElementById("timer");

var startScreen = document.getElementById("start");
var startButton = document.getElementById("startButton");

var message = document.getElementById("message");
var winner = document.getElementById("winner");
var resultText = document.getElementById("resultText");
var againButton = document.getElementById("again");

var countdown = document.getElementById("countdown");

var W = 1150;
var H = 700;

var keys = {};
var particles = [];
var effects = [];

var running = false;
var ended = false;

var p1;
var p2;

var projectiles = [];

var timeLeft = 60;
var lastTime = 0;

function resize() {

    var rect = game.getBoundingClientRect();

    W = Math.max(700, rect.width);
    H = Math.max(500, rect.height);

    canvas.width = W;
    canvas.height = H;
}

window.addEventListener("resize", resize);

function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
}

function distance(a, b) {
    return Math.hypot(
        a.x - b.x,
        a.y - b.y
    );
}

function createFighter(x, color, facing) {

    return {
        x: x,
        y: H - 145,

        vx: 0,
        vy: 0,

        width: 44,
        height: 82,

        hp: 100,
        energy: 0,

        color: color,

        facing: facing,

        grounded: true,

        attackTimer: 0,
        skillTimer: 0,
        ultimateTimer: 0,

        attackCooldown: 0,
        skillCooldown: 0,
        ultimateCooldown: 0,

        attackFlash: 0,
        hitFlash: 0,

        combo: 0,
        comboTimer: 0
    };
}

function resetGame() {

    resize();

    p1 = createFighter(
        W * 0.28,
        "#45a8ff",
        1
    );

    p2 = createFighter(
        W * 0.72,
        "#d96cff",
        -1
    );

    projectiles = [];
    particles = [];
    effects = [];

    timeLeft = 60;
    running = false;
    ended = false;

    message.style.display = "none";

    startCountdown();
}

function startCountdown() {

    var numbers = ["3", "2", "1", "FIGHT!"];
    var index = 0;

    countdown.style.display = "flex";

    function next() {

        countdown.textContent = numbers[index];

        index++;

        if (index >= numbers.length) {

            setTimeout(function () {

                countdown.style.display = "none";
                running = true;

            }, 650);

            return;
        }

        setTimeout(next, 700);
    }

    next();
}

function moveFighter(f, leftKey, rightKey, jumpKey, dt) {

    if (keys[leftKey]) {
        f.vx = -270;
        f.facing = -1;
    }
    else if (keys[rightKey]) {
        f.vx = 270;
        f.facing = 1;
    }
    else {
        f.vx *= 0.78;
    }

    if (keys[jumpKey] && f.grounded) {

        f.vy = -520;
        f.grounded = false;
    }

    f.vy += 1250 * dt;

    f.x += f.vx * dt;
    f.y += f.vy * dt;

    var floor = H - 145;

    if (f.y >= floor) {

        f.y = floor;
        f.vy = 0;
        f.grounded = true;
    }

    f.x = clamp(
        f.x,
        35,
        W - 35
    );

    f.attackCooldown =
        Math.max(0, f.attackCooldown - dt);

    f.skillCooldown =
        Math.max(0, f.skillCooldown - dt);

    f.ultimateCooldown =
        Math.max(0, f.ultimateCooldown - dt);

    f.attackTimer =
        Math.max(0, f.attackTimer - dt);

    f.skillTimer =
        Math.max(0, f.skillTimer - dt);

    f.ultimateTimer =
        Math.max(0, f.ultimateTimer - dt);

    f.attackFlash =
        Math.max(0, f.attackFlash - dt);

    f.hitFlash =
        Math.max(0, f.hitFlash - dt);

    f.comboTimer =
        Math.max(0, f.comboTimer - dt);

    if (f.comboTimer <= 0) {
        f.combo = 0;
    }
}

function normalAttack(attacker, defender) {

    if (attacker.attackCooldown > 0) {
        return;
    }

    attacker.attackCooldown = 0.32;
    attacker.attackTimer = 0.15;
    attacker.attackFlash = 0.15;

    var reach = 82;

    var dx = defender.x - attacker.x;

    var facingCorrect =
        (attacker.facing === 1 && dx > 0) ||
        (attacker.facing === -1 && dx < 0);

    if (
        Math.abs(dx) < reach &&
        Math.abs(defender.y - attacker.y) < 70 &&
        facingCorrect
    ) {

        defender.hp -= 7;
        defender.hitFlash = 0.18;

        attacker.energy =
            Math.min(100, attacker.energy + 7);

        attacker.combo++;
        attacker.comboTimer = 0.8;

        createHitEffect(
            defender.x,
            defender.y - 30,
            "#ffffff"
        );
    }
}

function skill(attacker, defender) {

    if (attacker.skillCooldown > 0) {
        return;
    }

    if (attacker.energy < 25) {
        return;
    }

    attacker.energy -= 25;
    attacker.skillCooldown = 1.1;
    attacker.skillTimer = 0.35;

    projectiles.push({
        x: attacker.x + attacker.facing * 35,
        y: attacker.y - 35,

        vx: attacker.facing * 650,
        vy: 0,

        radius: 15,

        damage: 15,

        color: attacker.color,

        owner: attacker
    });
}

function ultimate(attacker, defender) {

    if (attacker.ultimateCooldown > 0) {
        return;
    }

    if (attacker.energy < 100) {
        return;
    }

    attacker.energy = 0;
    attacker.ultimateCooldown = 4;
    attacker.ultimateTimer = 0.65;

    var dx = defender.x - attacker.x;

    var correctDirection =
        (attacker.facing === 1 && dx > 0) ||
        (attacker.facing === -1 && dx < 0);

    if (
        Math.abs(dx) < 280 &&
        correctDirection
    ) {

        defender.hp -= 32;
        defender.hitFlash = 0.35;

        createBigEffect(
            defender.x,
            defender.y - 40,
            attacker.color
        );

    } else {

        createBigEffect(
            attacker.x + attacker.facing * 130,
            attacker.y - 35,
            attacker.color
        );
    }
}

function createHitEffect(x, y, color) {

    effects.push({
        x: x,
        y: y,
        radius: 15,
        maxRadius: 55,
        life: 0.25,
        maxLife: 0.25,
        color: color
    });

    for (var i = 0; i < 7; i++) {

        particles.push({
            x: x,
            y: y,

            vx: (Math.random() - 0.5) * 260,
            vy: (Math.random() - 0.5) * 260,

            life: 0.35,
            color: color
        });
    }
}

function createBigEffect(x, y, color) {

    effects.push({
        x: x,
        y: y,
        radius: 20,
        maxRadius: 150,
        life: 0.55,
        maxLife: 0.55,
        color: color
    });

    for (var i = 0; i < 25; i++) {

        particles.push({
            x: x,
            y: y,

            vx: (Math.random() - 0.5) * 500,
            vy: (Math.random() - 0.5) * 500,

            life: 0.7,
            color: color
        });
    }
}

function updateProjectiles(dt) {

    for (var i = projectiles.length - 1; i >= 0; i--) {

        var p = projectiles[i];

        p.x += p.vx * dt;
        p.y += p.vy * dt;

        var target =
            p.owner === p1 ? p2 : p1;

        if (
            Math.abs(p.x - target.x) <
                target.width / 2 + p.radius &&
            Math.abs(p.y - (target.y - 35)) <
                target.height / 2
        ) {

            target.hp -= p.damage;
            target.hitFlash = 0.2;

            p.owner.energy =
                Math.min(
                    100,
                    p.owner.energy + 8
                );

            createHitEffect(
                target.x,
                target.y - 35,
                p.color
            );

            projectiles.splice(i, 1);
            continue;
        }

        if (
            p.x < -50 ||
            p.x > W + 50
        ) {
            projectiles.splice(i, 1);
        }
    }
}

function updateParticles(dt) {

    for (var i = particles.length - 1; i >= 0; i--) {

        var p = particles[i];

        p.x += p.vx * dt;
        p.y += p.vy * dt;

        p.vy += 500 * dt;

        p.life -= dt;

        if (p.life <= 0) {
            particles.splice(i, 1);
        }
    }

    for (var j = effects.length - 1; j >= 0; j--) {

        var e = effects[j];

        e.life -= dt;

        var progress =
            1 - e.life / e.maxLife;

        e.radius =
            15 +
            (e.maxRadius - 15) *
            progress;

        if (e.life <= 0) {
            effects.splice(j, 1);
        }
    }
}

function update(dt) {

    if (!running || ended) {
        return;
    }

    timeLeft -= dt;

    if (timeLeft <= 0) {

        timeLeft = 0;

        if (p1.hp > p2.hp) {
            finish("PLAYER 1", "HP còn nhiều hơn!");
        }
        else if (p2.hp > p1.hp) {
            finish("PLAYER 2", "HP còn nhiều hơn!");
        }
        else {
            finish("HÒA!", "Hai bên có cùng HP.");
        }

        return;
    }

    moveFighter(
        p1,
        "a",
        "d",
        "w",
        dt
    );

    moveFighter(
        p2,
        "arrowleft",
        "arrowright",
        "arrowup",
        dt
    );

    updateProjectiles(dt);
    updateParticles(dt);

    if (p1.hp <= 0) {
        p1.hp = 0;
        finish("PLAYER 2", "PLAYER 1 đã hết HP!");
    }

    if (p2.hp <= 0) {
        p2.hp = 0;
        finish("PLAYER 1", "PLAYER 2 đã hết HP!");
    }
}

function drawArena() {

    var groundY = H - 95;

    // nền
    var gradient =
        ctx.createLinearGradient(
            0,
            0,
            0,
            H
        );

    gradient.addColorStop(
        0,
        "#293856"
    );

    gradient.addColorStop(
        1,
        "#111722"
    );

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, W, H);

    // ánh sáng giữa sân
    var glow =
        ctx.createRadialGradient(
            W / 2,
            H * 0.5,
            20,
            W / 2,
            H * 0.5,
            400
        );

    glow.addColorStop(
        0,
        "rgba(110,160,255,0.16)"
    );

    glow.addColorStop(
        1,
        "rgba(0,0,0,0)"
    );

    ctx.fillStyle = glow;
    ctx.fillRect(0, 0, W, H);

    // sàn
    ctx.fillStyle = "#171d28";
    ctx.fillRect(
        0,
        groundY,
        W,
        H - groundY
    );

    ctx.strokeStyle =
        "rgba(255,255,255,0.12)";

    ctx.lineWidth = 2;

    for (
        var x = -H;
        x < W + H;
        x += 70
    ) {

        ctx.beginPath();

        ctx.moveTo(
            W / 2 + (x - W / 2) * 0.25,
            groundY
        );

        ctx.lineTo(
            x,
            H
        );

        ctx.stroke();
    }

    // đường giữa
    ctx.strokeStyle =
        "rgba(245,200,76,0.35)";

    ctx.beginPath();
    ctx.moveTo(W / 2, groundY - 8);
    ctx.lineTo(W / 2, H);
    ctx.stroke();
}

function drawFighter(f, label) {

    ctx.save();

    ctx.translate(
        f.x,
        f.y
    );

    // bóng
    ctx.fillStyle =
        "rgba(0,0,0,0.35)";

    ctx.beginPath();

    ctx.ellipse(
        0,
        44,
        32,
        9,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // aura khi ulti đầy
    if (f.energy >= 100) {

        ctx.strokeStyle =
            f.color;

        ctx.globalAlpha =
            0.35 + Math.sin(Date.now() / 120) * 0.12;

        ctx.lineWidth = 5;

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            55,
            0,
            Math.PI * 2
        );

        ctx.stroke();

        ctx.globalAlpha = 1;
    }

    // thân
    ctx.fillStyle =
        f.hitFlash > 0
        ? "#ffffff"
        : f.color;

    ctx.beginPath();

    ctx.roundRect(
        -22,
        -32,
        44,
        65,
        12
    );

    ctx.fill();

    // đầu
    ctx.fillStyle = "#ffd1b3";

    ctx.beginPath();

    ctx.arc(
        0,
        -48,
        20,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // tóc
    ctx.fillStyle = "#20242e";

    ctx.beginPath();

    ctx.arc(
        0,
        -57,
        21,
        Math.PI,
        Math.PI * 2
    );

    ctx.fill();

    // mắt
    ctx.fillStyle = "#111";

    ctx.beginPath();

    ctx.arc(
        f.facing * 8,
        -49,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // tay
    ctx.strokeStyle = "#ffd1b3";
    ctx.lineWidth = 9;
    ctx.lineCap = "round";

    ctx.beginPath();

    ctx.moveTo(
        f.facing * 17,
        -18
    );

    ctx.lineTo(
        f.facing * (
            f.attackTimer > 0
            ? 45
            : 25
        ),
        -18
    );

    ctx.stroke();

    // tên
    ctx.fillStyle = "white";
    ctx.font = "bold 13px Arial";
    ctx.textAlign = "center";

    ctx.fillText(
        label,
        0,
        55
    );

    ctx.restore();
}

function drawProjectiles() {

    for (var i = 0; i < projectiles.length; i++) {

        var p = projectiles[i];

        ctx.save();

        ctx.shadowBlur = 18;
        ctx.shadowColor = p.color;

        ctx.fillStyle = p.color;

        ctx.beginPath();

        ctx.arc(
            p.x,
            p.y,
            p.radius,
            0,
            Math.PI * 2
        );

        ctx.fill();

        ctx.restore();
    }
}

function drawEffects() {

    for (var i = 0; i < effects.length; i++) {

        var e = effects[i];

        ctx.save();

        ctx.globalAlpha =
            Math.max(
                0,
                e.life / e.maxLife
            );

        ctx.strokeStyle = e.color;
        ctx.lineWidth = 8;

        ctx.beginPath();

        ctx.arc(
            e.x,
            e.y,
            e.radius,
            0,
            Math.PI * 2
        );

        ctx.stroke();

        ctx.restore();
    }

    for (var j = 0; j < particles.length; j++) {

        var p = particles[j];

        ctx.globalAlpha =
            Math.max(0, p.life / 0.7);

        ctx.fillStyle = p.color;

        ctx.beginPath();

        ctx.arc(
            p.x,
            p.y,
            4,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }

    ctx.globalAlpha = 1;
}

function draw() {

    drawArena();

    drawEffects();
    drawProjectiles();

    drawFighter(
        p1,
        "P1"
    );

    drawFighter(
        p2,
        "P2"
    );
}

function updateHUD() {

    p1hp.style.width =
        clamp(p1.hp, 0, 100) + "%";

    p2hp.style.width =
        clamp(p2.hp, 0, 100) + "%";

    p1energy.style.width =
        clamp(p1.energy, 0, 100) + "%";

    p2energy.style.width =
        clamp(p2.energy, 0, 100) + "%";

    timerElement.textContent =
        Math.ceil(timeLeft);
}

function finish(who, reason) {

    if (ended) {
        return;
    }

    ended = true;
    running = false;

    winner.textContent =
        who === "HÒA!"
        ? "⚡ HÒA TRẬN ⚡"
        : "🏆 " + who + " THẮNG!";

    resultText.textContent = reason;

    message.style.display = "flex";
}

function loop(timestamp) {

    var dt =
        lastTime
        ? (timestamp - lastTime) / 1000
        : 0;

    lastTime = timestamp;

    dt = Math.min(dt, 0.033);

    update(dt);
    updateHUD();
    draw();

    requestAnimationFrame(loop);
}

document.addEventListener(
    "keydown",
    function (e) {

        var key = e.key.toLowerCase();

        keys[key] = true;

        if (
            key === "f" &&
            running
        ) {
            normalAttack(p1, p2);
        }

        if (
            key === "g" &&
            running
        ) {
            skill(p1, p2);
        }

        if (
            key === "h" &&
            running
        ) {
            ultimate(p1, p2);
        }

        if (
            key === "k" &&
            running
        ) {
            normalAttack(p2, p1);
        }

        if (
            key === "l" &&
            running
        ) {
            skill(p2, p1);
        }

        if (
            key === ";" &&
            running
        ) {
            ultimate(p2, p1);
        }

        if (
            key === " " ||
            key.indexOf("arrow") === 0
        ) {
            e.preventDefault();
        }
    }
);

document.addEventListener(
    "keyup",
    function (e) {

        keys[e.key.toLowerCase()] = false;
    }
);

startButton.addEventListener(
    "click",
    function () {
        resetGame();
    }
);

againButton.addEventListener(
    "click",
    function () {
        resetGame();
    }
);

resize();

requestAnimationFrame(loop);

})();
</script>

</body>
</html>
"""

components.html(
    GAME_HTML,
    height=710,
    scrolling=False
)
