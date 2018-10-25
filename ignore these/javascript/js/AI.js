var AI = {
  init: async function() {
    this.model = await tf.loadModel("http://localhost:8888/fetch_json");
    console.log("loaded");
  },
  choose_action: async function() {
    // input
    let px = await Math.round(player.position.x * 1000) / 1000;
    let pz = await Math.round(player.position.z * (-1) * 1000) / 1000;
    let input = await tf.tensor([[px, pz]]);
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
