var AI = {
  init: async function() {
    this.model = await tf.loadModel("http://localhost:8888/fetch_json");
    console.log("loaded");
  },
  closest_diff: async function() {
    for (var i=0;i<platforms_data.length;i++) {
        var platform = platforms_data[i];
        if (platform.z * (-1) < player.position.z) {
            let dx = player.position.x - platform.x;
            return dx / 10;
            break;
        }
    }
  },
  choose_action: async function() {
    // input
    let dx = await this.closest_diff();
    let pz = await player.position.z * (-1);
    let pr = await rotation;
    let input = await tf.tensor([[dx, pz, pr]]);
    // prediction
    var prediction = await this.model.predict(input);
    var choice = await prediction.argMax(1).dataSync()[0]; // axis = 1
    var action = await Number(choice - 1); // 0,1,2 --> -1,0,1
    // logging / debug
    console.log("input=");
    input.print();
    console.log("prediction = ");
    prediction.print();
    console.log("choice = " + choice);
    console.log("action = " + action);
    return action;
  }
}
