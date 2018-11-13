// game settings
const cameraRadius = 6.0;	// player control	// AI control
const frameRate = 70;		// 50 				// 70
const ballSpeed = 0.5; 		// 0.4				// 0.5
const steerSpeed = 0.1;		// 0.07				// 0.1
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
var water;

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
		await AI.init();
		//await startFountain();
		await this.loadStuff();
		await this.startPhysics();
		setTimeout(function() {
			interval = setInterval(update, frameRate); // start updating game elements
		}, 2000);
	},
	startEngine: function() {
		engine.runRenderLoop(function () {scene.render()});
	  window.addEventListener("resize", function () {engine.resize()});
	},
	createScene: function() {
		scene = new BABYLON.Scene(engine);
		var gravityVector = new BABYLON.Vector3(0,-10.81, 0);
		scene.enablePhysics(gravityVector);
		// camera
		camera = new BABYLON.FreeCamera("camera", new BABYLON.Vector3(0, 2, -10), scene);
		camera.setTarget(BABYLON.Vector3.Zero());
		// light
		light = new BABYLON.DirectionalLight("light", new BABYLON.Vector3(-1, -2, -1), scene);
		//light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);
		light.intensity = 1.2;
		// player
		player = BABYLON.Mesh.CreateBox("player",0.5,scene);
		player.scaling = new BABYLON.Vector3(1, 0.15, 1)
		player.position.y = 0.5;
		player.position.z = 0;
		player.position.x = 0.01;
		// Ground
    var groundTexture = new BABYLON.Texture("http://www.sy9000.xyz/assets/ground.JPG", scene);
    groundTexture.vScale = groundTexture.uScale = 4.0;

    var groundMaterial = new BABYLON.StandardMaterial("groundMaterial", scene);
    groundMaterial.diffuseTexture = groundTexture;

    var ground = BABYLON.Mesh.CreateGround("ground", 512, 512, 32, scene, false);
    ground.position.y = -5;
    ground.material = groundMaterial;
    // Water
    var waterMesh = BABYLON.Mesh.CreateGround("waterMesh", 512, 512, 32, scene, false);
		waterMesh.position.y = -4;
    water = new BABYLON.WaterMaterial("water", scene, new BABYLON.Vector2(1024, 1024));
    water.backFaceCulling = true;
    water.bumpTexture = new BABYLON.Texture("https://www.babylonjs-playground.com/textures/waterbump.png", scene);
    water.windForce = -5;
    water.waveHeight = 0.5;
    water.bumpHeight = 0.9;
    water.waveLength = 0.2;
    water.colorBlendFactor = 0;
    water.addToRenderList(ground);
    waterMesh.material = water;

		var light1 = new BABYLON.PointLight("pointLight", new BABYLON.Vector3(0, 10, 0), scene);
		light1.diffuse = new BABYLON.Color3(0.2, 0, 1.4); // 1/0.4
		light1.specular = new BABYLON.Color3(0.3, 0, 0.8); // 0.6/0.8
		light1.intensity = 1.0;
		return scene;
	},
	loadStuff: async function() {
		var loader = new BABYLON.AssetsManager(scene);
		loader.addMeshTask("car", "", "http://www.sy9000.xyz/assets/", "end2.obj"); // assets/
		loader.onFinish = function(tasks) {
			for (var i=0;i<tasks[0].loadedMeshes.length;i++) {
				var car = tasks[0].loadedMeshes[i];
				car.position.y = -2.1;
				car.position.x = 0;
				car.position.z = -44;
				car.rotation.y = Math.PI;
				car.scaling.x = 0.3;
				car.scaling.y = 0.3;
				car.scaling.z = 0.3;
				car.material = matList[5];
			}
		};
	  loader.load();
		var loader = new BABYLON.AssetsManager(scene);
		loader.addMeshTask("car2", "", "http://www.sy9000.xyz/assets/", "rock.obj"); // assets/
		loader.onFinish = function(tasks) {
			for (var i=0;i<tasks[0].loadedMeshes.length;i++) {
				var car2 = tasks[0].loadedMeshes[i];
				car2.position.y = -2.3;
				car2.position.x = 3;
				car2.position.z = -20;
				car2.rotation.y = Math.PI;
				car2.scaling.x = 0.2;
				car2.scaling.y = 0.2;
				car2.scaling.z = 0.2;
				car2.material = matList[6];
				water.addToRenderList(car2);
				for (var i=0;i<40;i++) {
					var newClone = car2.clone("index: " + i);
					newClone.position.x = Math.random() * 100 - 50;
					newClone.position.z = Math.random() * 70 - 80;
					water.addToRenderList(newClone);
				}
			}
		};
	  loader.load();
	},
	startPhysics: function() {
		player.physicsImpostor = new BABYLON.PhysicsImpostor(player, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0.1, restitution: 0.0}, scene);
	}
}
document.getElementById('body').onload = gameManager.pageload();

var frame = 0;
async function update() {
	frame += 1;
	// steer
	//if (keyRightDown) {rotation += steerSpeed};
	//if (keyLeftDown) {rotation -= steerSpeed};
	let action = await AI.choose_action();
	if (action != null) {
		rotation += action * steerSpeed;
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
		if (player.position.z <= -42) {
			engine.stopRenderLoop();
			clearInterval(interval);
			console.log("win");
		}
		// if dead
		if ((player.position.y < -1.0) || (player.position.y > 100.0)) {
			engine.stopRenderLoop();
			clearInterval(interval);
			console.log("game over");
		}
	}
}
