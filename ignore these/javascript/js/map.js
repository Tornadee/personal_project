let platforms_data = [
  {x:0.0,z:0},
  {x:0.0,z:4.5},
  {x:0.0,z:9.0},
  {x:0.9,z:13.5},
  {x:0.0,z:18.0},
  {x:0.9,z:22.5},
  {x:0.9,z:27.0},
  {x:0.0,z:31.5},
  {x:0.9,z:36.0},
  {x:0.9,z:40.5},
  {x:1.8,z:45.0},
  {x:2.7,z:49.5},
  {x:2.7,z:54.0}
];
function buildStart() {
  for (var i=0;i<platforms_data.length;i++) {
    let platform = platforms_data[i];
    makePlane([platform.x,0,platform.z * (-1)],[0,0,0],[2.5,0.2,5], 0);
  }
}
