var AI = {
  init: async function() {
    this.model = await tf.loadModel("http://localhost:8888/fetch_json");

  },
  choose_action: async function() {
    let px = Math.round(player.position.x * 1000) / 1000;
    let pz = Math.round(player.position.z * (-1) * 1000) / 1000;
    let input = [px, pz];
    var prediction = await this.model.predict(input);
    var choice = prediction.argmax();
    return prediction;
  }
}
