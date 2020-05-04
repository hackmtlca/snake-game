SNAKE_LENGTH = 20;
FOOD = 1000;
SCALE = 4;
MAX_SPEED = 50;
BACKGROUND_COLOR = [52, 58, 64];
HEALTH_DECREASE_RATE = 0.05;

function setup() {
  createCanvas(windowWidth, windowHeight);
  food = [];
  generateFood();
  offsetX = 0
  offsetY = 0
  state = 'MAIN_MENU'
}

function initGame() {
  state = 'GAME';
  textAlign(LEFT);
  player = new Snake(width / 2, height / 2);
}

function draw() {
  translate(-offsetX, -offsetY);
  background(BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2]);
  
  switch(state){
    case 'MAIN_MENU':
      menuLoop();
      break;
    case 'GAME':
      gameLoop();
      break;
  }
}

function keyPressed() {
  if(keyCode === 32 && state == 'MAIN_MENU'){
    initGame();
  }
}

function menuLoop() {
  offsetX = lerp(offsetX, 0, 0.025);
  offsetY = lerp(offsetY, 0, 0.025);

  for(let i = 0; i < food.length; i++) {
    food[i].display(offsetX, offsetY);
  }
  
  noStroke();
  textSize(32);
  fill(255);
  textAlign(CENTER);
  text('Snake Game', width / 2, height / 2);
  textSize(16);
  text('Press <SPACE> to Start', width / 2, height / 2 + 30);
}

function gameLoop() {
  player.displayClose();
  
  deltaScore = 0;

  for(let i = 0; i < food.length; i++) {
    if(arrayEqual(get(food[i].x - offsetX, food[i].y - offsetY), [BACKGROUND_COLOR[0] + 1,BACKGROUND_COLOR[1], BACKGROUND_COLOR[2], 255])){
      deltaScore += food[i].size / 4;
      food.splice(i,1);
      append(food, randomPoint());
    } else {
      food[i].display(offsetX, offsetY);
    }
  }
  
  player.score += parseInt(pow(deltaScore, 1.5));
  
  player.display(min(max((mouseX - width / 2) / 4, -MAX_SPEED), MAX_SPEED), min(max((mouseY - height / 2) / 4, -MAX_SPEED), MAX_SPEED));
  
  player.health = min(100, player.health + deltaScore) - HEALTH_DECREASE_RATE;
  
  if(player.health <= 0)
    gameOver();
  
  noStroke();
  textSize(32);
  fill(255);
  text('Health: ' + ceil(player.health), offsetX + 25, offsetY + height - 60);
  text('Score: ' + player.score, offsetX + 25, offsetY + height - 25);
  
  offsetX = player.head().x - width / 2;
  offsetY = player.head().y - height / 2;
}

function generateFood() {
  food = []
  
  for(let i = 0; i < FOOD; i++){
    append(food, randomPoint())
  }
}

function randomPoint() {
 return new Particle(random(-(width * SCALE), width * SCALE),random(-(width * SCALE), height * SCALE));
}

function arrayEqual(a1, a2) {
  if(a1.length != a2.length) {
    return false; 
  }
  
  for(let i = 0; i < a1.length; i++) {
    if(a1[i] != a2[i]) {
      return false;
    }
  }
  
  return true;
}

function gameOver() {
  fetch('./api/users/score', { method: 'POST', credentials: 'same-origin', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({'score': player.score})});
  state = 'MAIN_MENU';
}

function Particle(x, y) {
  this.x = x;
  this.y = y;
  this.size = random(10, 20);
  this.color = [random(255), random(100, 200), random(100)]
  
  this.display = function(offsetX, offsetY) {
    if(this.x > offsetX - width && this.x < offsetX + width && this.y > offsetY - height && this.y < offsetY + height) {
      stroke(this.color[0], this.color[1], this.color[2]);
      strokeWeight(this.size);
      point(this.x, this.y);
    }
  }
}

function Snake(x, y) {
  this.x = x;
  this.y = y;
  this.health = 100;
  this.score = 0;
  this.points = [];
  this.color = [random(255), random(100, 200), random(100)]
  this.length = SNAKE_LENGTH;
  
  for(let i = 0; i < this.length; i++) {
    append(this.points, new Spring2D(this.x, this.y));
  }
  
  this.head = function() {
    return this.points[0];
  }
  
  this.display = function(x, y) {
    this.points[0].updateDelta(x, y);
    this.points[0].display(x, y, false);
    
    for(let i = 1; i < this.length; i++) {
      this.points[i].update(this.points[i-1].x, this.points[i-1].y);
      this.points[i].display(this.points[i-1].x, this.points[i-1].y, true, this.color);
    }
  }
  
  this.displayClose = function() {
    for(let i = 1; i < this.length; i++){
      if(dist(this.points[0].x, this.points[0].y, this.points[i].x, this.points[i].y) < 20) {
        fill(BACKGROUND_COLOR[0] + 1, BACKGROUND_COLOR[1], BACKGROUND_COLOR[2]);
        beginShape();
        for(let i = 0; i < SNAKE_LENGTH; i++) {
          vertex(this.points[i].x, this.points[i].y);
        }
        endShape();
        break;
      }
    }
  }

}

function Spring2D(xpos, ypos) {
  this.x = xpos;
  this.y = ypos;
  this.vx = 0;
  this.vy = 0;
  this.mass = 7;
  this.radius = 10;
  this.stiffness = 0.3;
  this.damping = 0.7;

  this.update = function(targetX, targetY) {
    let forceX = (targetX - this.x) * this.stiffness;
    let ax = forceX / this.mass;
    this.vx = this.damping * (this.vx + ax);
    this.x += this.vx;
    let forceY = (targetY - this.y) * this.stiffness;
    let ay = forceY / this.mass;
    this.vy = this.damping * (this.vy + ay);
    this.y += this.vy;
  }
  
  this.updateDelta = function(deltaX, deltaY) {
    let forceX = deltaX * this.stiffness;
    let ax = forceX / this.mass;
    this.vx = this.damping * (this.vx + ax);
    this.x += this.vx;
    let forceY = deltaY * this.stiffness;
    let ay = forceY / this.mass;
    this.vy = this.damping * (this.vy + ay);
    this.y += this.vy;
  }

  this.display = function(nx, ny, hasLine, color) {
    noStroke();
    if(hasLine){
      stroke(color[0], color[1], color[2]);
      strokeWeight(30);
      line(this.x, this.y, nx, ny);
    }
  }
}