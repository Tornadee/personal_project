let platforms_data = [0,0,1,2,2,1,0,0,-1,-2,-3,-3,-2,-1,0,1,2,2,1,0,0,0,0,0];
function buildStart() {
  var z = -1.0;
  for (var i=0;i<platforms_data.length;i++) {
    let x = platforms_data[i] * 0.6;
    makePlane([x,0,z * (-1)],[0,0,0],[1.5,0.1,2.0], 0);
    z += 2.0;
  }
}
