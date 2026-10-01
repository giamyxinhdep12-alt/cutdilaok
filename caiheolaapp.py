import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ZONE RUSH",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 ZONE RUSH")
st.caption("Mini Battle Royale 2D — WASD để di chuyển • Chuột để ngắm • Click để bắn")

game_html = r"""
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
    background: #10141c;
    font-family: Arial, sans-serif;
}

#game {
    position: relative;
    width: 100%;
    max-width: 1100px;
    height: 680px;
    margin: auto;
    background: #202a25;
    overflow: hidden;
    user-select: none;
    cursor: crosshair;
}

canvas {
    display: block;
    width: 100%;
    height: 100%;
}

#hud {
    position: absolute;
    left: 15px;
    top: 15px;
    color: white;
    z-index: 10;
    pointer-events: none;
}

.panel {
    background: rgba(10, 14, 20, 0.82);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 12px;
    padding: 10px 14px;
    margin-bottom: 8px;
    backdrop-filter: blur(5px);
}

#hpOuter {
    width: 210px;
    height: 18px;
    background: #333;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 5px;
}

#hpBar {
    height: 100%;
    width: 100%;
    background: #35d06f;
    transition: width 0.1s;
}

#armorOuter {
    width: 210px;
    height: 12px;
    background: #333;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 5px;
}

#armorBar {
    height: 100%;
    width: 0%;
    background: #42a5ff;
}

#ammo {
    font-size: 22px;
    font-weight: bold;
}

#zoneInfo {
    color: #aee7ff;
}

#message {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: white;
    z-index: 30;
    display: none;
}

#message h1 {
    font-size: 58px;
    margin: 0 0 15px;
    text-shadow: 0 4px 20px #000;
}

#message p {
    font-size: 20px;
}

#restart {
    border: 0;
    border-radius: 10px;
    padding: 12px 25px;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
    background: #f4c542;
    color: #111;
}

#help {
    position: absolute;
    right: 15px;
    top: 15px;
    z-index: 10;
    color: white;
    background: rgba(10,14,20,0.75);
    border-radius: 12px;
    padding: 10px 14px;
    text-align: right;
    font-size: 13px;
}

#crosshair {
    position: absolute;
    width: 18px;
    height: 18px;
    border: 2px solid white;
    border-radius: 50%;
    pointer-events: none;
    z-index: 20;
    transform: translate(-50%, -50%);
}

#crosshair::after,
#crosshair::before {
    content: "";
    position: absolute;
    background: white;
}

#crosshair::after {
    width: 26px;
    height: 2px;
    left: -6px;
    top: 6px;
}

#crosshair::before {
    height: 26px;
    width: 2px;
    left: 6px;
    top: -6px;
}

#startScreen {
    position: absolute;
    inset: 0;
    background: rgba(5,8,12,0.93);
    z-index: 50;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.startBox h1 {
    font-size: 64px;
    margin: 0;
    color: #f4c542;
    letter-spacing: 4px;
}

.startBox p {
    font-size: 18px;
    color: #ccd3dc;
}

#startButton {
    margin-top: 15px;
    padding: 15px 40px;
    border: 0;
    border-radius: 12px;
    background: #f4c542;
    color: #111;
    font-size: 20px;
    font-weight: bold;
    cursor: pointer;
}

.small {
    opacity: 0.75;
    font-size: 13px;
}
</style>
</head>

<body>

<div id="game">

    <canvas id="canvas"></canvas>

    <div id="hud">

        <div class="panel">
            ❤️ HP
            <div id="hpOuter">
                <div id="hpBar"></div>
            </div>

            🛡️ Giáp
            <div id="armorOuter">
                <div id="armorBar"></div>
            </div>
        </div>

        <div class="panel">
            🔫 Đạn:
            <span id="ammo">30 / 120</span>
        </div>

        <div class="panel">
            👥 Còn lại:
            <span id="alive">11</span>
        </div>

        <div class="panel" id="zoneInfo">
            ⭕ Bo: <span id="zoneText">Ổn định</span>
        </div>

    </div>

    <div id="help">
        <b>W A S D</b> — Di chuyển<br>
        <b>Chuột</b> — Ngắm<br>
        <b>Click</b> — Bắn<br>
        <b>R</b> — Nạp đạn
    </div>

    <div id="crosshair"></div>

    <div id="message">
        <h1 id="messageTitle"></h1>
        <p id="messageText"></p>
        <button id="restart">CHƠI LẠI</button>
    </div>

    <div id="startScreen">
        <div class="startBox">
            <h1>ZONE RUSH</h1>
            <p>Mini Battle Royale</p>
            <p>Hạ các đối thủ và sống sót đến cuối cùng.</p>

            <button id="startButton">
                ▶ BẮT ĐẦU
            </button>

            <p class="small">
                WASD • Chuột • Click • R
            </p>
        </div>
    </div>

</div>

<script>
(function () {

"use strict";

var game = document.getElementById("game");
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

var hpBar = document.getElementById("hpBar");
var armorBar = document.getElementById("armorBar");
var ammoText = document.getElementById("ammo");
var aliveText = document.getElementById("alive");
var zoneText = document.getElementById("zoneText");
var crosshair = document.getElementById("crosshair");

var startScreen = document.getElementById("startScreen");
var startButton = document.getElementById("startButton");

var message = document.getElementById("message");
var messageTitle = document.getElementById("messageTitle");
var messageText = document.getElementById("messageText");
var restartButton = document.getElementById("restart");

var W = 1100;
var H = 680;

var running = false;
var gameOver = false;

var keys = {};
var mouse = {
    x: W / 2,
    y: H / 2,
    down: false
};

var player;
var bots = [];
var bullets = [];
var loot = [];
var particles = [];

var lastTime = 0;
var shootCooldown = 0;
var reloadTimer = 0;

var zone = {
    x: W / 2,
    y: H / 2,
    radius: 285,
    targetRadius: 285,
    shrinkTimer: 18
};

function resizeCanvas() {
    var rect = game.getBoundingClientRect();

    W = Math.max(600, rect.width);
    H = Math.max(450, rect.height);

    canvas.width = W;
    canvas.height = H;

    if (player) {
        player.x = Math.max(25, Math.min(W - 25, player.x));
        player.y = Math.max(25, Math.min(H - 25, player.y));
    }
}

window.addEventListener("resize", resizeCanvas);

function random(min, max) {
    return Math.random() * (max - min) + min;
}

function distance(a, b) {
    var dx = a.x - b.x;
    var dy = a.y - b.y;
    return Math.sqrt(dx * dx + dy * dy);
}

function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
}

function resetGame() {

    resizeCanvas();

    running = true;
    gameOver = false;

    startScreen.style.display = "none";
    message.style.display = "none";

    bullets = [];
    bots = [];
    loot = [];
    particles = [];

    shootCooldown = 0;
    reloadTimer = 0;

    player = {
        x: W / 2,
        y: H / 2,
        radius: 15,
        speed: 230,
        hp: 100,
        armor: 50,
        ammo: 30,
        reserve: 120,
        kills: 0,
        angle: 0
    };

    zone = {
        x: W / 2,
        y: H / 2,
        radius: Math.min(W, H) * 0.43,
        targetRadius: Math.min(W, H) * 0.43,
        shrinkTimer: 18
    };

    for (var i = 0; i < 10; i++) {

        var bx;
        var by;

        do {
            bx = random(45, W - 45);
            by = random(45, H - 45);
        } while (
            Math.hypot(bx - player.x, by - player.y) < 180
        );

        bots.push({
            x: bx,
            y: by,
            radius: 14,
            hp: 100,
            speed: random(45, 80),
            angle: random(0, Math.PI * 2),
            changeTimer: random(0.5, 2),
            shootTimer: random(0.7, 2),
            alive: true
        });
    }

    for (var j = 0; j < 14; j++) {

        loot.push({
            x: random(35, W - 35),
            y: random(35, H - 35),
            type: Math.random() < 0.6 ? "ammo" : "med",
            taken: false
        });
    }

    updateHud();
}

function createParticles(x, y, amount) {

    for (var i = 0; i < amount; i++) {

        particles.push({
            x: x,
            y: y,
            vx: random(-100, 100),
            vy: random(-100, 100),
            life: random(0.2, 0.6)
        });
    }
}

function shootPlayer() {

    if (!running || gameOver) {
        return;
    }

    if (reloadTimer > 0) {
        return;
    }

    if (shootCooldown > 0) {
        return;
    }

    if (player.ammo <= 0) {
        reload();
        return;
    }

    player.ammo--;

    shootCooldown = 0.14;

    var angle = Math.atan2(
        mouse.y - player.y,
        mouse.x - player.x
    );

    bullets.push({
        x: player.x + Math.cos(angle) * 20,
        y: player.y + Math.sin(angle) * 20,
        vx: Math.cos(angle) * 650,
        vy: Math.sin(angle) * 650,
        owner: "player",
        damage: 34,
        life: 1.3
    });

    createParticles(
        player.x + Math.cos(angle) * 20,
        player.y + Math.sin(angle) * 20,
        3
    );
}

function shootBot(bot) {

    var angle = Math.atan2(
        player.y - bot.y,
        player.x - bot.x
    );

    bullets.push({
        x: bot.x + Math.cos(angle) * 18,
        y: bot.y + Math.sin(angle) * 18,
        vx: Math.cos(angle) * 370,
        vy: Math.sin(angle) * 370,
        owner: "bot",
        damage: 10,
        life: 1.7
    });
}

function reload() {

    if (reloadTimer > 0) {
        return;
    }

    if (player.ammo >= 30) {
        return;
    }

    if (player.reserve <= 0) {
        return;
    }

    reloadTimer = 1.2;
}

function finishReload() {

    var needed = 30 - player.ammo;
    var amount = Math.min(needed, player.reserve);

    player.ammo += amount;
    player.reserve -= amount;
}

function damagePlayer(amount) {

    if (player.armor > 0) {

        var absorbed = Math.min(
            player.armor,
            amount * 0.55
        );

        player.armor -= absorbed;
        amount -= absorbed;
    }

    player.hp -= amount;

    if (player.hp <= 0) {
        player.hp = 0;
        endGame(false);
    }
}

function damageBot(bot, amount) {

    bot.hp -= amount;

    if (bot.hp <= 0 && bot.alive) {

        bot.hp = 0;
        bot.alive = false;

        player.kills++;

        if (Math.random() < 0.55) {

            loot.push({
                x: bot.x,
                y: bot.y,
                type: Math.random() < 0.65 ? "ammo" : "med",
                taken: false
            });
        }

        createParticles(bot.x, bot.y, 12);

        checkWin();
    }
}

function checkWin() {

    var aliveBots = 0;

    for (var i = 0; i < bots.length; i++) {
        if (bots[i].alive) {
            aliveBots++;
        }
    }

    if (aliveBots === 0) {
        endGame(true);
    }
}

function endGame(win) {

    if (gameOver) {
        return;
    }

    gameOver = true;
    running = false;

    message.style.display = "block";

    if (win) {
        messageTitle.textContent = "🏆 BOOYAH!";
        messageText.textContent =
            "Bạn đã sống sót! Hạ " + player.kills + " đối thủ.";
    } else {
        messageTitle.textContent = "💀 GAME OVER";
        messageText.textContent =
            "Bạn đã bị loại. Hạ được " + player.kills + " đối thủ.";
    }
}

function updatePlayer(dt) {

    var dx = 0;
    var dy = 0;

    if (keys["w"] || keys["arrowup"]) {
        dy -= 1;
    }

    if (keys["s"] || keys["arrowdown"]) {
        dy += 1;
    }

    if (keys["a"] || keys["arrowleft"]) {
        dx -= 1;
    }

    if (keys["d"] || keys["arrowright"]) {
        dx += 1;
    }

    if (dx !== 0 || dy !== 0) {

        var len = Math.sqrt(dx * dx + dy * dy);

        dx /= len;
        dy /= len;

        player.x += dx * player.speed * dt;
        player.y += dy * player.speed * dt;
    }

    player.x = clamp(player.x, 20, W - 20);
    player.y = clamp(player.y, 20, H - 20);

    player.angle = Math.atan2(
        mouse.y - player.y,
        mouse.x - player.x
    );

    if (mouse.down) {
        shootPlayer();
    }

    if (shootCooldown > 0) {
        shootCooldown -= dt;
    }

    if (reloadTimer > 0) {

        reloadTimer -= dt;

        if (reloadTimer <= 0) {
            reloadTimer = 0;
            finishReload();
        }
    }
}

function updateBots(dt) {

    for (var i = 0; i < bots.length; i++) {

        var bot = bots[i];

        if (!bot.alive) {
            continue;
        }

        var dx = player.x - bot.x;
        var dy = player.y - bot.y;
        var dist = Math.sqrt(dx * dx + dy * dy);

        bot.changeTimer -= dt;

        if (bot.changeTimer <= 0) {

            bot.angle = Math.atan2(dy, dx);

            if (dist > 240) {
                bot.angle += random(-0.35, 0.35);
            } else {
                bot.angle += random(-1.5, 1.5);
            }

            bot.changeTimer = random(0.6, 1.8);
        }

        if (dist > 180) {

            bot.x += Math.cos(bot.angle) * bot.speed * dt;
            bot.y += Math.sin(bot.angle) * bot.speed * dt;

        } else {

            bot.x += Math.cos(bot.angle + Math.PI / 2)
                * bot.speed * 0.45 * dt;

            bot.y += Math.sin(bot.angle + Math.PI / 2)
                * bot.speed * 0.45 * dt;
        }

        bot.x = clamp(bot.x, 20, W - 20);
        bot.y = clamp(bot.y, 20, H - 20);

        bot.shootTimer -= dt;

        if (
            bot.shootTimer <= 0 &&
            dist < 430
        ) {

            shootBot(bot);
            bot.shootTimer = random(0.7, 1.5);
        }

        var zoneDistance = Math.hypot(
            bot.x - zone.x,
            bot.y - zone.y
        );

        if (zoneDistance > zone.radius) {
            bot.hp -= 7 * dt;
        }

        if (bot.hp <= 0) {
            bot.hp = 0;
            bot.alive = false;
            createParticles(bot.x, bot.y, 8);
            checkWin();
        }
    }
}

function updateBullets(dt) {

    for (var i = bullets.length - 1; i >= 0; i--) {

        var b = bullets[i];

        b.x += b.vx * dt;
        b.y += b.vy * dt;
        b.life -= dt;

        var remove = false;

        if (
            b.life <= 0 ||
            b.x < -30 ||
            b.x > W + 30 ||
            b.y < -30 ||
            b.y > H + 30
        ) {
            remove = true;
        }

        if (!remove && b.owner === "player") {

            for (var j = 0; j < bots.length; j++) {

                var bot = bots[j];

                if (!bot.alive) {
                    continue;
                }

                if (distance(b, bot) < bot.radius + 4) {

                    damageBot(bot, b.damage);
                    createParticles(b.x, b.y, 5);
                    remove = true;
                    break;
                }
            }
        }

        if (!remove && b.owner === "bot") {

            if (distance(b, player) < player.radius + 4) {

                damagePlayer(b.damage);
                createParticles(b.x, b.y, 3);
                remove = true;
            }
        }

        if (remove) {
            bullets.splice(i, 1);
        }
    }
}

function updateLoot() {

    for (var i = 0; i < loot.length; i++) {

        var item = loot[i];

        if (item.taken) {
            continue;
        }

        if (distance(item, player) < 28) {

            item.taken = true;

            if (item.type === "ammo") {
                player.reserve += 45;
            } else {
                player.hp = Math.min(100, player.hp + 30);
            }
        }
    }
}

function updateZone(dt) {

    zone.shrinkTimer -= dt;

    if (zone.shrinkTimer <= 0) {

        if (zone.targetRadius > 80) {
            zone.targetRadius -= 55;
        }

        zone.shrinkTimer = 16;
    }

    if (zone.radius > zone.targetRadius) {

        zone.radius -= 18 * dt;

        if (zone.radius < zone.targetRadius) {
            zone.radius = zone.targetRadius;
        }
    }

    var playerDistance = Math.hypot(
        player.x - zone.x,
        player.y - zone.y
    );

    if (playerDistance > zone.radius) {
        player.hp -= 9 * dt;

        if (player.hp <= 0) {
            player.hp = 0;
            endGame(false);
        }

        zoneText.textContent = "⚠ ĐANG NGOÀI BO!";
    } else {
        zoneText.textContent =
            "Thu nhỏ sau " +
            Math.ceil(zone.shrinkTimer) +
            "s";
    }
}

function updateParticles(dt) {

    for (var i = particles.length - 1; i >= 0; i--) {

        var p = particles[i];

        p.x += p.vx * dt;
        p.y += p.vy * dt;
        p.life -= dt;

        if (p.life <= 0) {
            particles.splice(i, 1);
        }
    }
}

function updateHud() {

    if (!player) {
        return;
    }

    hpBar.style.width =
        Math.max(0, player.hp) + "%";

    armorBar.style.width =
        Math.max(0, player.armor * 2) + "%";

    ammoText.textContent =
        player.ammo + " / " + player.reserve;

    var count = 1;

    for (var i = 0; i < bots.length; i++) {
        if (bots[i].alive) {
            count++;
        }
    }

    aliveText.textContent = count;
}

function drawBackground() {

    ctx.fillStyle = "#26352c";
    ctx.fillRect(0, 0, W, H);

    var grid = 40;

    ctx.strokeStyle = "rgba(255,255,255,0.045)";
    ctx.lineWidth = 1;

    for (var x = 0; x < W; x += grid) {

        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, H);
        ctx.stroke();
    }

    for (var y = 0; y < H; y += grid) {

        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(W, y);
        ctx.stroke();
    }

    // Một số vật cản trang trí
    ctx.fillStyle = "#39473d";

    for (var i = 0; i < 18; i++) {

        var ox = (i * 137) % W;
        var oy = (i * 83) % H;

        ctx.fillRect(
            ox,
            oy,
            32,
            22
        );
    }
}

function drawZone() {

    ctx.save();

    ctx.fillStyle = "rgba(80, 140, 255, 0.09)";
    ctx.fillRect(0, 0, W, H);

    ctx.globalCompositeOperation = "destination-out";

    ctx.beginPath();
    ctx.arc(
        zone.x,
        zone.y,
        zone.radius,
        0,
        Math.PI * 2
    );
    ctx.fill();

    ctx.globalCompositeOperation = "source-over";

    ctx.strokeStyle = "rgba(110, 190, 255, 0.9)";
    ctx.lineWidth = 5;

    ctx.beginPath();
    ctx.arc(
        zone.x,
        zone.y,
        zone.radius,
        0,
        Math.PI * 2
    );
    ctx.stroke();

    ctx.restore();
}

function drawLoot() {

    for (var i = 0; i < loot.length; i++) {

        var item = loot[i];

        if (item.taken) {
            continue;
        }

        ctx.save();

        ctx.translate(item.x, item.y);

        ctx.fillStyle =
            item.type === "ammo"
            ? "#f4c542"
            : "#54d477";

        ctx.fillRect(-9, -9, 18, 18);

        ctx.fillStyle = "#101010";
        ctx.font = "bold 12px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        ctx.fillText(
            item.type === "ammo" ? "A" : "+",
            0,
            0
        );

        ctx.restore();
    }
}

function drawBot(bot) {

    if (!bot.alive) {
        return;
    }

    var angle = Math.atan2(
        player.y - bot.y,
        player.x - bot.x
    );

    ctx.save();

    ctx.translate(bot.x, bot.y);
    ctx.rotate(angle);

    ctx.fillStyle = "#d95d5d";

    ctx.beginPath();
    ctx.arc(0, 0, bot.radius, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#252525";
    ctx.fillRect(5, -4, 14, 8);

    ctx.restore();

    // HP bot
    ctx.fillStyle = "rgba(0,0,0,0.6)";
    ctx.fillRect(
        bot.x - 18,
        bot.y - 24,
        36,
        5
    );

    ctx.fillStyle = "#55d477";
    ctx.fillRect(
        bot.x - 18,
        bot.y - 24,
        36 * (bot.hp / 100),
        5
    );
}

function drawPlayer() {

    var angle = player.angle;

    ctx.save();

    ctx.translate(player.x, player.y);
    ctx.rotate(angle);

    ctx.fillStyle = "#4aa3ff";

    ctx.beginPath();
    ctx.arc(
        0,
        0,
        player.radius,
        0,
        Math.PI * 2
    );
    ctx.fill();

    ctx.fillStyle = "#151b22";
    ctx.fillRect(7, -4, 20, 8);

    ctx.restore();
}

function drawBullets() {

    for (var i = 0; i < bullets.length; i++) {

        var b = bullets[i];

        ctx.fillStyle =
            b.owner === "player"
            ? "#ffe66d"
            : "#ff7777";

        ctx.beginPath();
        ctx.arc(
            b.x,
            b.y,
            4,
            0,
            Math.PI * 2
        );
        ctx.fill();
    }
}

function drawParticles() {

    for (var i = 0; i < particles.length; i++) {

        var p = particles[i];

        ctx.globalAlpha =
            Math.max(0, p.life / 0.6);

        ctx.fillStyle = "#f4c542";

        ctx.beginPath();
        ctx.arc(
            p.x,
            p.y,
            3,
            0,
            Math.PI * 2
        );
        ctx.fill();
    }

    ctx.globalAlpha = 1;
}

function draw() {

    drawBackground();
    drawZone();
    drawLoot();

    for (var i = 0; i < bots.length; i++) {
        drawBot(bots[i]);
    }

    drawBullets();

    if (player) {
        drawPlayer();
    }

    drawParticles();
}

function gameLoop(timestamp) {

    var dt = (timestamp - lastTime) / 1000;

    if (!lastTime) {
        dt = 0;
    }

    lastTime = timestamp;

    dt = Math.min(dt, 0.033);

    if (running && !gameOver) {

        updatePlayer(dt);
        updateBots(dt);
        updateBullets(dt);
        updateLoot();
        updateZone(dt);
        updateParticles(dt);

        updateHud();
    }

    draw();

    requestAnimationFrame(gameLoop);
}

document.addEventListener("keydown", function (e) {

    var key = e.key.toLowerCase();

    keys[key] = true;

    if (key === "r") {
        reload();
    }

    if (
        key === " " ||
        key === "arrowup" ||
        key === "arrowdown" ||
        key === "arrowleft" ||
        key === "arrowright"
    ) {
        e.preventDefault();
    }
});

document.addEventListener("keyup", function (e) {

    keys[e.key.toLowerCase()] = false;
});

game.addEventListener("mousemove", function (e) {

    var rect = game.getBoundingClientRect();

    mouse.x =
        (e.clientX - rect.left) *
        (W / rect.width);

    mouse.y =
        (e.clientY - rect.top) *
        (H / rect.height);

    crosshair.style.left =
        (e.clientX - rect.left) + "px";

    crosshair.style.top =
        (e.clientY - rect.top) + "px";
});

game.addEventListener("mousedown", function (e) {

    if (e.button === 0) {
        mouse.down = true;
    }
});

window.addEventListener("mouseup", function (e) {

    if (e.button === 0) {
        mouse.down = false;
    }
});

startButton.addEventListener("click", function () {
    resetGame();
});

restartButton.addEventListener("click", function () {
    resetGame();
});

resizeCanvas();
requestAnimationFrame(gameLoop);

})();
</script>

</body>
</html>
"""

components.html(
    game_html,
    height=700,
    scrolling=False
)
