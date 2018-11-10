// game settings
const cameraRadius = 6.0;
const frameRate = 50;
const ballSpeed = 0.4;
const steerSpeed = 0.07;
// game objects
var camera;
var light;
var player;
var platforms = [];
// game variables
var rotation = 0;
// game essentials
var canvas;
var engine;
var scene;
var interval;
var gameManager = {
	pageload: function() {
		setTimeout(function() {
			// instead of this, show a button and click to start.
			gameManager.init();
		}, 200);
	},
	init: async function() {
		canvas = await document.getElementById("renderCanvas");
		engine = await new BABYLON.Engine(canvas, true);
		scene = await this.createScene();
		await this.startEngine();
		await initItemsJS();
		await buildStart();
		//await AI.init();
		//await startSkybox();
		//await startFountain();
		await this.startPhysics();
		interval = setInterval(update, frameRate); // start updating game elements
	},
	startEngine: function() {
		engine.runRenderLoop(function () {scene.render()});
	  window.addEventListener("resize", function () {engine.resize()});
	},
	createScene: function() {
		scene = new BABYLON.Scene(engine);
		var gravityVector = new BABYLON.Vector3(0,-1.81, 0);
		scene.enablePhysics(gravityVector);
		// camera
		camera = new BABYLON.FreeCamera("camera", new BABYLON.Vector3(0, 2, -10), scene);
		camera.setTarget(BABYLON.Vector3.Zero());
		// light
		light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);
		light.intensity = 1.0;
		// player
		player = BABYLON.Mesh.CreateBox("player",0.5,scene);
		player.scaling = new BABYLON.Vector3(1, 0.15, 1)
		player.position.y = 0.5;
		// Water
		//var ground = BABYLON.Mesh.CreateGround("ground", 512, 512, 32, scene);
		//var waterMaterial = new BABYLON.WaterMaterial("water_material", scene);
		//waterMaterial.bumpTexture = new BABYLON.Texture("bump.png", scene); // Set the bump texture

		//ground.material = waterMaterial;
		return scene;
	},
	startPhysics: function() {
		player.physicsImpostor = new BABYLON.PhysicsImpostor(player, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0.5, restitution: 0.0, friction:0.0 }, scene);
	}
}
document.getElementById('body').onload = gameManager.pageload();

var frame = 0;
async function update() {
	frame += 1;
	fountain.position = player.position;
	// steer
	if (keyRightDown) {rotation += steerSpeed};
	if (keyLeftDown) {rotation -= steerSpeed};
	//let action = await AI.choose_action();
	//console.log(action);
	//rotation += action * steerSpeed;
	// apply player movement
	vx = ballSpeed * Math.sin(rotation - 3.14);
	vz = ballSpeed * Math.cos(rotation - 3.14);
	player.position.x += vx;
	player.position.z += vz;
	player.rotation.y = rotation;
	// camera position
	camera.position.x = player.position.x + (cameraRadius * Math.sin(rotation));
	camera.position.z = player.position.z + (cameraRadius * Math.cos(rotation));
	camera.position.y = player.position.y + 2;
	// camera rotation
	camera.rotation.y = rotation - 3.14;
	camera.rotation.x = 0.3;
	camera.rotation.z = 0;
	// light position
	light.position = camera.position;
	// if win
	/*if (player.intersectsMesh(endingFloor)) {
		ballSpeed = 0.0;
	}*/
	// if dead
	if ((player.position.y < -1.0) || (player.position.y > 100.0)) {
		engine.stopRenderLoop();
		clearInterval(interval);
		console.log("game over");
	}
}
