let platforms_data = [
  {x:0,z:0},
  {x:0,z:4.5},
  {x:0,z:9},
  {x:0,z:13.5},
  {x:0,z:18},
  {x:0,z:21.5}
];


function buildStart() {
  for (var i=0;i<platforms_data.length;i++) {
    let platform = platforms_data[i];
    makePlane([platform.x,0,platform.z * (-1)],[0,0,0],[2,0.2,5], 0);
  }
}
