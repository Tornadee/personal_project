function startSkybox() {
  function skyblockMake(r, x, z) {
    var skybox = BABYLON.Mesh.CreateBox("skyBox", 100.0, scene);
    var skyboxMaterial = new BABYLON.StandardMaterial("space", scene);
    skyboxMaterial.backFaceCulling = false;
    skyboxMaterial.disableLighting = true;
    skybox.material = skyboxMaterial;
    skybox.infiniteDistance = true;
    skyboxMaterial.disableLighting = true;
    skyboxMaterial.reflectionTexture = new BABYLON.CubeTexture("assets/space/space", scene);
    skyboxMaterial.reflectionTexture.coordinatesMode = BABYLON.Texture.SKYBOX_MODE;
    //http://i.imgur.com/pXD1MZv.png
    skybox.rotation.y = r * (Math.PI / 180);
    skybox.position.x = x * -1;
    skybox.position.z = z * -1;
  }
  skyblockMake(0, 1, 0);
  skyblockMake(90, 0, -1);
  skyblockMake(180, -1, 0);
  skyblockMake(270, 0, 1);
}

function startFountain() {
  var fountain = BABYLON.Mesh.CreateBox("foutain", 1.0, scene);
  // Create a particle system
  var particleSystem = new BABYLON.ParticleSystem("particles", 2000, scene);

  //Texture of each particle
  particleSystem.particleTexture = new BABYLON.Texture("assets/flare.png", scene);

  // Where the particles come from
  particleSystem.emitter = fountain; // the starting object, the emitter
  particleSystem.minEmitBox = new BABYLON.Vector3(-0.2, 0, 0); // Starting all from
  particleSystem.maxEmitBox = new BABYLON.Vector3(0.2, 0, 0); // To...

  // Colors of all particles
  particleSystem.color1 = new BABYLON.Color4(0.7, 0.8, 1.0, 1.0);
  particleSystem.color2 = new BABYLON.Color4(0.2, 0.5, 1.0, 1.0);
  particleSystem.colorDead = new BABYLON.Color4(0, 0, 0.2, 0.0);

  // Size of each particle (random between...
  particleSystem.minSize = 0.01;
  particleSystem.maxSize = 0.05;

  // Life time of each particle (random between...
  particleSystem.minLifeTime = 0.3;
  particleSystem.maxLifeTime = 0.5;

  // Emission rate
  particleSystem.emitRate = 1500;

  // Blend mode : BLENDMODE_ONEONE, or BLENDMODE_STANDARD
  particleSystem.blendMode = BABYLON.ParticleSystem.BLENDMODE_ONEONE;

  // Set the gravity of all particles
  particleSystem.gravity = new BABYLON.Vector3(0, -9.81, 0);

  // Direction of each particle after it has been emitted
  particleSystem.direction1 = new BABYLON.Vector3(-0.7, 0.0, 3);
  particleSystem.direction2 = new BABYLON.Vector3(0.7, 0.0, -3);

  // Angular speed, in radians
  particleSystem.minAngularSpeed = 0;
  particleSystem.maxAngularSpeed = Math.PI;

  // Speed
  particleSystem.minEmitPower = 1;
  particleSystem.maxEmitPower = 3;
  particleSystem.updateSpeed = 0.009; // 0.005

  // Start the particle system
  particleSystem.start();
}
