var makePlane;
var idno = 0; // platform list counter
var idno2 = 0; // material list counter
var deletedIdno = 0;

var matList = [];
function initItemsJS() {
  mainMat = new BABYLON.StandardMaterial("mainMat", scene);
  //mainMat.diffuseColor = BABYLON.Color3.Blue();
  mainMat.diffuseTexture = new BABYLON.Texture("http://www.sy9000.xyz/assets/ice.png", scene); //http://i346.photobucket.com/albums/p430/seojoony/ice_packed_zpsxtozaj2c.png
  mainMat.diffuseTexture.uScale = 1.0;//Repeat u times on the Vertical Axes
  mainMat.diffuseTexture.vScale = 1.0;//Repeat v times on the Horizontal Axes
  mainMat.backFaceCulling = false;//Always show the front and the back of an element
  mainMat.alpha = 0.5
  matList.push(mainMat);

  function makeColorMat(r,g,b,a) {
    idno2 += 1;
    var customMat = new BABYLON.StandardMaterial("customMat" + idno2, scene);
    customMat.diffuseColor = new BABYLON.Color3(r/255, g/255, b/255);
    customMat.alpha = a;
    matList.push(customMat);
  }
  makeColorMat(255,255,0,1);
  makeColorMat(0,100,255,1);
  makeColorMat(0,0,0,1);
  makeColorMat(100,100,100,1);
  makeColorMat(100,100,200,1);
  makeColorMat(100,100,200,0.5);

  makePlane = function(posList, rotList, sizList, matIndex) {
    let pX = posList[0]; let pY = posList[1]; let pZ = posList[2];
    let rX = rotList[0]; let rY = rotList[1]; let rZ = rotList[2];
    let sX = sizList[0]; let sY = sizList[1]; let sZ = sizList[2];
    // mesh item
    var mesh = BABYLON.Mesh.CreateBox("mesh" + idno, 1, scene);
    mesh.scaling = new BABYLON.Vector3(sX,sY,sZ);
    mesh.position.x = pX * (-1);
    mesh.position.y = pY;
    mesh.position.z = pZ;
    mesh.rotation.x = rX * (Math.PI / 180);
    mesh.rotation.y = rY * (Math.PI / 180);
    mesh.rotation.z = rZ * (Math.PI / 180);
    // material
    mesh.material = matList[matIndex];
    // physics
    mesh.physicsImpostor = new BABYLON.PhysicsImpostor(mesh, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0.0, restitution: 0.2 }, scene);
    idno += 1;
  }
}

function removeLast() {
  mesh = scene.getMeshByName("mesh" + deletedIdno);
  mesh.dispose();
  deletedIdno += 1;
}

function cleanupBehind(repeat) {
  const setBack = 10;
  for (var i=0;i<repeat;i++) {
    if (idno > setBack) {
      removeLast();
    }
  }
}
